import pandas as pd
df=pd.read_csv("metro.csv")
import folium
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.templates.default='plotly_white'
metro_data=df
metro_data.head()
metro_data.isnull().sum()
metro_data.dtypes
metro_data['Opening Date']=pd.to_datetime(metro_data['Opening Date'])
line_colors = {
    'Red line': 'red',
    'Blue line': 'blue',
    'Yellow line': 'beige',
    'Green line': 'green',
    'Voilet line': 'purple',
    'Pink line': 'pink',
    'Magenta line': 'darkred',
    'Orange line': 'orange',
    'Rapid Metro': 'cadetblue',
    'Aqua line': 'black',
    'Green line branch': 'lightgreen',
    'Blue line branch': 'lightblue',
    'Gray line': 'lightgray'
}

delhi_map_with_line_tooltip = folium.Map(location=[28.7041, 77.1025], zoom_start=11)
for index,row in metro_data.iterrows():
    line=row['Line']
    color = line_colors.get(line, 'black')
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['Station Name']}",
        tooltip=f"{row['Station Name']}, {line}",
        icon=folium.Icon(color=color)
    ).add_to(delhi_map_with_line_tooltip)

metro_data['Opening Year'] = metro_data['Opening Date'].dt.year
metro_data['Opening Year']
number_year=metro_data['Opening Year'].value_counts().sort_index()
df1=number_year.reset_index()
df1.columns = ['Year', 'Number of Stations']
fig = px.bar(df1, x='Year', y='Number of Stations',
             title="Number of Metro Stations Opened Each Year in Delhi",
             labels={'Year': 'Year', 'Number of Stations': 'Number of Stations Opened'})
fig.update_layout(xaxis_tickangle=-45, xaxis=dict(tickmode='linear'),
                  yaxis=dict(title='Number of Stations Opened'),
                  xaxis_title="Year")
fig.show()
y=metro_data.groupby('Line')['Distance from Start (km)'].max()
x=metro_data['Line'].value_counts()
y/(x-1)
line_analysis = pd.DataFrame({
    'Line': x.index,
    'Number of Stations': x.values,
    'Average Distance Between Stations (km)': y/(x-1)
})

line_analysis = line_analysis.sort_values(by='Number of Stations', ascending=False)

line_analysis.reset_index(drop=True, inplace=True)
print(line_analysis)
fig1 = make_subplots(rows=1, cols=2, subplot_titles=('Number of Stations Per Metro Line',
                                                    'Average Distance Between Stations Per Metro Line'),
                    horizontal_spacing=0.2)

fig1.add_trace(
    go.Bar(y=line_analysis['Line'], x=line_analysis['Number of Stations'],
           orientation='h', name='Number of Stations', marker_color='crimson'),
    row=1, col=1
)

fig1.add_trace(
    go.Bar(y=line_analysis['Line'], x=line_analysis['Average Distance Between Stations (km)'],
           orientation='h', name='Average Distance (km)', marker_color='navy'),
    row=1, col=2
)

fig1.update_layout(height=600, width=1200, title_text="Metro Line Analysis", template="plotly_white")

fig1.show()
layout_counts = metro_data['Station Layout'].value_counts()
fig2 = px.bar(x=layout_counts.index, y=layout_counts.values,
             labels={'x': 'Station Layout', 'y': 'Number of Stations'},
             title='Distribution of Delhi Metro Station Layouts',
             color=layout_counts.index,
             )
fig2.show()
