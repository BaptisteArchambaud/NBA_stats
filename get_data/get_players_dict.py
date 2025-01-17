from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
import os
import json

def get_players_dict(year: int) -> dict[str, str]:
    '''Get players names into a dictionary'''
    filename = os.path.abspath(f"./data/players_list_{year}.json")

    # if players names list does not exist in local folder then use API
    if not os.path.exists(filename):
        client.players_season_totals(season_end_year=year, 
                                     output_type=OutputType.JSON, 
                                     output_file_path=filename)

    with open(filename, 'r') as file:
        players_data = json.load(file)

    players_dict = {player['slug']: player['name'] for player in players_data}
    return(players_dict)