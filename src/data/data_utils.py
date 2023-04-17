# data_utils.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, LabelEncoder


def list_to_dataframe(data_list):
    # Convert a list of dictionaries to a Pandas DataFrame if necessary
    return pd.DataFrame(data_list)


def split_data(data, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    # Split the data into training, validation, and test sets
    train_data, remainder = train_test_split(
        data, test_size=(val_ratio + test_ratio), random_state=42
    )
    val_data, test_data = train_test_split(
        remainder, test_size=(test_ratio / (val_ratio + test_ratio)), random_state=42
    )
    return train_data, val_data, test_data


def normalize_data(data, columns=None):
    # Normalize the data
    scaler = MinMaxScaler()
    if columns is None:
        columns = data.columns
    data[columns] = scaler.fit_transform(data[columns])
    return data, scaler


def categorical_encoding(data, columns=None, encoding_type="one_hot"):
    # Encode categorical variables
    if columns is None:
        columns = data.select_dtypes(include=["object", "category"]).columns

    if encoding_type == "one_hot":
        encoder = OneHotEncoder(sparse=False)
        encoded_data = pd.DataFrame(
            encoder.fit_transform(data[columns]),
            columns=encoder.get_feature_names_out(columns),
        )
        data = pd.concat([data.drop(columns, axis=1), encoded_data], axis=1)
    elif encoding_type == "label":
        encoder = LabelEncoder()
        for col in columns:
            data[col] = encoder.fit_transform(data[col])

    return data, encoder


def handle_missing_values(data, method="drop", columns=None, fill_value=None):
    # Impute or remove missing values
    if columns is None:
        columns = data.columns
    if method == "drop":
        data = data.dropna(subset=columns)
    elif method == "fillna":
        if fill_value is None:
            data[columns] = data[columns].fillna(data[columns].mean())
        else:
            data[columns] = data[columns].fillna(fill_value)
    return data


def resample_data(data, frequency, datetime_column="timestamp"):
    # Resample time-series data
    data[datetime_column] = pd.to_datetime(data[datetime_column])
    data = data.set_index(datetime_column)
    data = data.resample(frequency).mean()
    data = data.reset_index()
    return data
