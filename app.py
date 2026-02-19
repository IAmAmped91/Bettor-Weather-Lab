import streamlit as st
import datetime
import os
import random

# --- 1. INITIAL CONFIG & SESSION STATE ---
st.set_page_config(page_title="Bettor Weather Lab", page_icon="🏀", layout="wide")

# Initialize all session states
for key, val in {
    'stage': 'briefing', 'view': 'board', 'active_game': None, 
    'selected_picks': [], 'access_granted': False, 
    'flips_used': 0, 'swaps_used': 0, 'shared': False
}.items():
    if key not in st.session_state: st.session_state[key] = val

# --- 2. DATA: THURSDAY SLATE & LEADERBOARD ---
master_slate = {
    "2026-02-19": [
        {"m": "Celtics vs Warriors", "a": "Celtics", "h": "Warriors", "t": "9:00 PM", "l": {"s": "-3.5/+3.5", "m": "-160/+135", "o": "231.5"}},
        {"m": "Nuggets vs Clippers", "a": "Nuggets", "h": "Clippers", "t": "9:30 PM", "l": {"s": "-1.5/+1.5", "m": "-120/+100", "o": "221.0"}},
        {"m": "Suns vs Spurs", "a": "Suns", "h": "Spurs", "t": "7:30 PM", "l": {"s": "-9.5/+9.5", "m": "-450/+350", "o": "232.5"}}
    ]
}

leaderboard_data = [
    {"user": "Terrell Woods", "badge": "💎 PRO", "win_rate": "78%", "credits": 450},
    {"user": "Lab_Insider", "badge": "⭐ Expert", "win_rate": "64%", "credits": 120},
    {"user": "Sunny_Bettor", "badge": "✅ Verified", "win_rate": "55%", "credits": 85}
]

# --- 3. STAGE 1: THE BRIEFING ROOM ---
if st.session_state.stage == 'briefing':
    st.title("📂 The Briefing Room")
    if st.text_input("Lab Passcode:", type="password") == "SUNNY2026":
        st.success("ACCESS GRANTED.")
        v1, v2 = st.columns(2)
        for col, title, path in zip([v1, v2], ["Veteran Coach", "Lab Insider"], ["videos/coach.mp4", "videos/insider.mp4"]):
            with col:
                st.subheader(title)
                if os.path.exists(path): st.video(open(path, 'rb').read())
                else: st.warning(f"{title} video missing in /videos folder.")
        if st.button("PROCEED TO SELECTION FLOOR ➡️", use_container_width=True):
            st.session_state.stage = 'selection'; st.rerun()

# --- 4. STAGE 2: SELECTION FLOOR (TABS) ---
elif st.session_state.stage == 'selection':
    tabs = st.tabs(["🏀 Scouting Board", "🏆 Leaderboard", "👤 My Mission"])
    
    with tabs[0]: # SCOUTING BOARD
        if st.session_state.view == 'board':
            st.title("🏀 Unified Scouting Board (48hr)")
            for info in master_slate["2026-02-19"]:
                with st.container(border=True):
                    st.caption(f"🕒 {info['t']}")
                    for team_type, team_name, side_key in [("a", info['a'], "as"), ("h", info['h'], "hs")]:
                        c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 2])
                        with c1: st.write(f"### {team_name}")
                        with c2: 
                            if st.checkbox(f"{info['l']['s'].split('/')[0 if team_type=='a' else 1]}", key=f"s_{team_name}"):
                                st.session_state.selected_picks.append(f"{team_name} Spread")
                        with c3: 
                            if st.checkbox(f"{info['l']['m'].split('/')[0 if team_type=='a' else 1]}", key=f"m_{team_name}"):
                                st.session_state.selected_picks.append(f"{team_name} ML")
                        with c4: 
                            lbl = f"O {info['l']['o']}" if team_type == 'a' else f"U {info['l']['o']}"
                            if st.checkbox(lbl, key=f"ou_{team_name}"):
                                st.session_state.selected_picks.append(f"{info['m']} {lbl}")
                        if team_type == 'a':
                            with c5:
                                if st.button(f"🔍 {info['m']} PLAYER PROP AREA", key=f"p_{info['m']}", use_container_width=True):
                                    st.session_state.active_game = info['m']; st.session_state.view = 'props'; st.rerun()
        
        elif st.session_state.view == 'props':
            st.button("⬅️ BACK TO BOARD", on_click=lambda: setattr(st.session_state, 'view', 'board'))
            st.title(f"👤 Prop Market: {st.session_state.active_game}")
            p_tabs = st.tabs(["Pts", "3PT", "Reb", "Ast", "Stl", "Blk", "TO", "PRA", "P+R", "P+A", "R+A", "DD/TD"])
            for pt in p_tabs:
                with pt: st.info(f"Checklist for {pt.label} active for {st.session_state.active_game}.")

    with tabs[1]: # LEADERBOARD
        st.title("🏆 Lab Leaderboard")
        for player in leaderboard_data:
            with st.container(border=True):
                c1, c2, c3 = st.columns([2, 1, 1])
                c1.write(f"### {player['user']} {player['user'] == 'Terrell Woods' and '💎 PRO' or player['badge']}")
                c2.metric("Win Rate", player['win_rate'])
                c3.metric("Swap Credits", player['credits'])

    with tabs[2]: # MY MISSION
        st.title("🎟️ Ticket Progress")
        count = len(st.session_state.selected_picks)
        st.metric("Total Legs", f"{count} / 25")
        for pick in st.session_state.selected_picks: st.write(f"✅ {pick}")
        if count >= 25:
            if st.button("🔓 LOCK MISSION & ENTER COMMAND CENTER", use_container_width=True):
                st.session_state.stage = 'command'; st.rerun()

# --- 5. STAGES 3 & 4: COMMAND CENTER & DUAL PAYWALL ---
elif st.session_state.stage == 'command':
    is_shared = "ticket" in st.query_params
    
    if not st.session_state.access_granted and not is_shared:
        # ORIGINAL BUILDER PAYWALL ($10)
        st.title("🕹️ Command Center")
        if st.button("💰 PAY $10 TO UNLOCK MASTER MISSION", use_container_width=True):
            st.session_state.access_granted = True; st.rerun()
            
    elif is_shared and f"unlocked_{st.query_params['ticket']}" not in st.session_state:
        # SHARED VIEWER PAYWALL ($5 or $10 for PRO)
        builder_is_pro = True # Hardcoded for your links
        price = 10.0 if builder_is_pro else 5.0
        st.title("🔐 Shared AI Mission")
        st.markdown(f"<div style='border:3px solid #FFD700; padding:20px; text-align:center;'><h2>{'💎 PRO' if builder_is_pro else 'Standard'} View</h2><h1>${price:.2f}</h1></div>", unsafe_allow_html=True)
        if st.button(f"💰 PAY ${price:.2f} TO VIEW", use_container_width=True):
            st.session_state[f"unlocked_{st.query_params['ticket']}"] = True; st.rerun()
    else:
        # THE FINAL EXPORT & REWARDS
        st.title("🏁 Stage 4: Referee's Verdict")
        export_text = "🎯 BETTOR WEATHER LAB MISSION\n" + "\n".join(st.session_state.selected_picks)
        st.download_button("📥 EXPORT MISSION TO CLIPBOARD", data=export_text, use_container_width=True)
        
        # Share reward logic
        if st.button("🔗 SHARE MISSION FOR +2 FREE SWAPS", use_container_width=True):
            st.session_state.swaps_used -= 2
            st.toast("Success! Credits added.")
