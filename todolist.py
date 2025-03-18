#to do list app
# using Mysql
# Todo Project
# CRUD => Create, Read, Update, Delete
 
# Step
 
# python => python -V or python --version
# pip list => display all the dependency of python
# mysql => pip install mysql-connector-python
 
# connect => connection, method
# cursor => cursor => cursor object
# execute => execute the query
 
import streamlit as st 
import mysql.connector
import pandas as pd
import os

# Secure Database Connection
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password=os.getenv("MYSQL_PASSWORD", "Tanmaychasql@123"),  # Secure with env variable
        database="todolistbase",
        auth_plugin="mysql_native_password"
    ) 

# Ensure the Tasks table exists
def create_table():
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
    cursor.close()
    conn.close()

# Function to execute queries
def execute_query(query, values=None, fetch=False):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = None
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        result = None
    finally:
        cursor.close()
        conn.close()
    
    return result

# Ensure table exists before proceeding
create_table()

# Streamlit UI
st.title("📝 To-Do List App")

menu = st.sidebar.selectbox("MENU", ["Add Task", "View Tasks", "Update Task", "Delete Task"])

# Add Task
if menu == "Add Task":
    st.subheader("Add a New Task")
    task = st.text_input("Enter Task", max_chars=255)
    deadline = st.date_input("Enter Deadline")
    submit = st.button("Add Task")

    if submit:
        if not task.strip():
            st.warning("Task cannot be empty!")
        else:
            query = "INSERT INTO Tasks (Task, Deadline) VALUES (%s, %s)"
            values = (task, deadline)
            execute_query(query, values)
            st.success("Task Added Successfully!")

# View Tasks
elif menu == "View Tasks":
    st.subheader("View All Tasks")
    tasks = execute_query("SELECT * FROM Tasks", fetch=True)
    
    if tasks:
        tasks_df = pd.DataFrame(tasks)
        st.write(tasks_df)
    else:
        st.info("No tasks found!")

# Update Task
elif menu == "Update Task":
    st.subheader("Update Task")
    tasks = execute_query("SELECT * FROM Tasks", fetch=True)

    if tasks:
        tasks_df = pd.DataFrame(tasks)
        st.write(tasks_df)

        task_id = st.number_input("Enter Task ID", min_value=1, step=1)
        new_task = st.text_input("Enter New Task")
        new_deadline = st.date_input("Enter New Deadline")
        update = st.button("Update Task")

        if update:
            if not new_task.strip():
                st.warning("Task description cannot be empty!")
            else:
                query = "UPDATE Tasks SET Task = %s, Deadline = %s WHERE Task_ID = %s"
                values = (new_task, new_deadline, task_id)
                execute_query(query, values)
                st.success("Task Updated Successfully!")
    else:
        st.info("No tasks available to update!")

# Delete Task
elif menu == "Delete Task":
    st.subheader("Delete Task")
    tasks = execute_query("SELECT * FROM Tasks", fetch=True)

    if tasks:
        tasks_df = pd.DataFrame(tasks)
        st.write(tasks_df)

        task_id = st.number_input("Enter Task ID to Delete", min_value=1, step=1)
        delete = st.button("Delete Task")
        delete_all = st.button("Delete All Tasks")

        if delete:
            query = "DELETE FROM Tasks WHERE Task_ID = %s"
            values = (task_id,)
            execute_query(query, values)
            st.success(f"Task ID {task_id} Deleted Successfully!")

        if delete_all:
            confirm = st.checkbox("Are you sure you want to delete all tasks?")
            if confirm:
                execute_query("DELETE FROM Tasks")
                st.success("All Tasks Deleted Successfully!")
    else:
        st.info("No tasks available to delete!")

            