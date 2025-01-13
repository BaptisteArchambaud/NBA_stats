from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
import os
import pandas as pd

def get_players_list(year):
    '''Get players names into list'''
    filename = os.path.abspath(f"./data/players_list_{year}.json")

    # if players names list does not exist in local folder then use API
    if not os.path.exists(filename):
        client.players_season_totals(season_end_year=year, 
                                     output_type=OutputType.JSON, 
                                     output_file_path=filename)

    df = pd.read_json(filename)
    players_list = df["slug"].unique().tolist() 
    return(players_list)