from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.proxmox_service import ProxmoxService
from app.models.models import VM
from app import db

vm_bp = Blueprint('vm', __name__)
proxmox_service = ProxmoxService()

@vm_bp.route('/')
@login_required
def index():
    """VM dashboard showing all VMs for the current user."""
    user_vms = VM.query.filter_by(user_id=current_user.id).all()
    return render_template('vm/index.html', vms=user_vms)

@vm_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new VM."""
    if request.method == 'GET':
        # Get nodes for dropdown
        nodes = proxmox_service.get_nodes()
        # Get software options from config
        from flask import current_app
        software_options = current_app.config['SOFTWARE_OPTIONS']
        return render_template('vm/create.html', nodes=nodes, software_options=software_options)
    
    # Handle POST request
    # This will be handled by the API endpoint, but we'll redirect to the dashboard
    return redirect(url_for('vm.index'))

@vm_bp.route('/<int:vm_id>')
@login_required
def detail(vm_id):
    """Show VM details."""
    vm = VM.query.get_or_404(vm_id)
    
    # Ensure user owns this VM
    if vm.user_id != current_user.id:
        flash('You do not have permission to view this VM.', 'danger')
        return redirect(url_for('vm.index'))
    
    # Get VM status and resources from Proxmox
    status = proxmox_service.get_vm_status(vm.proxmox_node, vm.proxmox_id)
    resources = proxmox_service.get_vm_resources(vm.proxmox_node, vm.proxmox_id)
    
    return render_template('vm/detail.html', vm=vm, status=status, resources=resources)

@vm_bp.route('/<int:vm_id>/start', methods=['POST'])
@login_required
def start(vm_id):
    """Start a VM."""
    vm = VM.query.get_or_404(vm_id)
    
    # Ensure user owns this VM
    if vm.user_id != current_user.id:
        flash('You do not have permission to start this VM.', 'danger')
        return redirect(url_for('vm.index'))
    
    success = proxmox_service.start_vm(vm.proxmox_node, vm.proxmox_id)
    if success:
        vm.status = 'running'
        db.session.commit()
        flash('VM started successfully.', 'success')
    else:
        flash('Failed to start VM.', 'danger')
    
    return redirect(url_for('vm.detail', vm_id=vm_id))

@vm_bp.route('/<int:vm_id>/stop', methods=['POST'])
@login_required
def stop(vm_id):
    """Stop a VM."""
    vm = VM.query.get_or_404(vm_id)
    
    # Ensure user owns this VM
    if vm.user_id != current_user.id:
        flash('You do not have permission to stop this VM.', 'danger')
        return redirect(url_for('vm.index'))
    
    success = proxmox_service.stop_vm(vm.proxmox_node, vm.proxmox_id)
    if success:
        vm.status = 'stopped'
        db.session.commit()
        flash('VM stopped successfully.', 'success')
    else:
        flash('Failed to stop VM.', 'danger')
    
    return redirect(url_for('vm.detail', vm_id=vm_id))

@vm_bp.route('/<int:vm_id>/delete', methods=['POST'])
@login_required
def delete(vm_id):
    """Delete a VM."""
    vm = VM.query.get_or_404(vm_id)
    
    # Ensure user owns this VM
    if vm.user_id != current_user.id:
        flash('You do not have permission to delete this VM.', 'danger')
        return redirect(url_for('vm.index'))
    
    success = proxmox_service.delete_vm(vm.proxmox_node, vm.proxmox_id)
    if success:
        db.session.delete(vm)
        db.session.commit()
        flash('VM deleted successfully.', 'success')
    else:
        flash('Failed to delete VM.', 'danger')
    
    return redirect(url_for('vm.index'))

@vm_bp.route('/<int:vm_id>/scaling', methods=['GET', 'POST'])
@login_required
def scaling(vm_id):
    """Configure auto-scaling for a VM."""
    vm = VM.query.get_or_404(vm_id)
    
    # Ensure user owns this VM
    if vm.user_id != current_user.id:
        flash('You do not have permission to configure this VM.', 'danger')
        return redirect(url_for('vm.index'))
    
    if request.method == 'POST':
        # Update auto-scaling settings
        vm.auto_scaling_enabled = request.form.get('auto_scaling_enabled') == 'on'
        db.session.commit()
        flash('Auto-scaling settings updated.', 'success')
        return redirect(url_for('vm.detail', vm_id=vm_id))
    
    # Get scaling events for this VM
    from app.models.models import ScalingEvent
    events = ScalingEvent.query.filter_by(vm_id=vm.id).order_by(ScalingEvent.timestamp.desc()).all()
    
    return render_template('vm/scaling.html', vm=vm, events=events)
