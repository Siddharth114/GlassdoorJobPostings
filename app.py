import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv('DS_jobs.csv')
df['Location'] = df['Location'].replace({'United States': 'San Francisco, CA', 'Patuxent, Anne Arundel, MD':'Anne Arundel, MD'})
df[['Location City', 'Location State']] = df.Location.str.split(', ',expand=True)
df.drop('Location', axis=1, inplace=True)
df['python'] = df['python'].replace({0: np.nan, 1: 'python'})
df['excel'] = df['excel'].replace({0: np.nan, 1: 'excel'})
df['hadoop'] = df['hadoop'].replace({0: np.nan, 1: 'hadoop'})
df['spark'] = df['spark'].replace({0: np.nan, 1: 'spark'})
df['aws'] = df['aws'].replace({0: np.nan, 1: 'aws'})
df['tableau'] = df['tableau'].replace({0: np.nan, 1: 'tableau'})
df['big_data'] = df['big_data'].replace({0: np.nan, 1: 'big_data'})
df['Sector'] = df['Sector'].replace({'-1':'Unorganised Sector'})
df['Industry'] = df['Industry'].replace({'-1':'Unorganised Industries'})
df['job_simp'] = df['job_simp'].replace({'na':'Unspecified', 'mle':'ML Engineer'})

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
       'Finance', 'Aerospace & Defense', 'Unorganised Sector',
       'Transportation & Logistics', 'Media', 'Telecommunications',
       'Real Estate', 'Travel & Tourism', 'Agriculture & Forestry',
       'Education', 'Accounting & Legal', 'Non-Profit',
       'Construction, Repair & Maintenance', 'Consumer Services'))
        
        if sector_select == 'All sectors':
            sectors_df = df.groupby('Sector')['Industry'].value_counts().sort_values(ascending=False).reset_index(name='Number of Job Postings')
            sectors_df = sectors_df[['Sector', 'Number of Job Postings']]
            agg_functions = {'Number of Job Postings':'sum'}
            sectors_df = sectors_df.groupby(sectors_df['Sector']).aggregate(agg_functions).reset_index()
            
            fig = px.bar(sectors_df, x='Sector', y='Number of Job Postings', color_discrete_sequence=px.colors.qualitative.Antique)
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            col1.metric('Overall Average Salary (in thousands of dollars)',f'{overall_avg_salary}')
            col2.metric('Overall Average Starting Salary (in thousands of dollars)',f'{overall_min_salary}')
            col3.metric('Overall Average Maximum Salary (in thousands of dollars)',f'{overall_max_salary}')

            skill_counts = {}
            skills = ['python', 'excel', 'hadoop', 'spark', 'aws', 'tableau', 'big_data']
            for skill in skills:
                skill_counts[skill.capitalize()]=(df[skill].value_counts()[skill])

            skills_df = pd.DataFrame.from_dict(skill_counts, orient="index", columns=["Number of Job Postings"])
            skills_df = skills_df.reset_index()
            skills_df.rename(columns={'index':'Skill'}, inplace=True)

            fig = px.pie(skills_df, values='Number of Job Postings', names='Skill', hole=0.4, color_discrete_sequence=px.colors.qualitative.Antique)
            st.plotly_chart(fig, use_container_width=True)

            title_counts = {}
            titles = df['job_simp'].unique()
            for title in titles:
                if title=='Unspecified':
                    continue
                title_counts[title.capitalize()] = df['job_simp'].value_counts()[title]
            
            titles_df = pd.DataFrame.from_dict(title_counts, orient="index", columns=["Number of Job Postings"])
            titles_df = titles_df.reset_index()
            titles_df.rename(columns={'index':'Job Title'}, inplace=True)
            fig = px.pie(titles_df, values='Number of Job Postings', names='Job Title', hole=0.4, color_discrete_sequence=px.colors.qualitative.Antique)
            st.plotly_chart(fig, use_container_width=True)


            state_counts = {}
            states = df['job_state'].unique()
            for state in states:
                state_counts[state.strip()] = df['job_state'].value_counts()[state]
            states_df = pd.DataFrame.from_dict(state_counts, orient="index", columns=["Number of Job Postings"])
            states_df = states_df.reset_index()
            states_df.rename(columns={'index':'State'}, inplace=True)

            fig = px.choropleth(states_df, locations='State', locationmode='USA-states', color='Number of Job Postings',
                    scope='usa', color_continuous_scale='Blues',
                    title='USA States and Counts')
            st.plotly_chart(fig, use_container_width=True)


        else:
            sector_filter_df = df[df['Sector']==sector_select]['Industry']
            sector_filter_df = sector_filter_df.reset_index()
            sector_filter_df.drop(columns=('index'), inplace=True)
            sector_filter_df = sector_filter_df.groupby('Industry').size().reset_index(name='Number of Job Postings')
            
            fig = px.bar(sector_filter_df, x='Industry', y='Number of Job Postings', color_discrete_sequence=px.colors.qualitative.Antique)
            st.plotly_chart(fig, use_container_width=True)

            sector_filter_df_copy = df[df['Sector']==sector_select]
            sector_avg_salary = round(sum(sector_filter_df_copy['avg_salary'])/len(sector_filter_df_copy['avg_salary']), 2)
            sector_min_salary = round(sum(sector_filter_df_copy['min_salary'])/len(sector_filter_df_copy['min_salary']), 2)
            sector_max_salary = round(sum(sector_filter_df_copy['max_salary'])/len(sector_filter_df_copy['max_salary']), 2)

            col1, col2, col3 = st.columns(3)
            col1.metric('Sector Average Salary (in thousands of dollars)',f'{sector_avg_salary}', round(sector_avg_salary-overall_avg_salary, 2))
            col2.metric('Sector Average Starting Salary (in thousands of dollars)',f'{sector_min_salary}', round(sector_min_salary-overall_min_salary, 2))
            col3.metric('Sector Average Maximum Salary (in thousands of dollars)',f'{sector_max_salary}', round(sector_max_salary-overall_max_salary, 2))

            sector_filter_df_copy = df[df['Sector']==sector_select]
            skill_counts = {}
            skills = ['python', 'excel', 'hadoop', 'spark', 'aws', 'tableau', 'big_data']
            for skill in skills:
                skill_counts[skill.capitalize()]=(sector_filter_df_copy[skill].value_counts()[skill])

            sector_filter_skills_df = pd.DataFrame.from_dict(skill_counts, orient="index", columns=["Number of Job Postings"])
            sector_filter_skills_df = sector_filter_skills_df.reset_index()
            sector_filter_skills_df.rename(columns={'index':'Skill'}, inplace=True)
            
            fig = px.pie(sector_filter_skills_df, values='Number of Job Postings', names='Skill', hole=0.4, color_discrete_sequence=px.colors.qualitative.Antique)
            st.plotly_chart(fig, use_container_width=True)
            
            sector_filter_df_copy = df[df['Sector']==sector_select]
            title_counts = {}
            titles = sector_filter_df_copy['job_simp'].unique()
            for title in titles:
                if title=='Unspecified':
                    continue
                title_counts[title.capitalize()] = sector_filter_df_copy['job_simp'].value_counts()[title]
            
            titles_df = pd.DataFrame.from_dict(title_counts, orient="index", columns=["Number of Job Postings"])
            titles_df = titles_df.reset_index()
            titles_df.rename(columns={'index':'Job Title'}, inplace=True)

            fig = px.pie(titles_df, values='Number of Job Postings', names='Job Title', hole=0.4, color_discrete_sequence=px.colors.qualitative.Antique)
            st.plotly_chart(fig, use_container_width=True)




    
if __name__=='__main__':
    main()