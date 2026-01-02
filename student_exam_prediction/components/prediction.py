# components/prediction.py
# User prediction components

import streamlit as st
import pandas as pd
from utils.data_processor import encode_user_input

def render_prediction(user_input, model, feature_columns):
    '''Render prediction results'''
    st.header("5️⃣ Prediction for New Student")
    
    # Encode and prepare data
    encoded_input = encode_user_input(user_input)
    user_df = pd.DataFrame([encoded_input])
    user_df = user_df[feature_columns]
    
    # Make prediction
    prediction = model.predict(user_df)[0]
    
    st.success(f"🎓 **Predicted Exam Score: {prediction:.2f}**")
    
    # Display input details
    st.subheader("Input Details:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"📚 Study Hours: {user_input['study_hours']}")
        st.write(f"📅 Attendance: {user_input['class_attendance']}%")
        st.write(f"😴 Sleep Hours: {user_input['sleep_hours']}")
        st.write(f"👤 Gender: {user_input['gender']}")
        st.write(f"📖 Course: {user_input['course']}")
    
    with col2:
        st.write(f"🌐 Internet Access: {user_input['internet_access']}")
        st.write(f"💤 Sleep Quality: {user_input['sleep_quality']}")
        st.write(f"📝 Study Method: {user_input['study_method']}")
        st.write(f"🏫 Facility Rating: {user_input['facility_rating']}")
        st.write(f"📊 Exam Difficulty: {user_input['exam_difficulty']}")