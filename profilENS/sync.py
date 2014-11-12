#!/usr/bin/env python
from django.conf import settings
from django.template.defaultfilters import slugify

from subprocess import Popen, PIPE
import os
import redis

from profilENS.models import User

def TODO_LOGGING(*args):
    pass

def add_or_update(redis_db, iterator):
    ''' Add to the database if non existent, else update if necessary.'''

    current = {}

    # TODO: export to redis_db
    message = "[ FETCHING FROM database ]"
    # Todo: use log
    TODO_LOGGING(message)
    redis_db.set("status", "db")

    for user in User.objects.all():
        current[user.username] = user

    redis_db.set("status", "sync")
    message = "[ SYNCING ]"

    TODO_LOGGING(message)

    for line in iterator:
        redis_db.incr("n_user")
        clipper_username = line[0]
        full_name = line[4].split(" ")
        first_name = full_name[0]
        last_name = " ".join([name for name in full_name[1:]])
        username = slugify(first_name + "-" + last_name)
        if username in current.keys():
            user = current[username]
            # Update first/last name if necessary
            if user.first_name != first_name:
                user.first_name = first_name
                user.save()
                TODO_LOGGING("Updated first name of", username)
            if user.last_name != last_name:
                user.last_name = last_name
                user.save()
                TODO_LOGGING("Updated last name of", username)
        else:
            user = User(username=username, first_name=first_name,
                        last_name=last_name, email=clipper_username+"@clipper.ens.fr")
            user.save()
            print("Inserted", username)
        redis_db.lpush("update", username)

def import_from_clipper(redis_db):
    '''Get the data from the server'''
    # SSH settings
    login = settings.SSH_SYNC_USER
    server = settings.SSH_SYNC_SERVER
    TODO_LOGGING("[ FETCHING FROM '" + server + "' ]")

    redis_db.set("status", "ssh")
    cmd = Popen(["ssh", login + "@" + server, "ypcat", "passwd"], stdout=PIPE)
    data, err = cmd.communicate()

    if err is not None:
        TODO_LOGGING("Impossible to get passwd list")
        raise Exception()
    else:
        # generator that iterates over the lines of the passwd
        splitted = data.splitlines()
        redis_db.set("n_total_user", len(splitted))
        return (line.decode().split(':') for line in splitted)


def sync_with_clipper():
    ''' Perform a synchronization with the server'''
    try:
        # Open the redis_db database
        redis_db = redis.StrictRedis()

        # Try to open the connection, else fail
        if redis_db.get("lock")==b'True':
            TODO_LOGGING("Database lock still in place")
            raise Exception()
        else:
            redis_db.set("lock", True)
            redis_db.delete("status")

        # Import from clipper
        data = import_from_clipper(redis_db)

        # Add or update in database
        add_or_update(redis_db, data)

    finally:
        # Remove the lock and erase all status
        redis_db.set("lock", False)
        redis_db.delete("status")
        redis_db.delete("update")
        redis_db.delete("n_user")
        redis_db.delete("n_total_user")
        TODO_LOGGING("[DONE]")
