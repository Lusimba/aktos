# aktos

Aktos assignment project.

ssh and install --sudo apt-get install -y build-essential as part of docker setup

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

add these as env var - POSTGRES_USER=user - POSTGRES_PASSWORD=password - POSTGRES_DB=aktos

implement --wait for database, before starting the app.
