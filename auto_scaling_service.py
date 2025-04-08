import time
import logging
import threading
from flask import current_app
from app import db
from app.models.models import VM, ScalingEvent
from app.services.proxmox_service import ProxmoxService

logger = logging.getLogger(__name__)

class AutoScalingService:
    """Service for auto-scaling VMs based on CPU usage."""
    
    def __init__(self):
        """Initialize the auto-scaling service."""
        self.proxmox_service = ProxmoxService()
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the auto-scaling service in a background thread."""
        if self.running:
            logger.info("Auto-scaling service is already running")
            return False
        
        self.running = True
        self.thread = threading.Thread(target=self._run_scaling_loop)
        self.thread.daemon = True
        self.thread.start()
        logger.info("Auto-scaling service started")
        return True
    
    def stop(self):
        """Stop the auto-scaling service."""
        if not self.running:
            logger.info("Auto-scaling service is not running")
            return False
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Auto-scaling service stopped")
        return True
    
    def _run_scaling_loop(self):
        """Main loop for the auto-scaling service."""
        logger.info("Auto-scaling loop started")
        
        while self.running:
            try:
                with current_app.app_context():
                    self._check_vms_for_scaling()
            except Exception as e:
                logger.error(f"Error in auto-scaling loop: {str(e)}")
            
            # Sleep for a while before the next check
            time.sleep(60)  # Check every minute
    
    def _check_vms_for_scaling(self):
        """Check all VMs with auto-scaling enabled and scale if necessary."""
        # Get all VMs with auto-scaling enabled
        vms = VM.query.filter_by(auto_scaling_enabled=True).all()
        
        if not vms:
            logger.debug("No VMs with auto-scaling enabled")
            return
        
        logger.info(f"Checking {len(vms)} VMs for auto-scaling")
        
        for vm in vms:
            try:
                self._check_vm_for_scaling(vm)
            except Exception as e:
                logger.error(f"Error checking VM {vm.id} for scaling: {str(e)}")
    
    def _check_vm_for_scaling(self, vm):
        """Check a single VM for scaling needs."""
        # Skip VMs that are not running
        if vm.status != 'running':
            logger.debug(f"VM {vm.id} is not running, skipping auto-scaling check")
            return
        
        # Get current CPU usage
        resources = self.proxmox_service.get_vm_resources(vm.proxmox_node, vm.proxmox_id)
        if not resources:
            logger.warning(f"Could not get resources for VM {vm.id}")
            return
        
        cpu_usage = resources.get('cpu_usage', 0)
        logger.debug(f"VM {vm.id} CPU usage: {cpu_usage}%")
        
        # Get thresholds from config
        cpu_threshold_high = current_app.config['CPU_THRESHOLD_HIGH']
        cpu_threshold_low = current_app.config['CPU_THRESHOLD_LOW']
        
        # Check if scaling is needed
        if cpu_usage > cpu_threshold_high:
            self._scale_up(vm, cpu_usage)
        elif cpu_usage < cpu_threshold_low:
            self._scale_down(vm, cpu_usage)
    
    def _scale_up(self, vm, cpu_usage):
        """Scale up a VM by increasing CPU cores and memory."""
        logger.info(f"Scaling up VM {vm.id} (CPU usage: {cpu_usage}%)")
        
        # Get current configuration
        config = self.proxmox_service.get_vm_config(vm.proxmox_node, vm.proxmox_id)
        if not config:
            logger.warning(f"Could not get config for VM {vm.id}")
            return
        
        # Calculate new resources
        old_cpu_cores = vm.cpu_cores
        old_memory_mb = vm.memory_mb
        
        # Increase CPU cores by 1, up to a maximum of 4
        new_cpu_cores = min(old_cpu_cores + 1, 4)
        
        # Increase memory by 25%, up to a maximum of 8192 MB (8 GB)
        new_memory_mb = min(int(old_memory_mb * 1.25), 8192)
        
        # Only proceed if there's an actual change
        if new_cpu_cores == old_cpu_cores and new_memory_mb == old_memory_mb:
            logger.info(f"VM {vm.id} already at maximum resources, not scaling up")
            return
        
        # Update VM configuration in Proxmox
        params = {}
        if new_cpu_cores != old_cpu_cores:
            params['cores'] = new_cpu_cores
        if new_memory_mb != old_memory_mb:
            params['memory'] = new_memory_mb
        
        if params:
            success = self.proxmox_service.update_vm_config(vm.proxmox_node, vm.proxmox_id, params)
            if success:
                # Update VM record in database
                vm.cpu_cores = new_cpu_cores
                vm.memory_mb = new_memory_mb
                
                # Create scaling event record
                event = ScalingEvent(
                    event_type='scale_up',
                    cpu_usage=cpu_usage,
                    old_cpu_cores=old_cpu_cores,
                    new_cpu_cores=new_cpu_cores,
                    old_memory_mb=old_memory_mb,
                    new_memory_mb=new_memory_mb,
                    vm_id=vm.id
                )
                
                db.session.add(event)
                db.session.commit()
                
                logger.info(f"VM {vm.id} scaled up: CPU {old_cpu_cores} -> {new_cpu_cores}, Memory {old_memory_mb} -> {new_memory_mb}")
            else:
                logger.error(f"Failed to scale up VM {vm.id}")
    
    def _scale_down(self, vm, cpu_usage):
        """Scale down a VM by decreasing CPU cores and memory."""
        logger.info(f"Scaling down VM {vm.id} (CPU usage: {cpu_usage}%)")
        
        # Get current configuration
        config = self.proxmox_service.get_vm_config(vm.proxmox_node, vm.proxmox_id)
        if not config:
            logger.warning(f"Could not get config for VM {vm.id}")
            return
        
        # Calculate new resources
        old_cpu_cores = vm.cpu_cores
        old_memory_mb = vm.memory_mb
        
        # Decrease CPU cores by 1, down to a minimum of 1
        new_cpu_cores = max(old_cpu_cores - 1, 1)
        
        # Decrease memory by 20%, down to a minimum of 512 MB
        new_memory_mb = max(int(old_memory_mb * 0.8), 512)
        
        # Only proceed if there's an actual change
        if new_cpu_cores == old_cpu_cores and new_memory_mb == old_memory_mb:
            logger.info(f"VM {vm.id} already at minimum resources, not scaling down")
            return
        
        # Update VM configuration in Proxmox
        params = {}
        if new_cpu_cores != old_cpu_cores:
            params['cores'] = new_cpu_cores
        if new_memory_mb != old_memory_mb:
            params['memory'] = new_memory_mb
        
        if params:
            success = self.proxmox_service.update_vm_config(vm.proxmox_node, vm.proxmox_id, params)
            if success:
                # Update VM record in database
                vm.cpu_cores = new_cpu_cores
                vm.memory_mb = new_memory_mb
                
                # Create scaling event record
                event = ScalingEvent(
                    event_type='scale_down',
                    cpu_usage=cpu_usage,
                    old_cpu_cores=old_cpu_cores,
                    new_cpu_cores=new_cpu_cores,
                    old_memory_mb=old_memory_mb,
                    new_memory_mb=new_memory_mb,
                    vm_id=vm.id
                )
                
                db.session.add(event)
                db.session.commit()
                
                logger.info(f"VM {vm.id} scaled down: CPU {old_cpu_cores} -> {new_cpu_cores}, Memory {old_memory_mb} -> {new_memory_mb}")
            else:
                logger.error(f"Failed to scale down VM {vm.id}")
