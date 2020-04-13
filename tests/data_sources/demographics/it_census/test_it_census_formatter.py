from unittest import TestCase

import pandas as pd

from task_geo.data_sources.demographics.it_census import it_census_formatter
from task_geo.testing import check_dataset_format


class TestITCensus(TestCase):

    def test_validate_formatter(self):
        """ Validate formatter result according to Data Model"""
        # Setup
        raw = pd.read_csv('tests/fixtures/it_census_fixture.csv')

        # Run
        data = it_census_formatter(raw)

        # Check.
        check_dataset_format(data)
