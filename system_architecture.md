# Proxmox VM Automation Web App - System Architecture

## Overview

This document outlines the system architecture for a beginner-friendly DevOps project that demonstrates VM automation in Proxmox. The application will provide a web interface for creating VMs with different software options (ARR suite and open-source office suite) and implement auto-scaling based on CPU usage.

## System Components

### 1. Frontend Layer

**Technology Stack:**
- HTML5, CSS3 with Bootstrap 5 (responsive design)
- JavaScript with minimal dependencies
- Simple, intuitive UI with a focus on usability

**Key Features:**
- Dashboard for VM monitoring and management
- VM creation form with dropdown menu for software options
- Auto-scaling configuration interface
- Authentication and user management
- Mobile-responsive design

### 2. Backend Layer

**Technology Stack:**
- Python 3.10+ with Flask framework
- RESTful API design
- proxmoxer library for Proxmox API integration
- SQLite for development, PostgreSQL for production
- OAuth 2.0 with MFA support

**Key Components:**
- **Authentication Service**: Handles user authentication with OAuth and MFA
- **VM Management Service**: Interfaces with Proxmox API for VM operations
- **Software Installation Service**: Manages installation of selected software packages
- **Auto-scaling Service**: Monitors CPU usage and triggers scaling events
- **Logging Service**: Records system events and user actions

### 3. Database Layer

**Schema Design:**
- Users table: Stores user information and authentication details
- VMs table: Stores VM configurations and status
- Software table: Stores available software options
- Auto-scaling table: Stores auto-scaling rules and thresholds
- Logs table: Stores system logs and audit trails

### 4. Integration Layer

**Proxmox Integration:**
- Uses proxmoxer library to communicate with Proxmox API
- Implements API token-based authentication
- Handles VM lifecycle operations (create, start, stop, delete)
- Monitors VM resource usage

**Software Integration:**
- ARR Suite components (Sonarr, Radarr, etc.)
- Open-source office suites (LibreOffice, OpenOffice)
- Windows 10 base image for telecom users

### 5. Auto-scaling Layer

**Components:**
- CPU usage monitoring service
- Rule-based scaling engine
- Resource allocation manager
- Scaling history and analytics

**Functionality:**
- Monitors CPU usage at configurable intervals
- Applies predefined scaling rules based on thresholds
- Adjusts VM resources (CPU cores, memory) automatically
- Provides scaling history and performance metrics

### 6. Security Layer

**Components:**
- OAuth 2.0 authentication
- Multi-factor authentication (MFA)
- Role-based access control
- API token management
- Audit logging

## System Workflow

1. **User Authentication**:
   - User logs in via web interface using OAuth
   - MFA verification is required for enhanced security
   - Session token is generated for subsequent requests

2. **VM Creation**:
   - User selects VM specifications from the web interface
   - User selects software options from dropdown menu (ARR suite, open-source office suite)
   - Backend validates the request and forwards to Proxmox API
   - Proxmox creates the VM with specified parameters
   - Software installation scripts are triggered based on selection

3. **Auto-scaling**:
   - System continuously monitors CPU usage of VMs
   - When CPU usage exceeds threshold, auto-scaling is triggered
   - Resources are adjusted according to predefined rules
   - Scaling events are logged for auditing and analysis

4. **VM Management**:
   - Users can view, start, stop, and delete VMs
   - Resource usage statistics are displayed in real-time
   - Scaling history and events are available for review

## Deployment Architecture

**Development Environment**:
- Local development using Docker containers
- SQLite database for simplicity
- Mock Proxmox API for testing

**Production Environment**:
- Deployed on user's existing Proxmox environment
- PostgreSQL database for production data
- Secure API token for Proxmox integration
- HTTPS for secure communication

## Technical Considerations

1. **Scalability**:
   - Stateless backend design for horizontal scaling
   - Database connection pooling
   - Caching for frequently accessed data

2. **Security**:
   - HTTPS for all communications
   - OAuth 2.0 with MFA for authentication
   - API token rotation and management
   - Input validation and sanitization
   - Protection against common web vulnerabilities

3. **Reliability**:
   - Error handling and graceful degradation
   - Transaction management for database operations
   - Logging and monitoring for troubleshooting
   - Automated backups for database

4. **Maintainability**:
   - Modular code structure
   - Comprehensive documentation
   - Version control with Git
   - Automated testing

## Diagrams

### System Architecture Diagram

```
+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
|  Web Interface   |<--->|  Backend API     |<--->|  Proxmox API     |
|  (Bootstrap/JS)  |     |  (Python/Flask)  |     |  (proxmoxer)     |
|                  |     |                  |     |                  |
+------------------+     +------------------+     +------------------+
                               ^      ^
                               |      |
                               v      v
+------------------+     +------------------+
|                  |     |                  |
|  Database        |     |  Auto-scaling    |
|  (SQLite/Postgres)|     |  Service        |
|                  |     |  (Python)        |
+------------------+     +------------------+
```

### VM Creation Workflow

```
+--------+    +--------+    +--------+    +--------+    +--------+
|        |    |        |    |        |    |        |    |        |
| User   |--->| Web UI |--->| Backend|--->| Proxmox|--->| VM     |
| Request|    | Form   |    | API    |    | API    |    | Created|
|        |    |        |    |        |    |        |    |        |
+--------+    +--------+    +--------+    +--------+    +--------+
                                |
                                v
                          +--------+
                          |        |
                          |Software|
                          |Install |
                          |        |
                          +--------+
```

### Auto-scaling Workflow

```
+--------+    +--------+    +--------+    +--------+
|        |    |        |    |        |    |        |
| CPU    |--->|Threshold--->|Resource|--->|Scaling |
| Monitor|    | Check  |    |Adjust  |    |Complete|
|        |    |        |    |        |    |        |
+--------+    +--------+    +--------+    +--------+
                  |
                  v
             +--------+
             |        |
             |Log     |
             |Event   |
             |        |
             +--------+
```

## Conclusion

This architecture provides a comprehensive foundation for a beginner-friendly DevOps project that demonstrates VM automation in Proxmox. The design prioritizes simplicity and usability while incorporating all the required features: VM creation with software options, auto-scaling based on CPU usage, and secure authentication with OAuth and MFA.

The modular approach allows for incremental development and testing, making it suitable for a learning project while still providing real-world utility. The use of popular, well-documented technologies ensures that the project remains accessible to beginners while demonstrating important DevOps concepts and skills.
