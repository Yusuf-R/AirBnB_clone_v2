#!/usr/bin/env bash
# installs Nginx if not already installed
# creates several directories as well as a sym link

# Install Nginx if not already installed
# -x is used to check if the file is avaiable and executable
# command -v will return the aboslute path + filename
# command -v nginx == /usr/sbin/nginx
if [ ! -x "$(command -v nginx)" ]; then
    sudo service "$(sudo lsof -i :80 | grep LISTEN | awk '{print $1}' | head -n 1)" stop &/dev/null;
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create the required directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file to test Nginx
echo "<html><head><title>Test HTML File</title></head><body><h1>This is a test.</h1></body></html>" | sudo tee /data/web_static/releases/test/index.html &>/dev/null

# Create a symbolic link to the test release
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set the ownership to ubuntu user and group
sudo chown -hR ubuntu:ubuntu /data/

# Configure user Nginx to serve content from the current release base on the user credentials
sudo sed -i '0,/^\(\s*\)server_name\s*.*$/s//\1server_name tavish.tech www.tavish.tech;/' /etc/nginx/sites-available/default
sudo sed -i '0,/^\(\s*\)server_name tavish.tech www.tavish.tech;$/s//&\n\n\1location \/hbnb_static {\n\1\1alias \/data\/web_static\/current\/;\n\1\1autoindex off;\n\1}/' /etc/nginx/sites-available/default

# Restart the Nginx
sudo service nginx stop &>/dev/null
sudo service nginx start &>/dev/null
