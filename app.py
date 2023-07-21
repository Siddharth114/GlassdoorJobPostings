import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('DS_jobs.csv')
df['Location'] = df['Location'].replace({'United States': 'San Francisco, CA', 'Patuxent, Anne Arundel, MD':'Anne Arundel, MD'})
df[['Location City', 'Location State']] = df.Location.str.split(', ',expand=True)
df.drop('Location', axis=1, inplace=True)
df['python'] = df['python'].replace({0: np.nan, 1: 'python'})
df['excel'] = df['excel'].replace({0: np.nan, 1: 'excel'})
df['hadoop'] = df['hadoop'].replace({0: np.nan, 1: 'hadoop'})
df['spark'] = df['spark'].replace({0: np.nan, 1: 'spark'})
df['aws'] = df['aws'].replace({0: np.nan, 1: 'aws'})
df['tableau'] = df['tableau'].replace({0: np.nan, 1: 'yableau'})
df['big_data'] = df['big_data'].replace({0: np.nan, 1: 'big_data'})

overall_avg_salary = round(sum(df['avg_salary'])/len(df['avg_salary']), 2)
overall_min_salary = round(sum(df['min_salary'])/len(df['min_salary']), 2)
overall_max_salary = round(sum(df['max_salary'])/len(df['max_salary']), 2)

st.set_page_config(layout='wide')

def main():

    nav = option_menu(None, ["Sector-Wise", 'State-Wise'], 
        icons=['briefcase', 'geo-alt'], default_index=0, menu_icon='list', orientation='horizontal')
    
    if nav=='Sector-Wise':
        
       

        sector_select = st.selectbox('Filter by Sector', ('All sectors', 'Insurance', 'Business Services', 'Manufacturing',
       'Information Technology', 'Biotech & Pharmaceuticals', 'Retail',
       'Oil, Gas, Energy & Utilities', 'Government', 'Health Care',
       'Finance', 'Aerospace & Defense', '-1',
       'Transportation & Logistics', 'Media', 'Telecommunications',
       'Real Estate', 'Travel & Tourism', 'Agriculture & Forestry',
       'Education', 'Accounting & Legal', 'Non-Profit',
       'Construction, Repair & Maintenance', 'Consumer Services'))
        
        if sector_select == 'All sectors':
            sectors_df = df.groupby('Sector')['Industry'].value_counts().sort_values(ascending=False).reset_index(name='Number of Job Postings')
            sectors_df = sectors_df[['Sector', 'Number of Job Postings']]
            agg_functions = {'Number of Job Postings':'sum'}
            sectors_df = sectors_df.groupby(sectors_df['Sector']).aggregate(agg_functions).reset_index()
            st.bar_chart(data=sectors_df, x='Sector', y='Number of Job Postings')

            col1, col2, col3 = st.columns(3)
            col1.metric('Overall Average Salary (in thousands of dollars)',f'{overall_avg_salary}')
            col2.metric('Overall Average Starting Salary (in thousands of dollars)',f'{overall_min_salary}')
            col3.metric('Overall Average Maximum Salary (in thousands of dollars)',f'{overall_max_salary}')


        else:
            sector_filter_df = df[df['Sector']==sector_select]['Industry']
            sector_filter_df = sector_filter_df.reset_index()
            sector_filter_df.drop(columns=('index'), inplace=True)
            sector_filter_df = sector_filter_df.groupby('Industry').size().reset_index(name='Number of Job Postings')
            st.bar_chart(data=sector_filter_df, x='Industry', y='Number of Job Postings')

            sector_filter_df_copy = df[df['Sector']==sector_select]
            sector_avg_salary = round(sum(sector_filter_df_copy['avg_salary'])/len(sector_filter_df_copy['avg_salary']), 2)
            sector_min_salary = round(sum(sector_filter_df_copy['min_salary'])/len(sector_filter_df_copy['min_salary']), 2)
            sector_max_salary = round(sum(sector_filter_df_copy['max_salary'])/len(sector_filter_df_copy['max_salary']), 2)

            col1, col2, col3 = st.columns(3)
            col1.metric('Sector Average Salary (in thousands of dollars)',f'{sector_avg_salary}', round(sector_avg_salary-overall_avg_salary, 2))
            col2.metric('Sector Average Starting Salary (in thousands of dollars)',f'{sector_min_salary}', round(sector_min_salary-overall_min_salary, 2))
            col3.metric('Sector Average Maximum Salary (in thousands of dollars)',f'{sector_max_salary}', round(sector_max_salary-overall_max_salary, 2))





    
if __name__=='__main__':
    main()