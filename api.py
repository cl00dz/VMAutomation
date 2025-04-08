from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from app.services.proxmox_service import ProxmoxService
from app.models.models import VM, ScalingEvent
from app import db
import logging

logger = logging.getLogger(__name__)
api_bp = Blueprint('api', __name__)
proxmox_service = ProxmoxService()

@api_bp.route('/nodes', methods=['GET'])
@login_required
def get_nodes():
    """Get all Proxmox nodes."""
    nodes = proxmox_service.get_nodes()
    return jsonify({'nodes': nodes})

@api_bp.route('/vms', methods=['GET'])
@login_required
def get_vms():
    """Get all VMs."""
    node = request.args.get('node')
    vms = proxmox_service.get_vms(node)
    return jsonify({'vms': vms})

@api_bp.route('/vms/<int:vmid>', methods=['GET'])
@login_required
def get_vm(vmid):
    """Get VM details."""
    node = request.args.get('node')
    if not node:
        return jsonify({'error': 'Node parameter is required'}), 400
    
    vm = proxmox_service.get_vm(node, vmid)
    if not vm:
        return jsonify({'error': 'VM not found'}), 404
    
    return jsonify({'vm': vm})

@api_bp.route('/vms', methods=['POST'])
@login_required
def create_vm():
    """Create a new VM."""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    node = data.get('node')
    if not node:
        return jsonify({'error': 'Node is required'}), 400
    
    # Prepare VM creation parameters
    params = {
        'name': data.get('name', f'vm-{current_user.username}'),
        'memory': data.get('memory', 1024),  # MB
        'cores': data.get('cores', 1),
        'sockets': data.get('sockets', 1),
        'net0': data.get('net0', 'virtio,bridge=vmbr0'),
        'ostype': data.get('ostype', 'win10'),
        'storage': data.get('storage', 'local-lvm'),
        'disk': data.get('disk', 'scsi0:local-lvm:10G'),
    }
    
    # Add optional parameters if provided
    if 'description' in data:
        params['description'] = data['description']
    
    # Create VM in Proxmox
    result = proxmox_service.create_vm(node, params)
    if not result:
        return jsonify({'error': 'Failed to create VM'}), 500
    
    # Get the VM ID from the result
    vmid = result.get('data')
    
    # Create VM record in database
    vm = VM(
        name=params['name'],
        proxmox_id=vmid,
        proxmox_node=node,
        status='stopped',
        cpu_cores=params['cores'],
        memory_mb=params['memory'],
        disk_gb=10,  # Extract from disk parameter
        os_type=params['ostype'],
        user_id=current_user.id
    )
    
    # Add software information if provided
    software = data.get('software', [])
    if software:
        vm.software_installed = ','.join(software)
    
    # Enable auto-scaling if requested
    vm.auto_scaling_enabled = data.get('auto_scaling_enabled', False)
    
    # Save to database
    db.session.add(vm)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'vm': {
            'id': vm.id,
            'proxmox_id': vm.proxmox_id,
            'name': vm.name,
            'node': vm.proxmox_node
        }
    }), 201

@api_bp.route('/vms/<int:vmid>/start', methods=['POST'])
@login_required
def start_vm(vmid):
    """Start a VM."""
    node = request.json.get('node')
    if not node:
        return jsonify({'error': 'Node is required'}), 400
    
    success = proxmox_service.start_vm(node, vmid)
    if not success:
        return jsonify({'error': 'Failed to start VM'}), 500
    
    # Update VM status in database
    vm = VM.query.filter_by(proxmox_id=vmid, proxmox_node=node).first()
    if vm:
        vm.status = 'running'
        db.session.commit()
    
    return jsonify({'success': True})

