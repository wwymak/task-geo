from unittest import TestCase
from unittest.mock import patch

import pandas as pd

from task_geo.data_sources.demographics.it_census import it_census_formatter
from task_geo.testing import check_dataset_format


@patch('task_geo.data_sources.demographics.it_census.it_area_data.it_area_data',
       return_value=pd.DataFrame(
           data={'city_code': {270: 1001, 271: 1002},
                 'city': {270: 'Agliè', 271: 'Airasca'},
                 'area': {270: 13.3069621729, 271: 15.9535292486}}
       ).set_index('city_code'))
@patch('task_geo.data_sources.demographics.it_census.it_territorial_units.it_territorial_units',
       return_value=pd.DataFrame(
           data={'city_code': {0: 1001, 1: 1002},
                 'region': {0: 'Piemonte', 1: 'Piemonte'},
                 'sub_region': {0: 'Torino', 1: 'Torino'},
                 'city': {0: 'Agliè', 1: 'Airasca'}}
       ).set_index('city_code'))
class TestITCensus(TestCase):

    def test_validate_formatter(self, *args):
        """ Validate formatter result according to Data Model"""
        # Setup
        raw = pd.read_csv('tests/fixtures/it_census_fixture.csv')

        # Run
        data = it_census_formatter(raw)

        # Check.
        check_dataset_format(data)
