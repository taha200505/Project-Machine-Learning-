# Student Exam Score Prediction System

A comprehensive Streamlit application for analyzing student performance data and predicting exam scores using machine learning.

## 📁 Project Structure

```
student_exam_prediction/
│
├── app.py                          # Main application entry point
├── config.py                       # Configuration and constants
├── requirements.txt                # Project dependencies
├── cleaned_data.csv                # Dataset file
│
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── data_loader.py              # Data loading utilities
│   ├── data_processor.py           # Data processing and encoding
│   └── model_trainer.py            # Model training utilities
│
├── components/                     # UI components
│   ├── __init__.py
│   ├── sidebar.py                  # Sidebar components
│   ├── header.py                   # Header and footer
│   ├── data_display.py             # Data preview and statistics
│   ├── visualizations.py           # Charts and plots
│   ├── model_evaluation.py         # Model metrics and evaluation
│   └── prediction.py               # User input and prediction
│
└── styles/                         # Styling modules
    ├── __init__.py
    └── custom_css.py               # Custom CSS
```

## 🚀 Installation

1. Clone the repository or extract the files
2. Navigate to the project directory
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## 💻 Usage

Run the application:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📊 Features

### Data Management
- Load data from CSV file
- Upload custom CSV files
- Interactive filtering by course, gender, study method, and internet access
- Feature selection for data display

### Data Analysis
- Comprehensive summary statistics
- Interactive visualizations:
  - Distribution analysis
  - Correlation heatmap
  - Scatter plots for key features
  - Categorical analysis

### Machine Learning
- Multiple regression models:
  - Linear Regression
  - Random Forest
  - Decision Tree
  - Support Vector Regression (SVR)
- Model performance metrics (R², RMSE, MAE, MSE)
- 5-fold cross-validation
- Feature importance visualization
- Predictions vs actual plot
- Residuals analysis

### Prediction
- Interactive form for new student data
- Real-time exam score prediction
- Detailed input summary

## 📝 Dataset Requirements

The dataset should contain the following columns:
- `study_hours` (float): Study hours per day
- `class_attendance` (float): Attendance percentage
- `sleep_hours` (float): Sleep hours per day
- `exam_score` (float): Target variable
- `gender` (int): Encoded gender (0=Female, 1=Male)
- `course` (int): Encoded course (0-4)
- `internet_access` (int): Encoded (0=No, 1=Yes)
- `sleep_quality` (int): Encoded (0-3)
- `study_method` (int): Encoded (0-3)
- `facility_rating` (int): Rating (1-5)
- `exam_difficulty` (int): Encoded (0-2)

## 🎨 Customization

### Modifying Categorical Mappings

Edit `config.py` to change the categorical mappings:

```python
CATEGORICAL_MAPPINGS = {
    'gender': {0: 'Female', 1: 'Male'},
    # ... other mappings
}
```

### Adding New Models

1. Add model configuration to `config.py`:
```python
MODEL_PARAMS = {
    'new_model': {
        'param1': value1,
        'param2': value2
    }
}
```

2. Update `utils/model_trainer.py`:
```python
from sklearn.new_module import NewModel

def get_model(model_name):
    models = {
        # ... existing models
        'New Model': NewModel(**MODEL_PARAMS['new_model'])
    }
    return models.get(model_name)
```

3. Add to model selection in `components/sidebar.py`

### Customizing Visualizations

Add new visualization functions to `components/visualizations.py`:

```python
def plot_new_chart(df, params):
    fig, ax = plt.subplots(figsize=(10, 6))
    # Your plotting code
    return fig
```

## 🔧 Troubleshooting

### Issue: "File not found"
- Ensure `cleaned_data.csv` is in the project root directory
- Check the file path in the sidebar

### Issue: "Not enough data to train model"
- Adjust filters to include more data
- Ensure dataset has at least 10 records

### Issue: Import errors
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+ recommended)

## 📦 Microservices Architecture Benefits

This modular structure provides:
- **Maintainability**: Each component is isolated and easy to update
- **Scalability**: Add new features without affecting existing code
- **Reusability**: Components can be reused in other projects
- **Testing**: Easy to test individual modules
- **Collaboration**: Multiple developers can work on different modules

## 📄 License

This project is open source and available for educational purposes.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or feedback, please open an issue in the repository.