
### **Quick start**

Install requirement package:

```sh
$ virtualenv -p python3 venv
$ . venv/bin/activate
(venv)$ pip install -U -r requirements.txt
```
If have an error when install package `mysqlclient`, the reason is the server miss `libmysqlclient-dev`, try with:

```sh
sudo apt-get install libmysqlclient-dev
```

Create PAS database: 
(MySQL version 5.5.57)

```sh
mysql> create database pas;
mysql> GRANT ALL PRIVILEGES ON pas.* to 'pas_admin'@'localhost' IDENTIFIED BY 'pas_admin';
mysql> GRANT ALL PRIVILEGES ON pas.* to 'pas_admin'@'%' IDENTIFIED BY 'pas_admin';
mysql> exit;
```

Create pas (Persons Authentication System) app:

```sh
$ python manage.py startapp pas
```

Add ***database models*** in file ***models.py***, and then make migration for pas app:

```sh
$ python manage.py makemigrations pas
```
To check SQL command to migrate file **initial.py**, run command:

```sh
python manage.py sqlmigrate pas initial.py
```

If you’re interested, you can also run [`python  manage.py  check`](https://docs.djangoproject.com/en/2.0/ref/django-admin/#django-admin-check) this checks for any problems in your project without making migrations or touching the database.

Now, run **migrate** again to create those model tables in your database:

```sh
$ python manage.py migrate
```
