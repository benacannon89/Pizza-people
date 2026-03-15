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
    # Starting with a few defaults
    st.session_state.mock_library = ["Margherita", "Peach & Balsamic", "Pepperoni Detroit"]

# --- 3. UI HELPERS ---
def go_home():
    st.session_state.view = "main"
    st.session_state.plan_executed = False

# --- 4. NAVIGATION HEADER ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🍕 Pizza People</h1>", unsafe_allow_html=True)

# Only show back button if not on home
if st.session_state.view != "main":
    if st.button("← Back to Start"): 
        go_home()
        st.rerun()
st.write("---")

# --- 5. MAIN MENU ---
if st.session_state.view == "main":
    col1, col2 = st.columns(2)
    with col1:
        # Removed 'height' to prevent version compatibility errors
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
    
    # Global Setup
    c1, c2 = st.columns(2)
    with c1:
        dough_choice = st.selectbox("Global Dough Type", list(DOUGH_PROFILES.keys()))
    with c2:
        qty = st.number_input("How many pizzas total?", min_value=1, value=4)

    st.write("### Assign Toppings")
    assignments = []
    # Dynamic list for dropdown
    menu_options = ["+ Add New Pizza to Library"] + st.session_state.mock_library
    
    for i in range(qty):
        choice = st.selectbox(f"Pizza #{i+1}", menu_options, key=f"piz_{i}")
        
        # If user chooses to add a new pizza inline
        if choice == "+ Add New Pizza to Library":
            with st.expander("✨ Define New Pizza Details", expanded=True):
                new_name = st.text_input("Pizza Name", key=f"name_input_{i}")
                new_sauce = st.text_area("Sauce Recipe", key=f"sauce_input_{i}")
                new_top = st.text_area("Toppings/Ingredients", key=f"top_input_{i}")
                if st.button("Save & Add to Library", key=f"save_btn_{i}"):
                    if new_name and new_name not in st.session_state.mock_library:
                        st.session_state.mock_library.append(new_name)
                        st.success(f"'{new_name}' added! Now select it from the dropdown above.")
                        st.rerun()
        assignments.append(choice)

    st.write("---")
    if st.button("🚀 Let's Get Started", use_container_width=True, type="primary"):
        st.session_state.plan_executed = True

    # EXECUTION PHASE
    if st.session_state.plan_executed:
        tab1, tab2 = st.tabs(["🛒 (1) Buy the Ingredients", "🥣 (2) Make the Dough"])
        
        with tab1:
            st.write("### Grocery List")
            st.info("Check items as you shop:")
            st.checkbox(f"Base Ingredients for {qty}x {dough_choice} Doughs")
            # Filter unique choices (excluding the "Add New" placeholder)
            unique_pizzas = set([a for a in assignments if a != "+ Add New Pizza to Library"])
            for pizza in unique_pizzas:
                st.checkbox(f"Toppings for {pizza}")
        
        with tab2:
            st.write(f"### Dough Lab: {dough_choice}")
            base_vals = DOUGH_PROFILES[dough_choice]
            
            with st.container(border=True):
                st.write("**Scaled Recipe**")
                cc1, cc2, cc3 = st.columns(3)
                f_total = cc1.number_input("Total Flour (g)", value=float(base_vals['flour'] * qty), format="%.1f")
                w_total = cc2.number_input("Total Water (g)", value=float(base_vals['water'] * qty), format="%.1f")
                hydra_calc = (w_total/f_total*100) if f_total > 0 else 0
                cc3.metric("Hydration", f"{hydra_calc:.1f}%")

            st.write("#### Historical Performance")
            st.caption(f"Past results for {dough_choice} style:")
            dummy_history = pd.DataFrame({"Date": ["2026-03-01", "2026-02-14"], "Grade": [9.1, 8.4], "Notes": ["Great airy crust", "A bit salty"]})
            st.table(dummy_history)

# --- 7. LIBRARY MODULE ---
elif st.session_state.view == "library":
    st.subheader("📚 Pizza Library Database")
    lib_df = pd.DataFrame({"Pizza Name": st.session_state.mock_library})
    st.dataframe(lib_df, use_container_width=True, hide_index=True)
    if st.button("Add New Pizza to Database"):
        st.info("This would open the intake form.")
