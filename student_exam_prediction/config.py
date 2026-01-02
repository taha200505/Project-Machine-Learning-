# config.py
# Configuration file with all constants and settings

# Page configuration
PAGE_TITLE = "Student Exam Score Predictor"
PAGE_ICON = "📚"
LAYOUT = "wide"

# File paths
DEFAULT_DATA_PATH = "cleaned_data.csv"

# Model options
MODELS = {
    'Linear Regression': 'linear',
    'Random Forest': 'random_forest',
    'Decision Tree': 'decision_tree',
    'SVR': 'svr'
}

# Categorical mappings
CATEGORICAL_MAPPINGS = {
    'gender': {0: 'Female', 1: 'Male'},
    'course': {
        0: 'Biology',
        1: 'Chemistry',
        2: 'Computer Science',
        3: 'Mathematics',
        4: 'Physics'
    },
    'internet_access': {0: 'No', 1: 'Yes'},
    'sleep_quality': {
        0: 'Poor',
        1: 'Fair',
        2: 'Good',
        3: 'Excellent'
    },
    'study_method': {
        0: 'Self-Study',
        1: 'Group Study',
        2: 'Online Courses',
        3: 'Tutoring'
    },
    'exam_difficulty': {0: 'Easy', 1: 'Medium', 2: 'Hard'}
}

# Feature configurations
NUMERIC_FEATURES = [
    'study_hours',
    'class_attendance',
    'sleep_hours',
    'facility_rating'
]

CATEGORICAL_FEATURES = [
    'gender',
    'course',
    'internet_access',
    'sleep_quality',
    'study_method',
    'exam_difficulty'
]

TARGET_COLUMN = 'exam_score'

# Slider configurations
SLIDER_CONFIG = {
    'study_hours': {'min': 0.0, 'max': 24.0, 'default': 5.0, 'step': 0.5},
    'class_attendance': {'min': 0.0, 'max': 100.0, 'default': 85.0, 'step': 1.0},
    'sleep_hours': {'min': 0.0, 'max': 24.0, 'default': 7.0, 'step': 0.5},
    'facility_rating': {'min': 1, 'max': 5, 'default': 3, 'step': 1}
}

# Model hyperparameters
MODEL_PARAMS = {
    'random_forest': {
        'n_estimators': 100,
        'random_state': 42
    },
    'decision_tree': {
        'random_state': 42
    },
    'svr': {
        'kernel': 'rbf'
    }
}

# Train-test split
TEST_SIZE = 0.2
RANDOM_STATE = 42
CV_FOLDS = 5
