# deployment guide for inspector-widget (on a fresh server install of ubuntu)
### pre-requirements
create a new user other than root if it's not already done and connect to it. https://www.simplified.guide/linux/user-add-new

open a terminal and type in the following commands to install pre-requirements for addind docker's repo
```
sudo apt-get update
```
```
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

now type in the following commands to add docker's GPG key
```
sudo mkdir -p /etc/apt/keyrings
```
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

setup docker repo using this command
```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

update the apt list with
```
sudo apt-get update
```

install docker using the command
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

setup your user so it is able to use docker
```
sudo usermod -aG docker ${USER}
```

reload user session so the changes are take into account
```
su - ${USER}
```

clone this repo wherever you want using
```
git clone https://github.com/osoc22/project-inspector-widget.git
```

go into the right folder of the repo using
```
cd project-inspector-widget/week1/flaskr
```

using your favorite editor, modify the .env file and replace the following fields with values for your needs :
- POSTGRES_USER=database user name goes here
- POSTGRES_PASSWORD=database user password goes there
- POSTGRES_HOST=postgres
- POSTGRES_PORT=5432
- POSTGRES_DB=name of your database
- DATABASE_URL=postgresql://database_user:database_passowrd@postgres/database_name
- SECRET_KEY:
    
    1 Generate a random string:
    ```
    import uuid
    uuid.uuid4().hex
    ```
    2 Set SECRET_KEY in .env file to the generated random string:
    SECRET_KEY = 'this is the random string'


build & run the docker containers using the command
```
docker compose up -d --build
```

if you make any change in the project, run the above command again to rebuild & re-run the containers with the new changes

if you want to kill every container of this application use
```
docker compose down
```
