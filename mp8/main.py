import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.compose import ColumnTransformer

class UserPredictor:
    def __init__(self):
        self.preprocessor = ColumnTransformer(
            transformers = [
                ('num', StandardScaler(), ['age', 'past_purchase_amt', 'total_time_spent', 'visit_count', 'avg_page_time']),
                ('cat', OneHotEncoder(), ['badge'])
            ]
        )
        self.pipeline = Pipeline([
            ('preprocessor', self.preprocessor),
            ('classifier', LogisticRegression())
        ])
        self.features = None
        
    def merge_logs(self, users_df, logs_df):
        if logs_df is not None:
            log_agg = logs_df.groupby('user_id').agg({
                'seconds': 'sum',
                'url': 'count'
            }).rename(columns = {'seconds': 'total_time_spent', 'url': 'visit_count'})            
            log_agg['avg_page_time'] = log_agg['total_time_spent'] / log_agg['visit_count']            
            users_df = users_df.merge(log_agg, how = 'left', on = 'user_id')
        
        users_df['total_time_spent'] = users_df['total_time_spent'].fillna(0)
        users_df['visit_count'] = users_df['visit_count'].fillna(0)
        users_df['avg_page_time'] = users_df['avg_page_time'].fillna(0)
        return users_df
    
    def fit(self, train_users, train_logs, train_y):
        train_users = self.merge_logs(train_users, train_logs)
        X = train_users.drop(columns = ['user_id'])
        train_users = train_users.dropna()
        self.features = X.columns
        y = train_y['y']
        scores = cross_val_score(self.pipeline, X, y)
        self.pipeline.fit(X, y)
        
    def predict(self, test_users, test_logs):
        test_users = self.merge_logs(test_users, test_logs)
        X = test_users[self.features]
        return self.pipeline.predict(X)
