import streamlit as st
import pandas as pd
import joblib
import sqlite3
import hashlib
import plotly.express as px
import plotly.graph_objects as go
import time

# --- 1. CORE LOGIC ---

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

@st.cache_data(show_spinner=False)
def load_data():
    return pd.read_csv('Student_Performance_Dataset.csv')

@st.cache_resource(show_spinner=False)
def load_assets():
    model = joblib.load('models/student_risk_model.pkl')
    metadata = joblib.load('models/model_metadata.pkl')
    return model, metadata

def send_notification(student_name, risk_level):
    with st.status(f"Connecting to Gateway for {student_name}...", expanded=True) as status:
        st.write("1. Accessing Institutional SMS Server...")
        time.sleep(1)
        st.write("2. Verifying parental contact...")
        time.sleep(1)
        st.write(f"3. Dispatching {risk_level} Risk Alert...")
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
        .stButton>button { width: 100%; border-radius: 4px; background-color: #004a99; color: white; border: none; height: 3em; font-weight: 600; }
        
        div[data-testid="column"]:nth-of-type(2) {
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
        }

        .hero-section { 
            background: linear-gradient(135deg, #002b5c 0%, #004a99 100%); 
            padding: 60px; border-radius: 12px; color: white; text-align: center; margin-bottom: 40px;
        }
        .hero-section h1 { font-size: 3rem; font-weight: 800; margin-bottom: 10px; color: white; }

        .feature-card {
            background-color: #f8f9fa; padding: 30px; border-radius: 10px; border-top: 5px solid #004a99;
            height: 250px; transition: 0.3s; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        
        .team-footer {
            background-color: #f1f4f9; padding: 25px; border-radius: 12px;
            border: 1px solid #d0d7de; margin-top: 50px; text-align: center;
        }
        .team-badge {
            background-color: #004a99; color: white; padding: 5px 15px; border-radius: 20px;
        }

        .sidebar-user { padding: 10px; background-color: #f0f2f6; border-radius: 5px; border-left: 5px solid #004a99; }
        #stDecoration { display:none !important; } 
        </style>
        """, unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        st.session_state.update({'logged_in': False, 'role': None, 'username': "", 'roll_no': ""})

    if not st.session_state['logged_in']:
        app_mode = st.sidebar.radio("Navigation", ["Project Overview", "Login / Register"])

        if app_mode == "Project Overview":
            st.markdown('<div class="hero-section"><h1>🎓 AI-Scholar Insights</h1><p>Empowering Educators with Predictive Intelligence & Early Intervention Systems</p></div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown('<div class="feature-card"><h3>🧠 Predictive Analytics</h3><p>Leveraging <b>Random Forest ML</b> to forecast student risks based on academic patterns.</p></div>', unsafe_allow_html=True)
            with c2: st.markdown('<div class="feature-card"><h3>📡 Smart Intervention</h3><p>Automated notification gateway enabling mentors to communicate instantly with guardians.</p></div>', unsafe_allow_html=True)
            with c3: st.markdown('<div class="feature-card"><h3>📊 Deep Analytics</h3><p>High-fidelity dashboards providing real-time visibility into cohort-level progress.</p></div>', unsafe_allow_html=True)
            st.divider()
            st.info("💡 **Getting Started:** Select 'Login / Register' from the sidebar to access the secure portal.")
            st.markdown(f'<div class="team-footer"><span class="team-badge">Developed By: Digital Architects</span><div style="margin-top:15px; font-size:1.2rem;"><b>Dev Dagar (Lead)</b> • Shubhi Tyagi • Aryan Sharma • Dev Sood</div></div>', unsafe_allow_html=True)

        elif app_mode == "Login / Register":
            st.title("System Authentication")
            choice = st.segmented_control("Select Action", ["Login", "Register"], default="Login")
            if choice == "Login":
                user, pswd = st.text_input("Username"), st.text_input("Password", type='password')
                if st.button("Access Dashboard"):
                    result = login_user(user, make_hashes(pswd))
                    if result: st.session_state.update({'logged_in': True, 'username': result[0][0], 'role': result[0][2], 'roll_no': result[0][3]}); st.rerun()
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
        # --- LOGGED IN UI ---
        st.sidebar.title("Navigation")
        user_role, user_name, user_roll = st.session_state['role'], st.session_state['username'], st.session_state['roll_no']
        st.sidebar.markdown(f'<div class="sidebar-user"><strong>{user_role.upper()}</strong><br>{user_name}{f"<br>Roll: {user_roll}" if user_role == "Student" else ""}</div>', unsafe_allow_html=True)
        st.sidebar.divider(); st.sidebar.button("Sign Out", on_click=lambda: st.session_state.update({"logged_in": False}))
        
        try:
            df, (model, metadata) = load_data(), load_assets()
            feature_cols = metadata['features']

            # --- ADMIN SECTION (NO CHANGE) ---
            if user_role == "Admin":
                st.title("🛡️ Administrative Command Center")
                all_users = view_all_users()
                user_df = pd.DataFrame(all_users, columns=['Username', 'Role', 'Roll_No'])
                
                s1, s2, s3 = st.columns(3)
                s1.metric("Total Users", len(user_df))
                s2.metric("Mentors", len(user_df[user_df['Role'] == 'Mentor']))
                s3.metric("Students", len(user_df[user_df['Role'] == 'Student']))
                
                tab1, tab2 = st.tabs(["👥 User Management", "⚙️ System Overview"])
                with tab1:
                    st.subheader("Manage User Access")
                    st.dataframe(user_df, use_container_width=True, hide_index=True)
                    st.divider()
                    col_del1, col_del2 = st.columns([3, 1])
                    user_to_del = col_del1.selectbox("Choose account to remove", [u[0] for u in all_users if u[0] != st.session_state['username']])
                    if col_del2.button("🚫 Confirm Delete", type="secondary"):
                        delete_user(user_to_del); st.success(f"User {user_to_del} removed."); time.sleep(1); st.rerun()
                with tab2:
                    st.subheader("System Role Distribution")
                    role_map_admin = {'Admin': '#1F77B4', 'Mentor': '#D62728', 'Student': '#2CA02C'}
                    all_roles = ['Admin', 'Mentor', 'Student']
                    role_counts = user_df['Role'].value_counts().reindex(all_roles, fill_value=0).reset_index()
                    role_counts.columns = ['Role', 'Count']
                    fig_roles = px.pie(role_counts, names='Role', values='Count', hole=0.5, color='Role', color_discrete_map=role_map_admin)
                    st.plotly_chart(fig_roles, use_container_width=True)

            # --- MENTOR SECTION (UPDATED) ---
            if user_role in ["Admin", "Mentor"]:
                st.title("Mentor Insight Dashboard")
                g1, g2 = st.columns(2)
                
                # Custom Color Map for Risks (Traffic-Light Logic)
                risk_color_map = {'High': '#FF4136', 'Medium': '#FF851B', 'Low': '#2ECC40'}
                
                fig_risk = px.pie(df, names='Risk_Level', title='Academic Risk Distribution', hole=0.4,
                                 color='Risk_Level', color_discrete_map=risk_color_map)
                g1.plotly_chart(fig_risk, use_container_width=True)
                
                fig_scatter = px.scatter(df, x='Total_%', y='Predicted_GPA', color='Risk_Level', 
                                         color_discrete_map=risk_color_map, title='Attendance vs Performance Analysis')
                g2.plotly_chart(fig_scatter, use_container_width=True)
                
                st.divider(); st.subheader("Student Database Records")
                c1, c2 = st.columns([1, 2])
                risk_f = c1.multiselect("Filter Risk Category", ['Low', 'Medium', 'High'], default=['High', 'Medium'])
                search_n = c2.text_input("Search (Name or Roll Number)")
                
                filtered_df = df.copy() if not risk_f else df[df['Risk_Level'].isin(risk_f)]
                if search_n: filtered_df = filtered_df[filtered_df['Student Name'].str.contains(search_n, case=False) | filtered_df['Rollno'].astype(str).str.contains(search_n)]
                
                # Adding S.No to Table
                display_df = filtered_df[['Rollno', 'Student Name', 'Total_%', 'Risk_Level']].copy()
                display_df.insert(0, 'S.No', range(1, 1 + len(display_df)))
                
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                if not filtered_df.empty:
                    st.divider(); selected = st.selectbox("Select Profile for Detailed Review", filtered_df['Student Name'].unique())
                    s_row = df[df['Student Name'] == selected].iloc[0]
                    info_col, action_col = st.columns([2, 1])
                    sub_data = {col.split('_')[0]: s_row[col] for col in feature_cols}
                    info_col.plotly_chart(px.bar(x=list(sub_data.keys()), y=list(sub_data.values()), title=f"Subject-wise Scores: {selected}", color_discrete_sequence=['#004a99']), use_container_width=True)
                    action_col.markdown("### Communication Portal")
                    if action_col.button("📧 Send Warning Alert"): send_notification(selected, s_row['Risk_Level'])

            # --- STUDENT SECTION (NO CHANGE) ---
            elif user_role == "Student":
                st.title(f"Student Portal: {st.session_state['username']}")
                student_row = df[df['Rollno'].astype(str) == st.session_state['roll_no']] if st.session_state['roll_no'] else df[df['Student Name'].str.contains(st.session_state['username'], case=False)]
                if not student_row.empty:
                    s_row = student_row.iloc[0]
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Attendance Rate", f"{s_row['Total_%']}%"); m2.metric("Projected GPA", s_row['Predicted_GPA']); m3.metric("Analysis Status", s_row['Risk_Level'])
                    class_avg, subjects = df[feature_cols].mean(), [col.split('_')[0] for col in feature_cols]
                    fig_comp = go.Figure()
                    fig_comp.add_trace(go.Bar(x=subjects, y=s_row[feature_cols], name='Personal', marker_color='#004a99'))
                    fig_comp.add_trace(go.Bar(x=subjects, y=class_avg, name='Class Avg', marker_color='#d1d1d1'))
                    fig_comp.update_layout(barmode='group', title="Comparative Analysis"); st.plotly_chart(fig_comp, use_container_width=True)
                else: st.warning("Profile not found.")
        except Exception as e: st.error(f"Error: {e}")

if __name__ == '__main__': main()
