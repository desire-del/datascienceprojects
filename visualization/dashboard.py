import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

# Load the data

df = pd.read_csv('Historical_Wildfires.csv')
df["Year"] = pd.to_datetime(df["Date"]).dt.year
df["Month"] = pd.to_datetime(df["Date"]).dt.month_name()

regions = {
    "WA": "Western Australia",
    "QL": "Queensland",
    "NT": "Northern Territory",
    "NSW": "New South Wales",
    "VI": "Victoria",
    "SA": "South Australia",
    "TA": "Tasmania"
}

# Create the app
app = dash.Dash(__name__)

# Define the layout

app.layout = html.Div(
    children=[
        html.H1(children="Australia Historical Wildfires",
                style={
                    'textAlign': 'center',
                    'color': '#503D36',
                    'font-size': 40
                    }),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H2("Select Region"),
                        dcc.RadioItems(
                            id="region",
                            options=[
                                {"label": region, "value": code}
                                for code, region in regions.items()
                            ],
                            value="WA",
                            inline=True,
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.H2("Select Year"),
                        dcc.Dropdown(
                            id="year",
                            options=[
                                {"label": str(year), "value": year}
                                for year in df["Year"].unique()
                            ],
                            value=df["Year"].min(),
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div([], id="plot1"),
                        html.Div([], id="plot2"),
                    ],
                    style={"display": "flex"},
                ),
            ]
        ),
    ]
)

# Define the callback
@app.callback(
    [
        Output(component_id="plot1", component_property="children"),
        Output(component_id="plot2", component_property="children"),
    ],
    [
        Input(component_id="year", component_property="value"),
        Input(component_id="region", component_property="value"),
    ],
)
def update_graph(year, region):
    region_df = df[df['Region'] == region]
    year_df = region_df[region_df['Year'] == year]
    est_fire_area = year_df.groupby("Month")["Estimated_fire_area"].mean().reset_index()
    fig1 = px.pie(
        est_fire_area,
        names="Month",
        values="Estimated_fire_area",
        title=f"Wildfires in {regions[region]} in {year}",
    )
    veg_data = year_df.groupby("Month")["Count"].sum().reset_index()
    fig2 = px.bar(
        veg_data,
        x="Month",
        y="Count",
        title=f"Vegetation fires in {regions[region]} in {year}",
    )
    
    return [
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2),
    ]

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)