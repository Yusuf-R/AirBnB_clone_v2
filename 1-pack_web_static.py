#!/usr/bin/python3
"""
This a Fabric script to generate a .tgz
archive from the contents of the web_static
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """This method will compress web_static folder"""

    local("mkdir -p versions")
    currentTime = datetime.now().strftime("%Y%m%d%H%M%S")
    path = "versions/web_static_{}.tgz".format(currentTime)
    local("tar -cvzf {} web_static".format(path))
    if local("[ -f versions/web_static_{}.tgz ]".format(currentTime)).strip():
        return path
