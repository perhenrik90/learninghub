Learning Hub
============

Simple tool for sharing e-learning resources and files. 
Still in early developmentstage.

Contributors
------------
Per-Henrik Kvalnes 

Functionalies (x implemented)
-----------------------------

[x] - creating a project
[x] - commenting on a project
[x] - upload a file to a project
[x] - download a file from a project
[x] - search within all projects (tags)
[ ] - search by title and project description
[ ] - search priorities (number of visits)
[x] - tag a project (# with a category)
[x] - self change password
[x] - user profile
[ ] - user profile image
[ ] - following other users
[ ] - wall / table of activities
[ ] - follow projects
[ ] - self registrating restricted to domains

Requirments
-------------------

- Python3 (runs on 2.7 ) 
- Python-django 
- Sqlite (for now) / mysql

Tested on Linux OpenSUSE, OpenSUSE on raspberry pi and Linux Mint. 




Setup
--------

sqlite3
1) change to sqlite in learninghub/learninghub/settings.py 
2) go to learninghub and run: python manage.py syncdb
3) python manage.py runserver

mysql
1) crate a mysql database with username and password
2) go to learningub/learninghub/settings.py and set db backend to mysql
3) add the database, user and password. 
4) go to learninghub and run: python manage.py syndb
5) python manage.py runserver

user administration is done by django default admin site. 
<your-size>/admin

