#!/usr/bin/python3
"""
Fabric script template to generate a .tgz archive
"""

from fabric.api import put, env, run
from os.path import exists

env.hosts = ["54.237.18.123", "100.26.239.31"]
env.user = "ubuntu"


def do_deploy(archive_path):
    """Deploys the web static to the server"""
    if not exists(archive_path):
        return False
    results = []
    res = put(archive_path, "/tmp")
    results.append(res.succeeded)

    basename = os.path.basename(archive_path)
    if basename[-4:] == ".tgz":
        name = basename[:-4]
    newdir = "/data/web_static/releases/" + name
    run("mkdir -p " + newdir)
    run("tar -xzf /tmp/" + basename + " -C " + newdir)

    run("rm /tmp/" + basename)
    run("mv " + newdir + "/web_static/* " + newdir)
    run("rm -rf " + newdir + "/web_static")
    run("rm -rf /data/web_static/current")
    run("ln -s " + newdir + " /data/web_static/current")

    return True
