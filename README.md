# Odoo GitCI

---

A simple web service for GitHub & Bitbucket webhooks to trigger a pull request and automate continues integration processes.

## Step 1: Configure SSH

#### On the active linux user generate an SSH public and private key using:
    ssh-keygen

#### Auto run the ssh agent on the service account adding the following code to "~/.bashrc"
    if [ ! -S ~/.ssh/ssh_auth_sock ]; then
    eval `ssh-agent`
    ln -sf "$SSH_AUTH_SOCK" ~/.ssh/ssh_auth_sock
    fi
    export SSH_AUTH_SOCK=~/.ssh/ssh_auth_sock
    ssh-add -l > /dev/null || ssh-add

#### Add the private key identity to the SSH keystore
    ssh-add ~/.ssh/id_rs

#### Add the public key to the Git repository/organization/project
    cat ~/.ssh/id_rsa.pub

## Step 2: Configure the microservice

#### create a runtime folder to run the microservice
    mkdir /opt/odooci

#### git clone this repository to the server to the runtime folder
    git clone https://github.com/nabilragab/odoo-gitci

#### create dedicated python virtual environment for the microservice
    python3.11 -m venv venv-gitci
    source venv-gitci/bin/activate
    pip install -r odoo-gitci/requirements.txt

#### install uWsgi server following the instructions from the official documentation
[https://uwsgi-docs.readthedocs.io/en/latest/Install.html](https://uwsgi-docs.readthedocs.io/en/latest/Install.html)

#### add a symbolic link to the crt and key files and chmod '440' permissions
    ln -s /etc/pki/domain.com/domain.crt /opt/odooci/domain.crt
    ln -s /etc/pki/domain.com/domain.key /opt/odooci/domain.key

#### create a clients configuration file from clients_sample.xml
    cp ./clients_sample.xml ../clients.xml && nano ../clients.xml

#### if you are using GitHub create a permanent environment variable at the bottom of the "~/.bashrc" file
    nano ~/.bashrc
    export GITHUB_SECRET_TOKEN=your_token

#### create a systemd service using the uWsgi.service file
    sudo cp /opt/ragabnet/odoo-gitci/uwsgi_sample.service /etc/systemd/system/odoo-gitci.service && sudo nano /etc/systemd/system/odoo-gitci.service
    sudo systemctl daemon-reload
    sudo systemctl enable odoo-gitci.service
    sudo systemctl start odoo-gitci.service

## Step 3: Configure the repository

#### Git Clone the repository to the server using SSH
    git clone git@github.com:username/repo-name.git

#### add the webhook to the repository
    https://domain.com:35553/deploy/push

### Thank You!

---

![ODOO](https://odoocdn.com/openerp_website/static/src/img/assets/png/odoo_logo_inverted.png)

---

Credits:
[nabil@ragab.net](mailto:nabil@ragab.net) | [www.ragab.net](www.ragab.net)

