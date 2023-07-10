#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive
The contents the web_static will be moved to the servers
"""

from fabric.api import local, put, env, run
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
    """Deploys the web static to the server"""
    if not exists(archive_path):
        return False

    try:
        archiveWithExt = archive_path.split("/")[-1]
        archiveNoExt = archiveWithExt.split(".")[0]
        releaseVersion = "/data/web_static/releases/{}/".format(archiveNoExt)
        symLink = "/data/web_static/current"

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(releaseVersion))
        run("tar -xzf /tmp/{} -C {}".format(archiveWithExt, releaseVersion))
        run("rm -rf /tmp/{}".format(archiveWithExt))
        run("mv {0}web_static/* {0}".format(releaseVersion))
        run("rm -rf {}web_static".format(releaseVersion))
        run("rm -rf {}".format(symLink))
        run("ln -s {} {}".format(releaseVersion, symLink))
        return True
    except Exception:
        return False


def deploy():
    """Fully deploys the staic web page"""
    archivePath = do_pack()
    if not archivePath:
        return False

    return do_deploy(archivePath)
