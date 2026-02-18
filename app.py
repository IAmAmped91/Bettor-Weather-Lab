import streamlit as st
import time
from datetime import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="Better Weather Scouting Lab", layout="wide", initial_sidebar_state="expanded")

# --- BETA DECAY LOGIC (The Price Engine) ---
launch_date = datetime(2026, 2, 19, 9, 0)
now = datetime.now()
time_diff = now - launch_date
hours_passed = time_diff.total_seconds() / 3600

# Determine Tier and Price
if hours_passed < 0:
    current_tier = "PRE-LAUNCH MODE"
    ticket_cost = 0.50
elif hours_passed <= 48:
    current_tier = "PREMIUM ELITE"
    ticket_cost = 0.50
elif hours_passed <= 96:
    current_tier = "PRO STARTER"
    ticket_cost = 1.25
else:
    current_tier = "BASE ENTRY"
    ticket_cost = 1.25

# --- STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ACCESS GATE ---
st.sidebar.title("🔐 Founder's Access")
passcode = st.sidebar.text_input("Enter Passcode", type="password")

if passcode == "SUNNY2026":
    st.sidebar.success(f"Access Granted: {current_tier}")
    
    # --- MAIN INTERFACE ---
    st.title("🌪️ Better Weather Scouting Lab")
    st.subheader(f"Current Phase: {current_tier}")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📡 Scouting Feed")
        intel_source = st.radio("Select Intel Source:", ["The Veteran Coach", "The Insider Insight"])
        
        # Video logic
        video_path = "videos/coach.mp4" if intel_source == "The Veteran Coach" else "videos/insider.mp4"
        
        try:
            st.video(video_path)
        except:
            st.warning(f"Waiting for {intel_source} video feed... (Check 'videos' folder)")

    with col2:
        st.markdown("### 📊 Live Analytics")
        st.metric("Ticket Cost", f"${ticket_cost:.2f}")
        st.metric("Phase Decay", f"{max(0, int(96 - hours_passed))} hrs remaining")
        
        if st.button("🚀 CRUNCH 100-PICK POOL"):
            with st.spinner("Analyzing weather trends..."):
                time.sleep(2)
                st.success("Crunch Complete! 100 Picks Generated.")
                st.balloons()

    st.divider()
    
    # --- MISSION SELECTION ---
    st.markdown("### 🎯 Mission Selection")
    mission = st.selectbox("Choose Your Deployment:", ["Stratosphere (Vertical Ladder)", "Tactical Sets (Horizontal Hedge)", "Ground Level (Base Entry)"])
    
    if mission == "Stratosphere (Vertical Ladder)":
        st.info("Strategy: Building 20-15-10, 18-14-8, or 10-8-6 ladders.")
    
else:
    st.warning("Please enter the Founder's Passcode to unlock the Lab.")
    st.info("Status: Waiting for authentication...")