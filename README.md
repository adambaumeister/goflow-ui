# GOFLOW-UI
## Description
A simple, example frontend for Goflow (https://github.com/adambaumeister/goflow/releases)

This utility is meant to provide an example web frontend on top of the backend provided by Goflow. 

Running this UI requires a working backend. Currently the following backends/fields are supported:

Backend Type | ip source | ip dst | src port | dst port | last_switched
----------- | ----------- | ----------- | ----------- | ----------- | -----------
MySQL | X | X | X |X | X
Timescaledb | X | X | X |X | X

This software is pre-release.

## Installation
This software can be installed via Pip, and runs using the Gunicorn WSGI server (by default, but you can use any WSGI server.)

As always, it's strongly recommended to use a virtual environment, as below.
```bash
# setup and install
python3 -m venv goflow-ui 
cd goflow-ui
bin/pip3 install git+https://github.com/adambaumeister/goflow-ui.git

# Configure, the config file ships with the package
# You may wish to copy this somewhere else, like /etc/goflow-ui so it isn't overwritten by package updates!
vi lib/python3.5/site-packages/gfui/config.yml
# Export the required environment variables
export CONFIG_FILE=lib/python3.5/site-packages/gfui/config.yml
export SQL_PASSWORD=your_sql_password

# Start the server
cd bin
gunicorn start:app -b :8080
```

The server will be available at http://your-server:8080. 


