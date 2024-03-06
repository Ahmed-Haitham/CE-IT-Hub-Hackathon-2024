# CE-IT-Hub-Hackathon-2024

## Steps on windows to install WSL
1. Open terminal as admin and run:
    ```bash
    run wsl --install
    ```
2. Reboot your machine

3. Open ubuntu (executable) and run:
    ```bash
    sudo apt update
    ```

## Install p&g certificate on wsl
1. Open Ubuntu terminal and run:
    ```bash
    sudo su
    ```
2. Paste one big command from developerportal into root cmd line(https://developerportal.pg.com/docs/default/component/devdocs/network/ssl-inspection/Solutions/#option-2-one-big-command)
3. Press enter in the first pink window
4. Use space key to add pgrootcert, then press enter
5. CTRL+D to exit root terminal
6. Start docker service:
    ```bash
    sudo service docker stop
    sudo service docker start
    ```

## now install docker:
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo docker run hello-world
```

## now install git and clone repo on wsl
### Prerequisite (have git credentials manager set up on windows: https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git)
```bash
sudo-apt-get install git
git config --global user.name "YOURNAME"
git config --global user.email "YOURGITHUB EMAIL"
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"
git clone https://github.com/Ahmed-Haitham/CE-IT-Hub-Hackathon-2024
```

## now connect vs code to wsl
1. Make sure that VS code is added to your windows path (environment variable settings)
2. Open your vs code on windows and install the wsl extension
3. From your ubuntu terminal, type:
    ```bash
    cd /mnt/c
    code .
    ```
    Likely now you will get errors from VS code. Restarting your computer and opening vs code again should fix it.

## Now build the docker images using docker compose
1. From your vs code connected to wsl ubuntu, add a .env file in the root directory. This file will contain required variables for your database configuration. 
You can paste the following for development purpose. For PROD, .env file should contain strong passwords/secrets:
    ```ini
    PG_INSTANCE=pginstance
    PG_USER=user
    PG_PASSWORD=pass
    DB_PORT=5432
    JWT_SECRET_KEY=asd3j4kEdj!
    JWT_REFRESH_SECRET_KEY=lkf3Rsad312@df%
    ADMIN_USERNAME=admin
    ADMIN_PASSWORD=admin
    ```
2. Build the application:
    ```bash
    cd CE-IT-Hub-Hackathon-2024
    sudo docker compose up -d --build
    ```
3. Now you should have 2 containers running (web and db). Check it by running:
  ```bash
  sudo docker compose ps
  ```
4. If you have issues spinning up containers, use:
    ```bash
    sudo docker compose logs CONTAINERNAME
    ```
5. Now you should have a running postgres db on port 5432 and a fastapi server on http://127.0.0.1:8000/. To spin the containers down:
    ```bash
    sudo docker compose down
    ```
6. If you also want to delete the persisted database volume:
    ```bash
    sudo docker compose down -v
    ```

## Optional: Create a python virtual environment and install requirements
This will help you by making vs code suggest valid autocompletes:
```bash
cd ENV DIRECTORY
python3 -m venv hackenv
pip install -r requirements.txt
```
