#!/usr/bin/python
from __future__ import unicode_literals
from optparse import OptionParser
from arcrestsplite import ArcGIS
from builtins import str as futureenc


def do(source):
    arcgis = ArcGIS()
    if (arcgis.isarcgislayer(source)):
        data = arcgis.inspect(source)
        print data
        querable = arcgis.querable(source)
        if (querable):
            querabletxt = "this source is querable"
        else:
            querabletxt = "this source is not querable"
        print querabletxt
    else:
        print "%s is an invalid source" % (source)
        
def main():
    usage = """
    %prog [options] source
    
    this script show information about an ArcGIS Rest 'layer' 
    
    source => url of the ArcGIS rest layer
    """
    parser = OptionParser(usage)
    (options,args) = parser.parse_args()
    if len(args) == 0:
        parser.print_help()
    else:
        source = args[0]
        do(source)
        
if __name__ == "__main__":
    main()