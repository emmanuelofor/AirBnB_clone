#!/usr/bin/python3
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

# Setting the servers where the code will be deployed
env.hosts = ['100.25.19.204', '54.157.159.85']


def do_pack():
    """
    Generates a .tgz archive from the contents of the 'web_static' folder.
    The function do_pack must return the archive path if the archive has been correctly generated.
    Otherwise, it should return None.
    """
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)
    # Check if versions directory exists, and create it if not.
    if not os.path.isdir("versions"):
        if local("mkdir -p versions").failed:
            return None
    # Create a .tgz archive using the tar command.
    if local("tar -cvzf {} web_static".format(file)).failed:
        return None
    return file


def do_deploy(archive_path):
    """
    Distributes an archive to the configured web servers.
    Args:
        archive_path (str): The path to the archive file to be deployed on the server.
    Returns:
        If an error occurred during the operation, the function returns False.
        If everything executed properly, the function returns True.
    """
    if not os.path.isfile(archive_path):
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    # Transfer the archive_path to the /tmp/ directory of the web server
    if put(archive_path, "/tmp/{}".format(file)).failed:
        return False
    # Create a new directory for the archive on the web server
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        return False
    # Uncompress the archive to the folder on the web server
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)).failed:
        return False
    # Remove the archive from the web server
    if run("rm /tmp/{}".format(file)).failed:
        return False
    # Move files from the web_static folder to the parent folder
    if run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name)).failed:
        return False
    # Remove the now empty web_static directory
    if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed:
        return False
    # Delete the symbolic link current from the web server
    if run("rm -rf /data/web_static/current").failed:
        return False
    # Create a new the symbolic link current on the web server, linked to the new version of your code
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed:
        return False
    return True


def deploy():
    """
    Creates and distributes an archive to the web servers.
    It creates an archive using do_pack(), and then deploys it to the web servers using do_deploy().
    Returns:
        False if either do_pack() or do_deploy() fail, otherwise returns True.
    """
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)

