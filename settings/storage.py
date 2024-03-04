from pathlib import Path
import pandas as pd


class Storage:
    def __init__(self):
        self.path = 'provider/data/'

    def save(self, row):
        data = Path(self.path + 'candlesticks.csv')

        additional_row_datetime = row.index[-1] + pd.Timedelta(seconds=60)
        additional_row_data = {'open': None,
                               'high': None,
                               'low': None,
                               'close': None,
                               'volume': None}

        if data.is_file():
            old_data = pd.read_csv(data,
                                   index_col=0,
                                   dtype={'date': 'str',
                                          'open': float,
                                          'high': float,
                                          'low': float,
                                          'close': float,
                                          'volume': float})

            row_float = row.astype(float)
            old_data.iloc[-1] = row_float

            # Create the additional row as a DataFrame.
            additional_row = pd.DataFrame([additional_row_data], index=[additional_row_datetime])

            # Concatenate the additional DataFrame with the existing data.
            old_data = pd.concat([old_data, additional_row])

            # Rename the index name.
            old_data = old_data.rename_axis('date')

            old_data.to_csv(data)
        else:
            row.index.name = 'date'
            row.to_csv(data)

    def update(self, row):
        data = Path(self.path + 'candlesticks.csv')

        if data.is_file():
            old_data = pd.read_csv(data,
                                   index_col=0,
                                   dtype={'date': 'str',
                                          'open': float,
                                          'high': float,
                                          'low': float,
                                          'close': float,
                                          'volume': float})

            # Replace the last row of the DataFrame with the data provided in 'row'.
            row_float = row.astype(float)
            old_data.iloc[-1] = row_float

            old_data.to_csv(data)
        else:
            print("Can't update file because it doesn' exist.")
