from django.shortcuts import render
from rest_framework import generics
from tripResultReturnApi.models import cityWeatherInfo
from .serializer import tripResultApiSerial
from tripResultReturnApi.apiDataProcessing import getCityCoords,openMeteoDaily,chainWeather,insertIntoDb
from django.views.generic.edit import UpdateView 
import pandas as pd
import json


#apiDataProcessing custom code to retrieve city coords, weather data and to combine datasets together based on date for easier data handling via Pandas dataframes

weatherParamsList = ["temperature_2m_max","temperature_2m_min","precipitation_sum" ,"rain_sum","showers_sum","snowfall_sum","precipitation_hours","precipitation_probability_max","precipitation_probability_min","precipitation_probability_mean","wind_speed_10m_max","uv_index_max"]

# Create your views here.

class readTripWeather(generics.ListAPIView):
    queryset = cityWeatherInfo.objects.all()
    serializer_class = tripResultApiSerial
    lookup_field = 'trip'

#Below class is to be used for the insertion of the data.
class tripWeatherRetrieveUpdateDestroy(generics.ListCreateAPIView):
    queryset = cityWeatherInfo.objects.all()
    serializer_class = tripResultApiSerial

class tripWeatherPostTrip(UpdateView):
    model = cityWeatherInfo
    fields = ['city','country','trip','date','max_temperature','min_temperature','precipitation','rain','showers','snow','prec_hours','prec_prob_max','prec_prob_min','prec_prob_mean','wind_speed_max','uv_index_max']
    
    #Commented sections below were for testing purposes to provide a data set if the open maps url became accidentally blocked through overuse or by using the same city repeatedly.

    def postTripInfo(self, city, country, trip, date):  
        #below is to simulate the post of data/insertion request for the data into the database
        #json_example = '[{"trip":"US Trip","city":"Austin","country":"America","date":"2024-09-14"}]'
        #input will return all the data for the cities, date and country

        #journey = json.loads(json_example)
        #for journey_leg in journey:
            #trip = journey_leg["trip"]
            #city = journey_leg["city"]
            #country = journey_leg["country"]
            #date = journey_leg["date"]

        lat, long = getCityCoords(city,country)
        #lat = 37.55376052856445
        #long = -77.44317626953125
        
        #below is for combining multiple datasets in the software and returning them as a singular dataframe to be consumed in with the DB insert.
        flagCombine = False
        for openMeteoParam in weatherParamsList:
            frame_return = openMeteoDaily(openMeteoParam,lat,long)

            if flagCombine == True:
                combinedFrame = chainWeather(combinedFrame, frame_return)
            else: 
                combinedFrame = frame_return
                flagCombine = True

        df = combinedFrame

        dayDat = df.loc[df["date"] == date]
        singleDay = dayDat.to_json(orient='records', lines=True).splitlines()
        paramsStage = json.dumps({"trip":trip,"city":city,"country":country,"date":date})  

        for singleDayStage in singleDay:
            data = paramsStage + singleDayStage
            insertIntoDb(data)               

    def get_object(self, queryset=None):       
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get(pk=self.request.user.pk)

    def get(self, request, *args, **kwargs):
        dataManipulation = self.kwargs['tripinfo']
        dataList = str(dataManipulation).split('|')
        self.postTripInfo(dataList[0], dataList[1], dataList[2], dataList[3])
        self.object = self.get_object()  
        return super().get(request, *args, **kwargs)


#List of available input parameters for OpenMeteo API Calls Below is not an extensive list, there are additional data types but these are the most relevant to this project

'''
temperature_2m_max
temperature_2m_min 	
precipitation_sum 
rain_sum
showers_sum
snowfall_sum
precipitation_hours
precipitation_probability_max
precipitation_probability_min
precipitation_probability_mean 
wind_speed_10m_max
uv_index_max
'''