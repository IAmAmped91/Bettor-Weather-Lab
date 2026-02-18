import streamlit as st
import datetime

# --- 1. INITIAL CONFIG & SESSION STATE ---
st.set_page_config(page_title="Bettor Weather Lab", page_icon="🏀", layout="wide")

if 'stage' not in st.session_state: st.session_state.stage = 'briefing'
if 'view' not in st.session_state: st.session_state.view = 'board'
if 'active_game' not in st.session_state: st.session_state.active_game = None
if 'selected_picks' not in st.session_state: st.session_state.selected_picks = []
if 'access_granted' not in st.session_state: st.session_state.access_granted = False
if 'flips_used' not in st.session_state: st.session_state.flips_used = 0
if 'swaps_used' not in st.session_state: st.session_state.swaps_used = 0

# --- 2. DATA ENGINE (Slates, Rosters, & AI Coach) ---
game_data = {
    "Celtics vs Warriors": {"away": "Celtics", "home": "Warriors", "clock": "9:00 PM", "score": "0-0", "lines": {"spr": "-2.5 / +2.5", "ml": "-140 / +120", "tot": "228.5"}},
    "Knicks vs Pistons": {"away": "Pistons", "home": "Knicks", "clock": "7:30 PM", "score": "0-0", "lines": {"spr": "+4.5 / -4.5", "ml": "+152 / -180", "tot": "222.5"}},
    "Suns vs Spurs": {"away": "Suns", "home": "Spurs", "clock": "🔴 LIVE", "score": "45-42", "lines": {"spr": "-8.5 / +8.5", "ml": "-350 / +280", "tot": "231.0"}}
}

projections = {
    "Celtics vs Warriors": {"Jayson Tatum": 27.5, "Steph Curry": 26.5, "Jaylen Brown": 22.5},
    "Knicks vs Pistons": {"Jalen Brunson": 28.5, "Cade Cunningham": 22.5, "Josh Hart": 12.5}
}

ai_coach_intel = "🤖 **COACH:** Defensive matchups suggest a slow pace. Under is the high-probability lean."

# --- 3. STAGE 1: BRIEFING ROOM ---
if st.session_state.stage == 'briefing':
    st.title("📂 The Briefing Room")
    passcode = st.text_input("Lab Passcode:", type="password")
    if passcode == "SUNNY2026":
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Placeholder
        if st.button("PROCEED TO SELECTION FLOOR ➡️", use_container_width=True):
            st.session_state.stage = 'selection'
            st.rerun()

# --- 4. STAGE 2: SELECTION FLOOR (Board & Player Area) ---
elif st.session_state.stage == 'selection':
    if st.session_state.view == 'board':
        st.title("🏀 Unified Scouting Board")
        for g_name, info in game_data.items():
            with st.container(border=True):
                st.write(f"### {g_name} | {info['clock']}")
                c1, c2, c3, c4 = st.columns([1, 1, 1, 1.5])
                with c1: # SPREADS
                    if st.checkbox(f"{info['away']} {info['lines']['spr'].split(' / ')[0]}", key=f"s1_{g_name}"):
                        st.session_state.selected_picks.append(f"{info['away']} Spread")
                    if st.checkbox(f"{info['home']} {info['lines']['spr'].split(' / ')[1]}", key=f"s2_{g_name}"):
                        st.session_state.selected_picks.append(f"{info['home']} Spread")
                with c2: # ML
                    if st.checkbox(f"{info['away']} {info['lines']['ml'].split(' / ')[0]}", key=f"m1_{g_name}"):
                        st.session_state.selected_picks.append(f"{info['away']} ML")
                with c3: # TOTALS
                    if st.checkbox(f"Over {info['lines']['tot']}", key=f"o_{g_name}"):
                        st.session_state.selected_picks.append(f"{g_name} Over")
                with c4:
                    if st.button("🔍 ENTER PLAYER AREA", key=f"pa_{g_name}", use_container_width=True):
                        st.session_state.active_game = g_name
                        st.session_state.view = 'player_area'
                        st.rerun()

    elif st.session_state.view == 'player_area':
        game = st.session_state.active_game
        st.button("⬅️ BACK TO BOARD", on_click=lambda: setattr(st.session_state, 'view', 'board'))
        st.title(f"👤 Player Area: {game}")
        cat = st.radio("Projections:", ["Points", "Assists", "Rebounds"], horizontal=True)
        for player, line in projections.get(game, {}).items():
            with st.container(border=True):
                col_n, col_ou, col_val, col_chk = st.columns([2, 1.5, 1, 1])
                with col_n: st.write(f"**{player}**"); st.caption(f"Prop: {cat}")
                with col_ou: side = st.radio("Side:", ["Over", "Under"], key=f"ou_{player}_{cat}", horizontal=True, label_visibility="collapsed")
                with col_val: final_line = st.text_input("Line", value=str(line), key=f"v_{player}_{cat}", label_visibility="collapsed")
                with col_chk:
                    if st.checkbox("Add", key=f"chk_{player}_{cat}"):
                        st.session_state.selected_picks.append(f"{player} {side} {final_line} {cat}")

    # STICKY TICKET FOOTER
    count = len(st.session_state.selected_picks)
    st.markdown(f'<div style="position:fixed;bottom:0;left:0;width:100%;background:#1E1E1E;border-top:3px solid #FFD700;padding:10px;text-align:center;z-index:1000;"><h3 style="color:#FFD700;margin:0;">🎟️ TICKET: {count} / 25 LEGS</h3></div>', unsafe_allow_html=True)
    if count >= 25:
        if st.button("🔓 LOCK MISSION & GO TO COMMAND CENTER", use_container_width=True):
            st.session_state.stage = 'command'; st.rerun()

# --- 5. STAGE 3 & 4: COMMAND CENTER & REFEREE'S VERDICT ---
elif st.session_state.stage == 'command':
    if not st.session_state.access_granted:
        st.title("🕹️ Command Center: The Vault")
        st.error("🔐 MISSION DATA ENCRYPTED. Pay $10 to Reveal.")
        if st.button("💰 AUTHORIZE $10 REVEAL", use_container_width=True):
            st.session_state.access_granted = True; st.rerun()
    else:
        st.title("🏁 Stage 4: The Referee's Verdict")
        st.markdown("<h1 style='text-align:center;'>👍</h1>", unsafe_allow_html=True)
        for i in range(4):
            with st.expander(f"🎫 PrizePicks 6-Pack Set {i+1}", expanded=True):
                for leg_idx in range(6):
                    c_p, c_side, c_coach, c_flip, c_swap = st.columns([1.5, 1, 3, 1.5, 1.5])
                    with c_p: st.write("**Jayson Tatum**")
                    with c_side: st.write("**Over**")
                    with c_coach: st.info(ai_coach_intel)
                    with c_flip:
                        if st.button("🔄 FLIP", key=f"f_{i}_{leg_idx}"):
                            if st.session_state.flips_used < 2: st.session_state.flips_used += 1; st.toast("Flipped!")
                            else: st.error("LOCKED")
                    with c_swap:
                        if st.button("🔀 SWAP", key=f"s_{i}_{leg_idx}"):
                            if st.session_state.swaps_used < 3: st.session_state.swaps_used += 1; st.toast("Swapped!")
                            else: st.warning("⚠️ 50¢ Fee")
        st.divider()
        m1, m2 = st.columns(2)
        m1.metric("Coach Flips Available", 2 - st.session_state.flips_used)
        m2.metric("Free Swaps Available", 3 - st.session_state.swaps_used)
