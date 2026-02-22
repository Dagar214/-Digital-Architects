# -Digital-Architects
Our team name is Digital Architects and we are going to design a Major Project.

🎓 AI-Based Student Performance Prediction & Early Warning System
📌 Project Overview
This project is a comprehensive End-to-End Machine Learning solution designed for educational institutions. It proactively identifies students at risk of academic failure using historical data (grades, attendance, and engagement) and provides a real-time notification system for mentors and parents.

🚀 Key Features
AI Prediction Engine: Powered by a Random Forest Classifier to predict student risk levels (Low, Medium, High).

Secure Access Portal: Role-based access for Admin, Mentor, and Student with secret key protection.

Early Warning System: Automated SMS notification simulation to keep parents informed.

Nervous Learner Detection: Intelligent logic that identifies students with high practical skills but low theory performance.

Interactive Dashboards: Built with Streamlit and Plotly for real-time class-wide and individual analytics.

User Management: Admin panel to manage, view, and remove registered users.

🛠️ Tech Stack
Language: Python 3.x

Frontend: Streamlit (Custom CSS integrated)

Backend Database: SQLite (User Authentication)

Machine Learning: Scikit-learn, Pandas, NumPy, Joblib

Visualizations: Plotly Express, Plotly Graph Objects

📁 Project Structure
Plaintext
student-performance-system/
├── app.py                # Main Streamlit application
├── train_model.py        # Machine Learning training script
├── users.db              # SQLite database for authentication
├── requirements.txt      # List of dependencies
├── Student_Performance_Dataset.csv
└── models/               # Saved ML models & metadata
    ├── student_risk_model.pkl
    └── model_metadata.pkl
⚙️ Installation & Setup
Clone the repository:

Bash
git clone https://github.com/your-username/student-performance-system.git
cd student-performance-system
Set up virtual environment:

Bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
Install dependencies:

Bash
pip install -r requirements.txt
Run the application:

Bash
streamlit run app.py
🔐 Access Credentials
Admin Secret Key: ADMIN123

Mentor Secret Key: MENTOR456

👨‍💻 Author
Dev B.Tech CSE (AIML Specialization) [Your LinkedIn Profile Link] | [Your Portfolio Link]
