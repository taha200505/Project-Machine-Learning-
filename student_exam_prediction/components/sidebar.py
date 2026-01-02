# components/sidebar.py
# Sidebar components for filters and user input

import streamlit as st
from config import SLIDER_CONFIG

def render_feature_selector(columns):
    '''Render feature selection multiselect'''
    st.sidebar.subheader("📊 Select Features to Display")
    selected = st.sidebar.multiselect(
        "Choose features:",
        columns,
        default=columns
    )
    return selected

def render_filters(df):
    '''Render data filters'''
    st.sidebar.subheader("🔍 Filter Data")
    
    filters = {}
    
    # Course filter
    courses = ['All'] + sorted(df['course'].dropna().unique().tolist())
    filters['course'] = st.sidebar.selectbox("Course:", courses)
    
    # Gender filter
    genders = ['All'] + sorted(df['gender'].dropna().unique().tolist())
    filters['gender'] = st.sidebar.selectbox("Gender:", genders)
    
    # Study method filter
    methods = ['All'] + sorted(df['study_method'].dropna().unique().tolist())
    filters['study_method'] = st.sidebar.selectbox("Study Method:", methods)
    
    # Internet access filter
    internet = ['All'] + sorted(df['internet_access'].dropna().unique().tolist())
    filters['internet_access'] = st.sidebar.selectbox("Internet Access:", internet)
    
    return filters

def render_model_selector():
    '''Render model selection dropdown'''
    st.sidebar.subheader("🤖 Select Regression Model")
    model = st.sidebar.selectbox(
        "Choose model:",
        ['Linear Regression', 'Random Forest', 'Decision Tree', 'SVR']
    )
    return model

def render_user_input_form(df):
    '''Render user input form for predictions'''
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎯 Predict Exam Score")
    st.sidebar.write("Enter student details:")
    
    user_input = {}
    
    # Numeric inputs
    cfg = SLIDER_CONFIG
    user_input['study_hours'] = st.sidebar.slider(
        "Study Hours per Day:",
        cfg['study_hours']['min'],
        cfg['study_hours']['max'],
        cfg['study_hours']['default'],
        cfg['study_hours']['step']
    )
    
    user_input['class_attendance'] = st.sidebar.slider(
        "Class Attendance (%):",
        cfg['class_attendance']['min'],
        cfg['class_attendance']['max'],
        cfg['class_attendance']['default'],
        cfg['class_attendance']['step']
    )
    
    user_input['sleep_hours'] = st.sidebar.slider(
        "Sleep Hours per Day:",
        cfg['sleep_hours']['min'],
        cfg['sleep_hours']['max'],
        cfg['sleep_hours']['default'],
        cfg['sleep_hours']['step']
    )
    
    user_input['facility_rating'] = st.sidebar.slider(
        "Facility Rating:",
        cfg['facility_rating']['min'],
        cfg['facility_rating']['max'],
        cfg['facility_rating']['default'],
        cfg['facility_rating']['step']
    )
    
    # Categorical inputs
    user_input['gender'] = st.sidebar.selectbox(
        "Gender:",
        sorted(df['gender'].dropna().unique())
    )
    user_input['course'] = st.sidebar.selectbox(
        "Course:",
        sorted(df['course'].dropna().unique())
    )
    user_input['internet_access'] = st.sidebar.selectbox(
        "Internet Access:",
        sorted(df['internet_access'].dropna().unique())
    )
    user_input['sleep_quality'] = st.sidebar.selectbox(
        "Sleep Quality:",
        sorted(df['sleep_quality'].dropna().unique())
    )
    user_input['study_method'] = st.sidebar.selectbox(
        "Study Method:",
        sorted(df['study_method'].dropna().unique())
    )
    user_input['exam_difficulty'] = st.sidebar.selectbox(
        "Exam Difficulty:",
        sorted(df['exam_difficulty'].dropna().unique())
    )
    
    predict_button = st.sidebar.button("🎓 Predict Score")
    
    return user_input, predict_button