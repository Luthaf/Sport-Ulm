#!/usr/bin/env python
import os
import sys
print (os.getcwd())

if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sport@ulm.settings")
    from profilENS.models import User
    
    current = {}
    print ("[ FETCHING ]")
    for user in User.objects.all():
        current[user.username] = user
    print ("[ SYNCING ] (this might take a while)")
    for line in sys.stdin:
        bits = line.split(":")
        username = bits[0]
        full_name = bits[4].split(" ")
        first_name = full_name[0]
        last_name = " ".join(full_name[1:])
        if username in current.keys():
            user = current[username]
            # Update first/last name if necessary
            if user.first_name != first_name:
                user.first_name = first_name
                user.save()
                print ("Updated first name of ", username)
            if user.last_name != last_name:
                user.last_name = last_name
                user.save()
                print ("Updated last name of ", username)
        else:
            user = User(username = username, first_name = first_name,
                        last_name = last_name, email = username+"@clipper.ens.fr")
            user.save()
    print ("[ DONE ]")
