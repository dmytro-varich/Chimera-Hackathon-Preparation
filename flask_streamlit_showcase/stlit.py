import streamlit as st
import requests
import streamlit.components.v1 as components


# SIMPLE FLASK + STREAMLIT SHOWCASE


# Backend URL (Flask app)
BASE_URL = "http://127.0.0.1:5000"

st.title("User Management App")
st.sidebar.title("Actions")

# Function to display users
def display_users():
    st.subheader("All Users")
    response = requests.get(f"{BASE_URL}/users")
    if response.status_code == 200:
        users = response.json()
        for user in users:
            st.markdown(
                f"""
                <div style="padding: 10px;">
                    <h2>User {user['name']} Id:{user['id']}</h2>
                    <p>Email: {user['email']}</p>
                </div>
                """, unsafe_allow_html=True)
            # st.write(f"ID: {user['id']}, Name: {user['name']}, Email: {user['email']}")
    else:
        st.error("Error fetching users")

# Sidebar Actions
action = st.sidebar.selectbox("Choose an action", ["Design check", "Create User", "View Users", "Update User", "Delete User"])

if action == "Design check":
    col1, col2 = st.columns(2)
    with col1:
        st.write("This is the first column.")
    with col2:
        st.write("This is the second column.")

    option = st.selectbox('King of the castle:', [1,2,3,4,18,5])

    f'You`ve selected: {option}'


# Create User
if action == "Create User":
    st.subheader("Create a New User")
    name = st.text_input("Name")
    email = st.text_input("Email")
    if st.button("Create"):
        response = requests.post(f"{BASE_URL}/users", json={"name": name, "email": email})
        if response.status_code == 201:
            st.success("User created successfully")
        else:
            st.error(response.json().get("error", "Failed to create user"))

# View Users
elif action == "View Users":
    display_users()

# Update User
elif action == "Update User":
    st.subheader("Update User")
    user_id = st.number_input("Enter User ID", min_value=1, step=1)
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    if response.status_code == 200:
        user = response.json()
        f'Updating user {user["name"]}.'
    else:
        f'User with id {user_id} does not exist.'

    new_name = st.text_input("New Name")
    new_email = st.text_input("New Email")
    if st.button("Update"):
        response = requests.put(f"{BASE_URL}/users/{user_id}", json={"name": new_name, "email": new_email})
        if response.status_code == 200:
            st.success("User updated successfully")
        else:
            st.error(response.json().get("error", "Failed to update user"))

# Delete User
elif action == "Delete User":
    st.subheader(f"Delete User")
    user_id = st.number_input("Enter User ID to Delete", min_value=1, step=1)
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    if response.status_code == 200:
        user = response.json()
        f'Deleting user {user["name"]}'
    else:
        f'User with id {user_id} does not exist.'

    if st.button("Delete"):
        response = requests.delete(f"{BASE_URL}/users/{user_id}")
        if response.status_code == 200:
            st.success(response.json().get("message", "User deleted successfully"))
        else:
            st.error(response.json().get("error", "Failed to delete user"))
