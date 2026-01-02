# app.py
# Main Streamlit application - Entry point

import streamlit as st
import warnings
from sklearn.model_selection import train_test_split

# Import configurations
from config import (
    PAGE_TITLE, PAGE_ICON, LAYOUT,
    TARGET_COLUMN, TEST_SIZE, RANDOM_STATE, CV_FOLDS
)

# Import utilities
from utils.data_loader import load_data_with_ui
from utils.data_processor import decode_dataframe, filter_dataframe
from utils.model_trainer import train_and_evaluate, get_feature_importance

# Import components
from components.header import render_header, render_footer
from components.sidebar import (
    render_feature_selector,
    render_filters,
    render_model_selector,
    render_user_input_form
)
from components.data_display import (
    render_data_info,
    render_dataset_preview,
    render_summary_statistics
)
from components.visualizations import render_visualizations
from components.model_evaluation import render_model_evaluation
from components.prediction import render_prediction

warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Render header
    render_header()
    
    # Load data
    df_raw = load_data_with_ui()
    
    # Decode data for display
    df_display = decode_dataframe(df_raw)
    
    # ========================================================================
    # SIDEBAR - Feature Selection, Filters, Model Selection, User Input
    # ========================================================================
    
    selected_features = render_feature_selector(df_display.columns.tolist())
    filters = render_filters(df_display)
    model_choice = render_model_selector()
    user_input, predict_button = render_user_input_form(df_display)
    
    # ========================================================================
    # APPLY FILTERS
    # ========================================================================
    
    filtered_display = filter_dataframe(df_display, filters)
    filtered_raw = df_raw.loc[filtered_display.index]
    
    # ========================================================================
    # MAIN CONTENT
    # ========================================================================
    
    # Data info
    render_data_info(filtered_display, df_display)
    
    # Dataset preview
    render_dataset_preview(filtered_display, selected_features)
    st.markdown("---")
    
    # Summary statistics
    render_summary_statistics(filtered_display)
    st.markdown("---")
    
    # Visualizations
    render_visualizations(filtered_display)
    st.markdown("---")
    
    # ========================================================================
    # MODEL TRAINING AND EVALUATION
    # ========================================================================
    
    if len(filtered_raw) < 10:
        st.error("⚠️ Not enough data to train model. Please adjust filters.")
    else:
        # Prepare data for modeling
        X = filtered_raw.drop(TARGET_COLUMN, axis=1)
        y = filtered_raw[TARGET_COLUMN]
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE
        )
        
        # Train model
        with st.spinner(f'Training {model_choice} model...'):
            model, y_pred, metrics = train_and_evaluate(
                X_train, X_test, y_train, y_test,
                model_choice, CV_FOLDS
            )
        
        st.success(f"✅ {model_choice} model trained successfully!")
        
        # Get feature importance (if applicable)
        importance_df = get_feature_importance(
            model, X.columns.tolist(), model_choice
        )
        
        # Render model evaluation
        render_model_evaluation(
            y_test, y_pred, metrics,
            model_choice, importance_df
        )
        
        st.markdown("---")
        
        # ====================================================================
        # USER PREDICTION
        # ====================================================================
        
        if predict_button:
            render_prediction(user_input, model, X.columns.tolist())
    
    # Render footer
    render_footer()

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()