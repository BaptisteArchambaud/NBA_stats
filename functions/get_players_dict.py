from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
import os
import json

def get_players_dict(year_min: int, year_max: int) -> dict[str, dict]:
    '''Get players names, their season min and season max into a dictionary from specific season range year_min to year_max'''

    # dictionary of player names registered from year_min to year_max
    players_dict_years = {}

    for year in range(year_min, year_max+1):
        filename = os.path.abspath(f"./data/players_list_{year}.json")

        # if players names list does not exist in local folder then use API
        if not os.path.exists(filename):
            client.players_season_totals(season_end_year=year, output_type=OutputType.JSON, output_file_path=filename)

        with open(filename, 'r') as file:
            players_data = json.load(file)

        for player in players_data:
            player_id = player['slug']
            player_name = player['name']

            if player_id not in players_dict_years:
                # if new player then initialize data
                players_dict_years[player_id] = {"name": player_name, "season_min": year, "season_max": year}
            else:
                # if existing player then update season min and max
                players_dict_years[player_id]["season_max"] = max(players_dict_years[player_id]["season_max"], year)
                players_dict_years[player_id]["season_min"] = min(players_dict_years[player_id]["season_min"], year)

    return players_dict_years
