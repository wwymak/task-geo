# ITALIAN CENSUS


## General information

- **Description**: Demographic data at the commune(city) level for Italy
- **Credits**: Italian National Institute of Statistics.
- **Source**:
    - population by different regional levels: http://demo.istat.it/pop2019
    - italian communes to province mapping https://www.istat.it/it/archivio/6789#Elencodeicodiciedelledenominazionidelleunitterritoriali-0
    - cartographic data from https://www.istat.it/it/archivio/222527

## Description

**country**
- Description: country iso-2 code
- Type: str

**region**
- Description: Regions of Italy (e.g Calabria)
- Type: str

**sub_region**
- Description: Provinces of Italy (e.g. Bologna)
- Type: str

**city**
- Description: Communes of Italy (e.g. Milano)
- Type: str

**area**
- Description: land area
- Type: float
- Units: km^2

**population**
- Description: population
- Type: float

**population_density**
- Description: population/area
- Type: float
- Units: people per km^2

**male_ratio**
- Description: proportion of population that is male
- Type: float

**female_ratio**
- Description: proportion of population that is female
- Type: float

**ratio_age_0-4** (and all the rest of ratio_age_xx-yy columns)
- Description: ratio of population that has age 0 to 4 (inclusive on both ends)
- Type: float

## Transformations applied

(List all the transformation done to your data from the moment you retrieve it, to the
moment your data source returns it, this includes, but is not limited to:
- Filtering
- Aggregation
- Merging
- Enriching
- Decoding / Encoding
- Change of Units
- Adding/removing columns
- ...
)
