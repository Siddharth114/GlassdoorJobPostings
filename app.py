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

    if nav == "Filter by Sector":
        sector_select = st.sidebar.selectbox(
            "",
            (
                "All sectors",
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

        if sector_select == "All sectors":
            sectors_df = (
                df.groupby("Sector")["Industry"]
                .value_counts()
                .sort_values(ascending=False)
                .reset_index(name="Number of Job Postings")
            )
            sectors_df = sectors_df[["Sector", "Number of Job Postings"]]
            agg_functions = {"Number of Job Postings": "sum"}
            sectors_df = (
                sectors_df.groupby(sectors_df["Sector"])
                .aggregate(agg_functions)
                .reset_index()
            )
            st.subheader("Number of Job Postings by Industry")
            fig = px.bar(
                sectors_df,
                x="Sector",
                y="Number of Job Postings",
                color_discrete_sequence=px.colors.qualitative.Antique,
            )
            st.plotly_chart(fig, use_container_width=True)

            st.divider()

            st.subheader("Overall Salary Metrics (in thousands of dollars)")
            col1, col2, col3 = st.columns(3)
            col1.metric(
                "Average Salary",
                f"{overall_avg_salary}",
            )
            col2.metric(
                "Average Starting Salary",
                f"{overall_min_salary}",
            )
            col3.metric(
                "Average Maximum Salary",
                f"{overall_max_salary}",
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
                    skill_counts[skill.capitalize()] = df[skill].value_counts()[skill]
                except:
                    skill_counts[skill.capitalize()] = 0

            skills_df = pd.DataFrame.from_dict(
                skill_counts, orient="index", columns=["Number of Job Postings"]
            )
            skills_df = skills_df.reset_index()
            skills_df.rename(columns={"index": "Skill"}, inplace=True)

            fig = px.pie(
                skills_df,
                values="Number of Job Postings",
                names="Skill",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Antique,
            )
            col1.subheader("Skill Distribution")
            col1.plotly_chart(fig, use_container_width=True)
            title_counts = {}
            titles = df["job_simp"].unique()
            for title in titles:
                if title == "Unspecified":
                    continue
                title_counts[title.capitalize()] = df["job_simp"].value_counts()[title]

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
            col2.subheader("Job Title Distribution")
            col2.plotly_chart(fig, use_container_width=True)

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
                    state_counts[state.strip()] = df["job_state"].value_counts()[state]
                except KeyError:
                    state_counts[state.strip()] = 0
            states_df = pd.DataFrame.from_dict(
                state_counts, orient="index", columns=["Number of Job Postings"]
            )
            states_df = states_df.reset_index()
            states_df.rename(columns={"index": "State"}, inplace=True)
            st.divider()

            fig = px.choropleth(
                states_df,
                locations="State",
                locationmode="USA-states",
                color="Number of Job Postings",
                scope="usa",
                color_continuous_scale="mint",
            )
            st.subheader("State Heatmap")
            st.plotly_chart(fig, use_container_width=True)

        else:
            sector_filter_df = df[df["Sector"] == sector_select]["Industry"]
            sector_filter_df = sector_filter_df.reset_index()
            sector_filter_df.drop(columns=("index"), inplace=True)
            sector_filter_df = (
                sector_filter_df.groupby("Industry")
                .size()
                .reset_index(name="Number of Job Postings")
            )
            st.subheader("Number of Job Postings by Industry")
            fig = px.bar(
                sector_filter_df,
                x="Industry",
                y="Number of Job Postings",
                color_discrete_sequence=px.colors.qualitative.Antique,
            )
            st.plotly_chart(fig, use_container_width=True)
            st.divider()

            st.subheader("Sector Salary vs. Overall Salary (in thousands of dollars)")

            sector_filter_df_copy = df[df["Sector"] == sector_select]
            sector_avg_salary = round(
                sum(sector_filter_df_copy["avg_salary"])
                / len(sector_filter_df_copy["avg_salary"]),
                2,
            )
            sector_min_salary = round(
                sum(sector_filter_df_copy["min_salary"])
                / len(sector_filter_df_copy["min_salary"]),
                2,
            )
            sector_max_salary = round(
                sum(sector_filter_df_copy["max_salary"])
                / len(sector_filter_df_copy["max_salary"]),
                2,
            )

            col1, col2, col3 = st.columns(3)
            col1.metric(
                "Average Salary",
                f"{sector_avg_salary}",
                round(sector_avg_salary - overall_avg_salary, 2),
            )
            col2.metric(
                "Average Starting Salary",
                f"{sector_min_salary}",
                round(sector_min_salary - overall_min_salary, 2),
            )
            col3.metric(
                "Average Maximum Salary",
                f"{sector_max_salary}",
                round(sector_max_salary - overall_max_salary, 2),
            )

            style_metric_cards(border_left_color="#4682A9", background_color="#212A3E")

            col1, col2 = st.columns(2)

            sector_filter_df_copy = df[df["Sector"] == sector_select]
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
                    skill_counts[skill.capitalize()] = sector_filter_df_copy[
                        skill
                    ].value_counts()[skill]
                except:
                    skill_counts[skill.capitalize()] = 0

            sector_filter_skills_df = pd.DataFrame.from_dict(
                skill_counts, orient="index", columns=["Number of Job Postings"]
            )
            sector_filter_skills_df = sector_filter_skills_df.reset_index()
            sector_filter_skills_df.rename(columns={"index": "Skill"}, inplace=True)

            fig = px.pie(
                sector_filter_skills_df,
                values="Number of Job Postings",
                names="Skill",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Antique,
            )
            col1.subheader("Skill Distribution")
            col1.plotly_chart(fig, use_container_width=True)

            sector_filter_df_copy = df[df["Sector"] == sector_select]
            title_counts = {}
            titles = sector_filter_df_copy["job_simp"].unique()
            for title in titles:
                if title == "Unspecified":
                    continue
                title_counts[title.capitalize()] = sector_filter_df_copy[
                    "job_simp"
                ].value_counts()[title]

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
            col2.subheader("Job Title Distribution")
            col2.plotly_chart(fig, use_container_width=True)

            sector_filter_df_copy = df[df["Sector"] == sector_select]
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
                    state_counts[state.strip()] = sector_filter_df_copy[
                        "job_state"
                    ].value_counts()[state]
                except KeyError:
                    state_counts[state.strip()] = 0
            states_df = pd.DataFrame.from_dict(
                state_counts, orient="index", columns=["Number of Job Postings"]
            )
            states_df = states_df.reset_index()
            states_df.rename(columns={"index": "State"}, inplace=True)

            st.divider()
            fig = px.choropleth(
                states_df,
                locations="State",
                locationmode="USA-states",
                color="Number of Job Postings",
                scope="usa",
                color_continuous_scale="mint",
            )
            st.subheader("State Heatmap")
            st.plotly_chart(fig, use_container_width=True)

    elif nav == "PygWalker Exploration":
        pyg_html = pyg.walk(df, return_html=True)
        components.html(pyg_html, height=1000, scrolling=True)

    else:
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

        if state_select != "All States":
            state_df = df[df["job_state"] == state_codes[state_select]]
        else:
            state_df = df

        sectors_df = (
            state_df.groupby("Sector")["Industry"]
            .value_counts()
            .sort_values(ascending=False)
            .reset_index(name="Number of Job Postings")
        )
        sectors_df = sectors_df[["Sector", "Number of Job Postings"]]
        agg_functions = {"Number of Job Postings": "sum"}
        sectors_df = (
            sectors_df.groupby(sectors_df["Sector"])
            .aggregate(agg_functions)
            .reset_index()
        )
        st.subheader("Number of Job Postings by Sector")
        fig = px.bar(
            sectors_df,
            x="Sector",
            y="Number of Job Postings",
            color_discrete_sequence=px.colors.qualitative.Antique,
        )
        st.plotly_chart(fig, use_container_width=True)
        st.divider()

        if state_select=='All States':
            st.subheader("Overall Salary Metrics (in thousands of dollars)")
            col1, col2, col3 = st.columns(3)
            col1.metric(
                "Average Salary",
                f"{overall_avg_salary}",
            )
            col2.metric(
                "Average Starting Salary",
                f"{overall_min_salary}",
            )
            col3.metric(
                "Average Maximum Salary",
                f"{overall_max_salary}",
            )

            style_metric_cards(border_left_color="#4682A9", background_color="#212A3E")
            st.divider()
        else:
            st.subheader('Salary for Chosen State vs. Overall Salary Metrics (in thousands of dollars)')
            col1, col2, col3 = st.columns(3)
            state_avg_salary = round(
                sum(state_df['avg_salary'])/len(state_df['avg_salary']), 2
            )
            state_min_salary = round(
                sum(state_df['min_salary'])/len(state_df['min_salary']), 2
            )
            state_max_salary = round(
                sum(state_df['max_salary'])/len(state_df['max_salary']), 2
            )
            col1.metric(
                "Average Salary",
                f"{state_avg_salary}",
                round(state_avg_salary - overall_avg_salary, 2),
            )
            col2.metric(
                "Average Starting Salary",
                f"{state_min_salary}",
                round(state_min_salary - overall_min_salary, 2),
            )
            col3.metric(
                "Average Maximum Salary",
                f"{state_max_salary}",
                round(state_max_salary - overall_max_salary, 2),
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
                skill_counts[skill.capitalize()] = state_df[
                    skill
                ].value_counts()[skill]
            except:
                skill_counts[skill.capitalize()] = 0
        
        state_skills_df = pd.DataFrame.from_dict(
            skill_counts, orient="index", columns=["Number of Job Postings"]
        )
        state_skills_df = state_skills_df.reset_index()
        state_skills_df.rename(columns={'index':'Skill'}, inplace=True)
        fig = px.pie(
            state_skills_df,
            values="Number of Job Postings",
            names="Skill",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Antique,
        )
        col1.subheader("Skill Distribution")
        col1.plotly_chart(fig, use_container_width=True)

        title_counts = {}
        titles = state_df["job_simp"].unique()
        for title in titles:
            if title == "Unspecified":
                continue
            title_counts[title.capitalize()] = state_df[
                "job_simp"
            ].value_counts()[title]

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
        col2.subheader("Job Title Distribution")
        col2.plotly_chart(fig, use_container_width=True)




        

        












if __name__ == "__main__":
    main()
