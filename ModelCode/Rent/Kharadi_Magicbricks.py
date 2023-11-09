import numpy as np
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
import pandas as pd

# Load the dataset (you can replace this with your own dataset)

dataset = pd.read_csv("../../Data/Rent Data/kharadi_final.csv")

rent = dataset.pop("Rent")

# X_train,X_test,y_train, y_test = train_test_split(dataset.drop(["Furnishing"],axis=1),rent,test_size=0.2,random_state=10)

kharadi_model = RandomForestRegressor(n_estimators=400, max_depth=16, random_state=10, max_features='sqrt', min_samples_split=4, min_samples_leaf=2, bootstrap=True)

kharadi_model.fit(dataset.drop(["Furnishing"],axis = 1),rent)

test = pd.read_csv("../../Data/Rent Data/test.csv")

# print(kharadi_model.predict(test))