# components/header.py
# Header and title components

import streamlit as st
from styles.custom_css import get_custom_css

def render_header():
    '''Render application header'''
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    st.markdown(
        '<p class="main-header">📚 Student Exam Score Prediction System</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="sub-header">Analyze student performance factors and predict exam scores using machine learning</p>',
        unsafe_allow_html=True
    )
    st.markdown("---")

def render_footer():
    '''Render application footer'''
    st.markdown("---")
    st.markdown('''
    <div class="footer">
        <p>📚 Student Exam Score Prediction System | Built with Streamlit & Scikit-learn</p>
        <p>Adjust filters and model parameters in the sidebar to explore different scenarios</p>
    </div>
    ''', unsafe_allow_html=True)