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
if "stage" not in st.session_state:
    st.session_state.stage = "Plan"
if "mock_library" not in st.session_state:
    st.session_state.mock_library = ["Margherita", "Peach & Balsamic", "Pepperoni Detroit"]
if "current_plan" not in st.session_state:
    st.session_state.current_plan = {"dough_type": "Neapolitan", "qty": 4, "pizzas": []}

# --- 3. SIDEBAR: PIZZA HISTORY ---
with st.sidebar:
    st.header("🕰️ Pizza History")
    # Mock history data matching your requested inputs
    history_data = pd.DataFrame([
        {"Pizza": "Margherita", "Grade": 9.2, "Dough": "Neapolitan", "Hydration": "65%", "Temp": "850°F", "Notes": "Perfect leopard spotting"},
        {"Pizza": "Pepperoni", "Grade": 8.5, "Dough": "Detroit", "Hydration": "70%", "Temp": "550°F", "Notes": "Crispy cheese edges"},
    ])
    
    selected_hist = st.selectbox("Search Historical Bakes", history_data["Pizza"].unique())
    hist_details = history_data[history_data["Pizza"] == selected_hist].iloc[0]
    
    with st.container(border=True):
        st.write(f"**Grade: {hist_details['Grade']}/10**")
        st.caption(f"Style: {hist_details['Dough']} | {hist_details['Hydration']}")
        st.info(hist_details["Notes"])
    
    st.write("---")
    st.header("📚 Full Library")
    st.dataframe(pd.DataFrame(st.session_state.mock_library, columns=["Name"]), hide_index=True)

# --- 4. HEADER & PIPELINE NAV ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🍕 Pizza People</h1>", unsafe_allow_html=True)
st.write("---")
cols = st.columns(3)
stages = ["Plan", "Cook", "Grade"]
for i, s in enumerate(stages):
    color = "#FF4B4B" if st.session_state.stage == s else "gray"
    border = "3px solid #FF4B4B" if st.session_state.stage == s else "none"
    cols[i].markdown(f"<h3 style='text-align: center; color: {color}; border-bottom: {border};'>{i+1}. {s}</h3>", unsafe_allow_html=True)
st.write("---")

# --- STAGE 1: PLAN ---
if st.session_state.stage == "Plan":
    st.subheader("📝 Planning the Session")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.current_plan['dough_type'] = st.selectbox("Global Dough Type", list(DOUGH_PROFILES.keys()))
    with c2:
        st.session_state.current_plan['qty'] = st.number_input("Number of Pizzas", min_value=1, value=4)

    st.write("### Assign Pizzas")
    st.session_state.current_plan['pizzas'] = []
    menu_options = ["Unassigned", "+ Add New Pizza"] + st.session_state.mock_library
    
    for i in range(st.session_state.current_plan['qty']):
        choice = st.selectbox(f"Pizza #{i+1}", menu_options, key=f"piz_select_{i}")
        if choice == "+ Add New Pizza":
            with st.container(border=True):
                new_name = st.text_input("Name", key=f"new_name_{i}")
                if st.button("Save to Library", key=f"save_{i}"):
                    st.session_state.mock_library.append(new_name)
                    st.rerun()
        st.session_state.current_plan['pizzas'].append(choice)

    if st.button("Lock Plan & Buy Ingredients ➡️", use_container_width=True):
        st.session_state.stage = "Cook"
        st.rerun()

# --- STAGE 2: COOK ---
elif st.session_state.stage == "Cook":
    st.subheader("👨‍🍳 Cooking Phase")
    
    with st.expander("🛒 Shopping List"):
        st.checkbox(f"Dough: {st.session_state.current_plan['dough_type']} components")
        for p in set(st.session_state.current_plan['pizzas']):
            if p not in ["Unassigned", "+ Add New Pizza"]:
                st.checkbox(f"Toppings for {p}")

    st.write("### The Dough Lab")
    base = DOUGH_PROFILES[st.session_state.current_plan['dough_type']]
    qty = st.session_state.current_plan['qty']
    
    with st.container(border=True):
        st.write("**Ingredients (Editable)**")
        cc1, cc2, cc3 = st.columns(3)
        with cc1:
            f_val = st.number_input("Flour (g)", value=float(base['flour'] * qty), step=0.1, format="%.1f")
            s_val = st.number_input("Salt (g)", value=float(base['salt'] * qty), step=0.1, format="%.1f")
        with cc2:
            w_val = st.number_input("Water (g)", value=float(base['water'] * qty), step=0.1, format="%.1f")
            if st.session_state.current_plan['dough_type'] == "Sourdough":
                st.number_input("Starter (g)", value=float(base['starter'] * qty), step=0.1, format="%.1f")
            else:
                y_type = st.selectbox("Yeast Type", ["Instant Dry", "Active Dry", "Fresh"])
                st.number_input(f"{y_type} Amount (g)", value=float(base['yeast'] * qty), step=0.1, format="%.1f")
        with cc3:
            hydra = (w_val / f_val * 100) if f_val > 0 else 0
            st.metric("Live Hydration", f"{hydra:.1f}%")

    with st.container(border=True):
        st.write("**Proofing & Environment**")
        p1, p2 = st.columns(2)
        with p1:
            use_oven = st.toggle("Use proofing oven?")
            if use_oven:
                st.number_input("Proofing Oven Temp (°F)", value=85, step=1)
            else:
                st.number_input("Ambient Room Temp (°F)", value=72, step=1)
            
            ferm = st.radio("Fermentation", ["Cold Ferment", "Room Temp"], horizontal=True)
            bulk = st.text_input("Bulk Time", "24h")
        with p2:
            floor = st.number_input("Oven Floor Temp (°F)", value=850)
            ambient = st.number_input("Outside Air (°F)", value=72)

    if st.button("Bake Complete! Move to Grading ➡️", use_container_width=True):
        st.session_state.stage = "Grade"
        st.rerun()

# --- STAGE 3: GRADE ---
elif st.session_state.stage == "Grade":
    st.subheader("⭐ Grading & Notes")
    for pizza in st.session_state.current_plan['pizzas']:
        if pizza not in ["Unassigned", "+ Add New Pizza"]:
            with st.container(border=True):
                st.write(f"### {pizza}")
                st.slider(f"Grade", 0.0, 10.0, 8.0, step=0.1, key=f"g_{pizza}")
                st.text_area(f"Notes", key=f"n_{pizza}")

    if st.button("Finish Session & Archive", use_container_width=True):
        st.success("Bake Session Archived!")
        if st.button("Start New Session"):
            st.session_state.stage = "Plan"
            st.rerun()
