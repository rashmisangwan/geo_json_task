# API for GeoJSON for pincodes and area shapes

### APIs

* post_location - to add a location to DB
* get_using_postgres - to get nearby pincodes for given lat, long and distance, using postgres extensions
* get_using_self - to get nearby pincodes for given lat, long and distance, using self calculations
* get_containing_area - to get area in which the given lat, long exists

### Pre-requisites

  * Flask
  * Postgresql


### Step 1. 

In postgresql shell write following commands to add extensions - 

```
CREATE EXTENSION IF NOT EXISTS cube;
CREATE EXTENSION IF NOT EXISTS earthdistance;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
```

### Step 2. 

In postgresql shell write following commands to add area_codes table - 

```
create table area_codes(
  pincode varchar(15) PRIMARY KEY NOT NULL, 
  place_name varchar(50), 
  state_name varchar(50), 
  lat float(5), 
  long float(5), 
  accuracy SMALLINT,
  g_point cube
);
```

### Step 3. 

In postgresql shell write following commands to add area_geojson table - 

```
create table area_geojson(
  id SERIAL PRIMARY KEY, 
  place_name varchar(50) NOT NULL,
  parent_name varchar(50),
  type varchar(50),
  boundary_points polygon NOT NULL
);
```

### Step 4. 

Import Data via pgAdmin or `python init.py import_data` when area_data.json and pincode_data.json are in your root directory for geojson and area pincodes respectively


### Step 5. 

run the flask app `python app.py`