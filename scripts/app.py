import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from scripts.get_players_list import get_players_list
from scripts.get_player_stats import get_player_stats

year = 2024
players_list = get_players_list(year)
statistics_to_display = ["points_scored", "assists", "blocks", "defensive_rebounds", "offensive_rebounds", "steals"]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Time series of NBA players 2024 statistics"),
    dcc.Dropdown(players_list, multi=True, id='players_selector'),
    dcc.Dropdown(statistics_to_display, statistics_to_display[0], id='statistic_selector'),
    dcc.Graph(id="player_graph")
])

@app.callback(
    Output('player_graph', 'figure'),
    Input('players_selector', 'value'),
    Input('statistic_selector', 'value')
)

def update_graph(players, statistic):
    if players is None or len(players) == 0:
        return px.line(title="Select a player")
    all_data = []
    for player in players:
        player_data = get_player_stats(player, year)
        player_data["player"] = player
        all_data.append(player_data)

    players_data = pd.concat(all_data)
    graph = px.line(players_data, x="date", y=statistic, color="player").update_layout(xaxis_title="Time")
    return graph

if __name__ == '__main__':
    app.run_server(debug=False)