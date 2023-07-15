#!/usr/bin/python3
"""
creates and distributes an archive to your web servers,
using the function deploy
"""
from fabric.api import env, sudo, local
from fabric.context_managers import lcd

# IP address for our web servers defined as host
env.hosts = ["54.160.90.38", "100.25.36.19"]

# username
env.user = "ubuntu"


def do_clean(number=0):
    """
    A function to delets out oldder archive in the folder

    if num = 0 or 1:
        keep only most recent
        thus we will have only 1 file

    else if num = 2:
        keep one most recent and second most recent
    """

    path = "/data/web_static/releases/"

    # ensure arg value passed is an int
    try:
        number = int(number)
    except ValueError:
        print("{} is not a valid integer".format(number))
        return

    # check if number is negarive
    if number < 0:
        print("Number can not be a negative value")
        return

    # if num 0 or 1 num should be 1
    if number == 0 or number == 1:
        number = 1

    number += 1

    # delete all archives in the versons folder
    with lcd("versions"):
        print("Deleting old arvhives in the versions folder")
        local("ls | grep 'web_static_*' | sort -nr | "
              "tail -n +{} | xargs rm -rf".format(number))

    # deleting all archives in the releases folder
    with lcd(path):
        print("Deleting old archivers in our web servers")
        sudo("ls | grep 'web_static_*' | sort -nr | "
             "tail -n +{} | xargs rm -rf".
             format(number))

    print("\nClean-up Operation Sucessful!")
