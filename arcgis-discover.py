# -*- coding: utf-8 -*-
"""
Created on Tue Apr 07 15:11:49 2014
@author: Maurizio Napolitano <napo@fbk.eu>
The MIT License (MIT)
Copyright (c) 2016 Fondazione Bruno Kessler http://fbk.eu
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
from optparse import OptionParser
from arcrestsplite.arcrestapi import ArcGIS
version = "0.1" 
def main():
    usage = "%prog arcgis_restapi_url\n"
    usage += "eg:\n   %prog http://geo.umbriaterritorio.it/ArcGIS/rest/services"
    parser = OptionParser(usage)
#    parser.add_option("-v","--version",action="store_false",help="show version")  
    (options,args) = parser.parse_args()

    if len(args) == 0:
        parser.print_help()
    else:
        discover = args[0]
        arcgis = ArcGIS(discover)
        arcgis.discover() 
        for layer in arcgis.layers:
            if layer['querable']:
                url=layer['url']
                name=layer['name']
                print "%s %s" % (url,name)
if __name__ == "__main__":
    main()
