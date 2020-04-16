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

#### Area data per comune (city):
- simple renaming of columns from italian to english, and selecting the `city_code`, `city` and `area` columns

#### Comune -> Province -> Region mapping:
- simple renaming of columns from italian to english, and selecting the `city_code`, `region`, `sub_region`, `city`

#### Main demographic data per comune:
- each row in the raw data correspond to the population per age per city (e.g. population of 10 years old in Milan)
- from the population data, calculate the total population per city/comune by summing total males + total females
- filter out the rows that have age==999 (since this indicates the total)
- split the age ranges into buckets of 5 years
- groupby age group, calculate the total males/females/population by age group, and the ratio of population in each age group
- pivot data so each row correspond to 1 city

#### lifestyle metrics per region
- download data from istat-- you have to visit the relevant page and click on 'export' from the interactive menu, there is no option of doing this automatically(the link the frontend generates is not callable from code)
- filter rows to only include data that is 'per 100 population' tp get the ratio
- pivot data to have 1 row per region
