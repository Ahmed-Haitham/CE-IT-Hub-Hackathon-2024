# CE-IT-Hub-Hackathon-2024

## Steps on windows to install WSL
run wsl--install on admin terminal <br/>
reboot your machine <br/>
open ubuntu (executable) <br/>
run sudo apt update

## now install p&g certificate on wsl
enter root terminal (sudo su) <br/>
copy one big command from developerportal (add link) <br/>
paste it into root cmd line <br/>
press enter in the first pink window <br/>
use space key to add pgrootcert, then press enter <br/>
CTRL+D to exit root terminal <br/>
sudo service docker stop <br/>
sudo service docker start

## now install docker:
sudo apt-get update <br/>
sudo apt-get install ca-certificates curl <br/>
sudo install -m 0755 -d /etc/apt/keyrings <br/>
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc <br/>
sudo chmod a+r /etc/apt/keyrings/docker.asc <br/>
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update <br/>
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin <br/>
sudo docker run hello-world

## now install git and clone repo on wsl
### Prerequisite (have git credentials manager set up on windows: https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git)
sudo-apt-get install git <br/>
git config --global user.name "YOURNAME" <br/>
git config --global user.email "YOURGITHUB EMAIL" <br/>
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe" <br/>
git clone https://github.com/Ahmed-Haitham/CE-IT-Hub-Hackathon-2024

## Now build the docker images using docker compose
cd CE-IT-Hub-Hackathon-2024 <br/>
sudo docker compose up -d --build <br/>
Now you should have 2 containers running (web and db) <br/>
Check it by running: <br/>
sudo docker compose ps <br/>
If you have issues spinning up containers, use: <br/>
sudo docker compose logs CONTAINERNAME <br/>
To spin the containers down: <br/>
sudo docker compose down <br/>
If you also want to delete the persisted database volume: <br/>
sudo docker compose down -v
