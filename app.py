import streamlit as st
import time

# --- INITIAL CONFIG & SESSION STATE ---
st.set_page_config(page_title="Bettor Weather Lab", page_icon="🏀", layout="wide")

if 'stage' not in st.session_state:
    st.session_state.stage = 'briefing'
if 'selected_picks' not in st.session_state:
    st.session_state.selected_picks = []
if 'swaps_used' not in st.session_state:
    st.session_state.swaps_used = 0
if 'access_granted' not in st.session_state:
    st.session_state.access_granted = False

# --- STAGE 1: THE BRIEFING ROOM ---
if st.session_state.stage == 'briefing':
    st.title("📂 The Briefing Room")
    password = st.text_input("Enter Lab Passcode:", type="password")
    
    if password == "SUNNY2026":
        st.success("Access Granted.")
        col1, col2 = st.columns(2)
        with col1:
            st.info("🎙️ **The Veteran Coach**")
            st.video("https://www.youtube.com/watch?v=example1") # Replace with your URL
        with col2:
            st.info("🕵️ **The Insider**")
            st.video("https://www.youtube.com/watch?v=example2") # Replace with your URL
        
        if st.button("PROCEED TO SELECTION FLOOR ➡️"):
            st.session_state.stage = 'selection'
            st.rerun()

# --- STAGE 2: THE SELECTION FLOOR (FANDUEL STYLE) ---
elif st.session_state.stage == 'selection':
    st.title("🏀 Selection Floor: Master Board")

    # PRIZEPICKS HIGHLIGHT
    st.markdown("""
        <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; border: 2px solid #FFD700;">
            <h3 style="color: #FFD700; margin: 0;">🎯 PRIZEPICKS FAST-TRACK</h3>
            <p style="color: white; font-size: 14px;">Build 1 Master List (25 legs) to generate 4 optimized PrizePicks 6-packs.</p>
        </div>
    """, unsafe_allow_html=True)

    # SEARCH & DISCOVERY
    search_query = st.text_input("🔍 Search Player or Matchup:", placeholder="e.g. Luka, Mavericks")

    # GAME & TABBED LAYOUT
    selected_game = st.selectbox("Select Active Game:", ["Mavericks vs Heat", "Lakers vs Celtics", "Nuggets vs Suns"])
    
    tab1, tab2, tab3, tab4 = st.tabs(["Main Lines", "Player Points", "3-Pointers", "Combos"])

    with tab1:
        st.write("Game Outcome Options")
        if st.button(f"Add {selected_game} Spread"): st.session_state.selected_picks.append(f"{selected_game} Spread")

    with tab2:
        p_name = st.selectbox("Select Player:", ["Luka Doncic", "Kyrie Irving", "Jimmy Butler"])
        p_line = st.text_input("Line (e.g. O 28.5):", key="pts")
        if st.button("Add Points Prop"): st.session_state.selected_picks.append(f"{p_name} {p_line} Pts")

    with tab4: # COMBOS
        combo_type = st.radio("Combo Category:", ["P+R", "P+A", "R+A", "PRA"], horizontal=True)
        c_val = st.text_input("Line:", key="combo")
        if st.button("Add Combo"): st.session_state.selected_picks.append(f"Combo: {combo_type} {c_val}")

    st.divider()
    st.metric("Total Picks Collected", len(st.session_state.selected_picks))
    
    if st.button("CONFIRM & GO TO COMMAND CENTER ➡️"):
        st.session_state.stage = 'command'
        st.rerun()

# --- STAGE 3: COMMAND CENTER (THE PAYWALL) ---
elif st.session_state.stage == 'command':
    st.title("🕹️ Command Center")
    total_intel = len(st.session_state.selected_picks)

    if not st.session_state.access_granted:
        st.markdown(f"""
            <div style="background-color: #1E1E1E; padding: 30px; border-radius: 10px; border: 2px solid #00FF00; text-align: center;">
                <h2 style="color: #00FF00;">🔐 MISSION DATA ENCRYPTED</h2>
                <p>Pay <b>$10</b> to reveal your optimized PrizePicks 6-packs.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("💰 AUTHORIZE $10 REVEAL"):
            st.session_state.access_granted = True
            st.rerun()
    else:
        # STRATEGY TOGGLE
        risk_profile = st.radio("Risk Profile:", ["⚓ ANCHOR (Locked Sets)", "🛡️ HEDGE (Diversified)"], horizontal=True)
        
        if st.button("🔓 CRUNCH & OPEN 6-PACKS"):
            st.session_state.crunch_done = True

        if st.session_state.get('crunch_done'):
            st.markdown("<h1 style='text-align: center;'>🏁 👍</h1>", unsafe_allow_html=True)
            st.success("OFFICIAL: MISSION CLEARED")
            st.balloons()

            # TICKET REVEAL WITH SWAPS
            num_6packs = total_intel // 6
            for i in range(num_6packs):
                with st.expander(f"🎫 PrizePicks 6-Pack Set {i+1}", expanded=True):
                    # Show 6 legs per ticket
                    for idx in range(6):
                        col_l, col_s = st.columns([3, 1])
                        with col_l: st.write(f"Leg {idx+1}")
                        with col_s:
                            if st.button(f"🔄 Swap", key=f"s_{i}_{idx}"):
                                st.session_state.swaps_used += 1
                                if st.session_state.swaps_used > 2:
                                    st.warning("⚠️ 50¢ Processing Fee Applied")
                                else: st.success("Free Swap Applied")

            st.divider()
            if st.button("➕ Add Another 25-Leg Set ($3)"):
                st.session_state.stage = 'selection'
                st.rerun()

            if st.button("🔒 LOCK MISSION"):
                st.success("MISSION LOCKED. ALL SWAPS DISABLED.")
