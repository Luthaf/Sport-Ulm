# Installation

This application needs Python 3 and Django 1.7.

```
git clone https://bitbucket.org/Luthaf/sport-ulm.git
cd sport-ulm
pip install -r Requirements.txt
cp sport@ulm/local_settings.sample.py sport@ulm/local_settings.py
```

Edit the local_settings.py file to fit your needs, and then :

```
./manage.py migrate
./manage.py loaddata fixtures/*
```

# Run

```
./manage.py runserver
```
