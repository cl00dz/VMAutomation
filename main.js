// Main JavaScript for Proxmox VM Automation

// Document ready function
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Software selection in VM creation form
    const softwareOptions = document.querySelectorAll('.software-option');
    if (softwareOptions.length > 0) {
        softwareOptions.forEach(option => {
            option.addEventListener('click', function() {
                const checkbox = this.querySelector('input[type="checkbox"]');
                checkbox.checked = !checkbox.checked;
                this.classList.toggle('selected', checkbox.checked);
            });
        });
    }

    // Auto-scaling toggle
    const autoScalingToggle = document.getElementById('auto-scaling-toggle');
    const autoScalingOptions = document.getElementById('auto-scaling-options');
    if (autoScalingToggle && autoScalingOptions) {
        autoScalingToggle.addEventListener('change', function() {
            autoScalingOptions.classList.toggle('d-none', !this.checked);
        });
    }

    // VM resource usage charts
    const cpuChartCanvas = document.getElementById('cpu-chart');
    const memoryChartCanvas = document.getElementById('memory-chart');
    
    if (cpuChartCanvas && typeof Chart !== 'undefined') {
        const cpuChart = new Chart(cpuChartCanvas, {
            type: 'doughnut',
            data: {
                labels: ['Used', 'Available'],
                datasets: [{
                    data: [cpuChartCanvas.dataset.usage || 0, 100 - (cpuChartCanvas.dataset.usage || 0)],
                    backgroundColor: ['#007bff', '#e9ecef']
                }]
            },
            options: {
                cutout: '70%',
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
    
    if (memoryChartCanvas && typeof Chart !== 'undefined') {
        const memoryChart = new Chart(memoryChartCanvas, {
            type: 'doughnut',
            data: {
                labels: ['Used', 'Available'],
                datasets: [{
                    data: [memoryChartCanvas.dataset.usage || 0, 100 - (memoryChartCanvas.dataset.usage || 0)],
                    backgroundColor: ['#28a745', '#e9ecef']
                }]
            },
            options: {
                cutout: '70%',
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    // API calls for VM management
    setupVmApiCalls();
});

// Setup API calls for VM management
function setupVmApiCalls() {
    // Start VM button
    const startVmButtons = document.querySelectorAll('.start-vm-btn');
    startVmButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const vmId = this.dataset.vmid;
            const node = this.dataset.node;
            if (vmId && node) {
                startVm(vmId, node, this);
            }
        });
    });

    // Stop VM button
    const stopVmButtons = document.querySelectorAll('.stop-vm-btn');
    stopVmButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const vmId = this.dataset.vmid;
            const node = this.dataset.node;
            if (vmId && node) {
                stopVm(vmId, node, this);
            }
        });
    });

    // Delete VM button
    const deleteVmButtons = document.querySelectorAll('.delete-vm-btn');
    deleteVmButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('Are you sure you want to delete this VM? This action cannot be undone.')) {
                const vmId = this.dataset.vmid;
                const node = this.dataset.node;
                if (vmId && node) {
                    deleteVm(vmId, node, this);
                }
            }
        });
    });
}

// API function to start a VM
function startVm(vmId, node, button) {
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Starting...';
    
    fetch(`/api/vms/${vmId}/start`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ node: node })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('VM started successfully', 'success');
            // Update UI to reflect running state
            updateVmStatus(vmId, 'running');
        } else {
            showAlert('Failed to start VM: ' + (data.error || 'Unknown error'), 'danger');
        }
    })
    .catch(error => {
        showAlert('Error: ' + error.message, 'danger');
    })
    .finally(() => {
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-play"></i> Start';
    });
}

// API function to stop a VM
function stopVm(vmId, node, button) {
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Stopping...';
    
    fetch(`/api/vms/${vmId}/stop`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ node: node })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('VM stopped successfully', 'success');
            // Update UI to reflect stopped state
            updateVmStatus(vmId, 'stopped');
        } else {
            showAlert('Failed to stop VM: ' + (data.error || 'Unknown error'), 'danger');
        }
    })
    .catch(error => {
        showAlert('Error: ' + error.message, 'danger');
    })
    .finally(() => {
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-stop"></i> Stop';
    });
}

// API function to delete a VM
function deleteVm(vmId, node, button) {
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Deleting...';
    
    fetch(`/api/vms/${vmId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ node: node })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('VM deleted successfully', 'success');
            // Remove VM from UI
            const vmCard = button.closest('.vm-card');
            if (vmCard) {
                vmCard.remove();
            }
        } else {
            showAlert('Failed to delete VM: ' + (data.error || 'Unknown error'), 'danger');
        }
    })
    .catch(error => {
        showAlert('Error: ' + error.message, 'danger');
    })
    .finally(() => {
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-trash"></i> Delete';
    });
}

// Update VM status in UI
function updateVmStatus(vmId, status) {
    const statusIndicator = document.querySelector(`.vm-status[data-vmid="${vmId}"]`);
    if (statusIndicator) {
        statusIndicator.innerHTML = status;
        statusIndicator.className = `vm-status badge ${status === 'running' ? 'bg-success' : 'bg-danger'}`;
    }
    
    // Update buttons visibility
    const vmCard = document.querySelector(`.vm-card[data-vmid="${vmId}"]`);
    if (vmCard) {
        const startBtn = vmCard.querySelector('.start-vm-btn');
        const stopBtn = vmCard.querySelector('.stop-vm-btn');
        
        if (startBtn && stopBtn) {
            startBtn.style.display = status === 'running' ? 'none' : 'inline-block';
            stopBtn.style.display = status === 'running' ? 'inline-block' : 'none';
        }
    }
}

// Show alert message
function showAlert(message, type) {
    const alertsContainer = document.getElementById('alerts-container');
    if (!alertsContainer) return;
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertsContainer.appendChild(alert);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alert.classList.remove('show');
        setTimeout(() => {
            alert.remove();
        }, 150);
    }, 5000);
}
