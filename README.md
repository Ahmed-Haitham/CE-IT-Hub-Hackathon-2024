# CE-IT-Hub-Hackathon-2024

run wsl--install on admin terminal

reboot

open ubuntu

run sudo apt update

now install docker:
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo docker run hello-world

user:hackathon-postgre
pass:hackathonteam1



python3 -m venv venv

pip install fastapi
pip install "uvicorn[standard]"

sudo docker build -t ce_hackathon_team_1 .

sudo docker run -p 8000:8000 ce_hackathon_team_1

- sqlalchemy
- alembic


