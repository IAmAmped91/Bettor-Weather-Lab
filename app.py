import streamlit as st
import datetime

# --- INITIAL CONFIG & SESSION STATE ---
st.set_page_config(page_title="Bettor Weather Lab", page_icon="🏀", layout="wide")

if 'stage' not in st.session_state: st.session_state.stage = 'briefing'
if 'view' not in st.session_state: st.session_state.view = 'board'
if 'active_game' not in st.session_state: st.session_state.active_game = None
if 'selected_picks' not in st.session_state: st.session_state.selected_picks = []
if 'access_granted' not in st.session_state: st.session_state.access_granted = False
if 'swaps_used' not in st.session_state: st.session_state.swaps_used = 0

# --- DATA (Daily Slates & Rosters) ---
# Update scores and rosters daily for your stream
game_data = {
    "Bulls vs Knicks": {"score": "102 - 98", "clock": "4th Qtr", "status": "🔴 LIVE"},
    "Mavs vs Heat": {"score": "0 - 0", "clock": "7:00 PM", "status": "📅 TODAY"},
    "Lakers vs Celtics": {"score": "0 - 0", "clock": "Tomorrow", "status": "⏩ UPCOMING"}
}

rosters = {
    "Mavs vs Heat": sorted(["Luka Doncic", "Kyrie Irving", "Klay Thompson", "Jimmy Butler", "Bam Adebayo", "Tyler Herro"]),
    "Lakers vs Celtics": sorted(["LeBron James", "Anthony Davis", "Austin Reaves", "Jayson Tatum", "Jaylen Brown", "Derrick White"]),
    "Bulls vs Knicks": sorted(["Coby White", "Zach LaVine", "Nikola Vucevic", "Jalen Brunson", "Karl-Anthony Towns", "Josh Hart"])
}

# --- STAGE 1: BRIEFING ROOM ---
if st.session_state.stage == 'briefing':
    st.title("📂 The Briefing Room")
    if st.text_input("Lab Passcode:", type="password") == "SUNNY2026":
        st.video("https://www.youtube.com/watch?v=example1")
        if st.button("PROCEED TO SELECTION FLOOR ➡️"):
            st.session_state.stage = 'selection'
            st.rerun()

# --- STAGE 2: SELECTION FLOOR ---
elif st.session_state.stage == 'selection':

    # VIEW 1: UNIFIED MAIN BOARD
    if st.session_state.view == 'board':
        st.title("🏀 Unified Scouting Board")
        
        for g_name, info in game_data.items():
            with st.container(border=True):
                st.write(f"### {g_name}")
                st.caption(f"{info['status']} | {info['clock']} | Score: {info['score']}")
                
                c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
                
                # Checkbox Main Lines
                with c1:
                    if st.checkbox("Spread", key=f"s_{g_name}"):
                        pick = f"{g_name} Spread"
                        if pick not in st.session_state.selected_picks: st.session_state.selected_picks.append(pick)
                with c2:
                    if st.checkbox("ML", key=f"m_{g_name}"):
                        pick = f"{g_name} Moneyline"
                        if pick not in st.session_state.selected_picks: st.session_state.selected_picks.append(pick)
                with c3:
                    if st.checkbox("O/U", key=f"o_{g_name}"):
                        pick = f"{g_name} Total"
                        if pick not in st.session_state.selected_picks: st.session_state.selected_picks.append(pick)
                
                with c4:
                    if st.button("🔍 ENTER PLAYER AREA (PROPS)", key=f"btn_{g_name}", use_container_width=True):
                        st.session_state.active_game = g_name
                        st.session_state.view = 'player_area'
                        st.rerun()

    # VIEW 2: PLAYER AREA (CHECKLIST WITH SCOREBOARD)
    elif st.session_state.view == 'player_area':
        game = st.session_state.active_game
        info = game_data.get(game, {})
        
        # Back Button & Live Scoreboard Header
        st.button("⬅️ BACK TO BOARD", on_click=lambda: setattr(st.session_state, 'view', 'board'))
        
        st.markdown(f"""
            <div style="background-color: #333; padding: 15px; border-radius: 10px; border: 2px solid #FFD700; text-align: center; margin-bottom: 20px;">
                <h2 style="margin: 0; color: #FFD700;">{game}</h2>
                <h3 style="margin: 0; color: white;">{info.get('score', '')}</h3>
                <p style="margin: 0; color: #888;">{info.get('clock', '')}</p>
            </div>
        """, unsafe_allow_html=True)

        cat = st.radio("Scouting Projections:", ["Points", "Rebounds", "Assists", "3-Pointers", "Combos"], horizontal=True)
        st.divider()

        # The Full Roster Checklist
        for player in rosters.get(game, []):
            with st.container(border=True):
                col_n, col_ou, col_line, col_chk = st.columns([2, 2, 1.5, 1])
                with col_n:
                    st.write(f"**{player}**")
                    st.caption(f"Category: {cat}")
                with col_ou:
                    side = st.radio("Side:", ["Over", "Under"], key=f"ou_{player}_{cat}", horizontal=True, label_visibility="collapsed")
                with col_line:
                    line = st.text_input("Line", value="15.5", key=f"v_{player}_{cat}", label_visibility="collapsed")
                with col_chk:
                    pick_id = f"{player} {side} {line} {cat}"
                    if st.checkbox("Add", key=f"chk_{player}_{cat}"):
                        if pick_id not in st.session_state.selected_picks: st.session_state.selected_picks.append(pick_id)
                    elif pick_id in st.session_state.selected_picks:
                        st.session_state.selected_picks.remove(pick_id)

    # THE STICKY FOOTER TICKET
    st.markdown("""
        <style>
        .sticky-footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #1E1E1E; 
                        border-top: 3px solid #FFD700; padding: 10px; text-align: center; z-index: 1000; }
        </style>
    """, unsafe_allow_html=True)
    
    current_count = len(st.session_state.selected_picks)
    st.markdown(f'<div class="sticky-footer"><h3 style="color: #FFD700; margin: 0;">🎟️ TICKET: {current_count} / 25 LEGS</h3></div>', unsafe_allow_html=True)

    if current_count >= 25:
        if st.button("🔓 LOCK MISSION & GO TO COMMAND CENTER", use_container_width=True):
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
        # Ticket Generation Logic...
        num_sets = len(st.session_state.selected_picks) // 6
        for i in range(min(4, num_sets)):
            with st.expander(f"🎫 PrizePicks 6-Pack Set {i+1}", expanded=True):
                st.write("Optimized Picks Revealed...")
                if st.button(f"🔄 Swap", key=f"sw_{i}"):
                    st.session_state.swaps_used += 1
                    if st.session_state.swaps_used > 2: st.warning("⚠️ 50¢ Fee Applied")
        
        if st.button("➕ Add Another 25-Leg Set ($3)"):
            st.session_state.stage = 'selection'
            st.session_state.view = 'board'
            st.rerun()
