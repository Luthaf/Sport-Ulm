#!/usr/bin/env python
import os
from subprocess import Popen, PIPE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sport@ulm.settings")
from profilENS.models import User
import redis
    
def add_or_update(r, iterator):
    ''' Add to the database if non existent, else update if necessary.'''
    
    current = {}
    
    # TODO: export to redis
    message = "[ FETCHING FROM database ]"
    print(message)
    r.set("status", "db")
    
    for user in User.objects.all():
        current[user.username] = user

    r.set("status", "sync")
    message = "[ SYNCING ]"
    print(message)
    
    for line in iterator:
        r.incr("nUser")
        print(line)
        username = line[0]
        full_name = line[4].split(" ")
        first_name = full_name[0]
        last_name = " ".join([name for name in full_name[1:]])
        if username in current.keys():
            user = current[username]
            # Update first/last name if necessary
            if user.first_name != first_name:
                user.first_name = first_name
                user.save()
                print("Updated first name of", username)
            if user.last_name != last_name:
                user.last_name = last_name
                user.save()
                print("Updated last name of", username)
                
        else:
            user = User(username=username, first_name=first_name,
                        last_name=last_name, email=username+"@clipper.ens.fr")
            user.save()
            print("Inserted", username)
        r.lpush("update", username)

def import_from_clipper(r):
    '''Get the data from the server'''
    # SSH settings
    login = "ccadiou"
    serv = "sas.eleves.ens.fr"
    print("[ FETCHING FROM '"+serv+"' ]")
    
    r.set("status", "ssh")
    cmd = Popen(["ssh", login+"@"+serv, "ypcat", "passwd"], stdout=PIPE)
    data, err = cmd.communicate()

    if err is not None:
        raise Exception("Impossible to get passwd list")
    else:
        # generator that iterates over the lines of the passwd
        splitted = data.splitlines()
        r.set("totUser", len(splitted))
        return (line.decode().split(':') for line in splitted)


def sync_with_clipper():
    ''' Perform a synchronization with the server'''
    try:
        # Open the redis database
        r = redis.StrictRedis()

        # Try to open the connection, else fail
        if r.get("lock")==b'True':
            raise Exception("Oh ow, db lock!")
        else:
            r.set("lock", True)
            r.delete("status")
            
        # Import from clipper
        data = import_from_clipper(r)

        # Add or update in database
        add_or_update(r, data)

    finally:
        # Remove the lock and erase all status
        r.set("lock", False)
        r.delete("status")
        r.delete("update")
        r.delete("nUser")
        print("[DONE]")
    
if __name__ == "__main__":    
    sync_with_clipper()
