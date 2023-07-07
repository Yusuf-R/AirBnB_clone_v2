#!/usr/bin/python3
"""
This module generate a .tgz archive for all the content of our
webstatic files
"""

from datetime import datetime
from fabric.api import local


def do_pack():
    """
    function defination for the archive process

    Retunrs:
        the path of the archive process
    else:
        returns None
    """
    # set our current time for the proceess
    ct_time = datetime.now().strftime("%Y%m%d%H%M%S")

    # set our archive name
    archive_name = "web_static_" + ct_time + ".tgz"

    # set path
    path = "versions/{}".format(archive_name)

    try:
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(path))
        return path
    except Error:
        return None
