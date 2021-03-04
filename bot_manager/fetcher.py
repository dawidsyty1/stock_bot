import json
import pandas as pd
import glob
from .helper import setup_dir
from .api_alpha import get_indicator_data

def grab_data(item):
    entries = [key for key in json.loads(item.strategy.entry_rule).keys()]
    exitst = [key for key in json.loads(item.strategy.exit_rule).keys()]

    setup_dir(item.name)

    for inticator in set(entries + exitst):

        serialized_response = get_indicator_data(item, inticator)
        keys_response = [key for key in serialized_response.keys()]
        data = serialized_response[keys_response[1]]
        lenght = 500 if len(data.items()) > 500 else len(data.items())
        data = dict(list(data.items())[:lenght])
        df = pd.DataFrame.from_dict(data)
        df.to_csv(f'data/{item.name}/{inticator}.csv')

    all_filenames = [i for i in glob.glob(f'data/{item.name}/*.csv')]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    combined_csv.to_csv(f'data/{item.name}/{item.name}.csv', encoding='utf-8-sig')

