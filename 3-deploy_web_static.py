#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive
The contents the web_static will be moved to the servers
"""
from fabric.api import local, cd, sudo, put, env
from datetime import datetime
from os.path import exists

env.hosts = ["54.160.90.38", "100.25.36.19"]
env.user = "ubuntu"


def do_pack():
    """Compress the web_static folder"""

    try:
        local("mkdir -p versions")
        currentTime = datetime.now().strftime("%Y%m%d%H%M%S")
        path = "versions/web_static_{}.tgz".format(currentTime)
        local("tar -cvzf {} web_static".format(path))
        return path
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Function to deploy our static files

    Args:
        archive_path: path to the archive
    Returns:
        False:
            if file at the path doesn't exist
        True:
            if all operations were done correctly
    Raises:
        None
    """
    if not exists(archive_path):
        return False

    try:
        # filename with .tgz
        file_tgz = archive_path.split("/")[-1]

        # to get the filename without tgz
        file = file_tgz.split(".")[0]

        # download destination for my put command
        dest = "/tmp/"

        # set archive destination
        arch_dest = "/data/web_static/releases/{}".format(file)

        # sym link to my archive dest
        symbolic_link = "/data/web_static/current"

        # start message
        print("Deploying {} to our server".format(file))

        # upload the archive to the /tmp/ dir of the server
        put(archive_path, dest)

        with cd("/tmp/"):
            # uncompres the tgz to the given dest
            # first we create the destination as it doesn't
            # exist by default
            sudo("mkdir -p {}".format(arch_dest))

            # uncompress to the destnaion created
            sudo("tar -xzf {} -C {} --strip-components=1"
                 .format(file_tgz, arch_dest))

            # delete the tgz file
            sudo("rm -rf {}".format(file_tgz))

        # remove old link file
        sudo("rm -rf {}".format(symbolic_link))

        # ln -s link_source link_name
        sudo("ln -s {} {}".format(arch_dest, symbolic_link))
        print("All done")

    except Exception:
        print("Failed to deploy succesfully")
        return False


def deploy():
    """Fully deploys the staic web page"""
    archivePath = do_pack()
    if not archivePath:
        return False
    return do_deploy(archivePath)
