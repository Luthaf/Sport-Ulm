#!/bin/sh
USER='login_clipper'
SERV='sas.eleves.ens.fr'
ssh $USER@$SERV ypcat passwd | python sync_clipper.py
