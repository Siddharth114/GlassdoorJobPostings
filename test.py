import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import pygwalker as pyg
import streamlit.components.v1 as components
from streamlit_extras.metric_cards import style_metric_cards

df = pd.read_csv("DS_jobs.csv")
df[["Location City", "Location State"]] = df.Location.str.split(", ", expand=True)
df.drop("Location", axis=1, inplace=True)
df["python"] = df["python"].replace({0: np.nan, 1: "python"})
df["excel"] = df["excel"].replace({0: np.nan, 1: "excel"})
df["hadoop"] = df["hadoop"].replace({0: np.nan, 1: "hadoop"})
df["spark"] = df["spark"].replace({0: np.nan, 1: "spark"})
df["aws"] = df["aws"].replace({0: np.nan, 1: "aws"})
df["tableau"] = df["tableau"].replace({0: np.nan, 1: "tableau"})
df["big_data"] = df["big_data"].replace({0: np.nan, 1: "big_data"})
df["Sector"] = df["Sector"].replace({"-1": "Unorganised Sector"})
df["Industry"] = df["Industry"].replace({"-1": "Unorganised Industries"})
df["job_simp"] = df["job_simp"].replace({"na": "Unspecified", "mle": "ML Engineer"})
df["job_state"] = df["job_state"].apply(lambda x: x.strip())

overall_avg_salary = round(sum(df["avg_salary"]) / len(df["avg_salary"]), 2)
overall_min_salary = round(sum(df["min_salary"]) / len(df["min_salary"]), 2)
overall_max_salary = round(sum(df["max_salary"]) / len(df["max_salary"]), 2)

state_codes = {
    "New York": "NY",
    "Virginia": "VA",
    "Massachusetts": "MA",
    "California": "CA",
    "Illinois": "IL",
    "Missouri": "MO",
    "Washington": "WA",
    "District of Columbia": "DC",
    "Tennessee": "TN",
    "Texas": "TX",
    "Pennsylvania": "PA",
    "Arizona": "AZ",
    "Wisconsin": "WI",
    "Georgia": "GA",
    "Florida": "FL",
    "United States": "US",
    "Nebraska": "NE",
    "Kansas": "KS",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "Louisiana": "LA",
    "Ohio": "OH",
    "Indiana": "IN",
    "Maryland": "MD",
    "Colorado": "CO",
    "Utah": "UT",
    "Oregon": "OR",
    "Michigan": "MI",
    "South Carolina": "SC",
    "Mississippi": "MS",
    "Alabama": "AL",
    "Rhode Island": "RI",
    "Iowa": "IA",
    "Minnesota": "MN",
    "Oklahoma": "OK",
    "Connecticut": "CT",
    "North Carolina": "NC",
    "Delaware": "DE",
    "West Virginia": "WV",
}

st.set_page_config(layout="wide")

def main():
    nav = option_menu(
        None,
        ["Filter by Sector", "Filter by State", "PygWalker Exploration"],
        icons=["building", "geo-alt", "clipboard2-data"],
        default_index=0,
        menu_icon="list",
        orientation="horizontal",
    )

    if nav=='Filter by Sector':
        sector_select = st.sidebar.selectbox(
            "",
            (
                "All Sectors",
                "Insurance",
                "Business Services",
                "Manufacturing",
                "Information Technology",
                "Biotech & Pharmaceuticals",
                "Retail",
                "Oil, Gas, Energy & Utilities",
                "Government",
                "Health Care",
                "Finance",
                "Aerospace & Defense",
                "Unorganised Sector",
                "Transportation & Logistics",
                "Media",
                "Telecommunications",
                "Real Estate",
                "Travel & Tourism",
                "Agriculture & Forestry",
                "Education",
                "Accounting & Legal",
                "Non-Profit",
                "Construction, Repair & Maintenance",
                "Consumer Services",
            ),
        )
        if sector_select != 'All Sectors':
            sector_df = df[df['Sector']==sector_select]
        else:
            sector_df = df.copy()
            sector_df['Industry']=sector_df['Sector']

        bar_chart_df = sector_df['Industry']
        bar_chart_df = sector_df.reset_index()
        bar_chart_df.drop(columns=("index"), inplace=True)

        bar_chart_df = (
            bar_chart_df.groupby('Industry').size().reset_index(name='Number of Job Postings')
        )
        st.subheader(f"Number of Job Postings by {'Industry' if sector_select!='All Sectors' else 'Sector'}")
        fig = px.bar(
            bar_chart_df,
            x="Industry",
            y="Number of Job Postings",
            labels={'Industry':f"{'Industries' if sector_select!='All Sectors' else 'Sectors'}"},
            color_discrete_sequence=px.colors.qualitative.Antique,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.divider()

        filtered_avg_salary = round(sector_df['avg_salary'].mean(), 2)
        filtered_min_salary = round(sector_df['min_salary'].mean(), 2)
        filtered_max_salary = round(sector_df['max_salary'].mean(), 2)

        st.subheader('Overall Salary Metrics (in thousands of dollars)'if sector_select=='All Sectors' else "Sector Salary vs. Overall Salary (in thousands of dollars)")
        col1, col2, col3 = st.columns(3)
        col1.metric(
            'Average Salary',
            filtered_avg_salary,
            {0:None}.get(round(filtered_avg_salary-overall_avg_salary, 2), round(filtered_avg_salary-overall_avg_salary, 2))
        )
        col2.metric(
            'Average Starting Salary',
            filtered_min_salary,
            {0:None}.get(round(filtered_min_salary-overall_min_salary, 2), round(filtered_min_salary-overall_min_salary, 2))

        )
        col3.metric(
            'Average Maximum Salary',
            filtered_max_salary,
            {0:None}.get(round(filtered_max_salary-overall_max_salary, 2), round(filtered_max_salary-overall_max_salary, 2))
        )
        style_metric_cards(border_left_color="#4682A9", background_color="#212A3E")
        st.divider()

        
        






    
    elif nav=='Filter by State':
        pass
    
    
    else:
        pass



if __name__=='__main__':
    main()