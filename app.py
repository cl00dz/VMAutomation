from app import create_app
from app.services.auto_scaling_service import AutoScalingService
import os

# Create the application instance
app = create_app(os.getenv('FLASK_CONFIG', 'default'))

# Initialize auto-scaling service
auto_scaling_service = AutoScalingService()

@app.before_first_request
def start_auto_scaling():
    """Start the auto-scaling service when the application starts."""
    auto_scaling_service.start()

@app.teardown_appcontext
def stop_auto_scaling(exception=None):
    """Stop the auto-scaling service when the application stops."""
    auto_scaling_service.stop()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
