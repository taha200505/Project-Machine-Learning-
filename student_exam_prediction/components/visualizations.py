# components/visualizations.py
# All visualization components

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_distribution(df):
    '''Plot exam score distribution'''
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df['exam_score'], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    ax.set_xlabel('Exam Score', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title('Distribution of Exam Scores', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    return fig

def plot_correlation_heatmap(df):
    '''Plot correlation heatmap'''
    numeric_data = df.select_dtypes(include=[np.number])
    
    fig, ax = plt.subplots(figsize=(12, 8))
    correlation = numeric_data.corr()
    sns.heatmap(
        correlation,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        center=0,
        ax=ax,
        linewidths=0.5
    )
    ax.set_title('Feature Correlation Matrix', fontsize=14, fontweight='bold')
    return fig

def plot_scatter(df, x_col, y_col, color='blue', title=''):
    '''Generic scatter plot'''
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df[x_col], df[y_col], alpha=0.5, color=color)
    ax.set_xlabel(x_col.replace('_', ' ').title(), fontsize=12)
    ax.set_ylabel(y_col.replace('_', ' ').title(), fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3)
    return fig

def plot_categorical_avg(df, group_col, value_col, color='steelblue', kind='barh'):
    '''Plot average values by category'''
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_data = df.groupby(group_col)[value_col].mean().sort_values()
    avg_data.plot(kind=kind, ax=ax, color=color)
    ax.set_xlabel(f'Average {value_col.replace("_", " ").title()}', fontsize=12)
    ax.set_ylabel(group_col.replace('_', ' ').title(), fontsize=12)
    ax.set_title(
        f'Average {value_col.replace("_", " ").title()} by {group_col.replace("_", " ").title()}',
        fontsize=14,
        fontweight='bold'
    )
    ax.grid(axis='x', alpha=0.3)
    return fig

def render_visualizations(df):
    '''Render all visualization tabs'''
    st.header("3️⃣ Data Visualizations")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Distribution Analysis",
        "📈 Correlation Analysis",
        "🎯 Feature vs Score",
        "📉 Categorical Analysis"
    ])
    
    with tab1:
        st.subheader("Exam Score Distribution")
        fig = plot_distribution(df)
        st.pyplot(fig)
    
    with tab2:
        st.subheader("Correlation Heatmap")
        fig = plot_correlation_heatmap(df)
        st.pyplot(fig)
    
    with tab3:
        st.subheader("Key Features vs Exam Score")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = plot_scatter(
                df, 'study_hours', 'exam_score',
                'blue', 'Study Hours vs Exam Score'
            )
            st.pyplot(fig)
        
        with col2:
            fig = plot_scatter(
                df, 'class_attendance', 'exam_score',
                'green', 'Attendance vs Exam Score'
            )
            st.pyplot(fig)
        
        col3, col4 = st.columns(2)
        
        with col3:
            fig = plot_scatter(
                df, 'sleep_hours', 'exam_score',
                'purple', 'Sleep Hours vs Exam Score'
            )
            st.pyplot(fig)
        
        with col4:
            fig = plot_scatter(
                df, 'facility_rating', 'exam_score',
                'orange', 'Facility Rating vs Exam Score'
            )
            st.pyplot(fig)
    
    with tab4:
        st.subheader("Categorical Feature Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = plot_categorical_avg(df, 'course', 'exam_score', 'steelblue')
            st.pyplot(fig)
        
        with col2:
            fig = plot_categorical_avg(df, 'study_method', 'exam_score', 'coral')
            st.pyplot(fig)