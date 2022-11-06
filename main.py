from flask import Flask, request
import xmltodict
import os
import sys

app = Flask(__name__)
CLIENT_CONFIG = sys.argv[1]


@app.route('/deploy/push', methods=['GET', 'POST'])
def git_repo_push_request():
    """
        Receive a push request from GitHub or BitBucket and pull the latest code from the repo.
    """
    try:
        if "GitHub" in request.headers.get('User-Agent'):
            request_origin = "GitHub"
            event_type = request.headers.get('X-GitHub-Event')
            content_type = request.headers.get('Content-Type')
            secret_token = request.headers.get('X-Hub-Signature')
            if secret_token != os.environ.get('GITHUB_SECRET_TOKEN'):
                return {"error", "Invalid secret token, request not authorized."}
        elif "Bitbucket" in request.headers.get('User-Agent'):
            request_origin = "Bitbucket"
            event_type = request.headers.get('X-Event-Key')
            content_type = request.headers.get('Content-Type')
        else:
            request_origin = "Unknown"
            event_type = "Unknown"
            content_type = "Unknown"

        if request_origin == "Unknown":
            # check if the request came from GitHub and BitBucket
            return {"error": "Invalid request origin, only GitHub and BitBucket are supported"}
        if event_type == "Unknown":
            # check if the request is a push request
            return {"error": "Invalid event type, only push events are supported"}
        if content_type != "application/json":
            # check if the request is of type JSON
            return {"error": "Invalid content type, only JSON is supported"}

        repo_name = request.json['repository']['full_name']

        # read the clients.xml file to get the latest client
        try:
            with open(CLIENT_CONFIG) as fd:
                CLIENT_REPOS = xmltodict.parse(fd.read())
        except Exception as e:
            return {"error": f"Error reading the config file: {CLIENT_CONFIG} with exception: {e}"}

        # find a client repo in the DICT from XML file
        CLIENT = list(filter(lambda x: x['@repo'] == repo_name, CLIENT_REPOS['clients']['client']))

        if not CLIENT:
            return {"error": f"No client config found for the repo: {repo_name}"}

        # TODO: Do not forget to setup SSH key on the server user running this microservice,
        #  after generating your SSH key, add it to the GitHub repo as a deploy key, and run
        #  ssh-add to add the key to the ssh agent.

        # pull the latest code from the repo
        os.chdir(CLIENT[0]['@directory'])

        # get standard output from command
        os.system("git pull --recurse-submodules")
        git_stash = os.popen("git stash && git stash list").read()
        git_reset = os.popen("git reset --hard").read()
        git_pull = os.popen("git pull --recurse-submodules").read()

        # TODO: Add a check to see if the repo is already being pulled
        # TODO: add functionality to restart a docker image or a systemd instance

        return {
            "success": f"Successfully pulled the latest code from the repo: {repo_name}",
            "output": f"{git_stash}\n{git_reset}\n{git_pull}"
        }
    except Exception as e:
        return {"error": f"Server Error while processing the request: {e}"}


if __name__ == "__main__":
    app.run(debug=False)
else:
    application = app
