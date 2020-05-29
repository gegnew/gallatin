import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

ticks_table_drop = "DROP TABLE IF EXISTS ticks_table;"
weather_table_drop = "DROP TABLE IF EXISTS weather_table;"


# CREATE TABLES

locations_table_create = ("""
CREATE TABLE gallatin_db.locations ( 
	latitude             decimal(9,6)  NOT NULL ,
	longitude            decimal(9,6)  NOT NULL ,
	id                   integer  NOT NULL ,
	name                 varchar(50)   ,
	CONSTRAINT pk_locations_id PRIMARY KEY ( id )
 );
""")

routes_table_create = ("""
CREATE TABLE gallatin_db.routes ( 
	id                   integer   ,
	name                 varchar(100)   ,
	latitude             decimal(9,6)   ,
	longitude            decimal(9,6)   ,
	location_id          integer   ,
	CONSTRAINT unq_routes_id UNIQUE ( id ) 
 );
""")

ticks_table_create = ("""
CREATE TABLE gallatin_db.ticks ( 
	route_id             varchar(12)  NOT NULL ,
	route_name           varchar(50)   ,
	tick_date            date  NOT NULL ,
	user_name            varchar(50)   ,
	user_id              varchar(20)   
 );
""")

stations_table_create = ("""
CREATE TABLE gallatin_db.weather_stations ( 
	id                   integer  NOT NULL ,
	stid                 varchar(10)   ,
	elevation            integer   ,
	distance             decimal   ,
	longitude            decimal(9,6)   ,
	latitude             decimal(9,6)   ,
	"state"              varchar(2)   ,
	timezone             varchar(20)   ,
	location_id          integer   ,
	CONSTRAINT pk_weather_stations_id PRIMARY KEY ( id )
 );
""")

weather_table_create = ("""
CREATE TABLE gallatin_db.weather ( 
	date_time            timestamptz  NOT NULL ,
	solar_radiation_set_1 double precision   ,
	wind_cardinal_direction_set_1d varchar(5)   ,
	wind_gust_set_1      double precision   ,
	volt_set_1           double precision   ,
	snow_interval_set_1  double precision   ,
	dew_point_temperature_set_1d double precision   ,
	"peak_wind_direction_set_1 " double precision   ,
	wind_chill_set_1d    double precision   ,
	precip_accum_set_1   double precision   ,
	heat_index_set_1d    double precision   ,
	wind_direction_set_1 double precision   ,
	peak_wind_speed_set_1 double precision   ,
	wind_speed_set_1     double precision   ,
	relative_humidity_set_1 double precision   ,
	air_temp_set_1       double precision   ,
	station_id           varchar(10)   
 );
""")


# INSERT

locations_table_insert = ("""
INSERT INTO gallatin_db.locations
	( latitude, longitude, id, name) VALUES ( %s, %s, %s, %s );
""")

routes_table_insert = ("""
INSERT INTO gallatin_db.routes
	( id, name, latitude, longitude, location_id) VALUES ( %s, %s, %s, %s, %s );
""")

ticks_table_insert = ("""
INSERT INTO gallatin_db.ticks
	( route_id, route_name, tick_date, user_name, user_id) VALUES ( %s, %s, %s, %s, %s );
""")

stations_table_insert = ("""
INSERT INTO gallatin_db.weather_stations
	( id, stid, elevation, distance, longitude, latitude, "state", timezone, location_id) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s );
""")

weather_table_insert = ("""
INSERT INTO gallatin_db.weather
	( date_time, solar_radiation_set_1, wind_cardinal_direction_set_1d, wind_gust_set_1, volt_set_1, snow_interval_set_1, dew_point_temperature_set_1d, "peak_wind_direction_set_1 "
, wind_chill_set_1d, precip_accum_set_1, heat_index_set_1d, wind_direction_set_1, peak_wind_speed_set_1, wind_speed_set_1, relative_humidity_set_1, air_temp_set_1, station_id
) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );
""")

# QUERY LISTS

create_table_queries = [locations_table_create, routes_table_create, ticks_table_create, stations_table_create, weather_table_create]
insert_table_queries = [locations_table_insert, routes_table_insert, ticks_table_insert, stations_table_insert, weather_table_insert]