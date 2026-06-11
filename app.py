from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

app = Dash(__name__)

# Carregando os dados gerados pelo novo script
df_historico = pd.read_csv('data/vazamentos_brasil.csv')

URL_GEOJSON_BRASIL = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

app.layout = html.Div(
    style={
        'backgroundColor': '#111111',
        'color': '#f5f5f5',
        'padding': '20px 40px',
        'fontFamily': 'sans-serif',
        'maxWidth': '1400px',
        'margin': '0 auto'
    },
    children=[
        html.Div(
            style={'textAlign': 'center', 'marginBottom': '20px'},
            children=[
                html.H1(
                    children="leak-map-analytics",
                    style={'color': '#ff5555', 'margin': '0 0 5px 0', 'fontSize': '32px', 'letterSpacing': '1px'}
                ),
                html.P(
                    children="Análise Temporal e Impacto da LGPD no Cenário de Segurança Nacional",
                    style={'color': '#888888', 'margin': '0', 'fontSize': '14px'}
                ),
            ]
        ),

        html.Hr(style={'borderColor': '#222222', 'marginBottom': '25px'}),

        html.Div(
            style={'display': 'grid', 'gridTemplateColumns': '1fr 3fr', 'gap': '20px'},
            children=[
                # Coluna Esquerda: Controles
                html.Div(
                    style={
                        'backgroundColor': '#1e1e1e',
                        'padding': '20px',
                        'borderRadius': '8px',
                        'display': 'flex',
                        'flexDirection': 'column',
                        'border': '1px solid #2a2a2a'
                    },
                    children=[
                        html.H4("LINHA DO TEMPO",
                                style={'color': '#ff5555', 'margin': '0 0 10px 0', 'letterSpacing': '1px'}),
                        html.P("Selecione o ano de análise histórica:",
                               style={'color': '#aaaaaa', 'fontSize': '13px', 'marginBottom': '30px'}),

                        html.Div(
                            style={'padding': '0 10px'},
                            children=[
                                dcc.Slider(
                                    id='slider-anos',
                                    min=df_historico['Ano'].min(),
                                    max=df_historico['Ano'].max(),
                                    value=df_historico['Ano'].min(),
                                    marks={
                                        str(ano): {'label': str(ano), 'style': {'color': '#888888', 'fontSize': '11px'}}
                                        for ano in df_historico['Ano'].unique()},
                                    step=1,
                                    included=False
                                ),
                            ]
                        ),

                        html.Hr(style={'borderColor': '#2a2a2a', 'margin': '30px 0 20px 0'}),

                        html.H4("CONTEXTO LEGAL",
                                style={'color': '#ff5555', 'margin': '0 0 10px 0', 'letterSpacing': '1px'}),
                        html.Div(
                            id='status-lgpd',
                            style={'fontSize': '13px', 'lineHeight': '1.6', 'textAlign': 'left'}
                        )
                    ]
                ),

                # Coluna Direita: Visualizações
                html.Div(
                    style={'display': 'flex', 'flexDirection': 'column', 'gap': '20px'},
                    children=[
                        # Visão 1: Mapa (Ocupando a largura total da coluna direita)
                        html.Div(
                            style={
                                'backgroundColor': '#1e1e1e',
                                'padding': '10px',
                                'borderRadius': '8px',
                                'border': '1px solid #2a2a2a',
                                'height': '450px'
                            },
                            children=[
                                dcc.Graph(
                                    id='mapa-vazamentos-temporal',
                                    style={'height': '100%', 'width': '100%'}
                                )
                            ]
                        ),

                        # Container inferior dividido em 2 para as Visões 2 e 3
                        html.Div(
                            style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px'},
                            children=[
                                # Visão 2: Top 5 Estados
                                html.Div(
                                    style={
                                        'backgroundColor': '#1e1e1e',
                                        'padding': '15px',
                                        'borderRadius': '8px',
                                        'border': '1px solid #2a2a2a',
                                        'height': '300px'
                                    },
                                    children=[
                                        dcc.Graph(
                                            id='grafico-top5-estados',
                                            style={'height': '100%', 'width': '100%'}
                                        )
                                    ]
                                ),
                                # Visão 3: Evolução Temporal Nacional
                                html.Div(
                                    style={
                                        'backgroundColor': '#1e1e1e',
                                        'padding': '15px',
                                        'borderRadius': '8px',
                                        'border': '1px solid #2a2a2a',
                                        'height': '300px'
                                    },
                                    children=[
                                        dcc.Graph(
                                            id='grafico-evolucao-nacional',
                                            style={'height': '100%', 'width': '100%'}
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


@app.callback(
    [Output('mapa-vazamentos-temporal', 'figure'),
     Output('grafico-top5-estados', 'figure'),
     Output('grafico-evolucao-nacional', 'figure'),
     Output('status-lgpd', 'children'),
     Output('status-lgpd', 'style')],
    [Input('slider-anos', 'value')]
)
def atualizar_painel(ano_selecionado):
    # Filtro para Mapa e Top 5
    df_filtrado = df_historico[df_historico['Ano'] == ano_selecionado]

    # Preparando dados para Top 5
    df_top5 = df_filtrado.nlargest(5, 'Incidentes').sort_values('Incidentes', ascending=True)

    # Preparando dados para a Evolução (agrupando todos os anos)
    df_evolucao = df_historico.groupby('Ano', as_index=False)['Incidentes'].sum()

    # Textos Dinâmicos da LGPD
    if ano_selecionado < 2020:
        texto_lgpd = f"Ano {ano_selecionado}: Cenário Pré-LGPD. Ausência de uma legislação nacional centralizada de proteção e fiscalização, resultando em menor controle corporativo de dados expostos."
        cor_status = {'color': '#ffaa00', 'fontWeight': '500'}
    elif ano_selecionado in [2020, 2021]:
        texto_lgpd = f"Ano {ano_selecionado}: Vigência da LGPD. Em vigor no Brasil, há uma explosão nas notificações e relatórios de incidentes, pois as empresas passam a ser juridicamente obrigadas a reportar vazamentos à ANPD."
        cor_status = {'color': '#ff5555', 'fontWeight': '500'}
    else:
        texto_lgpd = f"Ano {ano_selecionado}: Cenário Pós-LGPD. Fase de maturação legal, adequação maciça dos sistemas empresariais às políticas de governança e estabilização de incidentes severos."
        cor_status = {'color': '#00ff77', 'fontWeight': '500'}

    # 1. Figura do Mapa
    max_incidentes = df_historico['Incidentes'].max()
    fig_mapa = px.choropleth_map(
        df_filtrado,
        geojson=URL_GEOJSON_BRASIL,
        locations="Estado",
        featureidkey="properties.name",
        color="Incidentes",
        color_continuous_scale="Reds",
        range_color=[0, max_incidentes],
        map_style="carto-darkmatter",
        center={"lat": -14.235, "lon": -53.925},
        zoom=3.1,
        opacity=0.75,
        labels={"Incidentes": "Vazamentos"},
        title=f"Distribuição Geográfica - Ano {ano_selecionado}"
    )
    fig_mapa.update_layout(
        margin={"r": 10, "t": 40, "l": 10, "b": 10},
        paper_bgcolor="#1e1e1e", plot_bgcolor="#1e1e1e", font_color="#f5f5f5"
    )

    # 2. Figura do Gráfico de Barras (Top 5)
    fig_barras = px.bar(
        df_top5,
        x="Incidentes",
        y="Estado",
        orientation="h",
        color="Incidentes",
        color_continuous_scale="Reds",
        range_color=[0, max_incidentes],
        title=f"Top 5 Estados - Ano {ano_selecionado}"
    )
    fig_barras.update_layout(
        margin={"r": 20, "t": 40, "l": 10, "b": 20},
        paper_bgcolor="#1e1e1e", plot_bgcolor="#1e1e1e", font_color="#f5f5f5",
        showlegend=False, coloraxis_showscale=False,
        xaxis_title="Incidentes Notificados", yaxis_title=""
    )

    # 3. Figura do Gráfico de Linha (Evolução)
    fig_linha = px.line(
        df_evolucao,
        x="Ano",
        y="Incidentes",
        markers=True,
        title="Evolução Nacional (Total de Vazamentos)"
    )
    fig_linha.update_traces(line_color='#ff5555', marker=dict(size=8, color='#ffaa00'))

    # Destacando o ano selecionado no gráfico de linha
    fig_linha.add_vline(x=ano_selecionado, line_width=2, line_dash="dash", line_color="#00ff77")

    fig_linha.update_layout(
        margin={"r": 20, "t": 40, "l": 10, "b": 20},
        paper_bgcolor="#1e1e1e", plot_bgcolor="#1e1e1e", font_color="#f5f5f5",
        xaxis_title="", yaxis_title="Total Incidentes"
    )

    return fig_mapa, fig_barras, fig_linha, texto_lgpd, cor_status


if __name__ == '__main__':
    app.run(debug=True)