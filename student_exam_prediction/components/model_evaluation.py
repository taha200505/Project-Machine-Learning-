# components/model_evaluation.py
# Model evaluation and visualization components

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def render_metrics(metrics):
    '''Display model performance metrics'''
    st.subheader("📊 Model Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("R² Score", f"{metrics['R²']:.4f}")
    with col2:
        st.metric("RMSE", f"{metrics['RMSE']:.4f}")
    with col3:
        st.metric("MAE", f"{metrics['MAE']:.4f}")
    with col4:
        st.metric("MSE", f"{metrics['MSE']:.4f}")

def render_cv_results(metrics):
    '''Display cross-validation results'''
    st.subheader("🔄 Cross-Validation Results (5-Fold)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Mean CV R²", f"{metrics['CV_Mean']:.4f}")
    with col2:
        st.metric("Std CV R²", f"{metrics['CV_Std']:.4f}")
    with col3:
        st.metric("Min CV R²", f"{metrics['CV_Scores'].min():.4f}")

def plot_predictions_vs_actual(y_test, y_pred, model_name):
    '''Plot predictions vs actual values'''
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(y_test, y_pred, alpha=0.6, color='blue', label='Predictions')
    ax.plot(
        [y_test.min(), y_test.max()],
        [y_test.min(), y_test.max()],
        'r--', lw=2, label='Perfect Prediction'
    )
    ax.set_xlabel('Actual Exam Score', fontsize=12)
    ax.set_ylabel('Predicted Exam Score', fontsize=12)
    ax.set_title(
        f'{model_name}: Predictions vs Actual',
        fontsize=14,
        fontweight='bold'
    )
    ax.legend()
    ax.grid(alpha=0.3)
    return fig

def plot_residuals(y_test, y_pred):
    '''Plot residuals'''
    residuals = y_test - y_pred
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(y_pred, residuals, alpha=0.6, color='purple')
    ax.axhline(y=0, color='r', linestyle='--', lw=2)
    ax.set_xlabel('Predicted Exam Score', fontsize=12)
    ax.set_ylabel('Residuals', fontsize=12)
    ax.set_title('Residuals Plot', fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3)
    return fig

def plot_feature_importance(importance_df):
    '''Plot feature importance'''
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(importance_df['Feature'], importance_df['Importance'], color='teal')
    ax.set_xlabel('Importance', fontsize=12)
    ax.set_ylabel('Feature', fontsize=12)
    ax.set_title('Feature Importance', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)
    return fig

def render_model_evaluation(y_test, y_pred, metrics, model_name, importance_df=None):
    '''Render complete model evaluation section'''
    st.header("4️⃣ Model Training & Evaluation")
    
    # Metrics
    render_metrics(metrics)
    
    # Cross-validation
    render_cv_results(metrics)
    
    # Predictions plot
    st.subheader("🎯 Predictions vs Actual Values")
    fig = plot_predictions_vs_actual(y_test, y_pred, model_name)
    st.pyplot(fig)
    
    # Residuals plot
    st.subheader("📉 Residuals Plot")
    fig = plot_residuals(y_test, y_pred)
    st.pyplot(fig)
    
    # Feature importance (if available)
    if importance_df is not None:
        st.subheader("📈 Feature Importance")
        fig = plot_feature_importance(importance_df)
        st.pyplot(fig)