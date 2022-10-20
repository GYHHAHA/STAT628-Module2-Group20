import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_validate

data = pd.read_csv("../data/cleaned_data.csv")
data["WRIST_OVER_THIGH"] = data["WRIST"]/data["THIGH"]
y = data["BODYFAT"]
X = data.loc[:,"AGE":]

def stepwise_model(columns_stepwise,y):
    X_stepwise = X.loc[:,columns_stepwise]
    model = LinearRegression()
    stepwise_reg = model.fit(X_stepwise,y)   
    return stepwise_reg

columns_stepwise = ["ABDOMEN","WRIST","FOREARM","WEIGHT"]
stepwise_res = [
    stepwise_model(columns_stepwise, y).coef_,
    stepwise_model(columns_stepwise, y).intercept_,
]
print(f"Stepwise Result: {stepwise_res}")

def lasso_model(columns_lasso ,y):
    X_lasso = X.loc[:,columns_lasso]
    model = LinearRegression()
    lasso_reg = model.fit(X_lasso,y)
    return lasso_reg

columns_lasso = ["WEIGHT","HEIGHT","ABDOMEN","THIGH"]
lasso_res = [
    lasso_model(columns_lasso,y).coef_,
    stepwise_model(columns_lasso,y).intercept_,
]
print(f"Lasso Result: {lasso_res}")

# Metrics
lasso_reg = lasso_model(columns_lasso ,y)
scores_lasso = cross_validate(
    lasso_reg, X.loc[:,columns_lasso], y, cv=6,
    scoring=('r2', 'neg_mean_squared_error'),
    return_train_score=True
)
lasso_test_mse = -scores_lasso['test_neg_mean_squared_error']
str_prefix = "The mean square error on test set based on lasso method"
print(str_prefix + f" is {lasso_test_mse.mean()}.")

step_reg = stepwise_model(columns_stepwise ,y)
scores_stepwise = cross_validate(
    step_reg, X.loc[:,columns_stepwise], y, cv=6,
    scoring=('r2', 'neg_mean_squared_error'),
    return_train_score=True
)
stepwise_test_mse = -scores_stepwise['test_neg_mean_squared_error']
str_prefix = "The mean square error on test set based on stepwise regression"
print(str_prefix + f" is {stepwise_test_mse.mean()}.")
