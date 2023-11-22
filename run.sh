#!/bin/bash

# Define the name of the virtual environment and the Python script
VENV_NAME="venv"
PYTHON_SCRIPT="main.py"

# Function to check if the requirements.txt file exists
requirements_file_exists() {
    if [ -f "requirements.txt" ]; then
        return 0  # File exists
    else
        return 1  # File does not exist
    fi
}

echo "Checking if the virtual environment exists..."

if [ -d "$VENV_NAME" ]; then
    echo "Virtual environment found. Activating..."
    source $VENV_NAME/bin/activate
else
    echo "Creating a virtual environment named $VENV_NAME..."
    python3 -m venv $VENV_NAME
    source $VENV_NAME/bin/activate
fi

# Check for requirements.txt and install packages
if requirements_file_exists; then
    echo "requirements.txt found. Installing dependencies..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Please ensure it exists in the current directory."
    # Optionally, you can exit the script if requirements.txt is not found
    # exit 1
fi

echo "---------------------------------"
echo ""
echo ""
echo ""
echo "Running the Python application..."
echo "... Check the applications dock as the application may be hidden behind other windows."
echo ""
echo ""
echo ""
echo "---------------------------------"
python $PYTHON_SCRIPT

# Deactivate the virtual environment after the script finishes
deactivate
echo "Script execution finished. Virtual environment deactivated."
