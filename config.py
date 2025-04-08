import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-development-only')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Proxmox configuration
    PROXMOX_HOST = os.environ.get('PROXMOX_HOST', 'localhost')
    PROXMOX_USER = os.environ.get('PROXMOX_USER', 'root@pam')
    PROXMOX_TOKEN_NAME = os.environ.get('PROXMOX_TOKEN_NAME', '')
    PROXMOX_TOKEN_VALUE = os.environ.get('PROXMOX_TOKEN_VALUE', '')
    
    # OAuth configuration
    OAUTH_PROVIDER = os.environ.get('OAUTH_PROVIDER', 'google')
    OAUTH_CLIENT_ID = os.environ.get('OAUTH_CLIENT_ID', '')
    OAUTH_CLIENT_SECRET = os.environ.get('OAUTH_CLIENT_SECRET', '')
    
    # Auto-scaling configuration
    CPU_THRESHOLD_HIGH = float(os.environ.get('CPU_THRESHOLD_HIGH', '80.0'))  # percentage
    CPU_THRESHOLD_LOW = float(os.environ.get('CPU_THRESHOLD_LOW', '20.0'))  # percentage
    SCALING_INTERVAL = int(os.environ.get('SCALING_INTERVAL', '300'))  # seconds
    
    # Software options
    SOFTWARE_OPTIONS = {
        'arr_suite': {
            'name': 'ARR Suite',
            'description': 'Media management suite including Sonarr, Radarr, and related applications',
            'install_script': 'arr_suite_install.sh'
        },
        'office_suite': {
            'name': 'Open Source Office Suite',
            'description': 'LibreOffice for document, spreadsheet, and presentation editing',
            'install_script': 'libreoffice_install.sh'
        }
    }


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL', 'sqlite:///dev.db')


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'sqlite:///test.db')


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://user:pass@localhost/proxmox_vm_automation')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
