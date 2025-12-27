import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Student Exam Score Predictor",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# FUNCTIONS
# ============================================================================

@st.cache_data
def load_data(filepath='cleaned_data.csv'):
    """Load the existing dataset from CSV file"""
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        st.error(f"❌ Error: File '{filepath}' not found. Please ensure the file is in the same directory as the script.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

def get_categorical_mappings():
    """Return mappings for encoded categorical variables"""
    mappings = {
        'gender': {0: 'Female', 1: 'Male'},
        'course': {0: 'Biology', 1: 'Chemistry', 2: 'Computer Science', 3: 'Mathematics', 4: 'Physics'},
        'internet_access': {0: 'No', 1: 'Yes'},
        'sleep_quality': {0: 'Poor', 1: 'Fair', 2: 'Good', 3: 'Excellent'},
        'study_method': {0: 'Self-Study', 1: 'Group Study', 2: 'Online Courses', 3: 'Tutoring'},
        'exam_difficulty': {0: 'Easy', 1: 'Medium', 2: 'Hard'}
    }
    return mappings

def decode_data(df):
    """Decode categorical variables for display"""
    df_decoded = df.copy()
    mappings = get_categorical_mappings()
    
    for col, mapping in mappings.items():
        if col in df_decoded.columns:
            df_decoded[col] = df_decoded[col].map(mapping)
    
    return df_decoded

def train_model(X_train, X_test, y_train, y_test, model_name):
    """Train selected model and return metrics"""
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'Decision Tree': DecisionTreeRegressor(random_state=42),
        'SVR': SVR(kernel='rbf')
    }
    
    model = models[model_name]
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
    
    return model, y_pred, {'MSE': mse, 'RMSE': rmse, 'MAE': mae, 'R²': r2, 'CV_Scores': cv_scores}

# ============================================================================
# MAIN APP
# ============================================================================

# Title and description
st.markdown('<p class="main-header">📚 Student Exam Score Prediction System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Analyze student performance factors and predict exam scores using machine learning</p>', unsafe_allow_html=True)

st.markdown("---")

# Load or generate data
st.sidebar.header("📁 Data Source")
data_source = st.sidebar.radio("Choose data source:", ["Load from CSV", "Upload CSV file"])

if data_source == "Load from CSV":
    csv_path = st.sidebar.text_input("CSV file path:", "cleaned_data.csv")
    if st.sidebar.button("Load Data"):
        df_raw = load_data(csv_path)
        st.session_state['df_raw'] = df_raw
        st.session_state['data_loaded'] = True
        st.sidebar.success(f"✅ Loaded {len(df_raw)} records!")
else:
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=['csv'])
    if uploaded_file is not None:
        df_raw = pd.read_csv(uploaded_file)
        st.session_state['df_raw'] = df_raw
        st.session_state['data_loaded'] = True
        st.sidebar.success(f"✅ Uploaded {len(df_raw)} records!")

# Initialize session state
if 'data_loaded' not in st.session_state:
    # Try to load default file
    try:
        df_raw = load_data('cleaned_data.csv')
        st.session_state['df_raw'] = df_raw
        st.session_state['data_loaded'] = True
    except:
        st.warning("⚠️ Please load your dataset using the sidebar options")
        st.stop()

# Get the data
df_raw = st.session_state['df_raw']

# Decode categorical variables for display
df = decode_data(df_raw)

# ============================================================================
# SIDEBAR
# ============================================================================

st.sidebar.header("🎛️ Control Panel")

# Feature selection
st.sidebar.subheader("📊 Select Features to Display")
all_columns = df.columns.tolist()
selected_features = st.sidebar.multiselect(
    "Choose features:",
    all_columns,
    default=all_columns
)

# Filters
st.sidebar.subheader("🔍 Filter Data")

# Get unique values for filters
courses = ['All'] + sorted(df['course'].dropna().unique().tolist())
selected_course = st.sidebar.selectbox("Course:", courses)

genders = ['All'] + sorted(df['gender'].dropna().unique().tolist())
selected_gender = st.sidebar.selectbox("Gender:", genders)

study_methods = ['All'] + sorted(df['study_method'].dropna().unique().tolist())
selected_study_method = st.sidebar.selectbox("Study Method:", study_methods)

internet_options = ['All'] + sorted(df['internet_access'].dropna().unique().tolist())
selected_internet = st.sidebar.selectbox("Internet Access:", internet_options)

# Apply filters
filtered_df = df.copy()
if selected_course != 'All':
    filtered_df = filtered_df[filtered_df['course'] == selected_course]
if selected_gender != 'All':
    filtered_df = filtered_df[filtered_df['gender'] == selected_gender]
if selected_study_method != 'All':
    filtered_df = filtered_df[filtered_df['study_method'] == selected_study_method]
if selected_internet != 'All':
    filtered_df = filtered_df[filtered_df['internet_access'] == selected_internet]

# Model selection
st.sidebar.subheader("🤖 Select Regression Model")
model_choice = st.sidebar.selectbox(
    "Choose model:",
    ['Linear Regression', 'Random Forest', 'Decision Tree', 'SVR']
)

