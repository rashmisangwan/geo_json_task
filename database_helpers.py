import csv
import json
import psycopg2
import sys

conn = None


# database connection method
def getConnection():
    conn = psycopg2.connect("dbname=geo_database user=postgres password=1234")
    cur = conn.cursor()
    return cur, conn

def import_data():
    values = []
    sql = """INSERT INTO area_codes(pincode, place_name, state_name, lat, long, accuracy, g_point) VALUES \n\t"""
    pincode_file = 'pincode_data.csv'


    with open(pincode_file, 'r') as csvfile:
        pincode_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        headerSet = False
        for row in pincode_reader:
            if not headerSet:
                headerSet = True
                continue

            query = "("
            query += "'" + row[0] + "',"
            query += "'" + row[1] + "',"
            query += "'" + row[2] + "',"
            if row[3]:
                query += row[3] + ","
            else:
                query += "null,"
            if row[4]:
                query += row[4] + ","
            else:
                query += "null,"
            if row[5]:
                query += row[5] + ","
            else:
                query += "null,"
            if row[3] and row[4]:
                query += "cube({}, {})".format(row[3], row[4])
            else:
                query += "null"
            query += ")"

            values.append(query)

        sql += ",\n\t ".join(str(x) for x in values)

    try:
        cur, conn = getConnection()
        cur.execute( sql )
        conn.commit()
        cur.close()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

def import_geojson_data():
    values = []
    sql = """INSERT INTO area_geojson(place_name, parent_name, type, boundary_points) Values \n\t"""
    area_file = 'area_data.json'

    with open(area_file) as f:
        data = json.load(f)

    for feature in data['features']:
        polygon_geom = ','.join(list(map(lambda x: str(tuple(x)), feature['geometry']['coordinates'][0])))

        query = "("
        query += "'" + feature['properties']['name'] + "',"
        query += "'" + feature['properties']['parent'] + "',"
        query += "'" + feature['properties']['type'] + "',"
        query += "'" + polygon_geom + "'"
        query += ")"

        values.append(query)

    print(values[0])
    sql += ",\n\t ".join(str(x) for x in values)

    try:
        cur, conn = getConnection()
        cur.execute( sql )
        conn.commit()
        cur.close()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

def show_data():
    sql = """SELECT * FROM area_codes"""

    try:
        cur, conn = getConnection()

        cur.execute(sql)

        print(cur.fetchall())
        cur.close()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

def delete_data():
    sql = """DELETE FROM area_codes"""

    try:
        cur, conn = getConnection()

        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

def should_save_data(_pincode, _lat, _long, _offset_distance):
    sql = """SELECT * FROM area_codes WHERE pincode = 'IN/{0}' OR earth_distance( ll_to_earth(lat::numeric, long::numeric), ll_to_earth({1},{2}) ) / 1000 <= {3}""".format(_pincode, _lat, _long, _offset_distance)
    shouldSave = False
    response = None

    try:
        cur, conn = getConnection()
        cur.execute( sql )
        data = cur.fetchall()
        if not data:
            shouldSave = True
        else:
            response = []
            for row in data:
                response.append({
                    "pincode": row[0],
                    "place_name": row[1],
                    "state_name": row[2],
                    "lat": row[3],
                    "long": row[4],
                })

        cur.close()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

    return shouldSave, response

def save_data(_pincode, _place, _state, _lat, _long):
    sql = """INSERT INTO area_codes(pincode, place_name, state_name, lat, long, g_point) VALUES ('IN/{}', '{}', '{}', {}, {}, cube({}, {})) """.format(_pincode, _place, _state, _lat, _long, _lat, _long)
    status = ''
    try:
        cur, conn = getConnection()
        cur.execute( sql )
        conn.commit()
        cur.close()
        status = 'SUCCESS'
    except Exception as e:
        status = 'ERROR'
        print(e)
    finally:
        if conn is not None:
            conn.close()

    return status

def delete_record(_pincode):
    sql = """DELETE FROM area_codes WHERE pincode = 'IN/{}'""".format(_pincode)
    status = ''
    try:
        cur, conn = getConnection()
        cur.execute( sql )
        conn.commit()
        cur.close()
        status = 'SUCCESS'
        print(sql)
    except Exception as e:
        status = 'ERROR'
        print(e)
    finally:
        if conn is not None:
            conn.close()

    return status

def get_nearby_data_default(_lat, _long, _distance):
    sql = """SELECT *, earth_distance( ll_to_earth(lat::numeric, long::numeric), ll_to_earth({0},{1}) ) as distance 
            FROM area_codes 
            WHERE (lat::numeric <> {0} and long::numeric <> {1} ) and earth_distance( ll_to_earth(lat::numeric, long::numeric), ll_to_earth({0},{1}) ) <= {2}
            ORDER BY distance ASC
            """.format(_lat, _long, _distance)
    status = ''
    response = []

    try:
        cur, conn = getConnection()
        cur.execute( sql )
        data = cur.fetchall()
        # print(sql)
        for row in data:
            response.append({
                "pincode": row[0],
                "place_name": row[1],
                "state_name": row[2],
                "lat": row[3],
                "long": row[4],
                "distance": row[7]
            })

        cur.close()
        status = 'SUCCESS'
    except Exception as e:
        status = 'ERROR'
        print(e)
    finally:
        if conn is not None:
            conn.close()

    return status, response

def get_nearby_data_self(_lat, _long, _distance):
    sql = """SELECT *, ( 6371 * acos( cos( radians({0}) ) * cos( radians(lat::numeric) ) * cos( radians(long::numeric) - radians({1}) ) + sin( radians({0}) ) * sin( radians(lat::numeric) ) ) ) AS distance
            FROM area_codes 
            WHERE (lat::numeric <> {0} and long::numeric <> {1} ) and  ( 6371 * acos( cos( radians({0}) ) * cos( radians(lat::numeric) ) * cos( radians(long::numeric) - radians({1}) ) + sin( radians({0}) ) * sin( radians(lat::numeric) ) ) ) < {2} 
            ORDER BY distance ASC
            """.format(_lat, _long, _distance)
    status = ''
    response = []

    try:
        cur, conn = getConnection()
        cur.execute( sql )
        data = cur.fetchall()
        for row in data:
            response.append({
                "pincode": row[0],
                "place_name": row[1],
                "state_name": row[2],
                "lat": row[3],
                "long": row[4],
                "distance": row[7]
            })

        cur.close()
        status = 'SUCCESS'
    except Exception as e:
        status = 'ERROR'
        print(e)
    finally:
        if conn is not None:
            conn.close()

    return status, response

def get_containing_area(_lat, _long):
    sql = """select * from area_geojson where boundary_points  @> '({}, {})';""".format(_lat, _long)
    status = ''
    response = []

    try:
        cur, conn = getConnection()
        cur.execute( sql )
        data = cur.fetchall()
        for row in data:
            response.append({
                "id": row[0],
                "place_name": row[1],
                "state_name": row[2]
            })

        cur.close()
        status = 'SUCCESS'
    except Exception as e:
        status = 'ERROR'
        print(e)
    finally:
        if conn is not None:
            conn.close()

    return status, response

def main(*kargs):
    program_name = sys.argv[1]

    if program_name == 'import_data':
        import_data()
        import_geojson_data()
    elif program_name == 'delete_data':
        delete_data()
    elif program_name == 'show_data':
        show_data()


if __name__ == '__main__':
    main()