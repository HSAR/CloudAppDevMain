THESE ARE THE STEPS WE TOOK TO SET UP DJANGO


cloned testapp:  https://github.com/django-nonrel/django-testapp.git

downloaded django .zip file from http://djangoappengine.readthedocs.org/en/latest/installation.html

unzipped and copied python modules from each folder e.g. "django" from django-nonrel-django-1.5.5-121-gcf7d480

made a google account: jinglrsoton@gmail.com for hosting the app

toby has password

made a test google app called jinglr-test

changed application name in app.yaml to jinglr-test

changed template import in urls.py  https://github.com/django-nonrel/django-testapp/issues/11

added ALLOWEDHOSTS = ['jinglr-test.appspot.com'] in settings.py

./manage.py runserver to run locally on devserver (localhost:8000)

./manage.py deploy to deploy to app engine (needs jinglrsoton credentials)

next: try creating very simple app