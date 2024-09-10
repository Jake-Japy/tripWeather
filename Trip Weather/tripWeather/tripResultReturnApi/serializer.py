from rest_framework import serializers
from tripResultReturnApi.models import cityWeatherInfo

#Serializer class to import the model serializer for use in views

class tripResultApiSerial(serializers.ModelSerializer):
    class Meta:
        model = cityWeatherInfo
        fields = ["city","country","trip","max_temperature","min_temperature","precipitation","rain","showers","snow","prec_prob_max","prec_prob_min","prec_prob_mean","wind_speed_max","uv_index_max"]


