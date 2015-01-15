import sys
from setuptools import setup

install_requires = [
    "future>=0.14.3",
    "requests>=2.4.3",
    "BeautifulSoup>=3.2.1",
    "Shapely>=1.3.0"
]

setup(
    name='arcgis-rest-to-spatialite',
    version='0.0.5',
    description='A tool to investigate a ArcGIS web service and store the data in spatialite',
    author='Maurizio Napolitano',
    author_email='napo@fbk.eu',
    url='https://github.com/napo/arcgisrest2spatialite',
    license='MIT',
    packages=('arcrestsplite',),
    scripts=(
	'bin/arcgis2splite.py',
	'bin/arcgis-get-layer.py',
	'bin/arcgis-discover.py',
	'bin/arcgis-inspect-layer.py',
    ),
    install_requires=install_requires,
)
