rem sets the PGADMIN password
set PGPASSWORD=geografio

rem run psql
"C:\Program Files\PostgreSQL\9.6\bin\psql.exe" -U postgres -c "CREATE DATABASE %1;" 
"C:\Program Files\PostgreSQL\9.6\bin\psql.exe" -U postgres -f craters.sql -d %1  
"C:\Program Files\PostgreSQL\9.6\bin\psql.exe" -U postgres -f IAU2000.sql -d %1

rem ensure python27 has psycopg2
"C:\Python27\ArcGIS10.5\Scripts\pip.exe" install psycopg2
"C:\Python27\ArcGIS10.5\Scripts\pip.exe" install pyshp

rem load crater data
"C:\Python27\ArcGIS10.5\python.exe" cload.py %1