# -Digital-Architects
Our team name is Digital Architects and we are going to design a Major Project.

<p align="center">
  <h1 align="center">🎓 AI-Scholar: Student Performance Prediction & Early Warning System</h1>
  <p align="center">
    <strong>An Intelligent ML-powered system to identify at-risk students and provide actionable academic insights.</strong>
  </p>
  <p align="center">
    Built with Python · Machine Learning · Streamlit · SQLite3 · Plotly
  </p>
</p>

<p align="center">
  <a href="https://ai-student-performance-system.streamlit.app"><strong>🔴 Live Demo</strong></a>
  ·
  <a href="#-try-it-instantly-demo-accounts">Demo Accounts</a>
  ·
  <a href="#-getting-started-run-locally">Run Locally</a>
  ·
  <a href="#-help--faq">FAQ</a>
</p>

---

<p align="center">
  <img src="https://img.shields.io/badge/Status-Live-success?style=for-the-badge" alt="Live"/>
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" alt="Python Version"/>
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/ML--Model-Random%20Forest-green?style=for-the-badge" alt="ML Model"/>
  <img src="https://img.shields.io/badge/Database-SQLite3-003B57?style=for-the-badge&logo=sqlite" alt="SQLite"/>
</p>

## 🌐 Live Application

**👉 [ai-student-performance-system.streamlit.app](https://ai-student-performance-system.streamlit.app)**

No setup needed — open the link and try it directly in your browser.

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
| 🎓 **Instant Demo Access** | Pre-seeded demo accounts for every role — no invite key required to explore. |
| ❓ **Built-in Help & Support** | In-app FAQ section plus direct support and GitHub issue links. |

## 🚀 Try It Instantly (Demo Accounts)

Open the [live app](https://ai-student-performance-system.streamlit.app) → go to **Login / Register** → expand **"Try a demo account"** and sign in with:

| Role | Username | Password |
|------|----------|----------|
| Student | `demo_student` | `Demo@123` |
| Mentor | `demo_mentor` | `Demo@123` |
| Admin | `demo_admin` | `Demo@123` |

Mentor and Admin **self-registration** requires a verification key — reach out via the Support link in the app footer if you need one.

## 📁 Project Structure

```text
Student-Performance-System/
│
├── models/                  # 🧠 Pre-trained ML models (.pkl files)
├── Student_Performance_Dataset.csv   # 📊 Student dataset used for predictions
├── app.py                   # 🖥️ Main Streamlit application (Frontend + Backend)
├── requirements.txt         # 📦 Python dependencies
├── users.db                 # 🗄️ Local SQLite database for credentials (auto-created, gitignored)
├── .gitignore               # 🚫 Files ignored by Git (venv, pycache, users.db)
└── README.md                # 📝 Project Documentation
```

## 🛠️ Tech Stack

- **Language:** Python 3.11
- **ML Libraries:** Scikit-learn (Random Forest), Pandas, NumPy
- **Web Framework:** Streamlit (for a fast, interactive UI)
- **Visualization:** Plotly & Seaborn (for professional charts)
- **Database:** SQLite3 (for user management and role-based access)
- **Deployment:** Streamlit Community Cloud

## 🚀 Getting Started (Run Locally)

```bash
# 1. Clone the repo
git clone https://github.com/Dagar214/-Digital-Architects.git
cd -Digital-Architects

# 2. Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## 🔍 How It Works (Logic Flow)

1. **Data Ingestion:** The system takes inputs like Attendance, Previous GPA, Study Hours, and Extracurricular activities.
2. **ML Processing:** The pre-trained model analyzes the features against historical patterns.
3. **Classification:** Output is generated as a "Warning Level" (Low, Medium, High).
4. **Actionable Insights:** Mentors see a list of students who need immediate attention.

## ❓ Help & FAQ

**How do I get access without a verification key?**
Use one of the [demo accounts](#-try-it-instantly-demo-accounts) — no key required.

**How do I register as a Mentor or Admin?**
You'll need a verification key. Reach out via the Support link in the app footer to request one.

**My student dashboard shows no data — why?**
Your registered University Roll Number must exactly match a roll number already present in the dataset.

**Found a bug or have a feature idea?**
Open an [issue on GitHub](https://github.com/Dagar214/-Digital-Architects/issues) or reach out via [LinkedIn](https://www.linkedin.com/in/dev-dagar-0a3b81307).

<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed-success?style=flat-square" />
  <img src="https://img.shields.io/badge/Contributions-Welcome-blue?style=flat-square" />
</p>

## 👥 Team Members

<div align="center">

| Role | Name | University Roll No. |
|------|------|--------------------|
| Team Lead | [Dev Dagar](https://www.linkedin.com/in/dev-dagar-0a3b81307) | 2301730073 |
| Member | Shubhi Tyagi | 2301730132 |
| Member | Aryan Sharma | 2301730119 |
| Member | Dev Sood | 2301730121 |

</div>