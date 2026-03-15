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
    if st.button("← Back to Start"): go_home()
st.write("---")

# --- 5. MAIN MENU ---
if st.session_state.view == "main":
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 What Pizza We Making?", use_container_width=True, height=150):
            st.session_state.view = "planner"
    with col2:
        if st.button("📚 See the Pizza Library", use_container_width=True, height=150):
            st.session_state.view = "library"

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
    menu_options = ["+ Add New Pizza to Library"] + st.session_state.mock_library
    
    for i in range(qty):
        choice = st.selectbox(f"Pizza #{i+1}", menu_options, key=f"piz_{i}")
        if choice == "+ Add New Pizza to Library":
            with st.expander("Define New Pizza", expanded=True):
                new_name = st.text_input("Pizza Name", key=f"name_{i}")
                new_sauce = st.text_area("Sauce Recipe", key=f"sauce_{i}")
                new_top = st.text_area("Ingredients", key=f"top_{i}")
                if st.button("Save to Library", key=f"save_{i}"):
                    st.session_state.mock_library.append(new_name)
                    st.toast("Saved!")
        assignments.append(choice)

    if st.button("🚀 Let's Get Started", use_container_width=True, type="primary"):
        st.session_state.plan_executed = True

    # EXECUTION PHASE
    if st.session_state.plan_executed:
        st.write("---")
        tab1, tab2 = st.tabs(["🛒 (1) Buy the Ingredients", "🥣 (2) Make the Dough"])
        
        with tab1:
            st.write("### Grocery List")
            # Logic: Pull ingredients from assigned pizzas
            st.checkbox(f"{qty}x portions of {dough_choice} ingredients")
            for a in set(assignments):
                st.checkbox(f"Ingredients for {a}")
        
        with tab2:
            st.write(f"### Dough Lab: {dough_choice}")
            base = DOUGH_PROFILES[dough_choice]
            
            # Filtered Dough Lab pre-populated
            with st.container(border=True):
                cc1, cc2 = st.columns(2)
                f_val = cc1.number_input("Flour (g)", value=float(base['flour'] * qty), format="%.1f")
                w_val = cc2.number_input("Water (g)", value=float(base['water'] * qty), format="%.1f")
                st.metric("Hydration", f"{(w_val/f_val*100):.1f}%")
            
            st.write("#### Historical Bakes (Filtered)")
            st.caption(f"Showing previous {dough_choice} results...")
            st.table(pd.DataFrame({"Date": ["2026-03-01"], "Grade": [9.1], "Notes": ["Great spring"]}))

# --- 7. LIBRARY MODULE ---
elif st.session_state.view == "library":
    st.subheader("Pizza Library Database")
    st.dataframe(pd.DataFrame({"Pizza": st.session_state.mock_library}), use_container_width=True)
