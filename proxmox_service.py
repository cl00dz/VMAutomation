from proxmoxer import ProxmoxAPI
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class ProxmoxService:
    """Service for interacting with Proxmox API."""
    
    def __init__(self):
        """Initialize the Proxmox API connection."""
        self.proxmox = None
        self.connected = False
    
    def connect(self):
        """Connect to Proxmox API using token authentication."""
        try:
            config = current_app.config
            self.proxmox = ProxmoxAPI(
                host=config['PROXMOX_HOST'],
                user=config['PROXMOX_USER'],
                token_name=config['PROXMOX_TOKEN_NAME'],
                token_value=config['PROXMOX_TOKEN_VALUE'],
                verify_ssl=False
            )
            self.connected = True
            logger.info(f"Connected to Proxmox host: {config['PROXMOX_HOST']}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Proxmox API: {str(e)}")
            self.connected = False
            return False
    
    def get_nodes(self):
        """Get list of Proxmox nodes."""
        if not self.connected and not self.connect():
            return []
        
        try:
            nodes = self.proxmox.nodes.get()
            return nodes
        except Exception as e:
            logger.error(f"Failed to get nodes: {str(e)}")
            return []
    
    def get_vms(self, node=None):
        """Get list of VMs, optionally filtered by node."""
        if not self.connected and not self.connect():
            return []
        
        try:
            vms = []
            nodes = [node] if node else [n['node'] for n in self.get_nodes()]
            
            for node_name in nodes:
                node_vms = self.proxmox.nodes(node_name).qemu.get()
                for vm in node_vms:
                    vm['node'] = node_name
                vms.extend(node_vms)
            
            return vms
        except Exception as e:
            logger.error(f"Failed to get VMs: {str(e)}")
            return []
    
    def get_vm(self, node, vmid):
        """Get VM details by node and ID."""
        if not self.connected and not self.connect():
            return None
        
        try:
            vm = self.proxmox.nodes(node).qemu(vmid).status.current.get()
            vm['node'] = node
            vm['vmid'] = vmid
            return vm
        except Exception as e:
            logger.error(f"Failed to get VM {vmid} on node {node}: {str(e)}")
            return None
    
    def create_vm(self, node, params):
        """Create a new VM on the specified node."""
        if not self.connected and not self.connect():
            return None
        
        try:
            result = self.proxmox.nodes(node).qemu.create(**params)
            return result
        except Exception as e:
            logger.error(f"Failed to create VM on node {node}: {str(e)}")
            return None
    
    def start_vm(self, node, vmid):
        """Start a VM."""
        if not self.connected and not self.connect():
            return False
        
        try:
            self.proxmox.nodes(node).qemu(vmid).status.start.post()
            return True
        except Exception as e:
            logger.error(f"Failed to start VM {vmid} on node {node}: {str(e)}")
            return False
    
    def stop_vm(self, node, vmid):
        """Stop a VM."""
        if not self.connected and not self.connect():
            return False
        
        try:
            self.proxmox.nodes(node).qemu(vmid).status.stop.post()
            return True
        except Exception as e:
            logger.error(f"Failed to stop VM {vmid} on node {node}: {str(e)}")
            return False
    
    def delete_vm(self, node, vmid):
        """Delete a VM."""
        if not self.connected and not self.connect():
            return False
        
        try:
            self.proxmox.nodes(node).qemu(vmid).delete()
            return True
        except Exception as e:
            logger.error(f"Failed to delete VM {vmid} on node {node}: {str(e)}")
            return False
    
    def get_vm_config(self, node, vmid):
        """Get VM configuration."""
        if not self.connected and not self.connect():
            return None
        
        try:
            config = self.proxmox.nodes(node).qemu(vmid).config.get()
            return config
        except Exception as e:
            logger.error(f"Failed to get VM {vmid} config on node {node}: {str(e)}")
            return None
    
    def update_vm_config(self, node, vmid, params):
        """Update VM configuration."""
        if not self.connected and not self.connect():
            return False
        
        try:
            self.proxmox.nodes(node).qemu(vmid).config.put(**params)
            return True
        except Exception as e:
            logger.error(f"Failed to update VM {vmid} config on node {node}: {str(e)}")
            return False
    
    def get_vm_status(self, node, vmid):
        """Get VM status."""
        if not self.connected and not self.connect():
            return None
        
        try:
            status = self.proxmox.nodes(node).qemu(vmid).status.current.get()
            return status
        except Exception as e:
            logger.error(f"Failed to get VM {vmid} status on node {node}: {str(e)}")
            return None
    
    def get_vm_resources(self, node, vmid):
        """Get VM resource usage."""
        if not self.connected and not self.connect():
            return None
        
        try:
            status = self.get_vm_status(node, vmid)
            if not status:
                return None
            
            resources = {
                'cpu_usage': status.get('cpu', 0) * 100,  # Convert to percentage
                'memory_usage': status.get('mem', 0) / (1024 * 1024),  # Convert to MB
                'disk_usage': status.get('disk', 0) / (1024 * 1024 * 1024),  # Convert to GB
                'uptime': status.get('uptime', 0)
            }
            return resources
        except Exception as e:
            logger.error(f"Failed to get VM {vmid} resources on node {node}: {str(e)}")
            return None
