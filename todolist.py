import streamlit as st
import mysql.connector
import pandas as pd
import os
from datetime import date

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="To-Do List App",
    page_icon="📝",
    layout="centered"
)

# -------------------------------
# Database Connection
# -------------------------------
def connect_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE", "todolistbase"),
        auth_plugin="mysql_native_password"
    )

# -------------------------------
# Create Table if not exists
# -------------------------------
def create_table():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tasks (
                Task_ID INT AUTO_INCREMENT PRIMARY KEY,
                Task VARCHAR(255) NOT NULL,
                Deadline DATE NOT NULL
            )
        """)
        conn.commit()
    except mysql.connector.Error as err:
        st.error(f"Database initialization error: {err}")
    finally:
        cursor.close()
        conn.close()

# -------------------------------
# Query Executor
# -------------------------------
def execute_query(query, values=None, fetch=False):
    conn = None
    cursor = None
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)

        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        if fetch:
            return cursor.fetchall()
        else:
            conn.commit()
            return None

    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# -------------------------------
# Initialize DB
# -------------------------------
create_table()

# -------------------------------
# UI
# -------------------------------
st.title("📝 To-Do List App")

menu = st.sidebar.selectbox(
    "MENU",
    ["Add Task", "View Tasks", "Update Task", "Delete Task"]
)

# -------------------------------
# Add Task
# -------------------------------
if menu == "Add Task":
    st.subheader("➕ Add a New Task")

    task = st.text_input("Task Description", max_chars=255)
    deadline = st.date_input("Deadline", min_value=date.today())
    submit = st.button("Add Task")

    if submit:
        if not task.strip():
            st.warning("⚠️ Task cannot be empty!")
        else:
            query = "INSERT INTO Tasks (Task, Deadline) VALUES (%s, %s)"
            execute_query(query, (task, deadline))
            st.success("✅ Task added successfully!")

# -------------------------------
# View Tasks
# -------------------------------
elif menu == "View Tasks":
    st.subheader("📋 All Tasks")

    tasks = execute_query("SELECT * FROM Tasks ORDER BY Deadline", fetch=True)

    if tasks:
        df = pd.DataFrame(tasks)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No tasks found.")

# -------------------------------
# Update Task
# -------------------------------
elif menu == "Update Task":
    st.subheader("✏️ Update Task")

    tasks = execute_query("SELECT * FROM Tasks", fetch=True)

    if tasks:
        df = pd.DataFrame(tasks)
        st.dataframe(df, use_container_width=True)

        task_id = st.number_input("Task ID", min_value=1, step=1)
        new_task = st.text_input("New Task Description")
        new_deadline = st.date_input("New Deadline", min_value=date.today())

        if st.button("Update Task"):
            if not new_task.strip():
                st.warning("⚠️ Task cannot be empty!")
            else:
                query = """
                    UPDATE Tasks
                    SET Task = %s, Deadline = %s
                    WHERE Task_ID = %s
                """
                execute_query(query, (new_task, new_deadline, task_id))
                st.success("✅ Task updated successfully!")
    else:
        st.info("No tasks available to update.")

# -------------------------------
# Delete Task
# -------------------------------
elif menu == "Delete Task":
    st.subheader("🗑️ Delete Task")

    tasks = execute_query("SELECT * FROM Tasks", fetch=True)

    if tasks:
        df = pd.DataFrame(tasks)
        st.dataframe(df, use_container_width=True)

        task_id = st.number_input("Task ID to delete", min_value=1, step=1)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Delete Selected Task"):
                execute_query(
                    "DELETE FROM Tasks WHERE Task_ID = %s",
                    (task_id,)
                )
                st.success(f"✅ Task ID {task_id} deleted!")

        with col2:
            confirm = st.checkbox("Confirm delete ALL tasks")
            if confirm and st.button("Delete All"):
                execute_query("DELETE FROM Tasks")
                st.success("🔥 All tasks deleted!")

    else:
        st.info("No tasks available to delete.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("🚀 Streamlit + MySQL | Docker & Kubernetes Ready")
