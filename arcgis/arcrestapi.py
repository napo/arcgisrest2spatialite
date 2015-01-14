# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 15:11:49 2014

@author: Maurizio Napolitano <napo@fbk.eu>

The MIT License (MIT)

Copyright (c) 2015 Maurizio Napolitano <napo@fbk.eu>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from bs4 import BeautifulSoup
import requests
import sqlite3
from shapely.geometry import MultiLineString
from shapely.geometry import MultiPolygon
from shapely.geometry import Polygon
from shapely.geometry import Point


class ArcGIS:
    """
    A class to inspect a ArcGIS web service and convert a layer
    in a spatialite database
    
    Usage:

    >>> from arcrestapi import ArcGIS
    >>> source = "http://geo.umbriaterritorio.it/ArcGIS/rest/services"
    >>> arcgis = ArcGIS(source)
    >>> arcgis.discover() 
    >>> for layer in arcgis.layers:
    >>>    if layer['querable']:
    >>>         url=layer['url']
    >>>         name=layer['name']
    >>>         arcgis.download(url,"dati_umbria.sqlite",name) 
    
    this class inspired by 
    https://github.com/Schwanksta/python-arcgis-rest-query

    """
    def __init__(self, url=None):
        self.url=url    
        self.typefields = {
            'esriFieldTypeString': 'string',
            'esriFieldTypeInteger': 'integer',
            'esriFieldTypeSmallInteger': 'integer',
            'esriFieldTypeDouble': 'real',
            'esriFieldTypeSingle': 'real',
            'esriFieldTypeDate': 'timestamp',
            'esriFieldTypeOID': 'integer',
            'esriFieldTypeRaster': 'blob'
        }   
        self.layers = []
        self.discoverd = False

    def _addlayers(self,url,response):
        services=response.get('services')
        folders=response.get('folders')
        if services is not None:
            if len(services) > 0:
                self._discoverservices(url,services)
        if folders is not None:
            if len(folders) > 0:
                self._discoverfolders(url,folders)
    
    def _replaceduplicate(self,name): 
        """
        this method prevent the presence of duplicates name in the layers list's
        this isn't not smart for the humans, but for the machines
        """
            
        k = 1
        names = []
        name = self._cleanname(name)
        nwname = name
        for l in self.layers:
            names.append(l['name'])
        while (nwname in names):
            for n in names:
                if n==nwname:
                    nwname=name+str(k)			
                else:
                    k=k+1  
        name = nwname
        return name
        
    def _discoverservices(self,url,services,mainurl):
        
        for service in services:
            if service['type']=='MapServer':
                name = service['name'].split("/")
                urllayers = url + "/" +  name.pop() + "/MapServer/layers"
                layers = requests.get(urllayers,params={'f': 'pjson'}).json()
                if len(layers) > 0:
                    for layer in layers['layers']:                            
                        layerurl = urllayers.replace('layers','')+str(layer['id'])
                        datalayer = {}
                        datalayer['url']=layerurl
                        datalayer['name']=self._replaceduplicate(layer['name'])
                        datalayer['folder']=url.replace(self.url,"")
                        datalayer['properties']=layer
                        datalayer['querable']=self.querable(layerurl)
                        self.layers.append(datalayer)

    def _discoverfolders(self,url,folders):
        for folder in folders:
            furl = urljoin(url,folder)
            response = requests.get(furl,params={'f': 'pjson'}).json()
            self._addlayers(furl,response)
            
    def discover(self,url=None):
        """
        method to discover all the layers offered by the ArcGIS service
        all the information are stored in self.layers
        """
        if (url is None or self.url is None):
            if url is None:
                url = self.url
            if self.url is None:
                self.url = url
            self.discoverd = True
            response = requests.get(urljoin(url),params={'f': 'pjson'}).json()
            self.currentversion = response['currentVersion']
            self._addlayers(url,response)

    def querable(self,url):
        """
        method to discover if a source is querable
        """        
        q = False
        links = BeautifulSoup(requests.get(url).text).findAll("a")
        for l in links:
            if l.getText()=='Query':
                q = True
                break
        return q

    def countfeatures(self,url):
        """
        method to know how much features are in a source
        """
        url = url + "/query"
        params={}
        params['where']='1=1'
        params['f']='pjson'
        params['returnCountOnly']='true'
        return int(requests.get(url,params=params).json()['count'])

    def _cleanname(self,name):
        """
        "workd around" method to prevent errors for the sql commands (FIX)
        """
        name = name.strip()
        name = name.replace("-","_")
        name = name.replace("  "," ")
        name = name.replace(" ","_")
        name = name.replace("__","_")
        name = name.replace(")","")
        name = name.replace("(","")
        name = name.replace("__","_")
        name = name.replace(",","")
        name = name.replace(";","")
        name = name.replace(".","")
        name = name.replace(",","")
        name = name.replace(":","_")
        name = name.replace("'","")
        name = name.replace('"','')
        name = name.lower()
        return name
        
    def download(self,url,dbout,name=None,left=None,right=None):
        """
        this method download the data from an ArcGIS rest API 
        server and save it on a spatialite file
        url => a valid querable ArcGIS rest API source
        dbout => the name of the spatialite file
        name => the name of the new table. If you don't give, the function extract 
        the name from the rest api
        left and right => this define the range of data to download. 
        If you don't give, the function assume to download everything
        """
        if name is None:
            name = requests.get(url,params={'f':'pjson'}).json()['name']
            name = self._cleanname(name)
        url = url + "/query"
        alldata = []
        totalrecords = self.countfeatures(url)
        if totalrecords == 1:
            totalrecords = 2
        if (left is None and right is None):
            for obj in range (1,totalrecords,1000):
                left=obj
                right=obj+999
                where = "OBJECTID>=%s and OBJECTID<=%s" % (left,right)
                params={}
                params['where']=where
                params['f']='pjson'    
                params['returnGeometry']='true'
                data = requests.get(url,params=params).json()
                alldata.append(data)
        else:
            where = "OBJECTID>=%s and OBJECTID<=%s" % (left,right)
            params={}
            params['where']=where
            params['f']='pjson'    
            params['returnGeometry']='true'
            data = requests.get(url,params=params).json()
            alldata.append(data)           
        
        self._insertdata(name,alldata,dbout)    
    
    def _createtable(self,name,fields):
        name = self._cleanname(name)      
        create="CREATE TABLE IF NOT EXISTS "+ name +" ("
        for field in fields:
            fieldname = self._cleanname(field['name'])
            fieldname = fieldname.replace("'","")
            fieldname = fieldname.replace('"','')
            create += fieldname +' '+self.typefields[field['type']] + ','
        create=create.rstrip(",")
        create+=");"
        return create
        
    def _addgeometrycolumn(self,name,data):
        name = self._cleanname(name)
        srid = data[0]['spatialReference']['wkid']
        geometrytype = data[0]['geometryType'].replace('esriGeometry','')
 #note: here to improve the different kinds of geometries 
        if geometrytype.upper() == "POLYLINE":
            geometrytype = "MultiLineString"
        if geometrytype.upper() == "POLYGON":
            geometrytype = "MultiPolygon"
        sql = "SELECT AddGeometryColumn('%s','geometry', %s, '%s','XY');" % (name,srid,geometrytype)
        return sql
            
    def _insertdata(self,name,data,dbout):
