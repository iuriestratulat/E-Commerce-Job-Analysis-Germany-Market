from dash import Dash, html, dcc
import plotly.express as px

app = Dash(__name__)
df = px.data.iris()
fig = px.scatter(df, x='sepal_width', y='sepal_length', color='species')
app.layout = html.Div([
    html.H1("Визуализация набора данных Iris"),
    dcc.Graph(figure=fig)
])
if __name__ == '__main__':
    app.run(debug=True)