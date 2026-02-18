import streamlit as st
import time
import datetime

# --- INITIAL CONFIG ---
st.set_page_config(page_title="Bettor Weather Lab", page_icon="🏀", layout="wide")

# Session State Initialization
if 'stage' not in st.session_state: st.session_state.stage = 'briefing'
if 'selected_picks' not in st.session_state: st.session_state.selected_picks = []
if 'swaps_used' not in st.session_state: st.session_state.swaps_used = 0
if 'access_granted' not in st.session_state: st.session_state.access_granted = False

# Mock Data (Update these daily)
teams = {
    "Bulls": ["Coby White", "Zach LaVine", "Nikola Vucevic"],
    "Knicks": ["Jalen Brunson", "Karl-Anthony Towns", "Josh Hart"],
    "Mavericks": ["Luka Doncic", "Kyrie Irving", "Klay Thompson"],
    "Heat": ["Jimmy Butler", "Bam Adebayo", "Tyler Herro"],
    "Lakers": ["LeBron James", "Anthony Davis", "Austin Reaves"],
    "Celtics": ["Jayson Tatum", "Jaylen Brown", "Derrick White"]
}

# --- STAGE 1: BRIEFING ---
if st.session_state.stage == 'briefing':
    st.title("📂 The Briefing Room")
    if st.text_input("Passcode:", type="password") == "SUNNY2026":
        st.video("https://www.youtube.com/watch?v=example1")
        if st.button("PROCEED TO SELECTION FLOOR ➡️"):
            st.session_state.stage = 'selection'
            st.rerun()

# --- STAGE 2: SELECTION FLOOR (LIVE & 48-HOUR SLATE) ---
elif st.session_state.stage == 'selection':
    st.title("🏀 The Selection Floor")

    # 1. LIVE GAMES (Top Priority)
    st.markdown("### 🔴 LIVE NOW: IN-GAME WAR ROOM")
    live_slate = [{"m": "Bulls vs Knicks", "s": "102 - 98", "q": "4th Qtr", "r": teams["Bulls"] + teams["Knicks"]}]
    
    for g in live_slate:
        with st.expander(f"🔥 LIVE: {g['m']} | Score: {g['s']} ({g['q']})", expanded=True):
            st.warning("⚠️ LIVE LINES: Scout fast as the clock ticks down!")
            t_live = st.tabs(["Live Points", "Live Combos"])
            with t_live[0]:
                p = st.selectbox("Live Player:", g['r'], key=f"l_p_{g['m']}")
                l = st.text_input("Current Line:", key=f"l_l_{g['m']}")
                if st.button("Add Live Pick", key=f"l_b_{g['m']}"):
                    st.session_state.selected_picks.append(f"LIVE: {p} {l} Pts")
                    st.rerun()

    st.divider()

    # 2. TONIGHT'S UPCOMING MISSIONS
    today = datetime.date.today()
    st.markdown(f"### 📅 TONIGHT - {today.strftime('%B %d')}")
    slate_today = [{"m": "Mavericks vs Heat", "t": "7:00 PM", "r": teams["Mavericks"] + teams["Heat"]}]
    
    for g in slate_today:
        with st.expander(f"🏀 {g['m']} | {g['t']} CST", expanded=False):
            t_today = st.tabs(["Points", "3-Pointers", "Combos", "Defense"])
            with t_today[0]:
                p = st.selectbox("Player:", g['r'], key=f"t_p_{g['m']}")
                l = st.text_input("Line:", key=f"t_l_{g['m']}")
                if st.button("Add to Mission", key=f"t_b_{g['m']}"):
                    st.session_state.selected_picks.append(f"{p} {l} Pts")

    st.divider()

    # 3. TOMORROW'S ADVANCE SCOUTING
    tomorrow = today + datetime.timedelta(days=1)
    st.markdown(f"### ⏩ TOMORROW - {tomorrow.strftime('%B %d')}")
    slate_tom = [{"m": "Lakers vs Celtics", "t": "7:30 PM", "r": teams["Lakers"] + teams["Celtics"]}]
    
    for g in slate_tom:
        with st.expander(f"🏀 {g['m']} | {g['t']} CST", expanded=False):
            t_tom = st.tabs(["Points", "3-Pointers", "Combos", "Defense"])
            with t_tom[0]:
                p = st.selectbox("Player:", g['r'], key=f"tom_p_{g['m']}")
                l = st.text_input("Line:", key=f"tom_l_{g['m']}")
                if st.button("Add to Mission", key=f"tom_b_{g['m']}"):
                    st.session_state.selected_picks.append(f"{p} {l} Pts")

    # 4. STICKY FOOTER
    st.divider()
    st.markdown(f"### 📥 Total Mission Intel: **{len(st.session_state.selected_picks)} / 25**")
    if st.button("🚀 FINALIZE 25-LEG ROSTER"):
        st.session_state.stage = 'command'
        st.rerun()

# --- STAGE 3: COMMAND CENTER ---
elif st.session_state.stage == 'command':
    st.title("🕹️ Command Center")
    if not st.session_state.access_granted:
        st.error("🔐 MISSION DATA ENCRYPTED. Pay $10 to Reveal.")
        if st.button("💰 AUTHORIZE $10 REVEAL"):
            st.session_state.access_granted = True
            st.rerun()
    else:
        st.markdown("<h1 style='text-align: center;'>🏁 👍</h1>", unsafe_allow_html=True)
        st.success("OFFICIAL: MISSION CLEARED")
        st.balloons()
        
        # Reveal Loop with Swap Logic
        num_6packs = len(st.session_state.selected_picks) // 6
        for i in range(min(4, num_6packs)):
            with st.expander(f"🎫 PrizePicks 6-Pack Set {i+1}", expanded=True):
                st.write(f"Scouting Report for Set {i+1}...")
                if st.button(f"🔄 Swap (Used: {st.session_state.swaps_used})", key=f"sw_{i}"):
                    st.session_state.swaps_used += 1
                    if st.session_state.swaps_used > 2: st.warning("⚠️ 50¢ Fee Applied")
        
        if st.button("➕ Add Another 25-Leg Set ($3)"):
            st.session_state.stage = 'selection'
            st.rerun()
