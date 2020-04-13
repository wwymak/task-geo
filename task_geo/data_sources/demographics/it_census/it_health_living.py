import pandas as pd

smokers = pd.read_csv('DCCV_AVQ_PERSONE_smoking.csv')
smokers = smokers.loc[(smokers.TIPO_DATO_AVQ == '14_FUMO_SI') & (
    smokers.Misura == 'per 100 persone con le stesse caratteristiche'), :]
smokers = smokers.rename(columns={'Territorio': 'Region',
                                  'Value': 'ratio_smoking'})[['Region', 'ratio_smoking']]

health = pd.read_csv('DCCV_AVQ_PERSONE_health.csv')
health = health.loc[health.Measure == 'per 100 people with the same characteristics']
health_pivot = health.pivot_table(index='Territory', values='Value', columns=['Data type'])
health_col_name_mapping = {
    'chronic patients - suffering from allergic diseases': 'ratio_allergic_diseases',
    'chronic patients - suffering from chronic bronchitis': 'ratio_chronic_bronchitis',
    'chronic patients - suffering from diabetes': 'ratio_diabetes',
    'chronic patients - suffering from gastric or duodenal ulcer': 'ratio_gastric_duodenal_ulcer',
    'chronic patients - suffering from heart disease': 'ratio_heart_diseases',
    'chronic patients - suffering from nervous disorders': 'ratio_nervous_disorders',
    'chronic patients - suffering from osteoarthritis, arthritis': 'ratio_arthritis',
    'chronic patients - with hypertension': 'ratio_hypertension',
    'chronic patients - with osteoporosis': 'ratio_osteoporosis'}

health_pivot = health_pivot.rename(columns=health_col_name_mapping).reset_index()

bmi = pd.read_csv('DCCV_AVQ_PERSONE1_bmi.csv')
bmi = bmi.loc[(bmi.Measure == 'per 100 people with the same characteristics') & (
    bmi.Gender == 'total'), :]
bmi_pivot = bmi.pivot_table(index='Territory', values='Value', columns=['Data type'])
bmi_column_name_mapping = {k: f"ration_{k.replace(' ', '_')}" for k in bmi.columns}
bmi_pivot = bmi_pivot.rename(columns=bmi_column_name_mapping).reset_index()

all_conditions = (bmi_pivot
                  .merge(health_pivot, left_on='Territory', right_on='Territory', how='left')
                  .merge(smokers, left_on='Territory', right_on='Territory', how='left'))
