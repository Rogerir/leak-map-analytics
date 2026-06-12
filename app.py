from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import requests

app = Dash(__name__)

# 1. Carregamento de Dados
df_jobs = pd.read_csv('data/AI_Impact_on_Jobs_2030.csv')

# Conversões para facilitar o entendimento (0 a 1 vira 0 a 100%)
df_jobs['Risco_IA_Porcentagem'] = df_jobs['AI_Replacement_Risk'] * 100
df_jobs['Demanda_Porcentagem'] = df_jobs['Future_Demand_Score'] * 100

# Simplificando a classificação da IA
mapa_vulnerabilidade = {'Low': 'Baixo Risco', 'Medium': 'Risco Médio', 'High': 'Alto Risco'}
df_jobs['Impacto_da_IA'] = df_jobs['Automation_Level'].map(mapa_vulnerabilidade)


# 2. Integração com API Externa (Cotação Dólar)
def obter_cotacao_usd():
    try:
        response = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL", timeout=5)
        return float(response.json()['USDBRL']['bid'])
    except:
        return 5.00  # Fallback


usd_hoje = obter_cotacao_usd()

# Estrutura de Layout Direta
app.layout = html.Div(
    id='main-container',
    style={'padding': '30px 40px', 'fontFamily': 'system-ui, sans-serif', 'minHeight': '100vh',
           'transition': 'all 0.3s'},
    children=[
        # Cabeçalho
        html.Div(
            style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center',
                   'marginBottom': '30px'},
            children=[
                html.Div([
                    html.H1("O Futuro dos Empregos com a IA",
                            style={'margin': '0 0 6px 0', 'fontSize': '30px', 'fontWeight': '700'}),
                    html.P("Quais profissões sobrevivem, quanto pagam e o que precisamos aprender até 2030.",
                           style={'margin': '0', 'fontSize': '15px', 'color': '#64748b'}),
                ]),
                html.Button(
                    id='theme-toggle', n_clicks=0,
                    style={'padding': '10px 20px', 'borderRadius': '8px', 'border': '1px solid', 'cursor': 'pointer',
                           'fontWeight': '600'}
                )
            ]
        ),

        # Linha de Resumo (Cards)
        html.Div(
            style={'display': 'flex', 'gap': '24px', 'marginBottom': '30px', 'flexWrap': 'wrap'},
            children=[
                html.Div(id='card-total',
                         style={'flex': '1', 'minWidth': '250px', 'padding': '24px', 'borderRadius': '12px'}),
                html.Div(id='card-risk',
                         style={'flex': '1', 'minWidth': '250px', 'padding': '24px', 'borderRadius': '12px'}),
                html.Div(id='card-usd',
                         style={'flex': '1', 'minWidth': '250px', 'padding': '24px', 'borderRadius': '12px'})
            ]
        ),

        # Corpo do Painel
        html.Div(
            style={'display': 'grid', 'gridTemplateColumns': '1fr 3fr', 'gap': '24px'},
            children=[
                # Filtros Esquerdo
                html.Div(
                    id='panel-left',
                    style={'padding': '24px', 'borderRadius': '12px', 'display': 'flex', 'flexDirection': 'column'},
                    children=[
                        html.H4("ESCOLHA A ÁREA DE ATUAÇÃO",
                                style={'margin': '0 0 12px 0', 'fontSize': '13px', 'fontWeight': '700'}),
                        html.P("Veja como a IA afeta este setor específico:",
                               style={'fontSize': '13px', 'marginBottom': '15px'}),

                        html.Div(
                            style={'marginBottom': '30px'},
                            children=[
                                dcc.Dropdown(
                                    id='drop-industry',
                                    options=[{'label': ind, 'value': ind} for ind in
                                             sorted(df_jobs['Industry'].unique())],
                                    value=sorted(df_jobs['Industry'].unique())[0],
                                    clearable=False,
                                    style={'color': '#0f172a'}
                                ),
                            ]
                        ),

                        html.Hr(
                            style={'margin': '20px 0', 'border': 'none', 'borderTop': '1px solid', 'opacity': '0.1'}),

                        html.H4("ALERTA DE ESTUDOS",
                                style={'margin': '0 0 12px 0', 'fontSize': '13px', 'fontWeight': '700'}),
                        html.Div(id='status-upskill')
                    ]
                ),

                # Gráficos (Direita)
                html.Div(
                    style={'display': 'flex', 'flexDirection': 'column', 'gap': '24px'},
                    children=[
                        html.Div(
                            id='panel-matriz',
                            style={'padding': '20px', 'borderRadius': '12px', 'height': '400px'},
                            children=[dcc.Graph(id='grafico-matriz', style={'height': '100%', 'width': '100%'},
                                                config={'displayModeBar': False})]
                        ),
                        html.Div(
                            style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '24px'},
                            children=[
                                html.Div(
                                    id='panel-top-jobs',
                                    style={'padding': '20px', 'borderRadius': '12px', 'height': '360px'},
                                    children=[
                                        dcc.Graph(id='grafico-top-jobs', style={'height': '100%', 'width': '100%'},
                                                  config={'displayModeBar': False})]
                                ),
                                html.Div(
                                    id='panel-skills',
                                    style={'padding': '20px', 'borderRadius': '12px', 'height': '360px'},
                                    children=[dcc.Graph(id='grafico-skills', style={'height': '100%', 'width': '100%'},
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
    [Output('grafico-matriz', 'figure'),
     Output('grafico-top-jobs', 'figure'),
     Output('grafico-skills', 'figure'),
     Output('status-upskill', 'children'),
     Output('status-upskill', 'style'),
     Output('card-total', 'children'),
     Output('card-total', 'style'),
     Output('card-risk', 'children'),
     Output('card-risk', 'style'),
     Output('card-usd', 'children'),
     Output('card-usd', 'style'),
     Output('main-container', 'style'),
     Output('panel-left', 'style'),
     Output('panel-matriz', 'style'),
     Output('panel-top-jobs', 'style'),
     Output('panel-skills', 'style'),
     Output('theme-toggle', 'children'),
     Output('theme-toggle', 'style')],
    [Input('drop-industry', 'value'),
     Input('theme-toggle', 'n_clicks')]
)
def atualizar_painel(industry_selecionada, theme_clicks):
    is_dark = theme_clicks % 2 != 0

    # Cores
    if is_dark:
        tema = {'bg_page': '#0f172a', 'bg_panel': '#1e293b', 'border': '#334155', 'text': '#f8fafc',
                'text_muted': '#94a3b8', 'accent': '#8b5cf6', 'card_bg': '#1e293b'}
        btn_text = '☀️ Modo Claro'
        btn_style = {'backgroundColor': '#334155', 'color': '#f8fafc', 'borderColor': '#475569'}
    else:
        tema = {'bg_page': '#f1f5f9', 'bg_panel': '#ffffff', 'border': '#e2e8f0', 'text': '#0f172a',
                'text_muted': '#64748b', 'accent': '#6366f1', 'card_bg': '#ffffff'}
        btn_text = '🌙 Modo Escuro'
        btn_style = {'backgroundColor': '#ffffff', 'color': '#0f172a', 'borderColor': '#cbd5e1'}

    estilos_base = {'backgroundColor': tema['bg_page'], 'color': tema['text']}
    estilo_panel = {'backgroundColor': tema['bg_panel'], 'border': f'1px solid {tema["border"]}'}
    btn_style.update({'padding': '10px 20px', 'borderRadius': '8px'})

    # Dados Filtrados Gerais
    df_filtrado = df_jobs[df_jobs['Industry'] == industry_selecionada]

    # Agrupamento da Matriz (Uma bolinha = Um Cargo)
    df_matriz = df_filtrado.groupby('Job_Title').agg({
        'Risco_IA_Porcentagem': 'mean',
        'Job_Growth_2030': 'mean',
        'Average_Salary_USD': 'mean'
    }).reset_index()

    # Convertendo Salários da Matriz para Reais em tempo real para exibir nas bolinhas
    df_matriz['Salario_Reais'] = df_matriz['Average_Salary_USD'] * usd_hoje

    def classificar_risco(risco):
        if risco <= 33:
            return 'Baixo Risco'
        elif risco <= 66:
            return 'Risco Médio'
        else:
            return 'Alto Risco'

    df_matriz['Impacto_da_IA'] = df_matriz['Risco_IA_Porcentagem'].apply(classificar_risco)

    # Métricas Gerais para os Cartões
    total_profissoes = df_matriz['Job_Title'].nunique()
    media_risco = df_matriz['Risco_IA_Porcentagem'].mean()
    media_setor_brl = df_matriz['Average_Salary_USD'].mean() * usd_hoje

    # Cartões Atualizados
    card_total_content = [
        html.P("PROFISSÕES ANALISADAS",
               style={'margin': '0 0 8px 0', 'fontSize': '12px', 'fontWeight': '600', 'color': tema['text_muted']}),
        html.H2(f"{total_profissoes} cargos", style={'margin': '0', 'fontSize': '28px', 'color': tema['text']})
    ]
    card_total_style = {**estilo_panel, 'flex': '1', 'padding': '24px', 'borderRadius': '12px',
                        'borderLeft': f'4px solid {tema["accent"]}'}

    card_risk_content = [
        html.P("RISCO MÉDIO DO SETOR",
               style={'margin': '0 0 8px 0', 'fontSize': '12px', 'fontWeight': '600', 'color': tema['text_muted']}),
        html.H2(f"{media_risco:.0f}%",
                style={'margin': '0', 'fontSize': '28px', 'color': '#ef4444' if media_risco > 50 else '#f59e0b'})
    ]
    card_risk_style = {**estilo_panel, 'flex': '1', 'padding': '24px', 'borderRadius': '12px',
                       'borderLeft': '4px solid #ef4444'}

    card_usd_content = [
        html.P("MÉDIA SALARIAL (Em Reais)",
               style={'margin': '0 0 8px 0', 'fontSize': '12px', 'fontWeight': '600', 'color': tema['text_muted']}),
        html.H2(f"R$ {media_setor_brl:,.2f}", style={'margin': '0', 'fontSize': '28px', 'color': '#10b981'})
    ]
    card_usd_style = {**estilo_panel, 'flex': '1', 'padding': '24px', 'borderRadius': '12px',
                      'borderLeft': '4px solid #10b981'}

    # 1. Gráfico Matriz
    fig_matriz = px.scatter(
        df_matriz, x="Risco_IA_Porcentagem", y="Job_Growth_2030",
        color="Impacto_da_IA", size="Salario_Reais",  # O tamanho agora baseia-se na coluna em Reais
        hover_name="Job_Title",
        hover_data={
            "Risco_IA_Porcentagem": ':.0f',
            "Salario_Reais": ':,.2f',  # Formatação exata com vírgula e 2 casas decimais
            "Impacto_da_IA": False,
            "Job_Growth_2030": False
        },
        title="Ato 1: Onde estão as Oportunidades e os Perigos?",
        color_discrete_map={'Baixo Risco': '#10b981', 'Risco Médio': '#f59e0b', 'Alto Risco': '#ef4444'},
        labels={
            "Risco_IA_Porcentagem": "Risco da IA roubar a vaga (%)",
            "Job_Growth_2030": "Crescimento de Vagas (%)",
            "Salario_Reais": "Salário Anual (R$)",  # Traduzido
            "Impacto_da_IA": "Impacto da IA"  # Limpo, sem underscore
        }
    )
    fig_matriz.update_layout(margin={"r": 20, "t": 50, "l": 40, "b": 40}, paper_bgcolor=tema['bg_panel'],
                             plot_bgcolor=tema['bg_panel'], font_color=tema['text'],
                             title_font=dict(size=14, weight='bold'))
    fig_matriz.update_xaxes(showgrid=True, gridcolor=tema['border'])
    fig_matriz.update_yaxes(showgrid=True, gridcolor=tema['border'])

    # 2. Profissões do Futuro
    df_cargos = df_filtrado.groupby('Job_Title')['Demanda_Porcentagem'].mean().reset_index().nlargest(5,
                                                                                                      'Demanda_Porcentagem')
    fig_top_jobs = px.bar(
        df_cargos, x="Demanda_Porcentagem", y="Job_Title", orientation='h',
        title="Ato 2: Profissões com Mais Futuro", color_discrete_sequence=[tema['accent']],
        labels={"Demanda_Porcentagem": "Potencial de Contratação (%)", "Job_Title": ""}
    )
    fig_top_jobs.update_layout(margin={"r": 20, "t": 50, "l": 20, "b": 40}, paper_bgcolor=tema['bg_panel'],
                               plot_bgcolor=tema['bg_panel'], font_color=tema['text'],
                               title_font=dict(size=14, weight='bold'), yaxis={'categoryorder': 'total ascending'})

    # 3. Gráfico de Habilidades
    skills = df_filtrado['Required_Skills'].dropna().astype(str).str.split(',').explode().str.strip()
    df_skills = skills.value_counts().head(5).reset_index()
    df_skills.columns = ['Habilidade', 'Qtd']

    fig_skills = px.bar(
        df_skills, x="Qtd", y="Habilidade", orientation='h',
        title="Ato 3: O que precisamos estudar hoje?", color_discrete_sequence=['#10b981'],
        labels={"Qtd": "Vezes que a empresa exige", "Habilidade": ""}
    )
    fig_skills.update_layout(margin={"r": 20, "t": 50, "l": 20, "b": 40}, paper_bgcolor=tema['bg_panel'],
                             plot_bgcolor=tema['bg_panel'], font_color=tema['text'],
                             title_font=dict(size=14, weight='bold'), yaxis={'categoryorder': 'total ascending'})

    # Mensagem Lateral (Alerta)
    perc_upskill = (df_filtrado['Upskilling_Needed'] == 'Yes').mean() * 100
    estilo_status = {'fontSize': '14px', 'lineHeight': '1.6', 'padding': '16px', 'backgroundColor': tema['bg_page'],
                     'borderRadius': '8px', 'color': tema['text']}
    if perc_upskill > 60:
        texto_status = f"Atenção: {perc_upskill:.0f}% dos profissionais desta área vão perder espaço se não voltarem a estudar as tecnologias do gráfico 'Ato 3'."
        estilo_status['borderLeft'] = '4px solid #ef4444'
    else:
        texto_status = f"Tranquilo: Cerca de {perc_upskill:.0f}% dos profissionais precisarão se atualizar. A maioria já possui as habilidades para trabalhar com IA."
        estilo_status['borderLeft'] = '4px solid #f59e0b'

    return fig_matriz, fig_top_jobs, fig_skills, texto_status, estilo_status, card_total_content, card_total_style, card_risk_content, card_risk_style, card_usd_content, card_usd_style, estilos_base, estilo_panel, estilo_panel, estilo_panel, estilo_panel, btn_text, btn_style


if __name__ == '__main__':
    app.run(debug=True)