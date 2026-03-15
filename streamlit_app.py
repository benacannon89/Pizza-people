import streamlit as st
import pandas as pd

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Pizza People", layout="wide", initial_sidebar_state="collapsed")

# --- 2. DOUGH PROFILES DATA ---
DOUGH_PROFILES = {
    "Neapolitan": {"flour": 162.5, "water": 105.0, "salt": 5.0, "yeast": 0.25, "oil": 0.0, "sugar": 0.0, "starter": 0.0},
    "New York Style": {"flour": 162.5, "water": 100.0, "salt": 3.2, "yeast": 1.0, "oil": 3.2, "sugar": 2.5, "starter": 0.0},
    "Detroit Style": {"flour": 150.0, "water": 105.0, "salt": 3.0, "yeast": 1.25, "oil": 3.0, "sugar": 0.0, "starter": 0.0},
    "Chicago Deep Dish": {"flour": 150.0, "water": 75.0, "salt": 2.5, "yeast": 1.25, "oil": 22.5, "sugar": 0.0, "starter": 0.0},
    "Sourdough": {"flour": 150.0, "water": 97.5, "salt": 4.5, "yeast": 0.0, "oil": 0.0, "sugar": 0.0, "starter": 30.0}
}

# --- 3. STATE MANAGEMENT ---
if "page" not in st.session_state:
    st.session_state.page = "home"

# --- 4. HEADER ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🍕 Pizza People</h1>", unsafe_allow_html=True)
st.write("---")

# --- 5. TOP NAVIGATION ---
col1, col2, col3 = st.columns(3)
if col1.button("🍴 See the Menu & Order", use_container_width=True): st.session_state.page = "menu"
if col2.button("🧪 Make Some Dough", use_container_width=True): st.session_state.page = "dough"
if col3.button("📚 Add to Library", use_container_width=True): st.session_state.page = "add"

# --- 6. PAGE LOGIC ---

# MODULE 2: DOUGH LAB (Updates here)
if st.session_state.page == "dough":
    st.header("🧪 The Dough Lab")
    
    selected_style = st.selectbox("Select Dough Style", list(DOUGH_PROFILES.keys()))
    num_pizzas = st.number_input("Number of Pizzas to Make", min_value=1, value=4)
    base = DOUGH_PROFILES[selected_style]
    
    # --- STEP 1: INGREDIENTS ---
    with st.container(border=True):
        st.subheader("🥣 Step 1: Ingredients")
        c1, c2, c3 = st.columns(3)
        with c1:
            f_val = st.number_input("Flour (g)", value=float(base['flour'] * num_pizzas), step=0.1, format="%.1f")
            s_val = st.number_input("Salt (g)", value=float(base['salt'] * num_pizzas), step=0.1, format="%.1f")
        with c2:
            w_val = st.number_input("Water (g)", value=float(base['water'] * num_pizzas), step=0.1, format="%.1f")
            if selected_style == "Sourdough":
                st.number_input("Active Starter (g)", value=float(base['starter'] * num_pizzas), step=0.1, format="%.1f")
            else:
                st.number_input("Yeast (g)", value=float(base['yeast'] * num_pizzas), step=0.1, format="%.1f")
        with c3:
            if base['oil'] > 0:
                st.number_input("Oil/Fat (g)", value=float(base['oil'] * num_pizzas), step=0.1, format="%.1f")
            if base['sugar'] > 0:
                st.number_input("Sugar (g)", value=float(base['sugar'] * num_pizzas), step=0.1, format="%.1f")
            st.metric("Hydration %", f"{(w_val / f_val * 100) if f_val > 0 else 0:.1f}%")

    # --- STEP 2: PROCESS & BAKE (Fermentation added) ---
    with st.container(border=True):
        st.subheader("🔥 Step 2: Process & Bake")
        p1, p2, p3 = st.columns(3)
        
        with p1:
            st.write("**Fermentation**")
            ferm_type = st.radio("Type", ["Cold Ferment (Fridge)", "Room Temp"], horizontal=True)
            if ferm_type == "Room Temp":
                room_temp = st.number_input("Room Temp (°F)", value=72)
            bulk_time = st.text_input("Bulk Duration", "24h")
            ball_time = st.text_input("Ball Duration", "6h")
            
        with p2:
            st.write("**Environment**")
            st.number_input("Floor Temp (°F)", value=850, step=25)
            st.number_input("Outside Air (°F)", value=72, step=1)
            
        with p3:
            st.write("**Results**")
            grade = st.slider("Final Grade", 0.0, 10.0, 8.0, step=0.1)

        st.text_area("Bake Notes")
        if st.button("Log This Experiment", use_container_width=True):
            st.success("Bake logged locally!")

# (Rest of the script remains same for menu/add)
elif st.session_state.page == "menu":
    st.header("Current Menu")
elif st.session_state.page == "add":
    st.header("Add to Library")
else:
    st.write("Welcome to Pizza People.")
