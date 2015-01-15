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
**NOTE**: you need an installation of spatialite 3.8+

## some command interfaces created with the class
### arcgis-inspect-layer.py
this script show a json with the information of a layer present in a ArcGIS Rest API source

Example1 - show the information of *numeri civici*
```
arcgis-inspect-layer.py http://geo.umbriaterritorio.it/ArcGIS/rest/services/Public/ECOGRAFICO_CATASTALE1_WGS84/MapServer/0
```

### arcgis-get-layer.py
this script dump the data in a spatialite file of a layer present in a ArcGIS Rest API source
**NOTE:** this operation can use a lot of time to be completed (it depends from the number of features in the layer)

Example2 - create the spatialite file *address_number.sqlite* from the source *numeri civici*
```
arcgis-get-layer.py http://geo.umbriaterritorio.it/ArcGIS/rest/services/Public/ECOGRAFICO_CATASTALE1_WGS84/MapServer/0 address_number.sqlite
```

### arcgis-discover.py 
this script extract the information about all the layers present in a ArcGIS Rest API service and store it in a spatialite file
The script create a table called *arcgiscatalog*

**NOTE:** this operation can use a lot of time to be completed

Example3 - create the catalog table of the geodata provided by the italian region Lombardia
```
arcgis-discover.py http://www.cartografia.regione.lombardia.it/ArcGIS10P/rest/services geodata_lombardia.sqlite
```

### arcgis2splite.py
this script extract the information about all the data present in a ArcGIS Rest API service and store it in a spatialite file
**NOTE:** 
- this operation can use a lot of time to be completed
- the file created can be very very big
- if there are two or more layers with the same name, the script create a new name with the number (Eg. "roads" and "roads1"

Example4 - dump all the geodata provided by the italian region Umbria
```
arcgis2splite.py http://geo.umbriaterritorio.it/ArcGIS/rest/services geodata_umbria.sqlite
```
note: in this example you obtain a file of 1.7Gb
The file is here http://bit.ly/1ATIyPC [last update 2015/13/01]

## some tips from the spatialite files created

- investigate a table of a spatialite file
Example5
```
spatialite geodata_lombardia.sqlite "select * from arcgiscatalog"
```
(this is the case of the table *arcgiscatalog* created from the command *arcgis-discover.py*)

- dump the data in a csv file
Example6 
```
spatialite -header -separator ";" geodata_lombardia.sqlite "select * from arcgiscatalog;" > geodatacatalog_lombardia.csv
```
- convert a table in a ESRI Shapefile by using ogr2ogr

Example5
```
ogr2ogr -f "ESRI Shapefile" address_numbers.shp geodata_umbria.sqlite numeri_civici
```
(this assume you have a table called *numeri_civici* with the address numbers stored in the file *geodata_umbria.sqlite*)

- show the content with a GIS software

![qgis] (https://raw.githubusercontent.com/napo/arcgisrest2spatialite/master/img/qgis_spatialite.png)
the qgis gui


![output] (https://raw.githubusercontent.com/napo/arcgisrest2spatialite/master/img/civici_umbria.png)
the output



 
