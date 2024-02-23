# CE-IT-Hub-Hackathon-2024

## Steps on windows to install WSL

run wsl--install on admin terminal

reboot your machine

open ubuntu (executable)

run sudo apt update

## now install docker:
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

## now install git and clone repo on wsl
### Prerequisite (have git credentials manager set up on windows: https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git)
sudo-apt-get install git
git config --global user.name "YOURNAME"
git config --global user.email "YOURGITHUB EMAIL"
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"
git clone https://github.com/Ahmed-Haitham/CE-IT-Hub-Hackathon-2024

## Now build the docker image
cd CE-IT-Hub-Hackathon-2024
sudo docker build . -t hackathon-app:v1
sudo docker run -p 8000:8000 hackathon-app:v1
=======
user:hackathon-postgre
pass:hackathonteam1


# NOT NEEDED, only for information: Steps needed to initially setup a docker image (not needed if you want to debug)
python3 -m venv venv

pip install fastapi
pip install "uvicorn[standard]"

sudo docker build -t ce_hackathon_team_1 .

sudo docker run -p 8000:8000 ce_hackathon_team_1


https://docs.docker.com/compose/install/linux/#install-the-plugin-manually

sudo docker compose up -d
