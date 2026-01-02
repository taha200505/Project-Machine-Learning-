# components/data_display.py
# Components for displaying data and statistics

import streamlit as st
import numpy as np

def render_data_info(filtered_df, total_df):
    '''Display data information banner'''
    st.info(
        f"📋 Showing {len(filtered_df)} records out of {len(total_df)} total records"
    )

def render_dataset_preview(df, selected_features):
    '''Render dataset preview section'''
    st.header("1️⃣ Dataset Preview")
    
    if selected_features:
        st.dataframe(df[selected_features].head(20), use_container_width=True)
    else:
        st.warning("⚠️ Please select at least one feature to display")

def render_summary_statistics(df):
    '''Render summary statistics section'''
    st.header("2️⃣ Summary Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Exam Score", f"{df['exam_score'].mean():.2f}")
    with col2:
        st.metric("Average Study Hours", f"{df['study_hours'].mean():.2f}")
    with col3:
        st.metric("Average Attendance", f"{df['class_attendance'].mean():.2f}%")
    with col4:
        st.metric("Average Sleep Hours", f"{df['sleep_hours'].mean():.2f}")
    
    # Detailed statistics
    st.subheader("Detailed Statistics")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    st.dataframe(df[numeric_cols].describe(), use_container_width=True)