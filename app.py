import streamlit as st
import time
import datetime

# --- INITIAL CONFIG & SESSION STATE ---
st.set_page_config(page_title="Bettor Weather Lab", page_icon="🏀", layout="wide")

# Initialize all session variables
if 'stage' not in st.session_state:
    st.session_state.stage = 'briefing'
if 'selected_picks' not in st.session_state:
    st.session_state.selected_picks = []
if 'swaps_used' not in st.session_state:
    st.session_state.swaps_used = 0
if 'access_granted' not in st.session_state:
    st.session_state.access_granted = False
if 'mode' not in st.session_state:
    st.session_state.mode = 'standard'

# --- STAGE 1: THE BRIEFING ROOM ---
if st.session_state.stage == 'briefing':
    st.title("📂 The Briefing Room")
    password = st.text_input("Enter Lab Passcode:", type="password")
    
    if password == "SUNNY2026":
        st.success("Access Granted.")
        col1, col2 = st.columns(2)
        with col1:
            st.info("🎙️ **The Veteran Coach**")
            st.video("https://www.youtube.com/watch?v=example1") # Update URLs as needed
        with col2:
            st.info("🕵️ **The Insider**")
            st.video("https://www.youtube.com/watch?v=example2") 
        
        if st.button("PROCEED TO SELECTION FLOOR ➡️"):
            st.session_state.stage = 'selection'
            st.rerun()

# --- STAGE 2: THE SELECTION FLOOR (FULL SLATE & TABS) ---
elif st.session_state.stage == 'selection':
    st.title("🏀 Today's Active Missions")

    # 1. PRIZEPICKS HIGHLIGHT & MODE TOGGLE
    st.markdown("""
        <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; border: 2px solid #FFD700; margin-bottom: 20px;">
            <h3 style="color: #FFD700; margin: 0;">🎯 PRIZEPICKS PRECISION SCOUTING</h3>
            <p style="color: white; font-size: 14px;">Build 1 Master List (25 legs) to generate 4 high-probability 6-packs.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 ACTIVATE PRIZEPICKS OPTIMIZER"):
        st.session_state.mode = 'prizepicks'
        st.toast("PrizePicks Mode Engaged!")

    # 2. FULL SLATE DISPLAY WITH COUNTDOWNS
    daily_slate = [
        {"matchup": "Mavericks vs Heat", "time": "19:00"}, # 7:00 PM CST
        {"matchup": "Lakers vs Celtics", "time": "19:30"},
        {"matchup": "Nuggets vs Suns", "time": "21:00"}
    ]

    for game in daily_slate:
        # Calculate Countdown
        now = datetime.datetime.now()
        game_time = datetime.datetime.combine(now.date(), datetime.time(int(game['time'].split(':')[0]), int(game['time'].split(':')[1])))
        time_diff = game_time - now
        
        if time_diff.total_seconds() > 0:
            status_msg = f"⏳ Starts in: {str(time_diff).split('.')[0]}"
            is_locked = False
        else:
            status_msg = "🚫 MISSION LOCKED: GAME STARTED"
            is_locked = True

        with st.expander(f"📅 {game['matchup']} | {status_msg}", expanded=False):
            if is_locked:
                st.error("This scouting window is closed.")
            else:
                # FANDUEL-STYLE TABS
                t1, t2, t3, t4, t5 = st.tabs(["Main Lines", "Player Points", "3-Pointers", "Rebounds", "Combos"])
                
                with t1:
                    c1, c2, c3 = st.columns(3)
                    if c1.button(f"{game['matchup'].split(' vs ')[0]} Spread", key=f"s_{game['matchup']}"):
                        st.session_state.selected_picks.append(f"{game['matchup']} Spread")
                
                with t2:
                    p_name = st.selectbox("Select Player:", ["Luka Doncic", "Kyrie Irving", "Jimmy Butler"], key=f"p_{game['matchup']}")
                    p_line = st.text_input("Line (e.g. O 28.5):", key=f"l_{game['matchup']}")
                    if st.button("Add Points Prop", key=f"btn_{game['matchup']}"):
                        st.session_state.selected_picks.append(f"{p_name} {p_line} Pts")
                
                with t5:
                    combo_type = st.radio("Category:", ["P+R", "P+A", "R+A", "PRA"], horizontal=True, key=f"radio_{game['matchup']}")
                    c_val = st.text_input("Combo Line:", key=f"c_val_{game['matchup']}")
                    if st.button("Add Combo", key=f"c_btn_{game['matchup']}"):
                        st.session_state.selected_picks.append(f"{p_name} {c_val} {combo_type}")

    st.divider()
    st.write(f"### 📥 Total Intel: {len(st.session_state.selected_picks)} / 25 Picks Collected")
    
    if st.button("CONFIRM MISSION & GO TO COMMAND CENTER ➡️"):
        st.session_state.stage = 'command'
        st.rerun()

# --- STAGE 3: COMMAND CENTER (PAYWALL & REVEAL) ---
elif st.session_state.stage == 'command':
    st.title("🕹️ Command Center")
    total_intel = len(st.session_state.selected_picks)
    
    if not st.session_state.access_granted:
        st.markdown("""
            <div style="background-color: #1E1E1E; padding: 30px; border-radius: 10px; border: 2px solid #00FF00; text-align: center;">
                <h2 style="color: #00FF00;">🔐 MISSION DATA ENCRYPTED</h2>
                <p>Pay <b>$10</b> to reveal your optimized PrizePicks 6-packs.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("💰 AUTHORIZE $10 REVEAL"):
            st.session_state.access_granted = True
            st.rerun()
    else:
        st.markdown("<h1 style='text-align: center;'>🏁 👍</h1>", unsafe_allow_html=True)
        st.success("OFFICIAL: MISSION CLEARED")
        st.balloons()

        # REVEAL TICKETS (25 picks = 4 tickets)
        num_6packs = 4 if total_intel >= 25 else total_intel // 6
        
        for i in range(num_6packs):
            with st.expander(f"🎫 PrizePicks 6-Pack Set {i+1}", expanded=True):
                for idx in range(6):
                    c_leg, c_swap = st.columns([3, 1])
                    with c_leg: st.write(f"Leg {idx+1}: {st.session_state.selected_picks[idx] if len(st.session_state.selected_picks) > idx else 'TBD'}")
                    with c_swap:
                        if st.button(f"🔄 Swap", key=f"swap_{i}_{idx}"):
                            st.session_state.swaps_used += 1
                            if st.session_state.swaps_used > 2:
                                st.warning("⚠️ 50¢ Processing Fee Applied")
                            else: st.success("Free Swap Applied")

        st.divider()
        if st.button("➕ Add Another 25-Leg Set ($3)"):
            st.session_state.stage = 'selection'
            st.rerun()
