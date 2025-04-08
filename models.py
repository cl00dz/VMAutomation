from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    """User model for authentication and authorization."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    mfa_secret = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    vms = db.relationship('VM', backref='owner', lazy='dynamic')
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class VM(db.Model):
    """Virtual Machine model."""
    __tablename__ = 'vms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    proxmox_id = db.Column(db.Integer)
    proxmox_node = db.Column(db.String(64))
    status = db.Column(db.String(16), default='stopped')
    cpu_cores = db.Column(db.Integer)
    memory_mb = db.Column(db.Integer)
    disk_gb = db.Column(db.Integer)
    os_type = db.Column(db.String(32))
    software_installed = db.Column(db.String(256))
    auto_scaling_enabled = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    scaling_events = db.relationship('ScalingEvent', backref='vm', lazy='dynamic')
    
    def __repr__(self):
        return f'<VM {self.name} ({self.proxmox_id})>'


class ScalingEvent(db.Model):
    """Auto-scaling event model."""
    __tablename__ = 'scaling_events'
    
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(16))  # 'scale_up' or 'scale_down'
    cpu_usage = db.Column(db.Float)  # percentage
    old_cpu_cores = db.Column(db.Integer)
    new_cpu_cores = db.Column(db.Integer)
    old_memory_mb = db.Column(db.Integer)
    new_memory_mb = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    vm_id = db.Column(db.Integer, db.ForeignKey('vms.id'))
    
    def __repr__(self):
        return f'<ScalingEvent {self.event_type} for VM {self.vm_id}>'