st.sidebar.markdown("---")

# User input for prediction
st.sidebar.subheader("🎯 Predict Exam Score")
st.sidebar.write("Enter student details:")

user_study_hours = st.sidebar.slider("Study Hours per Day:", 0.0, 24.0, 5.0, 0.5)
user_attendance = st.sidebar.slider("Class Attendance (%):", 0.0, 100.0, 85.0, 1.0)
user_sleep_hours = st.sidebar.slider("Sleep Hours per Day:", 0.0, 24.0, 7.0, 0.5)
user_gender = st.sidebar.selectbox("Gender:", sorted(df['gender'].dropna().unique()))
user_course = st.sidebar.selectbox("Course:", sorted(df['course'].dropna().unique()))
user_internet = st.sidebar.selectbox("Internet Access:", sorted(df['internet_access'].dropna().unique()))
user_sleep_quality = st.sidebar.selectbox("Sleep Quality:", sorted(df['sleep_quality'].dropna().unique()))
user_study_method = st.sidebar.selectbox("Study Method:", sorted(df['study_method'].dropna().unique()))
user_facility = st.sidebar.slider("Facility Rating:", 1, 5, 3)
user_difficulty = st.sidebar.selectbox("Exam Difficulty:", sorted(df['exam_difficulty'].dropna().unique()))

predict_button = st.sidebar.button("🎓 Predict Score")

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Display filtered data count
st.info(f"📋 Showing {len(filtered_df)} records out of {len(df)} total records")

# Dataset Preview
st.header("1️⃣ Dataset Preview")
if selected_features:
    st.dataframe(filtered_df[selected_features].head(20), use_container_width=True)
else:
    st.warning("⚠️ Please select at least one feature to display")

st.markdown("---")

# Summary Statistics
st.header("2️⃣ Summary Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Average Exam Score", f"{filtered_df['exam_score'].mean():.2f}")
with col2:
    st.metric("Average Study Hours", f"{filtered_df['study_hours'].mean():.2f}")
with col3:
    st.metric("Average Attendance", f"{filtered_df['class_attendance'].mean():.2f}%")
with col4:
    st.metric("Average Sleep Hours", f"{filtered_df['sleep_hours'].mean():.2f}")

# Detailed statistics
st.subheader("Detailed Statistics")
numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
st.dataframe(filtered_df[numeric_cols].describe(), use_container_width=True)

st.markdown("---")

# Visualizations
st.header("3️⃣ Data Visualizations")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribution Analysis", "📈 Correlation Analysis", "🎯 Feature vs Score", "📉 Categorical Analysis"])

with tab1:
    st.subheader("Exam Score Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(filtered_df['exam_score'], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    ax.set_xlabel('Exam Score', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title('Distribution of Exam Scores', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    st.pyplot(fig)

with tab2:
    st.subheader("Correlation Heatmap")
    numeric_data = filtered_df.select_dtypes(include=[np.number])
    
    fig, ax = plt.subplots(figsize=(12, 8))
    correlation = numeric_data.corr()
    sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax, linewidths=0.5)
    ax.set_title('Feature Correlation Matrix', fontsize=14, fontweight='bold')
    st.pyplot(fig)

