#!/usr/bin/python3
"""
This script is used to compress the web static package
"""
from fabric.api import *
from datetime import datetime
from os import path

# Specify the hosts and user details for deployment
env.hosts = ['100.25.19.204', '54.157.159.85']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def do_deploy(archive_path):
    """
    This function deploys the web files to the server
    """
    try:
        # Check if the archive exists
        if not (path.exists(archive_path)):
            return False

        # Upload the archive to the server's /tmp directory
        put(archive_path, '/tmp/')

        # Extract timestamp from archive path and create target directory
        timestamp = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'.format(timestamp))

        # Uncompress the archive into the target directory and remove the .tgz file
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C /data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

        # Remove the archive from the server's /tmp directory
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # Move the web static files to the parent directory
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* /data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

        # Remove the now empty web_static directory
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'.format(timestamp))

        # Remove the existing symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Create a new symbolic link that points to the new deployment
        run('sudo ln -s /data/web_static/releases/web_static_{}/ /data/web_static/current'.format(timestamp))
    except:
        # If any error occurred during the above operations, return False
        return False

    # If all operations completed successfully, return True
    return True

