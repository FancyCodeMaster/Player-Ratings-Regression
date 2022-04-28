import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder , OneHotEncoder
from sklearn.compose import ColumnTransformer

player_attributes = pd.read_csv("Player_Attributes.csv")

# Checking for the null containing columns
null_columns = []
for i in player_attributes.columns:
    if player_attributes.isnull().sum()[i] > 0:
        null_columns.append(i)

# Checking if these columns have way too null values
to_remove_columns = []
for i in null_columns:
    if player_attributes.isnull().sum()[i] > 61326:
        to_remove_columns.append(i)

# Checking null values in the rows of the dataframe
to_remove_rows = []
for i in range(player_attributes.shape[0]):
    if player_attributes.loc[i].isnull().sum() >= 2:
        to_remove_rows.append(i)

# removing the rows which had more than one null containing columns
player_attributes = player_attributes.drop(to_remove_rows)

# since there are no columns containg way too more null values , so not removing any columns

# Now , managing the missing values
categorical_null_columns = []
numerical_null_columns = []

for i in null_columns:
    if player_attributes[i].dtype == 'O':
        categorical_null_columns.append(i)
    else:
        numerical_null_columns.append(i)

numerical_simple_imputer = SimpleImputer(missing_values=np.nan , strategy="mean")
categorical_simple_imputer = SimpleImputer(missing_values=np.nan , strategy="most_frequent")

player_attributes[numerical_null_columns] = numerical_simple_imputer.fit_transform(player_attributes[numerical_null_columns])
player_attributes[categorical_null_columns] = categorical_simple_imputer.fit_transform(player_attributes[categorical_null_columns])

y = player_attributes['overall_rating'].values
y = y.reshape(-1,1)
del player_attributes['overall_rating']

# Now encoding the categorical data

categorical_indices = []
numerical_indices = []

for i in range(len(player_attributes.columns)):
    if player_attributes.iloc[: , i].dtype == "O":
        categorical_indices.append(i)
    elif player_attributes.iloc[: , i].dtype == "int64" or player_attributes.iloc[: , i].dtype == 'float64':
        numerical_indices.append(i)

# In the case of categorical encoding we have to further categorize into whether label encoding or one hot encoding can be applied
categorical_label_indices = []
categorical_onehot_indices = []

for i in categorical_indices:
    if len(player_attributes.iloc[: , i].value_counts()) <= 2:
        categorical_label_indices.append(i)
    elif len(player_attributes.iloc[: , i].value_counts()) > 2:
        categorical_onehot_indices.append(i)

# label encoding
label_encoder = LabelEncoder()
for i in categorical_label_indices:
    player_attributes.iloc[: , i] = label_encoder.fit_transform(player_attributes.iloc[: , i])

# for onehot encoding
b = 0
i = 0
dummy_var_indices = []
for j in categorical_onehot_indices:
    a = i+b
    dummy_var_indices.append(a)
    b = len(player_attributes.iloc[: , j].value_counts())
    i = a

ct = ColumnTransformer([("encoder" , OneHotEncoder() , categorical_onehot_indices)] , remainder="passthrough")
X = ct.fit_transform(player_attributes)

# Removing the dummy variables from X
include_var_indices = []

for i in range(X.shape[1]):
    if i not in dummy_var_indices:
        include_var_indices.append(i)

X = X[: , include_var_indices]
X = X.toarray()















