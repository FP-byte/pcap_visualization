
from pathlib import Path
import logging
import os
import pandas as pd
import json


class BaseDataObject:
    """
    Basis functions tha can be used by all classes

    """
    DATEFORMAT: str = '%d/%m/%Y %H:%M:%S'

    def __init__(self, filename) -> None:
         self.filename = Path(filename).root
         self.curr_folder = os.path.dirname(os.path.abspath(__file__))
         
          

    def dict_to_df(self, data_dict :dict) -> pd.DataFrame:
        """
        Returns a dataframe from a data dictionary with a new index.
        Data fields are colums names, previous index is dropped.
        Args:
            data_dict (dict): data dictionary of type {"field" : "data"}

        Returns:
            pd.DataFrame: dataframe of dictionay
        """
        
        return pd.DataFrame.from_dict(data_dict).T.reset_index(drop=True)

    def save_df(self, data:dict) -> pd.DataFrame:
        """
        Saves dataframe file to csv local folder "/data", creates the folder if it does not exist

        Args:
            data (dict)
            filename (str)

        Returns:
            pd.DataFrame
        """

        data_df = self.dict_to_df(data)
        curr_folder = os.path.dirname(os.path.abspath(__file__))
        save_path_csv = Path(f"{curr_folder}/data/csv/{self.filename}.csv").absolute()
        if not save_path_csv.exists():
            # Create the path
            save_path_csv.mkdir(parents=True, exist_ok=True)

        try:           
            with open(save_path_csv, 'w', encoding ='utf8') as json_file: 
                data_df.to_csv(data_df, index=False)
        
        except Exception as exception:
              logging.error("Error while saving csv file")
              logging.error("Exception: {}".format(type(exception).__name__))
              logging.error("Exception message: {}".format(exception))

        return data_df
    
    def save_dict_to_json(self, data :dict, filename: str):
        """
        Save dictionary to json format in directory data/json

        Args:
            data (dict)_
            filename (str)
        """
           
        save_path = Path(f"{self.curr_folder}/data/json/{filename}").absolute()
        if not save_path.exists():
            # Create the path
             save_path.mkdir(parents=True, exist_ok=True)
        try:           
            with open(save_path, 'w', encoding ='utf8') as json_file: 
                json.dump(data, json_file)           
        except Exception as exception:
              logging.error("Error while saving json file")
              logging.error("Exception: {}".format(type(exception).__name__))
              logging.error("Exception message: {}".format(exception))


    def covert_json_to_df(self, jsonfile:dict) -> pd.DataFrame:
        """
        Converts json to dataframe

        Args:
            jsonfile (dict)
            filename (str) 

        Returns:
            pd.Dataframe
        """
        
        df_packet_data = pd.DataFrame.from_dict(jsonfile).T.reset_index(drop=True)
        df_packet_data.to_csv(self.save_path_json, index=False)
        
        return df_packet_data