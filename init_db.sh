#!/bin/bash

# Initialize the database
echo "Initializing database..."
cd /home/ubuntu/devops_project
source venv/bin/activate
export FLASK_APP=app.app
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

echo "Database initialized successfully."
