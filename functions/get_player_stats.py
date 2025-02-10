from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
from basketball_reference_web_scraper.errors import InvalidPlayerAndSeason
import os
import pandas as pd

def get_player_stats(player_id: str, year: int) -> pd.DataFrame:
    '''Get player data from specific year'''
    filename = os.path.abspath(f"./data/{player_id}_{year}.json")
    
    try:
        # if player data does not exist in local folder then use API
        if not os.path.exists(filename):
            client.regular_season_player_box_scores(player_identifier=player_id, 
                                                    season_end_year=year,
                                                    output_type=OutputType.JSON, 
                                                    output_file_path=filename)

        player_stats = pd.read_json(filename)
        return(player_stats)
    
    # if no data in API for this player and year
    except(InvalidPlayerAndSeason):
        return(pd.DataFrame())