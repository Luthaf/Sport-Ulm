# Installation

```
git clone https://bitbucket.org/Luthaf/sport-ulm.git
cd sport-ulm
pip install -r Requirements.txt
cp sport@ulm/local_settings.sample.py sport@ulm/local_settings.py
```

Edit the local_settings.py file to fit your needs, and then : 

```
./manage.py migrate
./manage.py loaddata fixtures/*.json
```

# Run

```
./manage.py runserver
```