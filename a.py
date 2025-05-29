from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'jroshan@98'
app.config['MYSQL_DB'] = 'salary_db'

mysql = MySQL(app)

@app.route('/salary/increase', methods=['POST'])
def calculate_salary_increase():
    data = request.get_json()
    old_salary = float(data.get('old_salary'))
    new_salary = float(data.get('new_salary'))

    if old_salary == 0:
        return jsonify({'error': 'Old salary cannot be zero'}), 400

    # Calculate percentage increase
    increase_percent = ((new_salary - old_salary) / old_salary) * 100

    # Store in MySQL
    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO salary_increase (old_salary, new_salary, percentage_increase)
        VALUES (%s, %s, %s)
    """, (old_salary, new_salary, increase_percent))
    mysql.connection.commit()
    cursor.close()

    return jsonify({
        'old_salary': old_salary,
        'new_salary': new_salary,
        'percentage_increase': round(increase_percent, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)



import streamlit as st
import mysql.connector
import hashlib

# MySQL DB config
db_config = {
    "host": "mysql",
    "user": "root",
    "password": "root",
    "database": "salary_db"
}

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# DB Connect
def get_conn():
    return mysql.connector.connect(**db_config)

# User registration
def register_user(username, password):
    conn = get_conn()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
        conn.commit()
        return True
    except mysql.connector.errors.IntegrityError:
        return False
    finally:
        cursor.close()
        conn.close()

# User login
def login_user(username, password):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    hashed_pw = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, hashed_pw))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# Save salary data
def save_salary(user_id, old_salary, new_salary, percentage_increase):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO salary_records (user_id, old_salary, new_salary, percentage_increase)
        VALUES (%s, %s, %s, %s)
    """, (user_id, old_salary, new_salary, percentage_increase))
    conn.commit()
    cursor.close()
    conn.close()

# View salary history
def get_salary_history(user_id):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT old_salary, new_salary, percentage_increase, created_at
        FROM salary_records WHERE user_id = %s ORDER BY created_at DESC
    """, (user_id,))
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

# Streamlit App
st.set_page_config(page_title="Salary Tracker", page_icon="💰")

st.title("💼 Salary Increase Tracker")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if "user" not in st.session_state:
    st.session_state.user = None

if choice == "Register":
    st.subheader("Create Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type='password')
    if st.button("Register"):
        if register_user(new_user, new_password):
            st.success("User registered! Go to Login.")
        else:
            st.error("Username already exists.")

elif choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.user = user
            st.success(f"Welcome {user['username']}!")
        else:
            st.error("Invalid username or password")

# After login
if st.session_state.user:
    st.subheader("📈 Enter Salary Details")
    old_salary = st.number_input("Old Salary", min_value=0.0, format="%.2f")
    new_salary = st.number_input("New Salary", min_value=0.0, format="%.2f")

    if st.button("Calculate"):
        if old_salary == 0:
            st.error("Old salary cannot be zero.")
        else:
            percent = ((new_salary - old_salary) / old_salary) * 100
            save_salary(st.session_state.user['id'], old_salary, new_salary, percent)
            st.success(f"💹 Salary Increased by {percent:.2f}%")

    st.subheader("📊 Your Salary History")
    history = get_salary_history(st.session_state.user['id'])
    if history:
        st.table(history)
    else:
        st.info("No records yet.")

    st.subheader("Logout")
    if st.button("Logout"):
        st.session_state.user = None
        st.success("Logged out.")   

    st.subheader("📊 Salary History")
    history = get_salary_history(st.session_state.user['id'])
    if history:
        st.table(history)
    else:
        st.info("No records yet.")
        