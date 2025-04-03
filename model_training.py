from sklearn.linear_model._base import LinearRegression
from imports import *


def estimate(model, X_train, y_train):
    return model.fit(X_train, y_train)


def regress(X, y) -> LinearRegression:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    reg: LinearRegression = estimate(LinearRegression(), X_train, y_train)
    print(f"Regression score on test data: {reg.score(X_test, y_test)}")
    print(f"Regression score on train data: {reg.score(X_train, y_train)}")
    return reg


def compare_models(X, y, models):
    results = {}
    for model in models:
        name = model.__class__.__name__
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        results[name] = {
            "MSE": mean_squared_error(y_test, y_pred),
            "MAE": mean_absolute_error(y_test, y_pred),
            "R2": r2_score(y_test, y_pred)
        }
    return results
