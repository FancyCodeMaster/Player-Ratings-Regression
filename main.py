import pandas as pd
player_attributes = pd.read_csv("Player_Attributes.csv")


empty_features = []
for i in player_attributes.columns:
    if player_attributes.isnull().sum()[i] > 0:
        empty_features.append(i)

to_remove_rows = []
rows = player_attributes[0]

for i in rows:
    for j in player_attributes.columns:
        if player_attributes.isnull().iloc[i , 0:-1][j] == True and j != "overall_rating":
            to_remove_rows.append(i)


