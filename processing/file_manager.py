import os
import pandas as pd

def merge_files(path: str):
    for subdir, dirs, files in os.walk(path):
        for e, file in enumerate(files):
            #print os.path.join(subdir, file)
            filepath = subdir + os.sep + file

            if filepath.endswith(".csv"):
                filepath = str(filepath).replace(' \ '.strip(),'/')
                print(filepath)
            if e == 0:
                df = pd.read_csv(filepath)
            else:
                temp_df = pd.read_csv(filepath)
                df = df.append(temp_df)