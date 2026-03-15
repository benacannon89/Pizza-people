elif st.session_state.page == "dough":
    st.subheader("🧪 The Dough Lab")

    # 1. Define Ingredient Archetypes
    dough_profiles = {
        "Neapolitan": {"flour": 162.5, "water": 105.0, "salt": 5.0, "yeast": 0.25, "oil": 0.0, "sugar": 0.0},
        "New York Style": {"flour": 162.5, "water": 100.0, "salt": 3.2, "yeast": 1.0, "oil": 3.2, "sugar": 2.5},
        "Detroit Style": {"flour": 150.0, "water": 105.0, "salt": 3.0, "yeast": 1.25, "oil": 3.0, "sugar": 0.0},
        "Chicago Deep Dish": {"flour": 150.0, "water": 75.0, "salt": 2.5, "yeast": 1.25, "oil": 22.5, "sugar": 0.0}
    }

    # 2. Global Scaling
    selected_style = st.selectbox("Select Style", list(dough_profiles.keys()))
    num_pizzas = st.number_input("Number of Pizzas", min_value=1, value=4)
    
    # Calculate baseline for scaling
    base = dough_profiles[selected_style]
    
    st.write("---")
    
    # 3. Dynamic Ingredient Section
    st.markdown("### 🥣 Step 1: Ingredients")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        f_val = st.number_input("Flour (g)", value=float(base['flour'] * num_pizzas), step=0.1, format="%.1f")
        s_val = st.number_input("Salt (g)", value=float(base['salt'] * num_pizzas), step=0.1, format="%.1f")
    with c2:
        w_val = st.number_input("Water (g)", value=float(base['water'] * num_pizzas), step=0.1, format="%.1f")
        y_val = st.number_input("Yeast (g)", value=float(base['yeast'] * num_pizzas), step=0.1, format="%.1f")
    with c3:
        # Only show Oil and Sugar if they are part of the style's profile
        if base['oil'] > 0:
            o_val = st.number_input("Oil/Fat (g)", value=float(base['oil'] * num_pizzas), step=0.1, format="%.1f")
        if base['sugar'] > 0:
            su_val = st.number_input("Sugar (g)", value=float(base['sugar'] * num_pizzas), step=0.1, format="%.1f")
        
        hydra = (w_val / f_val) * 100 if f_val > 0 else 0
        st.metric("Final Hydration", f"{hydra:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)
    st.write("---")

    # 4. Process & Baking Section (Clear Delineation)
    st.markdown("### 🔥 Step 2: Process & Bake")
    p1, p2, p3 = st.columns(3)
    
    with p1:
        st.write("**Proofing**")
        bulk_time = st.text_input("Bulk Proof", "24h Cold")
        ball_time = st.text_input("Ball Proof", "6h Room Temp")
    with p2:
        st.write("**Environment**")
        floor_temp = st.number_input("Floor Temp (°F)", value=850)
        ambient_temp = st.number_input("Outside Air (°F)", value=72)
    with p3:
        st.write("**Results**")
        grade = st.slider("Grade (0-10)", 0.0, 10.0, 8.0, step=0.1)

    notes = st.text_area("Bake Notes")
    if st.button("Log This Experiment", use_container_width=True):
        st.balloons()
