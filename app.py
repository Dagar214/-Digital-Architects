import streamlit as st
import pandas as pd
import joblib
import sqlite3
import hashlib
import plotly.express as px
import plotly.graph_objects as go
import time

# --- 1. CORE LOGIC & SECURITY ---

def create_usertable():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT PRIMARY KEY, password TEXT, role TEXT, roll_no TEXT)')
    conn.commit()
    conn.close()

def add_userdata(username, password, role, roll_no=""):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO userstable(username, password, role, roll_no) VALUES (?,?,?,?)', (username, password, role, roll_no))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    conn.close()
    return data

def view_all_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username, role, roll_no FROM userstable')
    data = c.fetchall()
    conn.close()
    return data

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- OPTIMIZATION: CACHING DATA & MODELS ---
@st.cache_data
def load_data():
    return pd.read_csv('Student_Performance_Dataset.csv')

@st.cache_resource
def load_assets():
    model = joblib.load('models/student_risk_model.pkl')
    metadata = joblib.load('models/model_metadata.pkl')
    return model, metadata

# --- CONFIGURATION ---
ADMIN_SECRET_KEY = "ADMIN123"
MENTOR_SECRET_KEY = "MENTOR456"

# --- 2. USER INTERFACE ---
def main():
    st.set_page_config(page_title="AI-Based Student Performance Prediction & Early Warning System", layout="wide")
    create_usertable()

    st.markdown("""
        <style>
        .main { background-color: #ffffff; }
        .stButton>button { width: 100%; border-radius: 4px; background-color: #004a99; color: white; border: none; height: 3em; }
        .stMetric { border: 1px solid #e6e6e6; padding: 15px; border-radius: 5px; background-color: #f9f9f9; }
        .hero-section { background-color: #002b5c; padding: 40px; border-radius: 8px; color: white; text-align: left; margin-bottom: 25px; }
        .sidebar-user { padding: 10px; background-color: #f0f2f6; border-radius: 5px; margin-bottom: 20px; border-left: 5px solid #004a99; }
        </style>
        """, unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['role'] = None
        st.session_state['username'] = ""
        st.session_state['roll_no'] = ""

    if not st.session_state['logged_in']:
        app_mode = st.sidebar.radio("Navigation", ["Project Overview", "Login / Register"])

        if app_mode == "Project Overview":
            st.markdown('<div class="hero-section"><h1>AI-Based Student Performance Prediction & Early Warning System</h1><p><b>PHASE 1: Core Analytical Framework</b></p></div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                st.subheader("1. Predictive Analytics")
                st.write("Random Forest Classification for academic risk identification.")
            with c2:
                st.subheader("2. Communication Gateway")
                st.warning("Integration with SMS/Email API (Work in Progress for Final Phase)")
            with c3:
                st.subheader("3. Dashboard Interface")
                st.write("Real-time performance tracking for Mentors.")
            st.divider()
            st.info(" Login to access Phase 1 Dashboards.")

        elif app_mode == "Login / Register":
            st.title("System Authentication")
            choice = st.segmented_control("Select Action", ["Login", "Register"], default="Login")
            if choice == "Login":
                user = st.text_input("Username")
                pswd = st.text_input("Password", type='password')
                if st.button("Access Dashboard"):
                    result = login_user(user, make_hashes(pswd))
                    if result:
                        st.session_state['logged_in'], st.session_state['username'], st.session_state['role'], st.session_state['roll_no'] = True, result[0][0], result[0][2], result[0][3]
                        st.rerun()
                    else: st.error("Invalid Credentials")
            elif choice == "Register":
                st.subheader("New User Registration")
                new_user, new_pswd, role = st.text_input("Username"), st.text_input("Password", type='password'), st.selectbox("Role Assignment", ["Student", "Mentor", "Admin"])
                reg_roll_no = st.text_input("Enter University Roll Number") if role == "Student" else ""
                key_required = role in ["Admin", "Mentor"]
                access_key = st.text_input(f"Verification Key", type='password') if key_required else ""
                if st.button("Create Account"):
                    if (role == "Admin" and access_key == ADMIN_SECRET_KEY) or (role == "Mentor" and access_key == MENTOR_SECRET_KEY) or role == "Student":
                        if add_userdata(new_user, make_hashes(new_pswd), role, reg_roll_no): st.success("Registration Successful!")
                        else: st.error("Username already exists.")
                    else: st.error("Invalid Secret Key")

    else:
        # --- SIDEBAR ---
        st.sidebar.title("Navigation")
        st.sidebar.markdown(f"**User:** {st.session_state['username']}\n\n**Role:** {st.session_state['role']}")
        st.sidebar.button("Sign Out", on_click=lambda: st.session_state.update({"logged_in": False}))
        
        role = st.session_state['role']
        
        try:
            df, (model, metadata) = load_data(), load_assets()
            feature_cols = metadata['features']

            if role == "Admin":
                st.title("Administrative Control")
                with st.expander("User Account Management", expanded=True):
                    all_users = view_all_users()
                    user_df = pd.DataFrame(all_users, columns=['Username', 'Role', 'Roll_No'])
                    st.table(user_df)
                    st.info("User Deletion & Logging features will be enabled in Phase 2.")

            if role in ["Admin", "Mentor"]:
                st.title("Mentor Insight Dashboard")
                g1, g2 = st.columns(2)
                g1.plotly_chart(px.pie(df, names='Risk_Level', title='Risk Level Distribution'), use_container_width=True)
                g2.plotly_chart(px.scatter(df, x='Total_%', y='Predicted_GPA', color='Risk_Level', title='Attendance vs Performance'), use_container_width=True)
                
                st.divider()
                st.subheader("Student Database (Filter & Search)")
                risk_f = st.multiselect("Filter Status", ['Low', 'Medium', 'High'], default=['High', 'Medium'])
                filtered_df = df[df['Risk_Level'].isin(risk_f)]
                st.dataframe(filtered_df[['Rollno', 'Student Name', 'Total_%', 'Risk_Level']], use_container_width=True)

                if not filtered_df.empty:
                    st.divider()
                    st.subheader("Communication Portal")
                    st.info("⚠️ SMS API Connection pending. Notification logging will be part of the final submission.")
                    if st.button("Send Alert (Phase 2 Preview)"):
                        st.warning("This feature is scheduled for implementation in the next phase.")

            elif role == "Student":
                st.title(f"Student Portal: {st.session_state['username']}")
                student_row = df[df['Rollno'].astype(str) == st.session_state['roll_no']] if st.session_state['roll_no'] else df[df['Student Name'].str.contains(st.session_state['username'], case=False)]
                
                if not student_row.empty:
                    s_row = student_row.iloc[0]
                    st.subheader("Academic Overview")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Attendance", f"{s_row['Total_%']}%")
                    m2.metric("Projected GPA", s_row['Predicted_GPA'])
                    m3.metric("Risk Level", s_row['Risk_Level'])

                    # Comparison Graph
                    class_avg = df[feature_cols].mean()
                    fig_comp = go.Figure()
                    fig_comp.add_trace(go.Bar(x=feature_cols, y=s_row[feature_cols], name='Personal'))
                    fig_comp.add_trace(go.Bar(x=feature_cols, y=class_avg, name='Class Avg'))
                    st.plotly_chart(fig_comp, use_container_width=True)
                    
                    st.divider()
                    st.subheader("Future Milestones")
                    st.info("Coming Soon: Personalized Subject Proficiency Analysis and Study Suggestions.")
                else:
                    st.warning("Profile records not synchronized in mid-term database.")

        except Exception as e:
            st.error(f"Module Loading Error: {e}")

if __name__ == '__main__':
    main()





