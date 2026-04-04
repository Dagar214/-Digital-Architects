# -Digital-Architects
Our team name is Digital Architects and we are going to design a Major Project.

<p align="center">
  <h1 align="center">🎓 Student Performance Prediction & Early Warning System</h1>
  <p align="center">
    <strong>An Intelligent ML-powered system to identify at-risk students and provide actionable academic insights.</strong>
  </p>
  <p align="center">
    Built with Python · Machine Learning · Streamlit · SQLite3 · Plotly
  </p>
</p>

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" alt="Python Version"/>
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/ML--Model-Random%20Forest-green?style=for-the-badge" alt="ML Model"/>
  <img src="https://img.shields.io/badge/Database-SQLite3-003B57?style=for-the-badge&logo=sqlite" alt="SQLite"/>
</p>

## 🧐 Problem Statement
Educational institutions often struggle to identify students who are likely to struggle academically until it's too late. Manually tracking attendance, previous grades, and participation for hundreds of students is inefficient and prone to error.

**Our Solution:** This project automates the identification of "High Risk" students by analyzing their academic patterns, allowing mentors to intervene early and improve overall institutional results.

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔐 **Multi-Role Auth** | Separate secure portals for Admins, Mentors, and Students. |
| 🧠 **Predictive Engine** | ML model that classifies students into Low, Medium, or High risk categories. |
| 📊 **Live Analytics** | Interactive Plotly dashboards showing Attendance vs. GPA trends. |
| 🛡️ **Secure DB** | SQLite3 integration with SHA-256 password hashing for data privacy. |
| 📥 **Data Management** | Easy CSV-based dataset upload and processing. |

## 📁 Project Structure

```text
Student-Performance-System/
│
├── models/                  # 🧠 Pre-trained ML models (.pkl files)
├── Dataset.csv              # 📊 Sample student data for training/testing
├── app.py                   # 🖥️ Main Streamlit application (Frontend + Backend)
├── requirements.txt         # 📦 Python dependencies
├── users.db                 # 🗄️ Local SQLite database for credentials
├── .gitignore               # 🚫 Files to be ignored by Git (venv, pycache)
└── README.md                # 📝 Project Documentation
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.11 |
| **ML Libraries** | Scikit-learn (Random Forest), Pandas, NumPy |
| **Web Framework** | Streamlit |
| **Visualization** | Plotly & Seaborn |
| **Database** | SQLite3 |

## 🚀 Getting Started

1. Clone the Repo: git clone [https://github.com/Dagar214/-Digital-Architects.git](https://github.com/Dagar214/-Digital-Architects.git)

2. Install Dependencies: pip install -r requirements.txt

3. Run the App: streamlit run app.py

## 🔍 How it Works (Logic Flow)

1. Data Ingestion: The system takes inputs like Attendance, Previous GPA, Study Hours, and Extracurricular activities.

2. ML Processing: The pre-trained model analyzes the features against historical patterns.

3. Classification: Output is generated as a 'Warning Level' (Low, Medium, High).

4. Actionable Insights: Mentors see a list of students who need immediate attention

<p align="center">
Developed with ❤️ by <b>Team Digital Architects</b> for Major Project 2026
</p>

## 👥 Team Members

<div align="center">

| Role | Nam | University Roll No. |
|------|------|--------------------|
|  Team Lead | Dev Dagar | 2301730073 |
|  Member | Shubhi Tyagi | 2301730132 |
|  Member | Aryan Sharma | 2301730119 |
|  Member | Dev Sood | 2301730121 |

</div>
