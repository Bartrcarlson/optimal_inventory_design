#!/bin/bash

# Name of the virtual environment
ENV_NAME="opt_plot_alloc"

# Check if virtual environment already exists
if [ -d "$ENV_NAME" ]; then
    echo "Virtual environment $ENV_NAME already exists."
else
    # Create virtual environment
    python3 -m venv $ENV_NAME
    echo "Virtual environment $ENV_NAME created."
fi

# Activate the virtual environment
source $ENV_NAME/bin/activate

# Install dependencies
pip install pandas geopandas pyyaml gdal numpy

echo "Dependencies installed. Virtual environment setup is complete."

# To make sure other scripts run from this terminal use this environment, keep it activated.
echo "The virtual environment is now activated. Run your Python scripts in this terminal to use this environment."
