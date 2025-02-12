import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from functions.get_players_dict import get_players_dict
from functions.get_player_stats import get_player_stats

year_min = 2020
year_max = 2024
players_dict = get_players_dict(year_min, year_max)
statistics_to_display = {"points_scored":"Points scored", 
                         "assists":"Assists", 
                         "blocks":"Blocks", 
                         "defensive_rebounds":"Defensive rebounds", 
                         "offensive_rebounds":"Offensive rebounds", 
                         "steals":"Steals"}

# range of months to remove in the plot during off-season
rangebreaks = []
for year in range(year_min, year_max+1):
    start_date = pd.to_datetime(f'{year}-05-01')
    end_date = pd.to_datetime(f'{year}-09-30')
    rangebreaks.append(dict(values=pd.date_range(start=start_date, end=end_date)))

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(f"Time series of NBA players statistics from {year_min} to {year_max}"),
    dcc.Dropdown(options=[{"label": player["name"], "value": player_id} for player_id, player in players_dict.items()], multi=True, id='players_selector'),
    dcc.Dropdown(statistics_to_display, "points_scored", id='statistic_selector'),
    dcc.Graph(id="player_graph"),
    dcc.RangeSlider(year_min, year_max, 1, value=[year_max-1, year_max], marks={i: f"{i-1}-{i}" for i in range(year_min, year_max+1)}, id='dates_slider')
])

@app.callback(Output('player_graph', 'figure'), [Input('players_selector', 'value'), Input('statistic_selector', 'value'), Input('dates_slider', 'value')])

def update_graph(players, statistic, years):

    if players is None or len(players) == 0:
        return px.line(title="Select a player")

    players_list = []
    # get data from all selected players
    for player_id in players:
        player_list = []
        # get data from all selected seasons
        for year in range(years[0], years[1]+1):
            # get data only if selected year is included in player career range
            if year >= players_dict[player_id]["season_min"] and year <= players_dict[player_id]["season_max"]:
                player_year_df = get_player_stats(player_id, year)
                player_year_df["player"] = players_dict[player_id]["name"]
                player_list.append(player_year_df)
        player_df = pd.concat(player_list) if player_list else pd.DataFrame()
        players_list.append(player_df)
    players_df = pd.concat(players_list) if players_list else pd.DataFrame()

    if players_df.empty:
        return px.line()

    graph = px.line(players_df, x="date", y=statistic, color="player"
                    ).update_layout(xaxis_title="Time", 
                                    yaxis_title=statistics_to_display.get(statistic), 
                                    xaxis_rangebreaks=rangebreaks
                                    ).update_traces(connectgaps=True)

    return graph

if __name__ == '__main__':
    app.run_server(debug=False)