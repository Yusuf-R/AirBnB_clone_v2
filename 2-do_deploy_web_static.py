#!/usr/bin/python3
"""
Script will deploy our static files to our webservers
"""
from fabric.api import cd, env, sudo, run, task, put
# from fabric.context_managers import cd
from os.path import exists


# IP address for our web servers defined as host
env.hosts = ["54.160.90.38", "100.25.36.19"]
# env.hosts = ["100.26.233.228", "34.229.67.124"]


# load balancer
# env.hosts = ["34.229.70.109"]

# username
env.user = "ubuntu"


@task
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
            sudo("tar -xzf {} -C {} --strip-components=1".format(file_tgz, arch_dest))

            # delete the tgz file
            sudo("rm -rf {}".format(file_tgz))

        # remove old link file
        sudo("rm -rf {}".format(symbolic_link))

        # ln -s link_source link_name
        sudo("ln -s {} {}".format(arch_dest))
    
        print("All done")

    except Exception:
              print("Failed to deploy succesfully")
              return False
