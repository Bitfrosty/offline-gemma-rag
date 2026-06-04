#!/usr/bin/env bash

set -e

echo "Updating packages..."
sudo apt update
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    build-essential
sudo apt install -y ca-certificates curl gnupg
sudo update-ca-certificates
	
echo "Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

echo "Pulling models..."
ollama pull gemma4:e2b
ollama pull nomic-embed-text

echo "Installing MongoDB..."

curl -fsSL https://pgp.mongodb.com/server-8.0.asc | \
sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg \
--dearmor

echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | \
sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list

sudo apt update
sudo apt install -y mongodb-org

echo "Creating MongoDB data directory..."
mkdir -p ~/mongodb-data

echo "Creating Python virtual environment..."
python3 -m venv venv

echo "Activating venv..."
source venv/bin/activate

echo "Installing Python requirements..."

if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    pip install \
        fastapi \
        uvicorn \
        requests \
        pymongo \
        numpy \
        python-multipart
fi

echo "Setup complete."
echo ""
echo "Start MongoDB:"
echo "mongod --dbpath ~/mongodb-data"
echo ""
echo "Start Ollama:"
echo "ollama serve"
echo ""
echo "Start backend:"
echo "./backend.sh"
