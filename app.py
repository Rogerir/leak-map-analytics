from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

app = Dash(__name__)

df = pd.read_csv('data/vazamentos_brasil.csv')

URL_GEOJSON_BRASIL = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

fig_mapa = px.choropleth_map(
    df,
    geojson=URL_GEOJSON_BRASIL,
    locations="Estado",
    featureidkey="properties.name",
    color="Incidentes",
    color_continuous_scale="Reds",
    map_style="carto-darkmatter",
    center={"lat": -14.235, "lon": -51.925},
    zoom=3,
    opacity=0.7,
    labels={"Incidentes": "Nº de Vazamentos"},
    title="Distribuição Geográfica de Incidentes - Histórico Nacional"
)

fig_mapa.update_layout(
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    paper_bgcolor="#1e1e1e",
    plot_bgcolor="#1e1e1e",
    font_color="#f5f5f5"
)

app.layout = html.Div(
    style={'backgroundColor': '#111111', 'color': '#f5f5f5', 'padding': '20px', 'fontFamily': 'sans-serif'},
    children=[
        html.H1(
            children="leak-map-analytics",
            style={'textAlign': 'center', 'color': '#ff5555', 'margin': '0'}
        ),
        html.P(
            children="Painel de Monitoramento Estatístico e Vulnerabilidades em Tempo Real",
            style={'textAlign': 'center', 'color': '#888888', 'marginBottom': '30px'}
        ),

        html.Hr(style={'borderColor': '#333333'}),

        # Container do Mapa
        html.Div(
            style={'backgroundColor': '#1e1e1e', 'padding': '15px', 'borderRadius': '8px'},
            children=[
                dcc.Graph(
                    id='mapa-vazamentos-brasil',
                    figure=fig_mapa
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run(debug=True)