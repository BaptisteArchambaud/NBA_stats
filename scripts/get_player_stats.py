from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
import os
import pandas as pd

def get_player_stats(player_identifier, year):
    '''Get specific player data'''
    filename = os.path.abspath(f"./data/{player_identifier}_{year}.json")
    
    # if player data does not exist in local folder then use API
    if not os.path.exists(filename):
        client.regular_season_player_box_scores(player_identifier=player_identifier, 
                                                season_end_year=year,
                                                output_type=OutputType.JSON, 
                                                output_file_path=filename)

    player_stats = pd.read_json(filename)
    return(player_stats)