#!/bin/bash

# Create a zip archive of the project
echo "Creating project archive..."
cd /home/ubuntu
zip -r proxmox_vm_automation.zip devops_project -x "devops_project/venv/*"
echo "Archive created: /home/ubuntu/proxmox_vm_automation.zip"
