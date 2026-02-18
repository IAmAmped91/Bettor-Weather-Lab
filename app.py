import streamlit as st
import datetime

# --- INITIAL CONFIG & SESSION STATE ---
st.set_page_config(page_title="Bettor Weather Lab", page_icon="🏀", layout="wide")

if 'stage' not in st.session_state: st.session_state.stage = 'briefing'
if 'selected_picks' not in st.session_state: st.session_state.selected_picks = []
if 'prizepicks_mode' not in st.session_state: st.session_state.prizepicks_mode = False
if 'access_granted' not in st.session_state: st.session_state.access_granted = False
if 'swaps_used' not in st.session_state: st.session_state.swaps_used = 0

# --- TEAM ROSTERS ---
teams = {
    "Bulls": ["Coby White", "Zach LaVine", "Nikola Vucevic", "Josh Giddey"],
    "Knicks": ["Jalen Brunson", "Karl-Anthony Towns", "Josh Hart", "OG Anunoby"],
    "Mavs": ["Luka Doncic", "Kyrie Irving", "Klay Thompson", "P.J. Washington"],
    "Heat": ["Jimmy Butler", "Bam Adebayo", "Tyler Herro", "Terry Rozier"],
    "Lakers": ["LeBron James", "Anthony Davis", "Austin Reaves", "D'Lo Russell"],
    "Celtics": ["Jayson Tatum", "Jaylen Brown", "Derrick White", "Jrue Holiday"]
}

# --- STAGE 1: THE BRIEFING ROOM ---
if st.session_state.stage == 'briefing':
    st.title("📂 The Briefing Room")
    if st.text_input("Lab Passcode:", type="password") == "SUNNY2026":
        st.video("https://www.youtube.com/watch?v=example1")
        if st.button("PROCEED TO SELECTION FLOOR ➡️"):
            st.session_state.stage = 'selection'
            st.rerun()

# --- STAGE 2: THE SELECTION FLOOR ---
elif st.session_state.stage == 'selection':
    # 1. TOP NAVIGATION & TOGGLE
    col_t, col_m = st.columns([3, 1])
    with col_t:
        st.title("🏀 Scouting Floor")
    with col_m:
        mode_label = "🎯 PRIZEPICKS MODE" if not st.session_state.prizepicks_mode else "🏦 STANDARD MODE"
        if st.button(mode_label):
            st.session_state.prizepicks_mode = not st.session_state.prizepicks_mode
            st.rerun()

    # 2. THE UNIFIED BOARD (Infinite Scroll)
    slates = [
        {"label": "🔴 LIVE FIRE", "games": [{"m": "Bulls vs Knicks", "s": "102-98", "r": teams["Bulls"]+teams["Knicks"]}]},
        {"label": "📅 TODAY", "games": [{"m": "Mavs vs Heat", "r": teams["Mavs"]+teams["Heat"]}]},
        {"label": "⏩ TOMORROW", "games": [{"m": "Lakers vs Celtics", "r": teams["Lakers"]+teams["Celtics"]}]}
    ]

    for day in slates:
        st.markdown(f"### {day['label']}")
        for g in day['games']:
            with st.container(border=True):
                st.subheader(f"🏀 {g['m']}")
                
                # Main Lines (Hidden in PrizePicks Mode)
                if not st.session_state.prizepicks_mode:
                    c1, c2, c3 = st.columns(3)
                    if c1.button("Spread", key=f"s_{g['m']}"): st.session_state.selected_picks.append(f"{g['m']} Spread")
                    if c2.button("Total", key=f"t_{g['m']}"): st.session_state.selected_picks.append(f"{g['m']} Total")
                    if c3.button("ML", key=f"m_{g['m']}"): st.session_state.selected_picks.append(f"{g['m']} ML")
                
                # PLAYER SERIES (The Deep Dive)
                st.write("**Player Series**")
                tabs = st.tabs(["Points", "Combos", "3-Pointers", "Defense"])
                
                with tabs[0]: # Points
                    for player in sorted(g['r']):
                        col_n, col_i, col_a = st.columns([2, 1, 1])
                        with col_n: st.write(player)
                        with col_i: val = st.text_input("Line", key=f"lp_{player}_{g['m']}", label_visibility="collapsed")
                        with col_a: 
                            if st.button("Add", key=f"ap_{player}_{g['m']}"):
                                if val: st.session_state.selected_picks.append(f"{player} {val} Pts")
                # (Other tabs would follow the same pattern)

    # 3. THE STICKY FOOTER TICKET
    st.markdown("""
        <style>
        .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #1E1E1E; 
                  color: white; text-align: center; padding: 15px; border-top: 3px solid #FFD700; z-index: 1000; }
        </style>
    """, unsafe_allow_html=True)
    
    current_count = len(st.session_state.selected_picks)
    recent_picks = ", ".join([p.split(" ")[0] for p in st.session_state.selected_picks[-3:]])
    
    st.markdown(f"""
        <div class="footer">
            <span style="font-size: 20px;">🎟️ <b>TICKET PROGRESS: {current_count} / 25 LEGS</b></span><br>
            <span style="color: #888;">Latest: {recent_picks if recent_picks else 'Empty'}</span>
        </div>
    """, unsafe_allow_html=True)

    if current_count >= 25:
        if st.button("🔓 LOCK 25-LEG MISSION & CRUNCH", use_container_width=True):
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
        st.success("🏁 MISSION CLEARED 👍")
        num_6packs = len(st.session_state.selected_picks) // 6
        for i in range(min(4, num_6packs)):
            with st.expander(f"🎫 PrizePicks 6-Pack Set {i+1}", expanded=True):
                st.write("Ticket Intel Revealed Here...")
                if st.button(f"🔄 Swap", key=f"sw_{i}"):
                    st.session_state.swaps_used += 1
                    if st.session_state.swaps_used > 2: st.warning("⚠️ 50¢ Fee Applied")
        
        if st.button("➕ Add Another 25-Leg Set ($3)"):
            st.session_state.stage = 'selection'
            st.rerun()
