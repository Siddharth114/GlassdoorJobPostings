import pandas as pd
import numpy as np
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

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

sector_grouped_df = df.groupby('Sector')['Industry'].value_counts().sort_values(ascending=False)


app = Dash(__name__)

app.layout = html.Div([
    html.H1("Glass Door Job Postings", style={'text-align': 'center'}),

    dcc.Dropdown(id='slct_sector',
                 options = [
                     {'label':'Information Technology', 'value':'Information Technology'},
                     {'label':'Business Services', 'value':'Business Services'},
                     {'label':'Manufacturing', 'value':'Manufacturing'},
                     {'label':'Insurance', 'value':'Insurance'},
                     {'label':'Biotech & Pharmaceuticals', 'value':'Biotech & Pharmaceuticals'},
                     {'label':'Retail', 'value':'Retail'},
                     {'label':'Oil, Gas, Energy & Utilities', 'value':'Oil, Gas, Energy & Utilities'},
                     {'label':'Government', 'value':'Government'},
                     {'label':'Health Care', 'value':'Health Care'},
                     {'label':'Finance', 'value':'Finance'},
                     {'label':'Aerospace & Defense', 'value':'Aerospace & Defense'},
                     {'label':'Unorganized', 'value':'-1'},
                     {'label':'Transportation & Logistics', 'value':'Transportation & Logistics'},
                     {'label':'Media', 'value':'Media'},
                     {'label':'Telecommunications', 'value':'Telecommunications'},
                     {'label':'Real Estate', 'value':'Real Estate'},
                     {'label':'Travel & Tourism', 'value':'Travel & Tourism'},
                     {'label':'Agriculture & Forestry', 'value':'Agriculture & Forestry'},
                     {'label':'Education', 'value':'Education'},
                     {'label':'Accounting & Legal', 'value':'Accounting & Legal'},
                     {'label':'Non-Profit', 'value':'Non-Profit'},
                     {'label':'Construction, Repair & Maintenance', 'value':'Construction, Repair & Maintenance'},
                     {'label':'Consumer Services', 'value':'Consumer Services'},
                 ],
                 multi=False,
                 value='Insurance',
                 style = {'width':'40%'}
    ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})
])

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
     [Input(component_id='slct_sector', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The sector chosen by the user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Sector"] == option_slctd]
    fig = px.histogram(
        dff,
        x='Industry',
    )

    return container, fig

if __name__ == '__main__':
    app.run(debug=True)