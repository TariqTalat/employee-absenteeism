import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib

class AbsenteeismModel:
    def __init__(self, model_path):
        # Load the trained model
        self.model = joblib.load(model_path)
        self.scaler = StandardScaler()
        self.feature_names = None

    def preprocess_data(self, file_path):
        # Load data
        df = pd.read_csv(file_path)

        # Drop irrelevant columns
        df.drop(['ID'], axis=1, inplace=True)

        # Handle categorical variable
        column_names = pd.get_dummies(df["Reason for Absence"], drop_first=True)
        df['Reason_1'] = column_names.loc[:, 1:14].max(axis=1)
        df['Reason_2'] = column_names.loc[:, 15:17].max(axis=1)
        df['Reason_3'] = column_names.loc[:, 18:21].max(axis=1)
        df['Reason_4'] = column_names.loc[:, 22:].max(axis=1)

        df.drop(["Reason for Absence"], axis=1, inplace=True)

        # Reordering columns
        column_names_reorder = ['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4',
                                'Date', 'Transportation Expense', 'Distance to Work', 'Age',
                                'Daily Work Load Average', 'Body Mass Index', 'Education', 'Children',
                                'Pets']
        
        df = df[column_names_reorder]

        # Convert date
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
        df['Month'] = df['Date'].apply(lambda x: x.month)
        df['Day of the week'] = df['Date'].apply(lambda x: x.weekday())
        df['Education'] = df['Education'].map({1: 0, 2: 1, 3: 1, 4: 1})
        df.drop(['Date'], axis=1, inplace=True)

        # Replace NaN values
        df = df.fillna(value=0)

        # Standardize relevant columns
        self.feature_names = df.columns.tolist()
        exclude_cols = ['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4', 'Education']
        cols_to_scale = [col for col in self.feature_names if col not in exclude_cols]
        df[cols_to_scale] = self.scaler.fit_transform(df[cols_to_scale])

        return df

    def predict(self, df):
        X = df[self.feature_names]
        return self.model.predict(X)

    def predict_proba(self, df):
        X = df[self.feature_names]
        return self.model.predict_proba(X)[:, 1]  # Return probability of class 1

    def add_predictions(self, df):
        df['Prediction'] = self.predict(df)
        df['Probability'] = self.predict_proba(df)
        return df
