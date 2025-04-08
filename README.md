# Proxmox VM Automation Web App - README

## Project Overview

This project is a beginner-friendly DevOps application that demonstrates VM automation in Proxmox environments. It provides a web interface for creating and managing virtual machines with software options and auto-scaling capabilities based on CPU usage.

## Features

- **VM Creation**: Create virtual machines in Proxmox with a simple web interface
- **Software Options**: Deploy VMs with ARR suite or open-source office suite for Windows 10 telecom users
- **Auto-Scaling**: Automatically scale VM resources based on CPU usage
- **Secure Authentication**: OAuth with Multi-Factor Authentication (MFA)
- **Responsive Design**: Mobile-friendly interface built with Bootstrap

## Technology Stack

- **Backend**: Python 3.10+ with Flask framework
- **Frontend**: HTML5, CSS3, JavaScript with Bootstrap 5
- **Database**: SQLite (development) / PostgreSQL (production)
- **Proxmox Integration**: proxmoxer library
- **Authentication**: Flask-Login with pyotp for MFA
- **API**: RESTful API design with Flask-RESTful

## Project Structure

```
proxmox-vm-automation/
├── app/                        # Application package
│   ├── controllers/            # Route handlers
│   │   ├── api.py              # API endpoints
│   │   ├── auth.py             # Authentication routes
│   │   ├── main.py             # Main routes
│   │   └── vm.py               # VM management routes
│   ├── models/                 # Database models
│   │   └── models.py           # User, VM, and ScalingEvent models
│   ├── services/               # Business logic
│   │   ├── auto_scaling_service.py  # Auto-scaling functionality
│   │   └── proxmox_service.py  # Proxmox API integration
│   ├── static/                 # Static assets
│   │   ├── css/                # CSS files
│   │   ├── js/                 # JavaScript files
│   │   └── img/                # Images
│   ├── templates/              # HTML templates
│   │   ├── auth/               # Authentication templates
│   │   ├── vm/                 # VM management templates
│   │   ├── base.html           # Base template
│   │   ├── index.html          # Home page
│   │   └── dashboard.html      # Dashboard
│   ├── __init__.py             # Application factory
│   ├── config.py               # Configuration
│   └── app.py                  # Application entry point
├── venv/                       # Virtual environment
├── requirements.txt            # Dependencies
├── init_db.sh                  # Database initialization script
├── testing_guide.md            # Testing documentation
├── user_guide.md               # User documentation
└── README.md                   # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cl00dz/VMAutomation.git
cd VMAutomation
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

## Configuration

The application can be configured through environment variables or a `.env` file:

- `PROXMOX_HOST`: Hostname or IP address of your Proxmox server
- `PROXMOX_USER`: Proxmox API username (e.g., `root@pam`)
- `PROXMOX_TOKEN_NAME`: API token name
- `PROXMOX_TOKEN_VALUE`: API token value
- `SECRET_KEY`: Secret key for session encryption
- `FLASK_CONFIG`: Configuration environment (`development`, `testing`, or `production`)
- `DATABASE_URL`: Database URL for production (PostgreSQL)

## Auto-Scaling

The auto-scaling functionality monitors CPU usage of VMs and automatically adjusts resources based on configurable thresholds:

- When CPU usage exceeds the high threshold (default: 80%), the VM is scaled up
- When CPU usage falls below the low threshold (default: 20%), the VM is scaled down
- Scaling events are recorded and can be viewed in the dashboard

## Documentation

- [User Guide](user_guide.md): Comprehensive guide for end users
- [Testing Guide](testing_guide.md): Instructions for testing the application

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Proxmox VE](https://www.proxmox.com/en/proxmox-ve) for the virtualization platform
- [proxmoxer](https://github.com/proxmoxer/proxmoxer) for the Python client library
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Bootstrap](https://getbootstrap.com/) for the frontend framework
