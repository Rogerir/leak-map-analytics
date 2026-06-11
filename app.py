from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

app = Dash(__name__)

df_historico = pd.read_csv('data/vazamentos_brasil.csv')
URL_GEOJSON_BRASIL = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

app.layout = html.Div(
    id='main-container',
    style={'padding': '20px 40px', 'fontFamily': 'Arial, sans-serif', 'minHeight': '100vh', 'transition': '0.3s'},
    children=[
        # Cabeçalho com Botão de Tema
        html.Div(
            style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center',
                   'marginBottom': '20px'},
            children=[
                html.Div(
                    children=[
                        html.H1("Painel Analítico de Incidentes LGPD",
                                style={'margin': '0 0 8px 0', 'fontSize': '28px'}),
                        html.P("Análise Histórica de Vazamentos de Dados no Cenário Nacional (2018-2023)",
                               style={'margin': '0', 'fontSize': '15px', 'color': '#888888'}),
                    ]
                ),
                html.Button(
                    id='theme-toggle',
                    n_clicks=0,
                    style={
                        'padding': '10px 20px', 'borderRadius': '20px', 'border': 'none',
                        'cursor': 'pointer', 'fontWeight': 'bold', 'transition': '0.3s'
                    }
                )
            ]
        ),

        html.Hr(
            style={'borderColor': '#888888', 'marginBottom': '25px', 'borderStyle': 'solid', 'borderWidth': '1px 0 0 0',
                   'opacity': '0.2'}),

        html.Div(
            style={'display': 'grid', 'gridTemplateColumns': '1fr 3fr', 'gap': '20px'},
            children=[
                # Coluna Esquerda: Controles
                html.Div(
                    id='panel-left',
                    style={'padding': '25px', 'borderRadius': '6px', 'display': 'flex', 'flexDirection': 'column',
                           'transition': '0.3s'},
                    children=[
                        html.H4("FILTRO TEMPORAL", style={'margin': '0 0 10px 0', 'fontSize': '14px'}),
                        html.P("Selecione o ano base para atualizar as visualizações ao lado:",
                               style={'fontSize': '13px', 'marginBottom': '40px', 'color': '#888888'}),

                        html.Div(
                            style={'padding': '0 5px'},
                            children=[
                                dcc.Slider(
                                    id='slider-anos',
                                    min=df_historico['Ano'].min(),
                                    max=df_historico['Ano'].max(),
                                    value=df_historico['Ano'].min(),
                                    marks={
                                        str(ano): {'label': str(ano), 'style': {'color': '#888888', 'fontSize': '12px'}}
                                        for ano in df_historico['Ano'].unique()},
                                    step=1,
                                    included=False
                                ),
                            ]
                        ),

                        html.Hr(style={'borderColor': '#888888', 'margin': '40px 0 20px 0', 'borderStyle': 'solid',
                                       'opacity': '0.2'}),

                        html.H4("CONTEXTO REGULATÓRIO", style={'margin': '0 0 15px 0', 'fontSize': '14px'}),
                        html.Div(id='status-lgpd')
                    ]
                ),

                # Coluna Direita: Visualizações
                html.Div(
                    style={'display': 'flex', 'flexDirection': 'column', 'gap': '20px'},
                    children=[
                        html.Div(
                            id='panel-map',
                            style={'padding': '15px', 'borderRadius': '6px', 'height': '450px', 'transition': '0.3s'},
                            children=[
                                dcc.Graph(id='mapa-vazamentos-temporal', style={'height': '100%', 'width': '100%'},
                                          config={'displayModeBar': False})]
                        ),
                        html.Div(
                            style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px'},
                            children=[
                                html.Div(
                                    id='panel-top5',
                                    style={'padding': '15px', 'borderRadius': '6px', 'height': '320px',
                                           'transition': '0.3s'},
                                    children=[
                                        dcc.Graph(id='grafico-top5-estados', style={'height': '100%', 'width': '100%'},
                                                  config={'displayModeBar': False})]
                                ),
                                html.Div(
                                    id='panel-evolucao',
                                    style={'padding': '15px', 'borderRadius': '6px', 'height': '320px',
                                           'transition': '0.3s'},
                                    children=[dcc.Graph(id='grafico-evolucao-nacional',
                                                        style={'height': '100%', 'width': '100%'},
                                                        config={'displayModeBar': False})]
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
     Output('status-lgpd', 'style'),
     Output('main-container', 'style'),
     Output('panel-left', 'style'),
     Output('panel-map', 'style'),
     Output('panel-top5', 'style'),
     Output('panel-evolucao', 'style'),
     Output('theme-toggle', 'children'),
     Output('theme-toggle', 'style')],
    [Input('slider-anos', 'value'),
     Input('theme-toggle', 'n_clicks')]
)
def atualizar_painel(ano_selecionado, theme_clicks):
    # Lógica de Tema
    is_dark = theme_clicks % 2 != 0

    if is_dark:
        tema = {
            'bg_page': '#14181c', 'bg_panel': '#1e2329', 'border': '#2d333b',
            'text': '#c9d1d9', 'accent': '#58a6ff', 'map': 'carto-darkmatter'
        }
        btn_text = '☀️ Light Mode'
        btn_style = {'backgroundColor': '#2d333b', 'color': '#c9d1d9'}
    else:
        tema = {
            'bg_page': '#f4f6f9', 'bg_panel': '#ffffff', 'border': '#e0e0e0',
            'text': '#2c3e50', 'accent': '#0056b3', 'map': 'carto-positron'
        }
        btn_text = '🌙 Dark Mode'
        btn_style = {'backgroundColor': '#e0e0e0', 'color': '#2c3e50'}

    # Estilos Baseados no Tema
    estilo_page = {'backgroundColor': tema['bg_page'], 'color': tema['text'], 'padding': '20px 40px',
                   'fontFamily': 'Arial, sans-serif', 'minHeight': '100vh', 'transition': '0.3s'}
    estilo_panel = {'backgroundColor': tema['bg_panel'], 'padding': '20px', 'borderRadius': '6px',
                    'border': f'1px solid {tema["border"]}', 'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
                    'transition': '0.3s'}

    btn_style.update(
        {'padding': '10px 20px', 'borderRadius': '20px', 'border': f'1px solid {tema["border"]}', 'cursor': 'pointer',
         'fontWeight': 'bold', 'transition': '0.3s'})

    # Dados
    df_filtrado = df_historico[df_historico['Ano'] == ano_selecionado]
    df_top5 = df_filtrado.nlargest(5, 'Incidentes').sort_values('Incidentes', ascending=True)
    df_evolucao = df_historico.groupby('Ano', as_index=False)['Incidentes'].sum()

    # LGPD Status
    estilo_lgpd = {'fontSize': '13.5px', 'lineHeight': '1.6', 'padding': '15px', 'backgroundColor': tema['bg_page'],
                   'borderRadius': '4px', 'color': tema['text']}
    if ano_selecionado < 2020:
        texto_lgpd = f"Ano {ano_selecionado}: Cenário Pré-LGPD. Ausência de uma legislação nacional centralizada de proteção e fiscalização."
        estilo_lgpd['borderLeft'] = '4px solid #d35400'
    elif ano_selecionado in [2020, 2021]:
        texto_lgpd = f"Ano {ano_selecionado}: Vigência da LGPD. Em vigor no Brasil, há um salto nas notificações, pois as empresas passam a ser juridicamente obrigadas a reportar vazamentos à ANPD."
        estilo_lgpd['borderLeft'] = '4px solid #c0392b'
    else:
        texto_lgpd = f"Ano {ano_selecionado}: Cenário Pós-LGPD. Fase de maturação legal, adequação dos sistemas empresariais às políticas de governança."
        estilo_lgpd['borderLeft'] = '4px solid #27ae60'

    # Figuras
    max_incidentes = df_historico['Incidentes'].max()

    fig_mapa = px.choropleth_map(
        df_filtrado, geojson=URL_GEOJSON_BRASIL, locations="Estado", featureidkey="properties.name",
        color="Incidentes", color_continuous_scale="Blues", range_color=[0, max_incidentes],
        map_style=tema['map'], center={"lat": -14.235, "lon": -53.925}, zoom=3.1, opacity=0.85,
        title=f"Distribuição Geográfica - {ano_selecionado}"
    )
    fig_mapa.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0}, paper_bgcolor=tema['bg_panel'],
                           plot_bgcolor=tema['bg_panel'], font_color=tema['text'])

    fig_barras = px.bar(
        df_top5, x="Incidentes", y="Estado", orientation="h", color="Incidentes",
        color_continuous_scale="Blues", range_color=[0, max_incidentes], title=f"Top 5 Estados - {ano_selecionado}"
    )
    fig_barras.update_layout(margin={"r": 10, "t": 40, "l": 10, "b": 20}, paper_bgcolor=tema['bg_panel'],
                             plot_bgcolor=tema['bg_panel'], font_color=tema['text'], showlegend=False,
                             coloraxis_showscale=False, xaxis_title="Notificações", yaxis_title="")
    fig_barras.update_xaxes(showgrid=True, gridwidth=1, gridcolor=tema['border'])

    fig_linha = px.line(df_evolucao, x="Ano", y="Incidentes", markers=True, title="Evolução Nacional")
    fig_linha.update_traces(line_color=tema['accent'], marker=dict(size=8, color=tema['accent']))
    fig_linha.add_vline(x=ano_selecionado, line_width=2, line_dash="dash", line_color="#e74c3c")
    fig_linha.update_layout(margin={"r": 10, "t": 40, "l": 10, "b": 20}, paper_bgcolor=tema['bg_panel'],
                            plot_bgcolor=tema['bg_panel'], font_color=tema['text'], xaxis_title="",
                            yaxis_title="Total Incidentes")
    fig_linha.update_yaxes(showgrid=True, gridwidth=1, gridcolor=tema['border'])

    return fig_mapa, fig_barras, fig_linha, texto_lgpd, estilo_lgpd, estilo_page, estilo_panel, estilo_panel, estilo_panel, estilo_panel, btn_text, btn_style


if __name__ == '__main__':
    app.run(debug=True)