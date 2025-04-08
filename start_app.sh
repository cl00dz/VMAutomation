#!/bin/bash

# Start the Proxmox VM Automation Web App
echo "Starting Proxmox VM Automation Web App..."
cd /home/ubuntu/devops_project
source venv/bin/activate
export FLASK_APP=app.app
flask run --host=0.0.0.0 --port=5000
