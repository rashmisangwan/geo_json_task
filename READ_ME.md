Step 1. 
===========
CREATE EXTENSION IF NOT EXISTS cube;
CREATE EXTENSION IF NOT EXISTS earthdistance;


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