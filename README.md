
# SQLite APP
Language - Python 3.7

## Libraries

Flask - has a build werkzeug server for running web apps, very common to build web apps.
Flask-RESTful - for creating RESTAPI.
Flask-JWT - has authentication methods for secured get methods.
sqlite3 - useful database library for python, reminds of MySQL syntax. also considered a NoSQL database. 

## About the code 

The project presents CRUD methods for items, authentication and registration of new users. This is the most basic for beginners who would like to make a web application and need to maintain only simple database and API. My opinion for you is to start with this architecture.


## Instructions 

Make sure you have PyCharm and Postman installed. Download the folder "sqlite_app" and open it with PyCharm platform. then right click on 'src/app.py' and run. go to postman and make the following endpoints for testing: "http://localhost:5000/item/<string:name>", "http://localhost:5000/items", "http://localhost:5000/register", "http://localhost:5000/login".
