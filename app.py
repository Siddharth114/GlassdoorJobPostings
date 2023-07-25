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

overall_avg_salary = round(df["avg_salary"].mean(), 2)
overall_min_salary = round(df["min_salary"].mean(), 2)
overall_max_salary = round(df["max_salary"].mean(), 2)

overall_rating = round(df["Rating"].mean(), 2)

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

    if nav == "Filter by Sector":
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
        if sector_select != "All Sectors":
            sector_df = df[df["Sector"] == sector_select]
        else:
            sector_df = df.copy()
            sector_df["Industry"] = sector_df["Sector"]

        bar_chart_df = sector_df["Industry"]
        bar_chart_df = bar_chart_df.reset_index()
        bar_chart_df.drop(columns=("index"), inplace=True)

        bar_chart_df = (
            bar_chart_df.groupby("Industry")
            .size()
            .reset_index(name="Number of Job Postings")
        )
        st.subheader(
            f"Number of Job Postings by {'Industry' if sector_select!='All Sectors' else 'Sector'}",
            help=f'Bar Chart visualising the number of job postings in each {"industry of the filtered sector" if sector_select!="All Sectors" else "sector"} '
        )
        fig = px.bar(
            bar_chart_df,
            x="Industry",
            y="Number of Job Postings",
            labels={
                "Industry": f"{'Industries' if sector_select!='All Sectors' else 'Sectors'}"
            },
            color_discrete_sequence=px.colors.qualitative.Antique,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.divider()

        filtered_avg_salary = round(sector_df["avg_salary"].mean(), 2)
        filtered_min_salary = round(sector_df["min_salary"].mean(), 2)
        filtered_max_salary = round(sector_df["max_salary"].mean(), 2)

        st.subheader(
            "Overall Salary Metrics (in thousands of dollars)"
            if sector_select == "All Sectors"
            else "Sector Salary vs. Overall Salary (in thousands of dollars)",
            help='Metrics of the salary of all job postings' if sector_select=='All Sectors' else 'Comparison of filtered sector\'s salary metrics with overall salary'
        )
        col1, col2, col3 = st.columns(3)
        col1.metric(
            "Average Salary",
            filtered_avg_salary,
            {0: None}.get(
                round(filtered_avg_salary - overall_avg_salary, 2),
                round(filtered_avg_salary - overall_avg_salary, 2),
            ),
        )
        col2.metric(
            "Average Starting Salary",
            filtered_min_salary,
            {0: None}.get(
                round(filtered_min_salary - overall_min_salary, 2),
                round(filtered_min_salary - overall_min_salary, 2),
            ),
        )
        col3.metric(
            "Average Maximum Salary",
            filtered_max_salary,
            {0: None}.get(
                round(filtered_max_salary - overall_max_salary, 2),
                round(filtered_max_salary - overall_max_salary, 2),
            ),
        )
        style_metric_cards(border_left_color="#4682A9", background_color="#212A3E")
        st.divider()

        col1, col2 = st.columns(2)

        skill_counts = {}
        skills = [
            "python",
            "excel",
            "hadoop",
            "spark",
            "aws",
            "tableau",
            "big_data",
        ]

        for skill in skills:
            try:
                skill_counts[skill.capitalize()] = sector_df[skill].value_counts()[
                    skill
                ]
            except:
                skill_counts[skill.capitalize()] = 0
        skill_df = pd.DataFrame.from_dict(
            skill_counts, orient="index", columns=["Number of Job Postings"]
        )
        skill_df = skill_df.reset_index()
        skill_df.rename(columns={"index": "Skill"}, inplace=True)
        fig = px.pie(
            skill_df,
            values="Number of Job Postings",
            names="Skill",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Antique,
        )
        col1.subheader("Skill Distribution", help='Distribution of various skills used in the filtered sector')
        col1.plotly_chart(fig, use_container_width=True)

        title_counts = {}
        titles = sector_df["job_simp"].unique()
        for title in titles:
            if title == "Unspecified":
                continue
            else:
                title_counts[title.capitalize()] = sector_df["job_simp"].value_counts()[
                    title
                ]

        titles_df = pd.DataFrame.from_dict(
            title_counts, orient="index", columns=["Number of Job Postings"]
        )
        titles_df = titles_df.reset_index()
        titles_df.rename(columns={"index": "Job Title"}, inplace=True)

        fig = px.pie(
            titles_df,
            values="Number of Job Postings",
            names="Job Title",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Antique,
        )
        col2.subheader("Job Title Distribution", help='Distribution of various job titles in the filtered sector')
        col2.plotly_chart(fig, use_container_width=True)
        st.divider()

        state_counts = {}
        states = [
            "AL",
            "AK",
            "AZ",
            "AR",
            "CA",
            "CO",
            "CT",
            "DE",
            "FL",
            "GA",
            "HI",
            "ID",
            "IL",
            "IN",
            "IA",
            "KS",
            "KY",
            "LA",
            "ME",
            "MD",
            "MA",
            "MI",
            "MN",
            "MS",
            "MO",
            "MT",
            "NE",
            "NV",
            "NH",
            "NJ",
            "NM",
            "NY",
            "NC",
            "ND",
            "OH",
            "OK",
            "OR",
            "PA",
            "RI",
            "SC",
            "SD",
            "TN",
            "TX",
            "UT",
            "VT",
            "VA",
            "WA",
            "WV",
            "WI",
            "WY",
        ]
        for state in states:
            try:
                state_counts[state.strip()] = sector_df["job_state"].value_counts()[
                    state
                ]
            except KeyError:
                state_counts[state.strip()] = 0

        states_df = pd.DataFrame.from_dict(
            state_counts, orient="index", columns=["Number of Job Postings"]
        )
        states_df = states_df.reset_index()
        states_df.rename(columns={"index": "State"}, inplace=True)

        fig = px.choropleth(
            states_df,
            locations="State",
            locationmode="USA-states",
            color="Number of Job Postings",
            scope="usa",
            color_continuous_scale="mint",
        )
        st.subheader("State Heatmap", help='A heatmap showing the number of job postings categorized by each state')
        st.plotly_chart(fig, use_container_width=True)
        st.divider()

        st.subheader(
            "Overall Job Rating Metrics (out of 5)"
            if sector_select == "All Sectors"
            else "Sector-wise job rating vs. Overall rating (out of 5)",
            help='Overall job rating metrics' if sector_select=='All Sectors' else 'Comparison of rating metrics of the filtered sector with overall rating'
        )
        col1, col2, col3 = st.columns([1, 3, 1])
        filtered_rating = round(sector_df["Rating"].mean(), 2)
        col2.metric(
            "Average Rating",
            overall_rating,
            {0: None}.get(
                round(filtered_rating - overall_rating, 2),
                round(filtered_rating - overall_rating, 2),
            ),
        )

    elif nav == "Filter by State":
        state_select = st.sidebar.selectbox(
            "",
            (
                "All States",
                "New York",
                "Virginia",
                "Massachusetts",
                "California",
                "Illinois",
                "Missouri",
                "Washington",
                "District of Columbia",
                "Tennessee",
                "Texas",
                "Pennsylvania",
                "Arizona",
                "Wisconsin",
                "Georgia",
                "Florida",
                "United States",
                "Nebraska",
                "Kansas",
                "New Hampshire",
                "New Jersey",
                "Louisiana",
                "Ohio",
                "Indiana",
                "Maryland",
                "Colorado",
                "Utah",
                "Oregon",
                "Michigan",
                "South Carolina",
                "Mississippi",
                "Alabama",
                "Rhode Island",
                "Iowa",
                "Minnesota",
                "Oklahoma",
                "Connecticut",
                "North Carolina",
                "Delaware",
                "West Virginia",
            ),
        )

        if state_select=='All States':
            state_df = df.copy()
        else:
            state_df = df[df['job_state']==state_codes[state_select]]
        

        bar_chart_df = state_df['Sector']
        bar_chart_df = bar_chart_df.reset_index()
        bar_chart_df.drop(columns=("index"), inplace=True)

        bar_chart_df = (
            bar_chart_df.groupby('Sector').size().reset_index(name='Number of Job Postings')
        )
        
        
        st.subheader("Number of Job Postings by Sector", help='A visualisation of the number of job postings of each sector in the filtered state')
        fig=px.bar(
            bar_chart_df,
            x='Sector',
            y='Number of Job Postings',
            color_discrete_sequence=px.colors.qualitative.Antique,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.divider()

        
        filtered_avg_salary = round(state_df["avg_salary"].mean(), 2)
        filtered_min_salary = round(state_df["min_salary"].mean(), 2)
        filtered_max_salary = round(state_df["max_salary"].mean(), 2)

        st.subheader(
            "Overall Salary Metrics (in thousands of dollars)"
            if state_select == "All States"
            else "State Salary vs. Overall Salary (in thousands of dollars)",
            help='Metrics of the salary of all job postings' if state_select=='All States' else 'Comparison of filtered state\'s salary metrics with overall salary'
        )
        col1, col2, col3 = st.columns(3)
        col1.metric(
            "Average Salary",
            filtered_avg_salary,
            {0: None}.get(
                round(filtered_avg_salary - overall_avg_salary, 2),
                round(filtered_avg_salary - overall_avg_salary, 2),
            ),
        )
        col2.metric(
            "Average Starting Salary",
            filtered_min_salary,
            {0: None}.get(
                round(filtered_min_salary - overall_min_salary, 2),
                round(filtered_min_salary - overall_min_salary, 2),
            ),
        )
        col3.metric(
            "Average Maximum Salary",
            filtered_max_salary,
            {0: None}.get(
                round(filtered_max_salary - overall_max_salary, 2),
                round(filtered_max_salary - overall_max_salary, 2),
            ),
        )
        style_metric_cards(border_left_color="#4682A9", background_color="#212A3E")
        st.divider()

        col1, col2 = st.columns(2)
        skill_counts = {}
        skills = [
            "python",
            "excel",
            "hadoop",
            "spark",
            "aws",
            "tableau",
            "big_data",
        ]
        for skill in skills:
            try:
                skill_counts[skill.capitalize()] = state_df[skill].value_counts()[
                    skill
                ]
            except:
                skill_counts[skill.capitalize()] = 0
        skill_df = pd.DataFrame.from_dict(
            skill_counts, orient="index", columns=["Number of Job Postings"]
        )
        skill_df = skill_df.reset_index()
        skill_df.rename(columns={"index": "Skill"}, inplace=True)
        fig = px.pie(
            skill_df,
            values="Number of Job Postings",
            names="Skill",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Antique,
        )
        col1.subheader("Skill Distribution", help='Distribution of various skills used in the filtered state')
        col1.plotly_chart(fig, use_container_width=True)

        title_counts = {}
        titles = state_df["job_simp"].unique()
        for title in titles:
            if title == "Unspecified":
                continue
            else:
                title_counts[title.capitalize()] = state_df["job_simp"].value_counts()[
                    title
                ]

        titles_df = pd.DataFrame.from_dict(
            title_counts, orient="index", columns=["Number of Job Postings"]
        )
        titles_df = titles_df.reset_index()
        titles_df.rename(columns={"index": "Job Title"}, inplace=True)

        fig = px.pie(
            titles_df,
            values="Number of Job Postings",
            names="Job Title",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Antique,
        )
        col2.subheader("Job Title Distribution", help='Distribution of various job titles in the filtered sector')
        col2.plotly_chart(fig, use_container_width=True)
        st.divider()

        st.subheader(
            "Overall Job Rating Metrics (out of 5)"
            if state_select == "All States"
            else "State-wise job rating vs. Overall rating (out of 5)",
            help='Overall job rating metrics' if state_select=='All States' else 'Comparison of rating metrics of the filtered state with overall rating'
        )
        col1, col2, col3 = st.columns([1, 3, 1])
        filtered_rating = round(state_df["Rating"].mean(), 2)
        col2.metric(
            "Average Rating",
            overall_rating,
            {0: None}.get(
                round(filtered_rating - overall_rating, 2),
                round(filtered_rating - overall_rating, 2),
            ),
        )

    elif nav=='PygWalker Exploration':
        pyg_html = pyg.walk(df, return_html=True)
        components.html(pyg_html, height=1000, scrolling=True)


if __name__ == "__main__":
    main()
