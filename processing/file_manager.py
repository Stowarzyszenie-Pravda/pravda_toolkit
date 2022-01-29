from heapq import merge
import os
import pandas as pd

def merge_files(path: str, drop_duplicates_by: str = None) -> pd.DataFrame:
    """Merges .csv files into a single DataFrame 

    Args:
        path (str): Path to the folder containing the .csv files
        path (str): Element to drop duplicates by (eg. 'id', 'Username'). Deafult = None.

    Returns:
        [pd.DataFrame]: Returns merged DataFrame
    """
    for subdir, dirs, files in os.walk(path):
        for e, file in enumerate(files):
            #print os.path.join(subdir, file)
            filepath = subdir + os.sep + file
            
            if 'processed' in filepath or 'gephi' in filepath:
                continue

            if filepath.endswith(".csv"):
                filepath = str(filepath).replace(' \ '.strip(),'/')
                print(filepath)
            if e == 0:
                df = pd.read_csv(filepath)
            else:
                temp_df = pd.read_csv(filepath)
                df = df.append(temp_df)
    
    if drop_duplicates_by != None:
        df = df.drop_duplicates(subset = [drop_duplicates_by])
    return df
