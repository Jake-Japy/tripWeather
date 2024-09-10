from django.db import models
import datetime
import configparser
import psycopg2
import os

# Create your models here.

# definitions for data models to reflect directly in database and allow usage by Django
class cityWeatherInfo(models.Model):  

    trip = models.CharField(max_length=128,default='Misc')
    city = models.CharField(max_length=128,default='New York')
    country = models.CharField(max_length=128,default='United State')
    date = models.DateTimeField(default=datetime.datetime.now())
    max_temperature = models.FloatField(default=200.0)
    min_temperature = models.FloatField(default=200.0)
    precipitation = models.FloatField(default=200.0)
    rain = models.FloatField(default=200.0)
    showers = models.FloatField(default=200.0)
    snow = models.FloatField(default=200.0)
    prec_hours = models.IntegerField(default=200)
    prec_prob_max = models.FloatField(default=200.0)
    prec_prob_min = models.FloatField(default=200.0)
    prec_prob_mean = models.FloatField(default=200.0)
    wind_speed_max = models.FloatField(default=200.0)
    uv_index_max = models.FloatField(default=200.0)

    def __str__(self):
        return self.city
    

#Definitions for testing models examples Basic tests included

#Test for database on postgres
#testing commented out, development of this is still in progress
'''
def tripweather_db_exists():

    configPath = os.getcwd() + '\\tripWeather\\connection_params.ini'
    config = configparser.ConfigParser()
    config.read(configPath)
    db_host = config.get('Database','host')
    db_user = config.get('Database','user')
    db_pass = config.get('Database','password')
    db_port = config.get('Database','port')
    db_name = config.get('Database','dbname')

    conn = psycopg2.connect(
    database="postgres",
    user=db_user,
    password=db_pass,
    host=db_host,
    port=db_port
    )

    conn.autocommit = True
    cursor = conn.cursor()
    #check for DB tripweather on postgres to make migrations
    sqlCheckExist = 
    SELECT datname FROM pg_database WHERE datname = 'tripweather' 
    cursor.execute(sqlCheckExist)
    info = cursor.fetchall()
    if info[0][0] == 'tripweather':
        result = True
    else:
        result = False
    return result

''' 