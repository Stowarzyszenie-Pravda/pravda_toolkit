import pandas as pd
import ast

def change_reply_to_user_list(reply_to):
    user_list = []
    temps = ast.literal_eval(reply_to)
    for temp in temps:
        user_list.append(temp["screen_name"])
    return user_list

def generate_edge_list(df):
    graph_list = []
    for index, row in df.iterrows():
        for user in change_reply_to_user_list(row["reply_to"]):
            graph_list.append([row["username"],user])
    return pd.DataFrame(graph_list, columns=['source', 'target'])


def hydrate(df):
    pass