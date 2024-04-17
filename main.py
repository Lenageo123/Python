import streamlit as st
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns


def validate_password(password):
    regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"
    return re.match(regex, password)

def register_user(username, password):
    if not os.path.exists("users.csv"):
        with open("users.csv", "w") as f:
            f.write("username,password\n")
    with open("users.csv", "a") as f:
        f.write(f"{username},{password}\n")
    st.success("Registration successful!")



def authenticate_user(username, password):
    if os.path.exists("users.csv"):
        df = pd.read_csv("users.csv")
        if not df.empty and ((df['username'] == username) & (df['password'] == password)).any():
            return True
    return False


def main():
    st.set_page_config(page_title='Health Visualizer',
                       layout='centered',
                       page_icon='📊')

    st.title('📊  Health Visualizer')

    session_state = st.session_state

    
    if 'logged_in' not in session_state:
        session_state.logged_in = False
    if 'username' not in session_state:
        session_state.username = ""

    
    if not session_state.logged_in:
        st.sidebar.title("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if authenticate_user(username, password):
                session_state.logged_in = True
                session_state.username = username
                st.success("You have successfully logged in!")
            else:
                st.error("Invalid username or password. Please try again.")

        st.sidebar.title("Register")
        new_username = st.sidebar.text_input("New Username")
        new_password = st.sidebar.text_input("New Password", type="password")
        if st.sidebar.button("Register"):
            if validate_password(new_password):
                register_user(new_username, new_password)
                st.success("You have successfully registered!")
            else:
                st.error("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit.")

    
    if session_state.logged_in:
        folder_path = "D:\\Lena\\BCA_Semester4\\Python2\\trial\\data"
        files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        selected_file = st.selectbox('Select a file', files, index=None)

        if selected_file:
            file_path = os.path.join(folder_path, selected_file)
            df = pd.read_csv(file_path)
            col1, col2 = st.columns(2)
            columns = df.columns.tolist()

            with col1:
                st.write("")
                st.write(df.head())

            with col2:
                x_axis = st.selectbox('Select the X-axis', options=columns+["None"])
                y_axis = st.selectbox('Select the Y-axis', options=columns+["None"])
                plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
                plot_type = st.selectbox('Select the type of plot', options=plot_list)

            if st.button('Generate Plot'):
                try:
                    fig, ax = plt.subplots(figsize=(6, 4))
                    if plot_type == 'Line Plot':
                        sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
                    elif plot_type == 'Bar Chart':
                        sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
                    elif plot_type == 'Scatter Plot':
                        sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
                    elif plot_type == 'Distribution Plot':
                        sns.histplot(df[x_axis], kde=True, ax=ax)
                        y_axis='Density'
                    elif plot_type == 'Count Plot':
                        sns.countplot(x=df[x_axis], ax=ax)
                        y_axis = 'Count'
                    ax.tick_params(axis='x', labelsize=10)
                    ax.tick_params(axis='y', labelsize=10)
                    plt.title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=12)
                    plt.xlabel(x_axis, fontsize=10)
                    plt.ylabel(y_axis, fontsize=10)
                    st.pyplot(fig)
                except Exception as e:
                    st.error("Sorry, the selected visualization is not possible. Please try different options.")


if __name__ == "__main__":
    main()
