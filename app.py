from dash import Dash, html, dcc, Input, Output, callback


app = Dash(__name__)

app.layout = html.Div([
    html.H1("Leak-Map Analytics", style={'textAlign': 'center'}),
    html.P("Projeto de Visualização de Vazamentos de Dados - Unichristus", style={'textAlign': 'center'}),

    html.Hr(),

    html.Div([
        "Pesquisar Vazamento: ",
        dcc.Input(id='meu-input', value='Brasil', type='text')
    ], style={'textAlign': 'center'}),

    html.Br(),

    html.Div(id='meu-output', style={'textAlign': 'center', 'fontWeight': 'bold'})
])


@callback(
    Output(component_id='meu-output', component_property='children'),
    Input(component_id='meu-input', component_property='value')
)
def update_output_div(input_value):
    return f'Resultado da busca: {input_value}'


if __name__ == '__main__':
    app.run(debug=True)