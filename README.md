# Olympics dashboard

![](https://1000logos.net/wp-content/uploads/2021/03/Olympics-logo.png)
Olympics Dashboard is a database management project which aims at providing a platform about how the Olympics has evolved over time, participation, and performance rate based on gender, different countries, different sport and sports events. A lot of data is generated and collected each year at the Olympics which calls for a method to bring out more meaning from the data. A visualization-based approach has been taken in this project in that direction. A dashboard is proposed based on a historical dataset on the modern Olympic Games, including all the Games from Athens 1896 to Rio 2016. 

# MySQL workbench

Install MySQL workbench and then import all the data from [Olympics dataset](https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results)

To import the data fasters use the following command

```bash
LOAD DATA INFILE 'abc.csv' INTO TABLE abc
```

After this setup the SQL connection with the Django project using this tutorial as reference [Connect Django Project to Already Existing Database](https://www.youtube.com/watch?v=CkYvpKZyEqI&t=668s)
# Django Project Template
The dashboard is built on top of the Django framework.
###### Django is a high-level Python web framework that enables rapid development of secure and maintainable websites.

## Getting Started
Setup project environment with [virtualenv](https://virtualenv.pypa.io) and [pip](https://pip.pypa.io).

```bash
$ virtualenv project-env
$ source project-env/bin/activate

$ django-admin startproject --template https://github.com/jaregauri/olympics_dashboard.git projectname
$ cd projectname/
$ cp settings_custom.py.edit settings_custom.py
$ python manage.py migrate
$ pip3 install Django
$ pip3 install pymysql
$ python manage.py runserver
```

# Few data visuals fom the dashboard 


## Male and Female participants by a country over years from all sports
![](https://drive.google.com/uc?export=view&id=1PDjFp4AJxqbAyHXtC9AjmSsNHgwniV_5)


## Medals won for a specific year by a country and in a particular sport
![](https://drive.google.com/uc?export=view&id=14uBIhxEOI-hzYHhdjgzJFldJJq9LBM-X)


## Trends in male and female participation over the years for a sport
![](https://drive.google.com/uc?export=view&id=1wa2q14qaFy-g31HKZaD6ybSol-RqTcq1)


## Contributing

I love contributions, so please feel free to fix bugs, improve things, provide documentation. Just send a pull request.