with tab3:
    st.subheader("Key Features vs Exam Score")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Study hours vs exam score
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(filtered_df['study_hours'], filtered_df['exam_score'], alpha=0.5, color='blue')
        ax.set_xlabel('Study Hours', fontsize=12)
        ax.set_ylabel('Exam Score', fontsize=12)
        ax.set_title('Study Hours vs Exam Score', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        # Attendance vs exam score
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(filtered_df['class_attendance'], filtered_df['exam_score'], alpha=0.5, color='green')
        ax.set_xlabel('Class Attendance (%)', fontsize=12)
        ax.set_ylabel('Exam Score', fontsize=12)
        ax.set_title('Attendance vs Exam Score', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        st.pyplot(fig)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Sleep hours vs exam score
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(filtered_df['sleep_hours'], filtered_df['exam_score'], alpha=0.5, color='purple')
        ax.set_xlabel('Sleep Hours', fontsize=12)
        ax.set_ylabel('Exam Score', fontsize=12)
        ax.set_title('Sleep Hours vs Exam Score', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        st.pyplot(fig)
    
    with col4:
        # Facility rating vs exam score
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(filtered_df['facility_rating'], filtered_df['exam_score'], alpha=0.5, color='orange')
        ax.set_xlabel('Facility Rating', fontsize=12)
        ax.set_ylabel('Exam Score', fontsize=12)
        ax.set_title('Facility Rating vs Exam Score', fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        st.pyplot(fig)

with tab4:
    st.subheader("Categorical Feature Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Average score by course
        fig, ax = plt.subplots(figsize=(10, 6))
        avg_by_course = filtered_df.groupby('course')['exam_score'].mean().sort_values()
        avg_by_course.plot(kind='barh', ax=ax, color='steelblue')
        ax.set_xlabel('Average Exam Score', fontsize=12)
        ax.set_ylabel('Course', fontsize=12)
        ax.set_title('Average Score by Course', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        # Average score by study method
        fig, ax = plt.subplots(figsize=(10, 6))
        avg_by_method = filtered_df.groupby('study_method')['exam_score'].mean().sort_values()
        avg_by_method.plot(kind='barh', ax=ax, color='coral')
        ax.set_xlabel('Average Exam Score', fontsize=12)
        ax.set_ylabel('Study Method', fontsize=12)
        ax.set_title('Average Score by Study Method', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig)

st.markdown("---")

# Model Training and Evaluation
st.header("4️⃣ Model Training & Evaluation")

if len(filtered_df) < 10:
    st.error("⚠️ Not enough data to train model. Please adjust filters.")
else:
    # Use raw encoded data for modeling
    filtered_df_raw = df_raw.loc[filtered_df.index]
    
    # Features and target
    X = filtered_df_raw.drop('exam_score', axis=1)
    y = filtered_df_raw['exam_score']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    with st.spinner(f'Training {model_choice} model...'):
        model, y_pred, metrics = train_model(X_train, X_test, y_train, y_test, model_choice)
    
    st.success(f"✅ {model_choice} model trained successfully!")
    
    # Display metrics
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
    
    # Cross-validation results
    st.subheader("🔄 Cross-Validation Results (5-Fold)")
    cv_col1, cv_col2, cv_col3 = st.columns(3)
    
    with cv_col1:
        st.metric("Mean CV R²", f"{metrics['CV_Scores'].mean():.4f}")
    with cv_col2:
        st.metric("Std CV R²", f"{metrics['CV_Scores'].std():.4f}")
    with cv_col3:
        st.metric("Min CV R²", f"{metrics['CV_Scores'].min():.4f}")
    
    # Plot predictions vs actual
    st.subheader("🎯 Predictions vs Actual Values")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(y_test, y_pred, alpha=0.6, color='blue', label='Predictions')
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='Perfect Prediction')
    ax.set_xlabel('Actual Exam Score', fontsize=12)
    ax.set_ylabel('Predicted Exam Score', fontsize=12)
    ax.set_title(f'{model_choice}: Predictions vs Actual', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    
    # Residuals plot
    st.subheader("📉 Residuals Plot")
    residuals = y_test - y_pred
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(y_pred, residuals, alpha=0.6, color='purple')
    ax.axhline(y=0, color='r', linestyle='--', lw=2)
    ax.set_xlabel('Predicted Exam Score', fontsize=12)
    ax.set_ylabel('Residuals', fontsize=12)
    ax.set_title('Residuals Plot', fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    
    # Feature importance (for tree-based models)
    if model_choice in ['Random Forest', 'Decision Tree']:
        st.subheader("📈 Feature Importance")
        
        feature_importance = pd.DataFrame({
            'Feature': X.columns,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(feature_importance['Feature'], feature_importance['Importance'], color='teal')
        ax.set_xlabel('Importance', fontsize=12)
        ax.set_ylabel('Feature', fontsize=12)
        ax.set_title('Feature Importance', fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig)
    
    st.markdown("---")
    
    # User prediction
    if predict_button:
        st.header("5️⃣ Prediction for New Student")
        
        # Get reverse mappings
        mappings = get_categorical_mappings()
        reverse_mappings = {col: {v: k for k, v in mapping.items()} for col, mapping in mappings.items()}
        
        # Prepare user input (encode categorical values)
        user_data = {
            'study_hours': user_study_hours,
            'class_attendance': user_attendance,
            'sleep_hours': user_sleep_hours,
            'gender': reverse_mappings['gender'][user_gender],
            'course': reverse_mappings['course'][user_course],
            'internet_access': reverse_mappings['internet_access'][user_internet],
            'sleep_quality': reverse_mappings['sleep_quality'][user_sleep_quality],
            'study_method': reverse_mappings['study_method'][user_study_method],
            'facility_rating': user_facility,
            'exam_difficulty': reverse_mappings['exam_difficulty'][user_difficulty]
        }
        
        user_df = pd.DataFrame([user_data])
        
        # Reorder columns to match training data
        user_df = user_df[X.columns]
        
        # Make prediction
        prediction = model.predict(user_df)[0]
        
        st.success(f"🎓 **Predicted Exam Score: {prediction:.2f}**")
        
        # Display input details
        st.subheader("Input Details:")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"📚 Study Hours: {user_study_hours}")
            st.write(f"📅 Attendance: {user_attendance}%")
            st.write(f"😴 Sleep Hours: {user_sleep_hours}")
            st.write(f"👤 Gender: {user_gender}")
            st.write(f"📖 Course: {user_course}")
        
        with col2:
            st.write(f"🌐 Internet Access: {user_internet}")
            st.write(f"💤 Sleep Quality: {user_sleep_quality}")
            st.write(f"📝 Study Method: {user_study_method}")
            st.write(f"🏫 Facility Rating: {user_facility}")
            st.write(f"📊 Exam Difficulty: {user_difficulty}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px;'>
    <p>📚 Student Exam Score Prediction System | Built with Streamlit & Scikit-learn</p>
    <p>Adjust filters and model parameters in the sidebar to explore different scenarios</p>
</div>
""", unsafe_allow_html=True)