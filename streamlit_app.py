elif st.session_state.page == "dough":
    st.subheader("🧪 The Dough Lab")

    # 1. Updated Dough Profiles with Sourdough
    dough_profiles = {
        "Neapolitan": {"flour": 162.5, "water": 105.0, "salt": 5.0, "yeast": 0.25, "oil": 0.0, "sugar": 0.0, "starter": 0.0},
        "New York Style": {"flour": 162.5, "water": 100.0, "salt": 3.2, "yeast": 1.0, "oil": 3.2, "sugar": 2.5, "starter": 0.0},
        "Detroit Style": {"flour": 150.0, "water": 105.0, "salt": 3.0, "yeast": 1.25, "oil": 3.0, "sugar": 0.0, "starter": 0.0},
        "Chicago Deep Dish": {"flour": 150.0, "water": 75.0, "salt": 2.5, "yeast": 1.25, "oil": 22.5, "sugar": 0.0, "starter": 0.0},
        "Sourdough": {"flour": 150.0, "water": 97.5, "salt": 4.5, "yeast": 0.0, "oil": 0.0, "sugar": 0.0, "starter": 30.0}
    }

    selected_style = st.selectbox("Select Style", list(dough_profiles.keys()))
    num_pizzas = st.number_input("Number of Pizzas", min_value=1, value=4)
    base = dough_profiles[selected_style]
    
    st.write("---")
    
    # 2. Dynamic Ingredient Section
    st.markdown("### 🥣 Step 1: Ingredients")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        f_val = st.number_input("Flour (g)", value=float(base['flour'] * num_pizzas), step=0.1, format="%.1f")
        s_val = st.number_input("Salt (g)", value=float(base['salt'] * num_pizzas), step=0.1, format="%.1f")
    with c2:
        w_val = st.number_input("Water (g)", value=float(base['water'] * num_pizzas), step=0.1, format="%.1f")
        
        # Logic to switch between Yeast and Starter
        if selected_style == "Sourdough":
            start_val = st.number_input("Active Starter (g)", value=float(base['starter'] * num_pizzas), step=0.1, format="%.1f")
        else:
            y_val = st.number_input("Yeast (g)", value=float(base['yeast'] * num_pizzas), step=0.1, format="%.1f")
            
    with c3:
        if base['oil'] > 0:
            st.number_input("Oil/Fat (g)", value=float(base['oil'] * num_pizzas), step=0.1, format="%.1f")
        if base['sugar'] > 0:
            st.number_input("Sugar (g)", value=float(base['sugar'] * num_pizzas), step=0.1, format="%.1f")
        
        hydra = (w_val / f_val) * 100 if f_val > 0 else 0
        st.metric("Hydration %", f"{hydra:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)
    st.write("---")

    # 3. Process Section
    st.markdown("### 🔥 Step 2: Process & Bake")
    # ... (Rest of the process code remains the same)
