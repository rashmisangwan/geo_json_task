import csv
import psycopg2
import sys

conn = None

def import_data():
    values = []
    sql = """INSERT INTO area_codes(pincode, place_name, state_name, lat, long, accuracy, g_point) VALUES \n\t"""
    pincode_file = 'pincode_data.csv'


    with open(pincode_file, 'r') as csvfile:
        # pincode_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
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
        conn = psycopg2.connect("dbname=postgres user=postgres password=1234")
        cur = conn.cursor()
        print(sql)
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
        conn = psycopg2.connect("dbname=postgres user=postgres password=1234")
        cur = conn.cursor()

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
        conn = psycopg2.connect("dbname=postgres user=postgres password=1234")
        cur = conn.cursor()

        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

def main(*kargs):
    program_name = sys.argv[1]

    if program_name == 'import_data':
        import_data()
    elif program_name == 'delete_data':
        delete_data()
    elif program_name == 'show_data':
        show_data()


if __name__ == '__main__':
    main()