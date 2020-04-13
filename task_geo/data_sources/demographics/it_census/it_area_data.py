"""
Retrieve geographic data from Italian National Institute of Statistics.

Credits: https://www.istat.it/it/archivio/222527
License: http://creativecommons.org/licenses/by/3.0/it/

"""
from io import BytesIO
from zipfile import ZipFile

import pandas as pd
import requests
import shapefile


def _it_area_data_connector():
    URL = 'http://www.istat.it/storage/cartografia/confini_amministrativi/' \
          'generalizzati/Limiti01012020_g.zip'

    zipped = requests.get(URL)
    zipdata = BytesIO(zipped.content)
    with ZipFile(zipdata) as content:
        communes_shp = content.open('Limiti01012020_g/Com01012020_g/Com01012020_g_WGS84.shp')
        communes_dbf = content.open('Limiti01012020_g/Com01012020_g/Com01012020_g_WGS84.dbf')
        shapefile_reader = shapefile.Reader(shp=communes_shp, dbf=communes_dbf)

        fields = [x[0] for x in shapefile_reader.fields][1:]
        records = [y[:] for y in shapefile_reader.records()]
        data = pd.DataFrame(columns=fields, data=records)

    return data


def _it_area_data_formatter(data):
    data = data.copy()
    data = data.rename(columns={
        'PRO_COM': 'city_code',
        'COMUNE': 'city',
        'SHAPE_AREA': 'area'
    })
    # convert area in m^2 to km^2
    data['area'] = data['area'] / 1e6
    data = data[['city_code', 'city', 'area']]
    return data


def it_area_data():
    data = _it_area_data_connector()
    data = _it_area_data_formatter(data)
    return data
