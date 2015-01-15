#!/usr/bin/python
from __future__ import unicode_literals
from optparse import OptionParser
from arcrestsplite import ArcGIS
from builtins import str as futureenc


def do(source,destination,table):
    arcgis = ArcGIS()
    if (arcgis.isarcgislayer(source)):
        if table is None:
            name = futureenc(arcgis.inspect(source)['name'])
            name = arcgis._cleanname(name)
        if arcgis.querable(source):
            arcgis.download(source,destination,table)
    else:
        print "%s is an invalid source" % (source)
        
def main():
    usage = """
    %prog [options] source destination
    
    this script download the data from a ArcGIS Rest 'layer' and dump it on a spatialite file
    
    source => url of the ArcGIS rest resource
    destination => path of the spatialite file
    """
    parser = OptionParser(usage)
    parser.add_option("-t","--table",action="store",dest="table",help="name of the desidered table")
    (options,args) = parser.parse_args()
    if len(args) == 0:
        parser.print_help()
    else:
        source = args[0]
        destination = args[1]
        table = options.table
        do(source,destination,table)
        
if __name__ == "__main__":
    main()