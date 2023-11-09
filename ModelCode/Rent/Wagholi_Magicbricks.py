import numpy as np
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
import pandas as pd

dataset = pd.read_csv("../../Data/Rent Data/wagholi_final.csv")

rent = dataset.pop("Rent")

wagholi_model = RandomForestRegressor(n_estimators=255, max_depth=25, random_state=10, max_features='log2', min_samples_split=4, min_samples_leaf=1, bootstrap=True)

wagholi_model.fit(dataset,rent)

test = pd.read_csv("../../Data/Rent Data/test.csv")

# print(wagholi_model.predict(test))