#note: this method needs the use of spatialite >= 4.2 
        if (data[0].has_key("geometryType")):
            srid = str(data[0]["spatialReference"]["wkid"])
            geomtype = data[0]["geometryType"].replace("esriGeometry","")
            create = self._createtable(name,data[0]["fields"])
            add = self._addgeometrycolumn(name,data)
            con=sqlite3.connect(dbout)        
            con.enable_load_extension(True)
            cur = con.cursor()
            cur.execute('SELECT load_extension("mod_spatialite")');
            cur.execute('SELECT InitSpatialMetadata();')
            cur.execute(create)
            cur.execute(add)
            cur.execute('BEGIN;')
            for d in data:
                features=d["features"]
                for f in features:
                    name = self._cleanname(name)
                    sql = ""
                    sql1="INSERT INTO %s (" % name
                    sql2 = ""
                    sql3 = ""
 #note: here to improve the different kinds of geometries 
                    if (geomtype.upper() == 'POLYGON'): 
                        polygons = []
                        
                        rings = f["geometry"]["rings"]
                        for ring in rings:
                            polygon = Polygon(ring)
                            polygons.append(polygon)
                        mpoly = MultiPolygon(polygons)
                        geometry = 'GeometryFromText("%s",%s)' % (mpoly.wkt,srid)

                    if (geomtype.upper() == "POLYLINE"):
                        line = None
                        paths = f["geometry"]["paths"]
                        line = MultiLineString(paths)
                        geometry = 'Geom imagesetryFromText("%s",%s)' % (line.wkt,srid)
                        
                    if (geomtype.upper() == "POINT"):
                        point = Point(f['geometry']['x'],f['geometry']['y'])
                        geometry="GeometryFromText('%s',%s)" % (point.wkt,srid)
                        
                    for field in f["attributes"].items():
                        f = self._cleanname(field[0])
                        f = f.replace("'","")
                        f = f.replace('"','') 
                        sql2 +='"%s",' % f
                        v = field[1]
                        if isinstance(v, unicode):
                            v=v.replace('"','')
                        sql3+='"%s",' % v
                    sql2+='"geometry") VALUES ('
                    sql3+=geometry+');'
                    sql = sql1+sql2+sql3
                    cur.execute(sql)
            #cur.execute('COMMIT;')        
            con.commit()
        
        
    def isarcgisrest(self,url):
        """
        check if the source is a ArcGIS rest server
        """
        isrest=True
        if (url.find('ArcGIS/rest')==-1):
            isrest=False
        return isrest

def urljoin(*args):
    return "/".join(map(lambda x: str(x).rstrip('/'), args))
