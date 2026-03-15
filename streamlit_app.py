import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Pizza People", layout="wide")

# --- CUSTOM HEADER ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🍕 Pizza People</h1>", unsafe_allow_html=True)
st.write("---")

# --- STATE MANAGEMENT ---
if "page" not in st.session_state:
    st.session_state.page = "menu"

if 'dough_defaults' not in st.session_state:
    st.session_state.dough_defaults = {
        "Neapolitan": {"flour": 500.0, "water": 325.0, "salt": 15.0},
        "New York Style": {"flour": 500.0, "water": 310.0, "salt": 10.0},
        "Detroit Style": {"flour": 400.0, "water": 280.0, "salt": 8.0},
        "Chicago Deep Dish": {"flour": 600.0, "water": 300.0, "salt": 12.0},
        "Other": {"flour": 500.0, "water": 325.0, "salt": 15.0}
    }

# --- TOP NAVIGATION ---
col1, col2, col3 = st.columns(3)
if col1.button("🍴 See the Menu & Order", use_container_width=True): st.session_state.page = "menu"
if col2.button("🧪 Make Some Dough", use_container_width=True): st.session_state.page = "dough"
if col3.button("📚 Add to Library", use_container_width=True): st.session_state.page = "add"

# --- MODULE 1: MENU ---
if st.session_state.page == "menu":
    st.subheader("Pizza Menu")
    st.info("This is where your guests will 'order' pizzas.")
    # (Simplified menu placeholder)

# --- MODULE 2: DOUGH LAB (FIXED SYNTAX) ---
elif st.session_state.page == "dough":
    st.subheader("🧪 The Dough Lab")

    style = st.selectbox("Select Dough Style", list(st.session_state.dough_defaults.keys()))
    current_default = st.session_state.dough_defaults[style]

    with st.container(border=True):
        st.write(f"### Current {style} Bake")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            f_val = st.number_input("Flour (g)", value=current_default['flour'], step=0.1, format="%.1f")
            s_val = st.number_input("Salt (g)", value=current_default['salt'], step=0.1, format="%.1f")
        with c2:
            w_val = st.number_input("Water (g)", value=current_default['water'], step=0.1, format="%.1f")
            hydra = (w_val / f_val) * 100 if f_val > 0 else 0
            st.metric("Hydration %", f"{hydra:.1f}%")
        with c3:
            # DESIGN TIP: Oven Temperature tracking
            st.write("**Oven Specs**")
            floor_temp = st.number_input("Floor Temp (°F)", value=850, step=25)
            ambient_temp = st.number_input("Outside Air Temp (°F)", value=70, step=1)

        st.write("---")
        c4, c5 = st.columns(2)
        with c4:
            proof = st.text_input("Bulk Proof Time", placeholder="e.g. 24h Cold")
        with c5:
            ball_time = st.text_input("Time in Ball", placeholder="e.g. 6h Room Temp")

        notes = st.text_area("Bake Notes")
        grade = st.slider("Final Grade (Decimal)", 0.0, 10.0, 5.0, step=0.1)
        
        if st.button("Log This Bake"):
            st.success("Bake simulation successful! (Wait for Google Sheets API to save for real)")

    st.write("### History Log")
    # Mock table matching your requested columns
    history_cols = ["Date", "Grade", "Flour (g)", "Water (g)", "Hydration %", "Salt (g)", "Proof Time", "Time in Ball", "Floor Temp", "Notes"]
    mock_history = pd.DataFrame([
        ["2026-03-01", 9.2, 500.0, 325.0, "65.0%", 15.0, "24h", "6h", "850°F", "Perfect leopard spotting"]
    ], columns=history_cols)
    st.dataframe(mock_history, use_container_width=True, hide_index=True)

# --- MODULE 3: ADD TO LIBRARY ---
elif st.session_state.page == "add":
    st.subheader("Add to Library")
    # (Placeholder)
