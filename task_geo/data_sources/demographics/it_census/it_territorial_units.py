"""
Retrieve territorial names from Italian National Institute of Statistics.
This dataset helps to link communes with their parent provinces and regions

Credits: https://www.istat.it/it/archivio/6789
License: http://creativecommons.org/licenses/by/3.0/it/

"""
import pandas as pd

URL = 'https://www.istat.it/storage/codici-unita-amministrative/Elenco-comuni-italiani.csv'

TRANSLATED_COLUMNS = {
    'Denominazione in italiano': 'city',
    "Denominazione dell'Unità territoriale sovracomunale \n(valida a fini statistici)":
        'sub_region',
    'Denominazione regione': 'region',
    'Codice Comune formato numerico': 'city_code'
}


def _it_territorial_units_connector():
    data = pd.read_csv(URL, encoding='latin-1', sep=';')
    return data


def _it_territorial_units_formatter(data):
    data = data.copy()
    data = data.rename(columns=TRANSLATED_COLUMNS)
    data = data[['city_code', 'region', 'sub_region', 'city']].set_index('city_code')
    return data


def it_territorial_units():
    data = _it_territorial_units_connector()
    data = _it_territorial_units_formatter(data)
    return data
