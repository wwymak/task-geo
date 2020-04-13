import numpy as np
import pandas as pd

from task_geo.data_sources.demographics.it_census.it_area_data import it_area_data
from task_geo.data_sources.demographics.it_census.it_territorial_units import it_territorial_units

TRANSLATED_COLUMNS = {
    'Codice comune': 'city_code',
    'Denominazione': 'city',
    'Età': 'age',
    'Maschi celibi': 'single_men',
    'Maschi coniugati': 'married_males',
    'Maschi divorziati': 'divorced_males',
    'Maschi vedovi': 'widowed_males',
    'Maschi uniti civilmente': 'males_civil_union',
    'Maschi già in unione civile (per scioglimento)': 'males_civil_union_dissolution',
    'Maschi già in unione civile (per decesso del partner)': "males_civil_union_death",
    'Totale Maschi': 'total_males',
    'Femmine nubili': 'single_females',
    'Femmine coniugate': 'married_females',
    'Femmine divorziate': 'divorced_females',
    'Femmine vedove': 'female_widows',
    'Femmine unite civilmente': 'females_united_civilly',
    'Femmine già in unione civile (per scioglimento)': 'females_civil_union_dissolution',
    'Femmine già in unione civile (per decesso del partner)': "females_civil_union_death",
    'Totale Femmine': 'total_females'
}


def it_census_formatter(raw_data):
    city_area_data = it_area_data()
    territorial_name_mappings = it_territorial_units()

    raw_data = raw_data.rename(columns=TRANSLATED_COLUMNS)
    raw_data = raw_data[['city_code', 'city', 'age', 'total_males', 'total_females']]
    raw_data['population_by_age'] = raw_data['total_males'] + raw_data['total_females']
    raw_data = raw_data.loc[raw_data['age'] != 999]
    population_by_city = raw_data.groupby(['city_code'])[[
        'total_males', 'total_females']].sum()
    population_by_city['population'] = population_by_city.agg("sum", axis="columns")
    population_by_city['male_ratio'] = \
        population_by_city['total_males'] / population_by_city['population']
    population_by_city['female_ratio'] = \
        population_by_city['total_females'] / population_by_city['population']
    age_bins = np.append(np.arange(0, 85, 5), 150)
    age_bins_text = [f"age_{i-5}-{i-1}" for i in age_bins[1:-1]] + ['age_80_plus']
    age_bin_to_text_mapping = {idx + 1: text for idx, text in enumerate(age_bins_text)}
    raw_data['age_group'] = np.digitize(raw_data['age'], age_bins)
    data_by_age_groups = raw_data.groupby(['city_code', 'city', 'age_group'])[[
        'population_by_age']].sum().reset_index()
    data_by_age_groups.loc[:, 'age_group'] = data_by_age_groups['age_group']\
        .replace(age_bin_to_text_mapping)
    data_by_age_groups_pivot = data_by_age_groups.pivot_table(
        values=['population_by_age'],
        index=['city_code', 'city'],
        columns=['age_group']).reset_index().set_index('city_code')
    # flatten the column multiindex
    data_by_age_groups_pivot = data_by_age_groups_pivot['population_by_age']\
        .reset_index().set_index('city_code')\
        .merge(pd.DataFrame(data_by_age_groups_pivot['city']),
               left_index=True, right_index=True)
    data_by_age_groups_pivot = data_by_age_groups_pivot.merge(
        population_by_city, left_index=True, right_index=True)

    age_columns = [
        'age_0-4', 'age_10-14', 'age_15-19', 'age_20-24', 'age_25-29',
        'age_30-34', 'age_35-39', 'age_40-44', 'age_45-49', 'age_5-9',
        'age_50-54', 'age_55-59', 'age_60-64', 'age_65-69', 'age_70-74',
        'age_75-79', 'age_80_plus']

    for age_group in age_columns:
        data_by_age_groups_pivot[f"ratio_{age_group}"] = \
            data_by_age_groups_pivot[age_group] / data_by_age_groups_pivot['population']
    data_by_age_groups_pivot = data_by_age_groups_pivot[[
        'city', 'population', 'male_ratio', 'female_ratio',
        'ratio_age_0-4', 'ratio_age_10-14', 'ratio_age_15-19',
        'ratio_age_20-24', 'ratio_age_25-29', 'ratio_age_30-34',
        'ratio_age_35-39', 'ratio_age_40-44', 'ratio_age_45-49',
        'ratio_age_5-9', 'ratio_age_50-54', 'ratio_age_55-59',
        'ratio_age_60-64', 'ratio_age_65-69', 'ratio_age_70-74',
        'ratio_age_75-79', 'ratio_age_80_plus']]

    data_by_age_groups_pivot = data_by_age_groups_pivot\
        .merge(city_area_data.set_index('city_code'), left_index=True, right_index=True,
               suffixes=('', '_duplicated'))\
        .merge(territorial_name_mappings, left_index=True, right_index=True,
               suffixes=('', '_duplicated'))\
        .drop(columns=[
            column for column in data_by_age_groups_pivot.columns if '_duplicated' in column])
    data_by_age_groups_pivot['population_density'] = \
        data_by_age_groups_pivot['population'] / data_by_age_groups_pivot['area']
    data_by_age_groups_pivot['country'] = 'IT'
    ordered_columns = [
        'country', 'region', 'sub_region', 'city', 'area', 'population',
        'population_density', 'male_ratio', 'female_ratio',
        'ratio_age_0-4', 'ratio_age_10-14', 'ratio_age_15-19',
        'ratio_age_20-24', 'ratio_age_25-29', 'ratio_age_30-34',
        'ratio_age_35-39', 'ratio_age_40-44', 'ratio_age_45-49',
        'ratio_age_5-9', 'ratio_age_50-54', 'ratio_age_55-59',
        'ratio_age_60-64', 'ratio_age_65-69', 'ratio_age_70-74',
        'ratio_age_75-79', 'ratio_age_80_plus']
    data_by_age_groups_pivot = data_by_age_groups_pivot[ordered_columns]
    return data_by_age_groups_pivot
