import sys
import psycopg2
from psycopg2 import extras
import shapefile

# connect to the DB
try:
    db = sys.argv[1]
except IndexError:
    db = 'load'
psycopg2.extensions.register_adapter(dict, extras.Json)
connection = psycopg2.connect("dbname={} user=postgres password=geografio".format(db))
cursor = connection.cursor()

# load the data
srid = 930100
data = shapefile.Reader('data/LU78287GT_Moon2000.shp')
field_names = [field[0] for field in data.fields[1:]]

for row in data.shapeRecords():
    try:
        # create an object
        cursor.execute("INSERT INTO obj DEFAULT VALUES RETURNING id;")
        obj_id = cursor.fetchone()[0]

        # create an observation
        payload = dict(zip(field_names, row.record))
        cursor.execute("INSERT INTO observation (obj_id, data) VALUES (%(obj_id)s, %(data)s) RETURNING id;",
                       {'obj_id': obj_id, 'data': payload})
        obs_id = cursor.fetchone()[0]

        # create a geometry
        cursor.execute("INSERT INTO spatial_data (obs_id, geom, srid) VALUES (%(obs_id)s, ST_GeomFromGeoJson(%(geom)s), %(srid)s) RETURNING id;",
                       {'obs_id': obs_id, 'geom': row.shape.__geo_interface__, 'srid': srid})
        connection.commit()
    except UnicodeDecodeError:
        pass

