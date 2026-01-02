# utils/data_processor.py
# Data processing and encoding utilities

import pandas as pd
from config import CATEGORICAL_MAPPINGS

def get_reverse_mappings():
    '''Get reverse mappings for encoding'''
    return {
        col: {v: k for k, v in mapping.items()}
        for col, mapping in CATEGORICAL_MAPPINGS.items()
    }

def decode_dataframe(df):
    '''Decode categorical variables for display'''
    df_decoded = df.copy()
    
    for col, mapping in CATEGORICAL_MAPPINGS.items():
        if col in df_decoded.columns:
            df_decoded[col] = df_decoded[col].map(mapping)
    
    return df_decoded

def encode_user_input(user_data):
    '''Encode user input data'''
    reverse_mappings = get_reverse_mappings()
    encoded_data = user_data.copy()
    
    for col in CATEGORICAL_MAPPINGS.keys():
        if col in encoded_data:
            encoded_data[col] = reverse_mappings[col][encoded_data[col]]
    
    return encoded_data

def filter_dataframe(df, filters):
    '''Apply filters to dataframe'''
    filtered = df.copy()
    
    for col, value in filters.items():
        if value != 'All' and col in filtered.columns:
            filtered = filtered[filtered[col] == value]
    
    return filtered