# utils/data_loader.py
# Utilities for loading and caching data

import streamlit as st
import pandas as pd

@st.cache_data
def load_csv_data(filepath):
    '''Load dataset from CSV file'''
    try:
        df = pd.read_csv(filepath)
        return df, None
    except FileNotFoundError:
        return None, f"File '{filepath}' not found"
    except Exception as e:
        return None, f"Error loading data: {str(e)}"

def load_data_with_ui():
    '''Load data with user interface options'''
    st.sidebar.header("📁 Data Source")
    data_source = st.sidebar.radio(
        "Choose data source:",
        ["Load from CSV", "Upload CSV file"]
    )
    
    df = None
    
    if data_source == "Load from CSV":
        csv_path = st.sidebar.text_input("CSV file path:", "cleaned_data.csv")
        if st.sidebar.button("Load Data"):
            df, error = load_csv_data(csv_path)
            if error:
                st.sidebar.error(f"❌ {error}")
            else:
                st.session_state['df_raw'] = df
                st.session_state['data_loaded'] = True
                st.sidebar.success(f"✅ Loaded {len(df)} records!")
    else:
        uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=['csv'])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.session_state['df_raw'] = df
            st.session_state['data_loaded'] = True
            st.sidebar.success(f"✅ Uploaded {len(df)} records!")
    
    # Initialize with default file
    if 'data_loaded' not in st.session_state:
        df, error = load_csv_data('cleaned_data.csv')
        if df is not None:
            st.session_state['df_raw'] = df
            st.session_state['data_loaded'] = True
        else:
            st.warning("⚠️ Please load your dataset using the sidebar options")
            st.stop()
    
    return st.session_state.get('df_raw')