import pandas as pd
from datetime import datetime
import warnings

from basic import BaseDataObject
warnings.filterwarnings("ignore", 'This pattern has match groups')


class DataFrameCleaner(BaseDataObject):
    """Class for cleaning data."""
   
    def __init__(self, df_cleaned_data: pd.DataFrame) -> None:
        self.df_data = df_cleaned_data
        self.urls = self.get_urls()

    def clean_dataset(self):
        self.convert_timestamp_to_utc()
        self.fill_null()

    def get_urls(self):
        #list all urls without nan
        urls = self.df_data[self.df_data['url'].notna()]['url']
        return urls

    def convert_timestamp_to_utc(self):
        #add a colum to df with utc time
        self.df_data['utc_time'] = datetime.fromtimestamp(self.df_data['timestamp']).strftime(self.DATEFORMAT)
        #print('cleaner', self.df_data.columns)

    def fill_null(self):
        for col in self.df_data.columns:
            self.df_data[col].fillna("")
       