@api_bp.route('/vms/<int:vmid>/stop', methods=['POST'])
@login_required
def stop_vm(vmid):
    """Stop a VM."""
    node = request.json.get('node')
    if not node:
        return jsonify({'error': 'Node is required'}), 400
    
    success = proxmox_service.stop_vm(node, vmid)
    if not success:
        return jsonify({'error': 'Failed to stop VM'}), 500
    
    # Update VM status in database
    vm = VM.query.filter_by(proxmox_id=vmid, proxmox_node=node).first()
    if vm:
        vm.status = 'stopped'
        db.session.commit()
    
    return jsonify({'success': True})

@api_bp.route('/vms/<int:vmid>', methods=['DELETE'])
@login_required
def delete_vm(vmid):
    """Delete a VM."""
    node = request.json.get('node')
    if not node:
        return jsonify({'error': 'Node is required'}), 400
    
    success = proxmox_service.delete_vm(node, vmid)
    if not success:
        return jsonify({'error': 'Failed to delete VM'}), 500
    
    # Delete VM from database
    vm = VM.query.filter_by(proxmox_id=vmid, proxmox_node=node).first()
    if vm:
        db.session.delete(vm)
        db.session.commit()
    
    return jsonify({'success': True})

@api_bp.route('/vms/<int:vmid>/resources', methods=['GET'])
@login_required
def get_vm_resources(vmid):
    """Get VM resource usage."""
    node = request.args.get('node')
    if not node:
        return jsonify({'error': 'Node parameter is required'}), 400
    
    resources = proxmox_service.get_vm_resources(node, vmid)
    if not resources:
        return jsonify({'error': 'Failed to get VM resources'}), 500
    
    return jsonify({'resources': resources})

@api_bp.route('/vms/<int:vmid>/config', methods=['GET'])
@login_required
def get_vm_config(vmid):
    """Get VM configuration."""
    node = request.args.get('node')
    if not node:
        return jsonify({'error': 'Node parameter is required'}), 400
    
    config = proxmox_service.get_vm_config(node, vmid)
    if not config:
        return jsonify({'error': 'Failed to get VM configuration'}), 500
    
    return jsonify({'config': config})

@api_bp.route('/vms/<int:vmid>/config', methods=['PUT'])
@login_required
def update_vm_config(vmid):
    """Update VM configuration."""
    node = request.json.get('node')
    if not node:
        return jsonify({'error': 'Node is required'}), 400
    
    params = request.json.get('params', {})
    if not params:
        return jsonify({'error': 'No parameters provided'}), 400
    
    success = proxmox_service.update_vm_config(node, vmid, params)
    if not success:
        return jsonify({'error': 'Failed to update VM configuration'}), 500
    
    # Update VM in database if necessary
    vm = VM.query.filter_by(proxmox_id=vmid, proxmox_node=node).first()
    if vm:
        if 'cores' in params:
            vm.cpu_cores = params['cores']
        if 'memory' in params:
            vm.memory_mb = params['memory']
        db.session.commit()
    
    return jsonify({'success': True})

@api_bp.route('/software', methods=['GET'])
@login_required
def get_software_options():
    """Get available software options."""
    software_options = current_app.config['SOFTWARE_OPTIONS']
    return jsonify({'software_options': software_options})

@api_bp.route('/vms/<int:vmid>/scaling_events', methods=['GET'])
@login_required
def get_scaling_events(vmid):
    """Get scaling events for a VM."""
    vm = VM.query.filter_by(proxmox_id=vmid).first()
    if not vm:
        return jsonify({'error': 'VM not found'}), 404
    
    events = ScalingEvent.query.filter_by(vm_id=vm.id).order_by(ScalingEvent.timestamp.desc()).all()
    events_data = [{
        'id': event.id,
        'event_type': event.event_type,
        'cpu_usage': event.cpu_usage,
        'old_cpu_cores': event.old_cpu_cores,
        'new_cpu_cores': event.new_cpu_cores,
        'old_memory_mb': event.old_memory_mb,
        'new_memory_mb': event.new_memory_mb,
        'timestamp': event.timestamp.isoformat()
    } for event in events]
    
    return jsonify({'scaling_events': events_data})
