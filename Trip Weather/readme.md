# Use below run script for the DB for ease of access to the DB for the purposes of this project connection parameters are configured to use the below params in the django container
docker run --rm -h 127.0.0.1 -e POSTGRES_PASSWORD=password -e POSTGRES_HOST_AUTH_METHOD=trust -it -p 5433:5432/tcp postgres:alpine3.20 

# Use the below script to start the django container all configs are already set and necessary packages have been built into the container:

# Nominatim only allows 1 API call per second, further calls will result in temporary blockage to the API.
# Nominatim does not allow multiple repeated calls to their server for the same payload, ensure that data is stored once it is extracted and then re-used.
# It would be preferable to cache this info in some type of DB table for later lookup first however due to time constraints and scope of this project it has not been included.


# Forecast limit  for Open Meteo is 16 days
# Maximum requests per day = 10 000 on this non-commerical version for Open Meteo

URL For retrieving city data and performing insert into the db:
http://127.0.0.1:8001/api-data/createnewtrip/Honolulu|United%20States|USA|2024-09-13

Format is http://hostip:port/api-data/createnewtrip/[cityname]|[country]|[name_of_trip]|[date]
This will look like it gives an error but in fact the data has been processed via the API's and pushed into the DB
Screenshots have been provided of the data processed
The data for 200 temperature is arbitrary data manually inserted for testing purposes
In future I need to configure this to return the get request of the data inserted into the database

Django rest_framework:
Use this generic model to get trip data from the DB if you know the trip name:
http://127.0.0.1:8001/api-data/get/United%20States
http://127.0.0.1:8001/api-data/get/[name_of_trip]

custom model to add a trip and get the info for the trip from the third party API's:
http://127.0.0.1:8001/api-data/createnewtrip/Honolulu|United%20States|USA|2024-09-13
Format is api-data/createnewtrip/[cityname]|[country]|[name_of_trip]|[date]

Docker Containers: (used standard Alpine container for PG and configuring the Python container is as simple as pip freeze and then building the docker container) + DB configs for exposed ports on PG etc. (Port issue bug on the internal docker side configured to 5433:5432 so that ports differ as I already had a running PG server on my device it conflicted on the exposed ports giving me issues in case you already have one on your local like I did)

Database Used: PostgreSQL - PostgreSQL was preferred for the additional features that I could use in my custom url request configurations

Future Features to Add:
Support for multiple trips through json payload on post request (not allowing post requests through Django custom workaround devised)
Testing unit tests need to be added
Front end work
Connection to PG DB needs to be converted to a function or class (used frequently)
Better get request support (not just generic view on trip name)
Improved data structures to handle data betterr in PG DB.

Bug List:
Fix up the custom post request to display a non-error message
Fix unit tests bugs so that they can run correctly
Known bug when select for database creation returns null
Docker image for postgres works fine but the docker image for Python has developed a bug that needs to be repaired, source seems to be related to directory useage of the db connection parameters, the server can still be run with python manage.py runserver:8001


