#This unit contains all necessary connections to openMeteo and Nominatim Openstreetmap to process data and chain it together.
#Nominatim only allows 1 API call per second, further calls will result in temporary blockage to the API.
#Nominatim does not allow multiple repeated calls to their server for the same payload, ensure that data is stored once it is extracted and then re-used.
#It would be preferable to cache this info in some type of DB table for later lookup first however due to time constraints and scope of this project it has not been included yet.
#Code is called in views.py

def getCityCoords(cityName, countryName):
    #function to obtain the coords of a city by the name of the city
    import requests
    import json
    import time
    #we make this function sleep to prevent timeouts
    time.sleep(2)
    url = "https://nominatim.openstreetmap.org/search?q=" + cityName + "+%" + countryName + "&format=jsonv2" 

    responses = requests.get(url)

    #request to retrieve the coords of the city/country works but I have been blocked from accessing this data, below is a placeholder for the API request data that was received and is then processed into relevant data if you need an example response or become blocked for some reason.
    #responses = json.dumps([{"place_id": 28830325, "licence": "Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright", "osm_type": "node", "osm_id": 261833893, "lat": "-26.205", "lon": "28.049722", "class": "place", "type": "city", "place_rank": 16, "importance": 0.6422106417680402, "addresstype": "city", "name": "Johannesburg", "display_name": "Johannesburg, City of Johannesburg Metropolitan Municipality, Gauteng, 2001, South Africa", "boundingbox": ["-26.3650000", "-26.0450000", "27.8897220", "28.2097220"]}])
 
    processResponse = json.loads(responses.text)

    return processResponse[0]['lat'], processResponse[0]['lon']

def openMeteoDaily(dataRequestType, latitude, longitude):

    #callable module for ease of access to weather information and re-usability

    import openmeteo_requests
    import requests_cache
    import pandas as pd
    from retry_requests import retry

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required input param variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    # Below request will run using daily and has a variable to allow re-usability of function and select different data return types, in daily timezone must be specified, GMT was used to give proper date notation.
    # Forecast limit  for Open Meteo is 16 days set below
    # Maximum requests per day = 10 000 on this non-commerical version
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": dataRequestType,
        "timezone": "GMT",
        "forecast_days": 16
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    weatherType = daily.Variables(0).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = False),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = False),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    daily_data[dataRequestType] = weatherType

    daily_dataframe = pd.DataFrame(data = daily_data)
    return daily_dataframe

def chainWeather(dataFrameSource, dataFrameCombine):
    import pandas as pd
    #Simple Function combine the results from the openmenteo data and remove duplicated column of date
    #concat data frames using the date from the openMeteo function
    combinedDataframe = pd.concat([dataFrameSource, dataFrameCombine], axis=1)
    #Remove duplicated column by ignoring duplicated column index and selecting other column ranges into copied version
    combinedDataframe = combinedDataframe.loc[:,~combinedDataframe.columns.duplicated()].copy() 
    return combinedDataframe

def insertIntoDb(payloadInfo):
    import psycopg2
    import configparser
    import os
    import json

    configPath = os.getcwd() + '\\tripWeather\\connection_params.ini'
    config = configparser.ConfigParser()
    config.read(configPath)
    db_host = config.get('Database','host')
    db_user = config.get('Database','user')
    db_pass = config.get('Database','password')
    db_port = config.get('Database','port')
    db_name = config.get('Database','dbname')

    conn = psycopg2.connect(
    database=db_name,
    user=db_user,
    password=db_pass,
    host=db_host,
    port=db_port
    )
    
    conn.autocommit = True
    
    # creating a cursor
    cursor = conn.cursor()

    LoadsInfo = json.loads(str(payloadInfo).replace('}{',','))
    
    print(LoadsInfo)

    # sql statement to be executed
    sql = '''--Test data for in case the API's post/get etc dont work for some reason
    INSERT INTO public."tripResultReturnApi_cityweatherinfo"(
        city,
        precipitation,
        country,
        "date",
        max_temperature,
        min_temperature,
        prec_hours,
        prec_prob_max,
        prec_prob_min,
        prec_prob_mean,
        rain, 
        showers,
        snow,
        trip,
        uv_index_max,
        wind_speed_max
    )
    VALUES ('%s',%s,'%s',to_timestamp(%s)::TIMESTAMPTZ, %s,%s,%s,%s,%s,%s,%s,%s,%s,'%s',%s,%s)'''%(str(LoadsInfo['city']),LoadsInfo['precipitation_sum'],str(LoadsInfo['country']),LoadsInfo['date'],LoadsInfo['temperature_2m_max'],LoadsInfo['temperature_2m_min'],LoadsInfo['precipitation_hours'],LoadsInfo['precipitation_probability_max'],LoadsInfo['precipitation_probability_min'],LoadsInfo['precipitation_probability_mean'],LoadsInfo['rain_sum'],LoadsInfo['showers_sum'],LoadsInfo['snowfall_sum'],str(LoadsInfo['trip']),LoadsInfo['uv_index_max'],LoadsInfo['wind_speed_10m_max'],)

    # executing the sql statement, commit then close
    cursor.execute(sql)
    conn.commit()
    conn.close()

