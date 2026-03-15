import streamlit as st
import pandas as pd

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Pizza People", layout="wide", initial_sidebar_state="collapsed")

# --- 2. DOUGH PROFILES DATA ---
# Baseline amounts per 1 personal pizza
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
if "shopping_list" not in st.session_state:
    st.session_state.shopping_list = []

# --- 4. HEADER ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🍕 Pizza People</h1>", unsafe_allow_html=True)
st.write("---")

# --- 5. TOP NAVIGATION ---
col1, col2, col3 = st.columns(3)
if col1.button("🍴 See the Menu & Order", use_container_width=True): 
    st.session_state.page = "menu"
if col2.button("🧪 Make Some Dough", use_container_width=True): 
    st.session_state.page = "dough"
if col3.button("📚 Add to Library", use_container_width=True): 
    st.session_state.page = "add"

# --- 6. PAGE LOGIC ---

# MODULE 1: MENU & ORDERING
if st.session_state.page == "menu":
    st.header("Current Menu")
    st.info("Your pizza library will appear here as 'Menu Cards'.")
    # (Library rendering logic goes here)

# MODULE 2: DOUGH LAB
elif st.session_state.page == "dough":
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
            
            hydra = (w_val / f_val) * 100 if f_val > 0 else 0
            st.metric("Hydration %", f"{hydra:.1f}%")

    # --- STEP 2: PROCESS & BAKE ---
    with st.container(border=True):
        st.subheader("🔥 Step 2: Process & Bake")
        p1, p2, p3 = st.columns(3)
        
        with p1:
            st.write("**Proofing**")
            st.text_input("Bulk Proof", "24h Cold")
            st.text_input("Ball Proof", "6h Room Temp")
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

# MODULE 3: ADD TO LIBRARY
elif st.session_state.page == "add":
    st.header("📚 Add to the Pizza Library")
    with st.form("add_pizza_form"):
        name = st.text_input("Pizza Name")
        d_type = st.selectbox("Dough Type", list(DOUGH_PROFILES.keys()))
        sauce = st.text_area("Sauce Recipe")
        toppings = st.text_area("Topping List")
        if st.form_submit_button("Save Pizza to Library"):
            st.success(f"{name} added to library (locally)!")

# DEFAULT / HOME PAGE
else:
    st.write("Welcome to Pizza People. Use the buttons above to navigate.")
