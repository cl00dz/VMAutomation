# Proxmox VM Automation Web App - Testing Guide

This document provides instructions for testing the Proxmox VM Automation Web App.

## Prerequisites

Before testing, ensure you have:

1. A running Proxmox VE environment
2. API token access to your Proxmox environment
3. Python 3.10+ installed
4. Git installed

## Setup for Testing

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

## Test Cases

### 1. User Authentication

#### 1.1 User Registration
- Navigate to `/auth/register`
- Fill in the registration form with a username, email, and password
- Submit the form
- Verify that you are redirected to the MFA setup page
- Scan the QR code with an authenticator app
- Enter the MFA code
- Verify that you are redirected to the login page

#### 1.2 User Login
- Navigate to `/auth/login`
- Enter your username and password
- Submit the form
- Enter your MFA code when prompted
- Verify that you are redirected to the dashboard

### 2. VM Management

#### 2.1 VM Creation
- Navigate to `/vm/create`
- Fill in the VM creation form with:
  - VM name
  - Proxmox node
  - Operating system (Windows 10)
  - Hardware configuration (CPU cores, memory, disk size)
  - Software options (ARR suite or open-source office suite)
  - Auto-scaling configuration (enable/disable, thresholds)
- Submit the form
- Verify that you are redirected to the VM details page
- Verify that the VM appears in the Proxmox web interface

#### 2.2 VM Operations
- Navigate to `/vm`
- Find your VM in the list
- Test the Start button
- Verify that the VM status changes to "running"
- Test the Stop button
- Verify that the VM status changes to "stopped"
- Navigate to the VM details page
- Verify that all VM information is displayed correctly

### 3. Auto-Scaling

#### 3.1 Auto-Scaling Configuration
- Navigate to the VM details page
- Click on the "Auto-Scaling" tab
- Enable auto-scaling
- Set CPU thresholds (high and low)
- Save the configuration
- Verify that the configuration is saved correctly

#### 3.2 Auto-Scaling Functionality
- Start the VM
- Generate CPU load on the VM (e.g., run a CPU-intensive task)
- Wait for the auto-scaling interval to pass
- Verify that the VM is scaled up (increased CPU cores and memory)
- Reduce the CPU load
- Wait for the auto-scaling interval to pass
- Verify that the VM is scaled down (decreased CPU cores and memory)
- Check the scaling events in the dashboard

### 4. API Testing

#### 4.1 Get Nodes
- Send a GET request to `/api/nodes`
- Verify that the response contains a list of Proxmox nodes

#### 4.2 Get VMs
- Send a GET request to `/api/vms`
- Verify that the response contains a list of VMs

#### 4.3 Create VM
- Send a POST request to `/api/vms` with VM configuration
- Verify that the response indicates successful VM creation
- Verify that the VM appears in the Proxmox web interface

#### 4.4 VM Operations
- Send a POST request to `/api/vms/{vmid}/start`
- Verify that the VM starts
- Send a POST request to `/api/vms/{vmid}/stop`
- Verify that the VM stops
- Send a DELETE request to `/api/vms/{vmid}`
- Verify that the VM is deleted

## Troubleshooting

### Common Issues

1. **Connection to Proxmox fails**
   - Verify that the Proxmox host is reachable
   - Check that the API token has sufficient permissions
   - Ensure that the token is not expired

2. **Database initialization fails**
   - Check that you have write permissions to the project directory
   - Ensure that SQLite is installed on your system

3. **Auto-scaling doesn't work**
   - Verify that the VM is running
   - Check that auto-scaling is enabled for the VM
   - Ensure that the CPU thresholds are set correctly
   - Check the application logs for any errors

### Logging

The application logs are stored in the `logs` directory. Check these logs for any errors or warnings that might help diagnose issues.

## Conclusion

This testing guide covers the basic functionality of the Proxmox VM Automation Web App. If you encounter any issues not covered in this guide, please refer to the documentation or contact the development team.
