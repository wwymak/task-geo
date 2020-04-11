"""Retrieve territorial names from Italian National Institute of Statistics.
This dataset helps to link communes with their parent provinces and regions

Credits: https://www.istat.it/it/archivio/6789
License: http://creativecommons.org/licenses/by/3.0/it/

"""

import pandas as pd

URL = 'https://www.istat.it/storage/codici-unita-amministrative/Elenco-comuni-italiani.csv'


def it_territorial_units_connector():
    data = pd.read_csv(URL)
    return data

if __name__ == "__main__":
    data = it_territorial_units_connector()
    data.head()

    """
    cols  =
    ['Codice Regione',
       'Codice dell'Unità territoriale sovracomunale \n(valida a fini statistici)',
       'Codice Provincia (Storico)(1)', 'Progressivo del Comune (2)',
       'Codice Comune formato alfanumerico',
       'Denominazione (Italiana e straniera)', 'Denominazione in italiano',
       'Denominazione altra lingua', 'Codice Ripartizione Geografica',
       'Ripartizione geografica', 'Denominazione regione',
       'Denominazione dell'Unità territoriale sovracomunale \n(valida a fini statistici)',
       'Flag Comune capoluogo di provincia/città metropolitana/libero consorzio',
       'Sigla automobilistica', 'Codice Comune formato numerico',
       'Codice Comune numerico con 110 province (dal 2010 al 2016)',
       'Codice Comune numerico con 107 province (dal 2006 al 2009)',
       'Codice Comune numerico con 103 province (dal 1995 al 2005)',
       'Codice Catastale del comune', 'Popolazione legale 2011 (09/10/2011)',
       'NUTS1', 'NUTS2(3) ', 'NUTS3']
    """
