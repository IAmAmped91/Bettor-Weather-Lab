import streamlit as st
import datetime

# --- CONFIG ---
st.set_page_config(page_title="Bettor Weather Lab", page_icon="🏀", layout="wide")

if 'stage' not in st.session_state: st.session_state.stage = 'briefing'
if 'selected_picks' not in st.session_state: st.session_state.selected_picks = []
if 'swaps_used' not in st.session_state: st.session_state.swaps_used = 0
if 'access_granted' not in st.session_state: st.session_state.access_granted = False

# --- TEAM ROSTERS (Alphabetized) ---
teams = {
    "Mavs": sorted(["Luka Doncic", "Kyrie Irving", "Klay Thompson", "P.J. Washington", "Daniel Gafford"]),
    "Heat": sorted(["Jimmy Butler", "Bam Adebayo", "Tyler Herro", "Terry Rozier", "Duncan Robinson"]),
    "Lakers": sorted(["LeBron James", "Anthony Davis", "Austin Reaves", "D'Angelo Russell"]),
    "Celtics": sorted(["Jayson Tatum", "Jaylen Brown", "Derrick White", "Jrue Holiday", "Kristaps Porzingis"]),
    "Bulls": sorted(["Coby White", "Zach LaVine", "Nikola Vucevic", "Josh Giddey"]),
    "Knicks": sorted(["Jalen Brunson", "Karl-Anthony Towns", "Josh Hart", "OG Anunoby"])
}

# --- STAGE 1: BRIEFING ROOM ---
if st.session_state.stage == 'briefing':
    st.title("📂 The Briefing Room")
    if st.text_input("Lab Passcode:", type="password") == "SUNNY2026":
        st.video("https://www.youtube.com/watch?v=example1")
        if st.button("PROCEED TO SELECTION FLOOR ➡️"):
            st.session_state.stage = 'selection'
            st.rerun()

# --- STAGE 2: THE FULL SPREAD UNIFIED BOARD ---
elif st.session_state.stage == 'selection':
    st.title("🏀 Unified Scouting Board: Full Spread")
    
    dates = [
        {"label": "🔴 LIVE FIRE", "games": [{"m": "Bulls vs Knicks", "s": "105-102", "r": sorted(teams["Bulls"] + teams["Knicks"])}]},
        {"label": f"📅 TODAY - {datetime.date.today().strftime('%b %d')}", "games": [{"m": "Mavs vs Heat", "r": sorted(teams["Mavs"] + teams["Heat"])}]},
        {"label": f"⏩ TOMORROW - {(datetime.date.today() + datetime.timedelta(days=1)).strftime('%b %d')}", "games": [{"m": "Lakers vs Celtics", "r": sorted(teams["Lakers"] + teams["Celtics"])}]}
    ]

    for day in dates:
        st.markdown(f"### {day['label']}")
        for g in day['games']:
            with st.container(border=True):
                st.write(f"🏀 **{g['m']}**")
                cat_col, player_col, line_col = st.columns([1.5, 2, 1])
                
                with cat_col:
                    market = st.radio("Category:", ["Points", "Rebounds", "Assists", "3-Pointers", "Combos", "Steals", "Blocks"], key=f"cat_{g['m']}")
                with player_col:
                    p_target = st.selectbox(f"Select Player ({market}):", g['r'], key=f"p_{g['m']}_{market}")
                with line_col:
                    l_val = st.text_input("Line:", placeholder="O 22.5", key=f"l_{g['m']}_{market}")
                
                if st.button(f"📥 Add {p_target} ({market})", key=f"btn_{g['m']}_{market}"):
                    if l_val:
                        st.session_state.selected_picks.append(f"{p_target} {l_val} {market}")
                        st.toast(f"Added {p_target}!")

    st.divider()
    st.markdown(f"### 📥 Total Pool: **{len(st.session_state.selected_picks)} / 25**")
    if st.button("🚀 FINALIZE ROSTER & CRUNCH"):
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
        st.success("🏁 OFFICIAL: MISSION CLEARED 👍")
        st.balloons()
        num_6packs = len(st.session_state.selected_picks) // 6
        for i in range(min(4, num_6packs)):
            with st.expander(f"🎫 PrizePicks 6-Pack Set {i+1}", expanded=True):
                st.write(f"Scouting Results for Ticket {i+1}...")
                if st.button(f"🔄 Swap (Used: {st.session_state.swaps_used})", key=f"sw_{i}"):
                    st.session_state.swaps_used += 1
                    if st.session_state.swaps_used > 2: st.warning("⚠️ 50¢ Fee Applied")
        
        if st.button("➕ Add Another 25-Leg Set ($3)"):
            st.session_state.stage = 'selection'
            st.rerun()
