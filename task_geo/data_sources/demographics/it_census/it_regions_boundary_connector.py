"""Retrieve geographic data from Italian National Institute of Statistics.

Credits: https://www.istat.it/it/archivio/222527
License: http://creativecommons.org/licenses/by/3.0/it/

"""

from io import BytesIO
from zipfile import ZipFile

import shapefile
import pandas as pd
import requests

URL = 'http://www.istat.it/storage/cartografia/confini_amministrativi/generalizzati/Limiti01012020_g.zip'


def it_regions_boundary_connector():
    zipped = requests.get(URL)
    zipdata = BytesIO(zipped.content)
    with ZipFile(zipdata) as content:
        communes_shp = content.open('Limiti01012020_g/Com01012020_g/Com01012020_g_WGS84.shp')
        communes_dbf = content.open('Limiti01012020_g/Com01012020_g/Com01012020_g_WGS84.dbf')
        shapefile_reader = shapefile.Reader(shp=communes_shp, dbf=communes_dbf)

        fields = [x[0] for x in shapefile_reader.fields][1:]
        records = [y[:] for y in shapefile_reader.records()]
        geometries = [s.points for s in shapefile_reader.shapes()]
        shape_type = shapefile_reader.shapeType
        data = pd.DataFrame(columns=fields, data=records)
        data["geometry"] = geometries

    return data

if __name__ == "__main__":
    data = it_regions_boundary_connector()
    #['COD_RIP', 'COD_REG', 'COD_PROV', 'COD_CM', 'COD_UTS', 'PRO_COM',
       # 'PRO_COM_T', 'COMUNE', 'COMUNE_A', 'CC_UTS', 'SHAPE_AREA', 'SHAPE_LEN']
    data.head()
