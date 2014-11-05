#!/bin/sh
USER='ccadiou'
SERV='sas.eleves.ens.fr'
ssh $USER@$SERV ypcat passwd | python3 sync.py
