import streamlit as st
import datetime
import os

# --- 1. INITIAL CONFIG & SESSION STATE ---
st.set_page_config(page_title="Bettor Weather Lab", page_icon="🏀", layout="wide")

# Stage & View Management
if 'stage' not in st.session_state: st.session_state.stage = 'briefing'
if 'view' not in st.session_state: st.session_state.view = 'board'
if 'active_game' not in st.session_state: st.session_state.active_game = None

# Progress & Lifeline Counters
if 'selected_picks' not in st.session_state: st.session_state.selected_picks = []
if 'access_granted' not in st.session_state: st.session_state.access_granted = False
if 'flips_used' not in st.session_state: st.session_state.flips_used = 0
if 'swaps_used' not in st.session_state: st.session_state.swaps_used = 0

# --- 2. THE 48-HOUR ROLLING SLATE ---
master_slate = {
    "2026-02-18": [
        {"m": "Bulls vs Knicks", "a": "Bulls", "h": "Knicks", "t": "6:30 PM", "l": {"s": "+2.5/-2.5", "m": "+120/-140", "o": "218.5"}},
        {"m": "Heat vs Mavericks", "a": "Heat", "h": "Mavericks", "t": "7:00 PM", "l": {"s": "+4.5/-4.5", "m": "+160/-190", "o": "226.0"}}
    ],
    "2026-02-19": [
        {"m": "Nets vs Cavaliers", "a": "Nets", "h": "Cavaliers", "t": "6:00 PM", "l": {"s": "+6.5/-6.5", "m": "+220/-270", "o": "220.5"}},
        {"m": "Celtics vs Warriors", "a": "Celtics", "h": "Warriors", "t": "9:00 PM", "l": {"s": "-3.5/+3.5", "m": "-160/+135", "o": "231.5"}}
    ]
}

# --- 3. STAGE 1: BRIEFING ROOM (Video Fix) ---
if st.session_state.stage == 'briefing':
    st.title("📂 The Briefing Room")
    passcode = st.text_input("Lab Passcode:", type="password")
    
    if passcode == "SUNNY2026":
        st.success("ACCESS GRANTED. The Lab is open.")
        
        # We check if the videos exist in the folder before trying to play them
        video_col1, video_col2 = st.columns(2)
        
        with video_col1:
            st.subheader("The Veteran Coach")
            # This path matches your GitHub 'videos' folder
            coach_path = "videos/coach.mp4" 
            if os.path.exists(coach_path):
                st.video(coach_path)
            else:
                st.warning("Video 'coach.mp4' not found in the /videos folder.")
        
        with video_col2:
            st.subheader("The Lab Insider")
            insider_path = "videos/insider.mp4"
            if os.path.exists(insider_path):
                st.video(insider_path)
            else:
                st.warning("Video 'insider.mp4' not found in the /videos folder.")

        if st.button("PROCEED TO SELECTION FLOOR ➡️", use_container_width=True):
            st.session_state.stage = 'selection'; st.rerun()

# --- 4. STAGE 2: SELECTION FLOOR (Unified Board) ---
elif st.session_state.stage == 'selection':
    if st.session_state.view == 'board':
        st.title("🏀 Unified Scouting Board (48hr)")
        window = [datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1)]
        for date_obj in window:
            date_str = date_obj.strftime("%Y-%m-%d")
            label = "🔴 LIVE / TODAY" if date_obj == datetime.date.today() else f"📅 {date_obj.strftime('%A, %b %d')}"
            if date_str in master_slate:
                st.markdown(f"## {label}")
                for info in master_slate[date_str]:
                    with st.container(border=True):
                        st.write(f"### {info['m']} | {info['t']}")
                        c1, c2, c3, c4 = st.columns([1, 1, 1, 1.5])
                        with c1: st.caption("Spread"); spr = info['l']['s'].split('/')
                        with c2: st.caption("Moneyline"); ml = info['l']['m'].split('/')
                        with c3: st.caption("Total (O/U)"); tot = info['l']['o']
                        
                        # Away/Home Rows with Dual Checkboxes
                        a1, a2, a3, a4 = st.columns([1, 1, 1, 1.5])
                        with a1: 
                            if st.checkbox(f"{info['a']} {spr[0]}", key=f"s1_{info['m']}"):
                                st.session_state.selected_picks.append(f"{info['a']} Spread")
                        with a2: 
                            if st.checkbox(f"{info['a']} {ml[0]}", key=f"m1_{info['m']}"):
                                st.session_state.selected_picks.append(f"{info['a']} ML")
                        with a3:
                            if st.checkbox(f"Over {tot}", key=f"o_{info['m']}"):
                                st.session_state.selected_picks.append(f"{info['m']} Over")
                        with a4:
                            if st.button("🔍 PLAYER AREA", key=f"btn_{info['m']}", use_container_width=True):
                                st.session_state.active_game = info['m']; st.session_state.view = 'player_area'; st.rerun()

                        h1, h2, h3, h4 = st.columns([1, 1, 1, 1.5])
                        with h1: 
                            if st.checkbox(f"{info['h']} {spr[1]}", key=f"s2_{info['m']}"):
                                st.session_state.selected_picks.append(f"{info['h']} Spread")
                        with h2: 
                            if st.checkbox(f"{info['h']} {ml[1]}", key=f"m2_{info['m']}"):
                                st.session_state.selected_picks.append(f"{info['h']} ML")
                        with h3:
                            if st.checkbox(f"Under {tot}", key=f"u_{info['m']}"):
                                st.session_state.selected_picks.append(f"{info['h']} Under")

    # STICKY FOOTER
    count = len(st.session_state.selected_picks)
    st.markdown(f'<div style="position:fixed;bottom:0;left:0;width:100%;background:#1E1E1E;border-top:3px solid #FFD700;padding:10px;text-align:center;z-index:1000;"><h3 style="color:#FFD700;margin:0;">🎟️ TICKET: {count} / 25 LEGS</h3></div>', unsafe_allow_html=True)
    if count >= 25:
        if st.button("🔓 LOCK MISSION & GO TO COMMAND CENTER", use_container_width=True):
            st.session_state.stage = 'command'; st.rerun()

# --- 5. STAGE 3 & 4: COMMAND CENTER & REFEREE ---
# (Command Center, Paywall, and Lifeline logic remain as built)
