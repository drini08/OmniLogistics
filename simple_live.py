import streamlit as st
import time

# Initialize the counter in session state
if 'latest_value' not in st.session_state:
    st.session_state.latest_value = 0

# Auto-refresh every second
st.experimental_autorefresh(interval=1000, limit=None, key='live_refresh')

# Increment the counter
st.session_state.latest_value += 1

st.title('Live Data')
st.write(st.session_state.latest_value)
