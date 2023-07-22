import plotly.express as px
import pandas as pd

# Create a sample dataframe with state codes and counts
df = pd.read_csv('test.csv', index_col=[0])

print(df.info())

# df = pd.DataFrame({
#     'State': ['NY', 'VA', 'MA', 'CA', 'IL', 'MO', 'WA', 'DC', 'TN', 'TX', 'PA', 'AZ', 'WI', 'GA', 'FL',
#               'US', 'NE', 'KS', 'NH', 'NJ', 'LA', 'OH', 'IN', 'MD', 'CO', 'UT', 'OR', 'MI', 'SC', 'MS',
#               'AL', 'RI', 'IA', 'MN', 'OK', 'CT', 'NC', 'DE', 'WV'],
#     'Number of Job Postings': [52, 89, 62, 165, 30, 12, 16, 26, 8, 17, 12, 4, 6, 9, 8, 11, 3, 1, 2, 10,
#                                1, 14, 5, 40, 10, 3, 2, 5, 2, 1, 4, 2, 3, 4, 6, 4, 9, 1, 1]
# })

# print('----------------------------')
print(df.info())



# Plot the choropleth map using state codes
fig = px.choropleth(df, locations='State', locationmode='USA-states',
                    color='Number of Job Postings', scope='usa',
                    color_continuous_scale='Blues',
                    title='USA States and Counts')

fig.show()