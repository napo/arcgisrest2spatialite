#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from optparse import OptionParser
from arcrestsplite import ArcGIS
from builtins import str as futureenc

def do(source,destination,verbose):
    arcgis = ArcGIS(source)
    arcgis.discover() 
    for layer in arcgis.layers:
        if layer['querable']:
            url=futureenc(layer['url'])
            name=futureenc(layer['name'])
            if verbose:
                print url
            arcgis.download(url,destination,name)
        
def main():
    verbose = False
    usage = """
	%prog [options] source destination
	
	this script dump an entire arcgis rest api service on a spatialite file
	
	source => a valid arcgis rest api service
	destination => path of the spatialite file where store the data
"""
    parser = OptionParser(usage)
    parser.add_option("-v","--verbose",action="store_true",dest="verbose",help="verbose output")
    (options,args) = parser.parse_args()
    if len(args) == 0:
        parser.print_help()
    else:
        source = args[0]
        destination = args[1]
        verbose = options.verbose
        do(source,destination,verbose)
        
if __name__ == "__main__":
    main()
