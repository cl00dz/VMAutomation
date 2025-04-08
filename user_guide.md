# Proxmox VM Automation Web App - User Guide

## Overview

The Proxmox VM Automation Web App is a beginner-friendly DevOps project that demonstrates VM automation in Proxmox environments. This application allows you to create, manage, and auto-scale virtual machines through a simple web interface.

## Features

- **VM Creation**: Create virtual machines in your Proxmox environment with a few clicks
- **Software Options**: Choose from pre-configured software options including ARR suite and open-source office suite
- **Auto-Scaling**: Automatically scale VM resources based on CPU usage
- **Secure Authentication**: OAuth with Multi-Factor Authentication (MFA) for enhanced security
- **Responsive Design**: Access the application from any device with a responsive web interface

## Getting Started

### Prerequisites

- A running Proxmox VE environment
- API token access to your Proxmox environment
- Python 3.10+ installed
- Git installed

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/proxmox-vm-automation.git
cd proxmox-vm-automation
```

2. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Create a `.env` file with your Proxmox credentials:
```bash
PROXMOX_HOST=your-proxmox-host.example.com
PROXMOX_USER=root@pam
PROXMOX_TOKEN_NAME=your-token-name
PROXMOX_TOKEN_VALUE=your-token-value
SECRET_KEY=your-secret-key
```

4. Initialize the database:
```bash
chmod +x init_db.sh
./init_db.sh
```

5. Start the application:
```bash
export FLASK_APP=app.app
flask run --host=0.0.0.0 --port=5000
```

6. Access the application in your web browser at `http://localhost:5000`

## User Guide

### Registration and Login

1. **Register a new account**:
   - Click on the "Register" button in the navigation bar
   - Fill in your username, email, and password
   - Submit the form
   - Set up Multi-Factor Authentication (MFA) by scanning the QR code with an authenticator app
   - Enter the MFA code to complete registration

2. **Login to your account**:
   - Click on the "Login" button in the navigation bar
   - Enter your username and password
   - Enter your MFA code when prompted
   - You will be redirected to the dashboard

### Dashboard

The dashboard provides an overview of your virtual machines and recent auto-scaling events:

- **Stats Overview**: Shows the total number of VMs, running VMs, total CPU cores, and total memory
- **Quick Actions**: Buttons for creating new VMs, viewing all VMs, and managing your profile
- **Recent VMs**: A list of your most recently created VMs with basic information
- **Recent Auto-Scaling Events**: A timeline of recent auto-scaling events for your VMs

### Creating a VM

1. Click on the "Create New VM" button on the dashboard or VM list page
2. Fill in the VM creation form:
   - **Basic Information**: VM name, Proxmox node, operating system, and description
   - **Hardware Configuration**: CPU cores, memory, and disk size
   - **Software Options**: Select from available software options (ARR suite, open-source office suite)
   - **Auto-Scaling Configuration**: Enable/disable auto-scaling and set CPU thresholds
3. Click the "Create VM" button to create the VM
4. You will be redirected to the VM details page once the VM is created

### Managing VMs

The VM list page shows all your virtual machines with basic information and actions:

- **Start/Stop**: Start or stop a VM with the respective buttons
- **Details**: View detailed information about a VM by clicking the "Details" button
- **Delete**: Delete a VM by clicking the "Delete" button (this action cannot be undone)

### VM Details

The VM details page provides comprehensive information about a specific VM:

- **Basic Information**: VM name, ID, node, status, and creation date
- **Hardware Configuration**: CPU cores, memory, and disk size
- **Software**: Installed software options
- **Auto-Scaling**: Auto-scaling status and configuration
- **Resource Usage**: Current CPU and memory usage
- **Actions**: Buttons for starting, stopping, and deleting the VM

### Auto-Scaling Configuration

To configure auto-scaling for a VM:

1. Navigate to the VM details page
2. Click on the "Auto-Scaling" tab
3. Enable auto-scaling by toggling the switch
4. Set the CPU thresholds:
   - **High Threshold**: The CPU usage percentage above which the VM will scale up
   - **Low Threshold**: The CPU usage percentage below which the VM will scale down
5. Set the scaling interval (how often to check CPU usage)
6. Click "Save" to apply the configuration

## Auto-Scaling Behavior

When auto-scaling is enabled for a VM, the system will:

1. Monitor the VM's CPU usage at regular intervals
2. Scale up the VM (increase CPU cores and memory) when CPU usage exceeds the high threshold
3. Scale down the VM (decrease CPU cores and memory) when CPU usage falls below the low threshold
4. Record scaling events in the database for later review

The auto-scaling service follows these rules:

- CPU cores can scale between 1 and 4 cores
- Memory can scale between 512 MB and 8 GB
- Scaling up increases CPU cores by 1 and memory by 25%
- Scaling down decreases CPU cores by 1 and memory by 20%
- The VM must be running for auto-scaling to take effect

## Troubleshooting

### Common Issues

1. **Cannot connect to Proxmox**:
   - Verify that your Proxmox host is reachable
   - Check that your API token has sufficient permissions
   - Ensure that your token is not expired

2. **VM creation fails**:
   - Check the application logs for specific error messages
   - Verify that the Proxmox node has sufficient resources
   - Ensure that the storage specified in the configuration exists

3. **Auto-scaling doesn't work**:
   - Verify that the VM is running
   - Check that auto-scaling is enabled for the VM
   - Ensure that the CPU thresholds are set correctly
   - Check the application logs for any errors

### Getting Help

If you encounter any issues not covered in this guide, please:

1. Check the application logs in the `logs` directory
2. Refer to the testing guide for additional troubleshooting steps
3. Contact the development team for support

## Conclusion

The Proxmox VM Automation Web App provides a simple, user-friendly interface for managing virtual machines in your Proxmox environment. With features like software options and auto-scaling, it's a great way to showcase your DevOps skills and streamline your VM management workflow.
