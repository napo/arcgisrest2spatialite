import sys
from setuptools import setup

install_requires = [
    "requests>=2.4.3",
    "BeautifulSoup>=3.2.1",
    "Shapely>=1.3.0"
]

setup(
    name='arcgis-rest-to-spatialite',
    version='0.0.1',
    description='A tool to investigate a ArcGIS web service and store the data in spatialite',
    author='Maurizio Napolitano',
    author_email='napo@fbk.eu',
    url='https://github.com/napo/arcgisrest2spatialite',
    license='MIT',
    packages=('arcrestsplite',),
    scripts=(
        'bin/arcgis-discover',
    ),
    install_requires=install_requires,
)
