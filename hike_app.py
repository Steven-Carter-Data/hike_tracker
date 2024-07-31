import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import os

# File path for saving data
DATA_FILE = 'hike_data.csv'

# Load data from CSV
def load_data():
    if os.path.exists(DATA_FILE):
        data = pd.read_csv(DATA_FILE).to_dict('records')
        return data
    return []

# Save data to CSV
def save_data(data):
    df = pd.DataFrame(data)
    df.to_csv(DATA_FILE, index=False)

# Ensure 'Type' key exists for all records
def ensure_type_key(data):
    for item in data:
        if 'Type' not in item:
            item['Type'] = 'Hike'
    return data

# Initialize session state for storing data
if 'data' not in st.session_state:
    st.session_state['data'] = ensure_type_key(load_data())

# Function to add hike data
def add_hike(date, miles, name):
    st.session_state['data'].append({'Type': 'Hike', 'Date': date, 'Miles': miles, 'Name': name})
    save_data(st.session_state['data'])

# Function to remove hike data
def remove_hike(hike_to_remove):
    st.session_state['data'] = [hike for hike in st.session_state['data'] if f"{hike['Date']}, {hike['Name']}" != hike_to_remove]
    save_data(st.session_state['data'])

# Function to add motivation message
def add_motivation(name, message):
    st.session_state['data'].append({'Type': 'Motivation', 'Name': name, 'Message': message})
    save_data(st.session_state['data'])

# Function to remove motivation message
def remove_motivation(motivation_to_remove):
    # Adding a print statement to debug the issue
    print(f"Attempting to remove: {motivation_to_remove}")
    st.session_state['data'] = [item for item in st.session_state['data'] if item.get('Type') != 'Motivation' or f"{item.get('Name', '')}, {item.get('Message', '')}" != motivation_to_remove]
    save_data(st.session_state['data'])

# Function to calculate total miles
def calculate_total_miles():
    return sum(hike['Miles'] for hike in st.session_state['data'] if hike.get('Type') == 'Hike')

# Set layout to wide
st.set_page_config(
        page_title = "ACADIA", 
        layout="wide")

# Streamlit app layout
st.markdown(
    """
    <style>
    .main {
        background-color: #F4F1DE;
    }
    .stButton > button {
        background-color: #E07A5F;
        color: white;
    }
    .stTable {
        background-color: #F2CC8F;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Carter Family: Acadia Miles Tracker 🥾")

# Display image
st.image("acadia_1.jpg", caption="Acadia National Park")

# Input form for hike data
with st.form("hike_form"):
    date = st.date_input("Date")
    miles = st.number_input("Miles", min_value=0.0, step=0.1)
    name = st.text_input("Name of the Hike")
    submitted = st.form_submit_button("Add Hike")
    
    if submitted:
        add_hike(date, miles, name)
        st.success("Hike added!")

# Remove hike form
if st.session_state['data']:
    hikes_list = [f"{hike['Date']}, {hike['Name']}" for hike in st.session_state['data'] if hike.get('Type') == 'Hike']
    hike_to_remove = st.selectbox("Select a hike to remove", hikes_list)
    remove_submitted = st.button("Remove Hike")
    
    if remove_submitted and hike_to_remove:
        remove_hike(hike_to_remove)
        st.success("Hike removed!")

# Display data table
if st.session_state['data']:
    df = pd.DataFrame([item for item in st.session_state['data'] if item.get('Type') == 'Hike'])
    st.table(df)

# Calculate total miles and update gauge
total_miles = calculate_total_miles()
goal_miles = 50

# Create gauge chart
gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=total_miles,
    title={'text': "Total Miles Hiked"},
    gauge={
        'axis': {'range': [0, goal_miles]},
        'bar': {'color': "#3D405B"},
        'steps': [
            {'range': [0, goal_miles * 0.5], 'color': "#F2CC8F"},
            {'range': [goal_miles * 0.5, goal_miles * 0.75], 'color': "#81B29A"},
            {'range': [goal_miles * 0.75, goal_miles], 'color': "#3D405B"}
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': goal_miles
        }
    }
))

st.plotly_chart(gauge)

# Motivation Board
st.header("Motivation Board")
st.subheader("Family! Please add comments of encouragment for these incredible kids! 50 miles is the goal!")

# Input form for motivation message
with st.form("motivation_form"):
    name = st.text_input("Your Name")
    message = st.text_input("Motivational Message")
    submitted = st.form_submit_button("Add Message")
    
    if submitted:
        add_motivation(name, message)
        st.success("Motivational message added!")

# Remove motivation form
if st.session_state['data']:
    motivation_list = [f"{item.get('Name', '')}, {item.get('Message', '')}" for item in st.session_state['data'] if item.get('Type') == 'Motivation']
    motivation_to_remove = st.selectbox("Select a message to remove", motivation_list)
    remove_submitted = st.button("Remove Message")
    
    if remove_submitted and motivation_to_remove:
        remove_motivation(motivation_to_remove)
        st.success("Motivational message removed!")

# Display motivation messages
if st.session_state['data']:
    motivation_df = pd.DataFrame([item for item in st.session_state['data'] if item.get('Type') == 'Motivation'])
    if not motivation_df.empty:
        st.table(motivation_df)
