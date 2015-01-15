# arcgisrest2spatialite
## description
python class and scripts to investigate an ArcGIS rest API server and store the data in spatialite

inspired by 
* https://github.com/Schwanksta/python-arcgis-rest-query
* http://blog.spaziogis.it/2014/12/29/take-the-best-use-the-rest/

## install 
### from source
```
virtualenv arcgis2sqlite
cd arcgis2sqlite/
. bin/activate
git clone https://github.com/napo/arcgisrest2spatialite repo
cd repo
pip install -r requirements.txt
python setup.py install
```
## some command interfaces created with the class
### arcgis-discover.py 
this script extract the information about all the layers present in a ArcGIS Rest API service and store it in a spatialite file

**NOTE:** this operation can use a lot of time to be completed

Example1 - create the catalog table
```
arcgis-discover.py http://www.cartografia.regione.lombardia.it/ArcGIS10P/rest/services geodata_lombardia.sqlite
```
The script create a table called *arcgiscatalog*
Example2 - investigate che "arcgiscatalog"
```
spatialite geodata_lombardia.sqlite "select * from arcgiscatalog"
```
... and you can extract the data how you want
Example3 - create a csv file from the table
```
spatialite -header -separator ";" geodata_lombardia.sqlite "select * from arcgiscatalog;" > geodatacatalog_lombardia.csv
```

### arcgis2splite.py
this script extract the information about all the data present in a ArcGIS Rest API service and store it in a spatialite file
**NOTE:** 
- this operation can use a lot of time to be completed
- the file created can be very very big
- if there are two or more layers with the same name, the script create a new name with the number (Eg. "roads" and "roads1"

Example4 - create the spatialite file
```
arcgis2splite.py http://geo.umbriaterritorio.it/ArcGIS/rest/services geodata_umbria.sqlite
```
note: in this example you obtain a file of 1.7Gb
The file is here

After you can 
- convert a table in a ESRI Shapefile by using ogr2ogr, or qgis or ...
Example5 - convert from spatialite to esri shapefile with ogr2ogr
```
ogr2ogr -f "ESRI Shapefile" address_numbers.shp geodata_umbria.sqlite numeri_civici
```
(this assume you have a table called *numeri_civici* with the address numbers stored in the file *geodata_umbria.sqlite*)

- show the content with a GIS software

### arcgis-inspect-layer.py

### arcgis-get-layer.py


 
