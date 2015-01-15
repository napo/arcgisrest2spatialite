#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from builtins import str as futureenc
from optparse import OptionParser
from arcrestsplite import ArcGIS

def do(url,dbname,verbose):
    arcgis = ArcGIS(url)
    if arcgis.isarcgisrest:
        arcgis.discover() 
        arcgis.createdbcatalog(dbname)
        if verbose:
            print "url\tname\tquerable\txmin\tymin\txman\tyman\tsrd\tdescription\ttypel\tgeometrytype"
        if verbose:
            for layer in arcgis.layers:
                url = layer['url']
                name =  futureenc(layer['name'])
                querable = layer['querable']
                xmin = layer['properties']['extent']['xmin']
                ymin = layer['properties']['extent']['ymin']
                xmax = layer['properties']['extent']['xmax']
                ymax = layer['properties']['extent']['ymax']
                srid = layer['properties']['extent']['spatialReference']['wkid']
                description =  futureenc(layer['properties']['description'])
                typel = layer['properties']['type']
                geometrytype = layer['properties']['geometryType'].replace('esriGeometry','')
                print "%s\t%s\t%\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (url,name,querable,xmin,ymin,xmax,ymax,srid,description,typel,geometrytype)
    else:
        print "%s isn't a valid ArcGIS Rest service"
        
def main():
    verbose = False
    usage = """
	%prog [options] url
	
	this script extract the information about all the layers present in a ArcGIS Rest API service
	url => url of the ArcGIS Rest API service
    """
    parser = OptionParser(usage)
    parser.add_option("-v","--verbose",action="store_true",dest="verbose",help="verbose output")
    parser.add_option("-d","--dbname",action="store",dest="dbname",help="sqlite file to store the data")
    (options,args) = parser.parse_args()
    if len(args) == 0:
        parser.print_help()
    else:
        url = args[0]
        dbname = options.dbname
        verbose = options.verbose
	if dbname is None:
		verbose = True
        do(url,dbname,verbose)
        
if __name__ == "__main__":
    main()
