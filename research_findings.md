# Proxmox VM Automation Web App - Research Findings

## Proxmox API
- Proxmox uses a REST-like API with JSON as the primary data format
- Authentication can be done via ticket-based or API token-based methods
- API tokens are recommended for automation as they don't require CSRF tokens for POST/PUT/DELETE operations
- Python client libraries are available, with proxmoxer being the most popular and actively maintained
- The API allows for complete VM management including creation, modification, and deletion

## ARR Suite Components
- ARR (Application Request Routing) is a Microsoft IIS extension for load balancing and routing
- For media management, the "arr" suite typically refers to applications like:
  - Sonarr: TV show management
  - Radarr: Movie management
  - Lidarr: Music management
  - Readarr: Book management
  - Prowlarr: Indexer management

## Open Source Office Suite Options
- LibreOffice: Comprehensive, mature, and widely used
- Apache OpenOffice: Another popular option with similar features
- OnlyOffice: Modern interface, good MS Office compatibility
- FreeOffice: Simple alternative with good compatibility

## CPU-based Auto-scaling
- Found GitHub project "proxmox-vm-autoscale" that automatically adjusts VM resources based on CPU usage
- Proxmox has built-in monitoring capabilities accessible via API
- Dynamic Memory Management is available for KVM VMs through ballooning
- Custom scripts can be created to monitor CPU usage and trigger scaling events

## OAuth with MFA Implementation
- Several Python libraries support OAuth 2.0 implementation
- OAuthLib and Requests libraries are commonly used
- MFA can be implemented using libraries like pyotp for TOTP-based authentication
- Okta and other identity providers offer SDKs for Python that support MFA

## Technology Stack Recommendations (Beginner-Friendly)
- Backend: Python with Flask (simple, well-documented)
- Frontend: Bootstrap with minimal JavaScript (easy to learn, responsive design)
- Database: SQLite for development, PostgreSQL for production
- Authentication: Flask-Login with OAuth integration
- Proxmox Integration: proxmoxer library
- Deployment: Docker for containerization (optional, simplifies deployment)
