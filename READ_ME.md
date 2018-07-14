Step 1. 
===========
CREATE EXTENSION IF NOT EXISTS cube;
CREATE EXTENSION IF NOT EXISTS earthdistance;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;


Step 2. 
===========
create table area_codes(
  pincode varchar(15) PRIMARY KEY NOT NULL, 
  place_name varchar(50), 
  state_name varchar(50), 
  lat float(5), 
  long float(5), 
  accuracy SMALLINT,
  g_point cube
);


Step 3. 
===========
Import Data via pgAdmin or `python init.py import_data`


Step 4. 
===========
create table area_geojson(
  id SERIAL PRIMARY KEY, 
  place_name varchar(50) NOT NULL,
  parent_name varchar(50),
  type varchar(50),
  boundary_points polygon NOT NULL
);