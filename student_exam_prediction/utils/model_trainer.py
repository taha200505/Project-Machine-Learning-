# utils/model_trainer.py
# Model training and evaluation utilities

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import cross_val_score
from config import MODEL_PARAMS

def get_model(model_name):
    '''Get model instance based on name'''
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(**MODEL_PARAMS['random_forest']),
        'Decision Tree': DecisionTreeRegressor(**MODEL_PARAMS['decision_tree']),
        'SVR': SVR(**MODEL_PARAMS['svr'])
    }
    return models.get(model_name)

def train_and_evaluate(X_train, X_test, y_train, y_test, model_name, cv_folds=5):
    '''Train model and calculate metrics'''
    model = get_model(model_name)
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Metrics
    metrics = {
        'MSE': mean_squared_error(y_test, y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
        'MAE': mean_absolute_error(y_test, y_pred),
        'R²': r2_score(y_test, y_pred)
    }
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=cv_folds, scoring='r2')
    metrics['CV_Scores'] = cv_scores
    metrics['CV_Mean'] = cv_scores.mean()
    metrics['CV_Std'] = cv_scores.std()
    
    return model, y_pred, metrics

def get_feature_importance(model, feature_names, model_name):
    '''Get feature importance for tree-based models'''
    if model_name in ['Random Forest', 'Decision Tree']:
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)
        return importance_df
    return None