--Test data for in case the API's post/get etc dont work for some reason
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
VALUES ('Johannesburg','80.0','South Africa','2024-09-08'::TIMESTAMPTZ, 200.0,200.0,200,200,200,200,200,200,200,'ZA Flight',200, 100)