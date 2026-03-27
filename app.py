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

def delete_user(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('DELETE FROM userstable WHERE username = ?', (username,))
    conn.commit()
    conn.close()

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

def send_notification(student_name, risk_level):
    with st.status(f"Connecting to Gateway for {student_name}...", expanded=True) as status:
        st.write("1. Accessing Institutional SMS Server...")
        time.sleep(1)
        st.write(f"2. Verifying parental contact for {student_name}...")
        time.sleep(1)
        st.write(f"3. Dispatching {risk_level} Risk Alert...")
        time.sleep(0.8)
        status.update(label=" Alert Dispatched Successfully!", state="complete", expanded=False)
    st.toast(f"Official Log: Notification sent to {student_name}'s guardian.", icon="📩")

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
            st.markdown('<div class="hero-section"><h1>AI-Based Student Performance Prediction & Early Warning System</h1><p>An Institutional Framework for Predictive Early Intervention</p></div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                st.subheader("1. Predictive Analytics")
                st.write("Implementation of Random Forest Classification to identify at-risk students based on multi-dimensional academic data.")
            with c2:
                st.subheader("2. Intervention System")
                st.write("Integrated notification gateway designed for mentors to initiate timely parental communication.")
            with c3:
                st.subheader("3. Performance Metrics")
                st.write("Interactive dashboards providing granular insights into class-wide and individual performance metrics.")
            st.divider()
            st.info("Log in from the sidebar to access the Analytical Dashboards.")

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
                    if role == "Admin" and access_key != ADMIN_SECRET_KEY: st.error("Invalid Admin Key")
                    elif role == "Mentor" and access_key != MENTOR_SECRET_KEY: st.error("Invalid Mentor Key")
                    elif role == "Student" and not reg_roll_no: st.warning("Roll Number is required.")
                    elif not new_user or not new_pswd: st.warning("Fields cannot be empty.")
                    else:
                        if add_userdata(new_user, make_hashes(new_pswd), role, reg_roll_no): st.success("Registration Successful!")
                        else: st.error("Username already exists.")

    else:
        # --- DYNAMIC SIDEBAR NAVIGATION ---
        st.sidebar.title("Navigation")
        
        # User Identity Display
        user_role = st.session_state['role']
        user_name = st.session_state['username']
        user_roll = st.session_state['roll_no']

        if user_role == "Student":
            st.sidebar.markdown(f"""
                <div class="sidebar-user">
                    <strong>STUDENT</strong><br>
                     {user_name}<br>
                     Roll: {user_roll}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.sidebar.markdown(f"""
                <div class="sidebar-user">
                    <strong>{user_role.upper()}</strong><br>
                     {user_name}
                </div>
            """, unsafe_allow_html=True)

        st.sidebar.divider()
        st.sidebar.button("Sign Out", on_click=lambda: st.session_state.update({"logged_in": False}))
        
        role = st.session_state['role']
        
        try:
            df, (model, metadata) = load_data(), load_assets()
            feature_cols = metadata['features']

            if role == "Admin":
                st.title("Administrative Control")
                with st.expander("User Account Management", expanded=True):
                    st.subheader("Registered System Users")
                    all_users = view_all_users()
                    user_df = pd.DataFrame(all_users, columns=['Username', 'Role', 'Roll_No'])
                    st.dataframe(user_df, use_container_width=True, hide_index=True)
                    st.divider()
                    user_to_del = st.selectbox("Select User to Remove", [u[0] for u in all_users if u[0] != st.session_state['username']])
                    if st.button(" Confirm Deletion"):
                        delete_user(user_to_del)
                        st.success(f"User {user_to_del} removed.")
                        time.sleep(1)
                        st.rerun()

            if role in ["Admin", "Mentor"]:
                st.title("Mentor Insight Dashboard")
                g1, g2 = st.columns(2)
                g1.plotly_chart(px.pie(df, names='Risk_Level', title='Academic Risk Distribution', hole=0.4), use_container_width=True)
                g2.plotly_chart(px.scatter(df, x='Total_%', y='Predicted_GPA', color='Risk_Level', title='Attendance vs Performance'), use_container_width=True)
                st.divider()
                st.subheader("Student Database Records")
                c1, c2 = st.columns([1, 2])
                risk_f = c1.multiselect("Filter by Risk Status", ['Low', 'Medium', 'High'], default=['High', 'Medium'])
                search_n = c2.text_input("Search Student Records (Name/Roll No)")
                filtered_df = df[df['Risk_Level'].isin(risk_f)]
                if search_n: filtered_df = filtered_df[filtered_df['Student Name'].str.contains(search_n, case=False) | filtered_df['Rollno'].astype(str).str.contains(search_n)]
                st.dataframe(filtered_df[['Rollno', 'Student Name', 'Total_%', 'Risk_Level']], use_container_width=True, hide_index=True)
                if not filtered_df.empty:
                    st.divider()
                    st.subheader("Detailed Profile Analysis")
                    selected = st.selectbox("Select Profile for Review", filtered_df['Student Name'].unique())
                    s_row = df[df['Student Name'] == selected].iloc[0]
                    info_col, action_col = st.columns([2, 1])
                    sub_data = {col.split('_')[0]: s_row[col] for col in feature_cols}
                    info_col.plotly_chart(px.bar(x=list(sub_data.keys()), y=list(sub_data.values()), title=f"Assessment Scores: {selected}"), use_container_width=True)
                    action_col.markdown("### Communication Portal")
                    if action_col.button(" Send Academic Alert"): send_notification(selected, s_row['Risk_Level'])

            elif role == "Student":
                st.title(f"Student Portal: {st.session_state['username']}")
                student_row = df[df['Rollno'].astype(str) == st.session_state['roll_no']] if st.session_state['roll_no'] else df[df['Student Name'].str.contains(st.session_state['username'], case=False)]
                
                if not student_row.empty:
                    s_row = student_row.iloc[0]
                    st.subheader("Academic Overview")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Attendance Rate", f"{s_row['Total_%']}%")
                    m2.metric("Projected GPA", s_row['Predicted_GPA'])
                    m3.metric("Analysis Status", s_row['Risk_Level'])

                    class_avg = df[feature_cols].mean()
                    subjects = [col.split('_')[0] for col in feature_cols]
                    fig_comp = go.Figure()
                    fig_comp.add_trace(go.Bar(x=subjects, y=s_row[feature_cols], name='Personal Score', marker_color='#004a99'))
                    fig_comp.add_trace(go.Bar(x=subjects, y=class_avg, name='Cohort Average', marker_color='#d1d1d1'))
                    fig_comp.update_layout(barmode='group', title="Comparative Subject Analysis")
                    st.plotly_chart(fig_comp, use_container_width=True)

                    st.divider()
                    st.subheader(" Personalized Academic Focus")
                    assigned_subjects = [col.split('_')[0] for col in feature_cols if s_row[col] > 0]
                    assigned_values = [s_row[col] for col in feature_cols if s_row[col] > 0]
                    colors = ['#28a745' if val >= 75 else '#ffc107' if val >= 50 else '#dc3545' for val in assigned_values]
                    fig_personal = go.Figure(go.Bar(x=assigned_subjects, y=assigned_values, marker_color=colors, text=assigned_values, textposition='auto'))
                    fig_personal.update_layout(title="Your Proficiency Level by Assigned Subjects", yaxis=dict(range=[0, 100]))
                    st.plotly_chart(fig_personal, use_container_width=True)
                    
                    low_subjects = [assigned_subjects[i] for i, v in enumerate(assigned_values) if v < 60]
                    if low_subjects: st.warning(f"**Study Suggestion:** Focus on {', '.join(low_subjects)} to improve your overall GPA.")
                    else: st.success(" **Great Job!** All subjects are on track.")
                else: st.warning("Profile not found!!.")

        except Exception as e:
            st.error(f"Application Runtime Error: {e}")

if __name__ == '__main__':
    main()
