#1 step

On root run to create and virtual enviroment
```
python -m venv venv
```
Then inside the virtual enviroment, 
```
pip install -r requirements.txt 
```
to download all libraries of the project.


#2 step
```
cd /creditcard
```
then run this command if you want to create your own superuser
```
python manage.py createsuperuser
```
or use my login to generate your access token.
username: augusto.carniel
password: 123456


#3 step
```
python manage.py runserver
```
Run this command to start your server and start to test the application

You can use postman to call the url's
