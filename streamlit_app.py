import streamlit as st
import pandas as pd

# --- 1. CONFIG & DATA ---
st.set_page_config(page_title="Pizza People", layout="wide")

DOUGH_PROFILES = {
    "Neapolitan": {"flour": 162.5, "water": 105.0, "salt": 5.0, "yeast": 0.25, "oil": 0.0, "sugar": 0.0, "starter": 0.0},
    "New York Style": {"flour": 162.5, "water": 100.0, "salt": 3.2, "yeast": 1.0, "oil": 3.2, "sugar": 2.5, "starter": 0.0},
    "Detroit Style": {"flour": 150.0, "water": 105.0, "salt": 3.0, "yeast": 1.25, "oil": 3.0, "sugar": 0.0, "starter": 0.0},
    "Chicago Deep Dish": {"flour": 150.0, "water": 75.0, "salt": 2.5, "yeast": 1.25, "oil": 22.5, "sugar": 0.0, "starter": 0.0},
    "Sourdough": {"flour": 150.0, "water": 97.5, "salt": 4.5, "yeast": 0.0, "oil": 0.0, "sugar": 0.0, "starter": 30.0}
}

# --- 2. STATE MANAGEMENT ---
if "view" not in st.session_state:
    st.session_state.view = "main"
if "plan_executed" not in st.session_state:
    st.session_state.plan_executed = False
if "mock_library" not in st.session_state:
    st.session_state.mock_library = ["Margherita", "Peach & Balsamic", "Pepperoni Detroit"]

# --- 3. UI HELPERS ---
def go_home():
    st.session_state.view = "main"
    st.session_state.plan_executed = False

# --- 4. NAVIGATION HEADER ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🍕 Pizza People</h1>", unsafe_allow_html=True)
if st.session_state.view != "main":
    if st.button("← Back to Start"): 
        go_home()
        st.rerun()
st.write("---")

# --- 5. MAIN MENU ---
if st.session_state.view == "main":
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 What Pizza We Making?", use_container_width=True):
            st.session_state.view = "planner"
            st.rerun()
    with col2:
        if st.button("📚 See the Pizza Library", use_container_width=True):
            st.session_state.view = "library"
            st.rerun()

# --- 6. PLANNER MODULE ---
elif st.session_state.view == "planner":
    st.subheader("Event Planner")
    
    c1, c2 = st.columns(2)
    with c1:
        dough_choice = st.selectbox("Global Dough Type", list(DOUGH_PROFILES.keys()))
    with c2:
        qty = st.number_input("How many pizzas total?", min_value=1, value=4)

    st.write("### Assign Toppings")
    assignments = []
    # Dropdown starts with "Unassigned" as the default
    menu_options = ["Unassigned", "+ Add New Pizza to Library"] + st.session_state.mock_library
    
    for i in range(qty):
        choice = st.selectbox(f"Pizza #{i+1}", menu_options, key=f"piz_{i}")
        
        # Only populate the definition form if "+ Add New" is selected
        if choice == "+ Add New Pizza to Library":
            with st.container(border=True):
                st.markdown("#### ✨ Define New Pizza Details")
                new_name = st.text_input("Pizza Name", key=f"name_in_{i}")
                new_sauce = st.text_area("Sauce Recipe", key=f"sauce_in_{i}")
                new_top = st.text_area("Toppings", key=f"top_in_{i}")
                if st.button("Save & Add to Library", key=f"save_in_{i}"):
                    if new_name and new_name not in st.session_state.mock_library:
                        st.session_state.mock_library.append(new_name)
                        st.success(f"'{new_name}' added! Now select it from the dropdown.")
                        st.rerun()
        assignments.append(choice)

    st.write("---")
    if st.button("🚀 Let's Get Started", use_container_width=True, type="primary"):
        st.session_state.plan_executed = True

    # EXECUTION PHASE
    if st.session_state.plan_executed:
        st.write("---")
        tab1, tab2 = st.tabs(["🛒 (1) Buy the Ingredients", "🥣 (2) Make the Dough"])
        
        with tab1:
            st.write("### Grocery List")
            st.checkbox(f"Base ingredients for {qty}x {dough_choice} Doughs")
            unique_pizzas = set([a for a in assignments if a not in ["Unassigned", "+ Add New Pizza to Library"]])
            for pizza in unique_pizzas:
                st.checkbox(f"Toppings for {pizza}")
        
        with tab2:
            st.write(f"### Dough Lab: {dough_choice}")
            base = DOUGH_PROFILES[dough_choice]
            
            # --- STEP 1: INGREDIENTS (Corrected with Salt & Decimals) ---
            with st.container(border=True):
                st.subheader("🥣 Step 1: Ingredients")
                cc1, cc2, cc3 = st.columns(3)
                with cc1:
                    f_val = cc1.number_input("Flour (g)", value=float(base['flour'] * qty), step=0.1, format="%.1f")
                    s_val = cc1.number_input("Salt (g)", value=float(base['salt'] * qty), step=0.1, format="%.1f")
                with cc2:
                    w_val = cc2.number_input("Water (g)", value=float(base['water'] * qty), step=0.1, format="%.1f")
                    if dough_choice == "Sourdough":
                        st.number_input("Active Starter (g)", value=float(base['starter'] * qty), step=0.1, format="%.1f")
                    else:
                        st.number_input("Yeast (g)", value=float(base['yeast'] * qty), step=0.1, format="%.1f")
                with cc3:
                    if base['oil'] > 0: st.number_input("Oil (g)", value=float(base['oil'] * qty), step=0.1, format="%.1f")
                    if base['sugar'] > 0: st.number_input("Sugar (g)", value=float(base['sugar'] * qty), step=0.1, format="%.1f")
                    hydra = (w_val / f_val * 100) if f_val > 0 else 0
                    st.metric("Hydration %", f"{hydra:.1f}%")

            # --- STEP 2: PROCESS & BAKE (With Dynamic Proofing & Temps) ---
            with st.container(border=True):
                st.subheader("🔥 Step 2: Process & Bake")
                p1, p2, p3 = st.columns(3)
                with p1:
                    st.write("**Fermentation**")
                    f_type = st.radio("Type", ["Cold Ferment", "Room Temp"], horizontal=True)
                    # Dynamic Default Logic
                    if dough_choice == "Sourdough":
                        d_bulk, d_ball = ("24-48h", "6h") if f_type == "Cold Ferment" else ("8-12h", "2-4h")
                    else:
                        d_bulk, d_ball = ("24h", "4-6h") if f_type == "Cold Ferment" else ("4-8h", "2h")
                    
                    if f_type == "Room Temp": st.number_input("Room Temp (°F)", value=72)
                    st.text_input("Bulk Duration", value=d_bulk)
                    st.text_input("Ball Duration", value=d_ball)
                with p2:
                    st.write("**Environment**")
                    st.number_input("Floor Temp (°F)", value=850, step=25)
                    st.number_input("Outside Air (°F)", value=72, step=1)
                with p3:
                    st.write("**Results**")
                    st.slider("Grade", 0.0, 10.0, 8.0, step=0.1)
                st.text_area("Bake Notes")
                if st.button("Log This Experiment", use_container_width=True):
                    st.success("Bake simulation logged!")

# --- 7. LIBRARY MODULE ---
elif st.session_state.view == "library":
    st.subheader("📚 Pizza Library Database")
    st.dataframe(pd.DataFrame({"Pizza Name": st.session_state.mock_library}), use_container_width=True, hide_index=True)
