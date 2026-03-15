# --- MODULE 2: DOUGH LAB ---
elif st.session_state.page == "dough":
    st.subheader("🧪 The Dough Lab")

    # 1. Editable Defaults Dictionary
    # In the future, this will be pulled from your "Dough_Styles" Sheet
    if 'dough_defaults' not in st.session_state:
        st.session_state.dough_defaults = {
            "Neapolitan": {"flour": 500.0, "water": 325.0, "salt": 15.0},
            "New York Style": {"flour": 500.0, "water": 310.0, "salt": 10.0},
            "Detroit Style": {"flour": 400.0, "water": 280.0, "salt": 8.0},
            "Chicago Deep Dish": {"flour": 600.0, "water": 300.0, "salt": 12.0},
            "Other": {"flour": 500.0, "water": 325.0, "salt": 15.0}
        }

    # 2. Select Style
    style = st.selectbox("Select Dough Style", list(st.session_state.dough_defaults.keys()))
    
    # 3. Form for Current Bake (Pre-filled with editable defaults)
    with st.container(border=True):
        st.write(f"### Current {style} Bake")
        col_a, col_b, col_c = st.columns(3)
        
        # Pull the specific default for the chosen style
        current_default = st.session_state.dough_defaults[style]
        
        with col_a:
            f_val = st.number_input("Flour (g)", value=current_default['flour'], step=0.1, format="%.1f")
            s_val = st.number_input("Salt (g)", value=current_default['salt'], step=0.1, format="%.1f")
        with col_b:
            w_val = st.number_input("Water (g)", value=current_default['water'], step=0.1, format="%.1f")
            hydra = (w_val / f_val) * 100 if f_val > 0 else 0
            st.metric("Hydration %", f"{hydra:.1f}%")
        with col_c:
            proof = st.text_input("Bulk Proof Time (e.g. 24h)")
            ball_time = st.text_input("Time in Ball (e.g. 6h)")

        notes = st.text_area("Bake Notes (Wood vs Gas, floor temp, etc.)")
        grade = st.slider("Final Grade", 0.0, 10.0, 5.0, step=0.5)
        
        if st.button("Log This Bake"):
            st.success(f"Logged {style} bake with {hydra:.1f}% hydration!")

    # 4. History Table for the Specific Style
    st.write(f"---")
    st.write(f"### {style} History")
    
    # Mock History Data with your specific columns
    # In the final version, this will filter your "Bake_History" Sheet
    history_cols = ["Date", "Grade", "Flour (g)", "Water (g)", "Hydration %", "Salt (g)", "Proof Time", "Time in Ball", "Notes"]
    mock_history = pd.DataFrame([
        ["2026-03-01", 9.0, 500.0, 325.0, "65.0%", 15.0, "24h", "6h", "Perfect crust"],
        ["2026-02-15", 7.5, 500.0, 350.0, "70.0%", 15.0, "48h", "4h", "A bit too sticky"]
    ], columns=history_cols)
    
    st.dataframe(mock_history, use_container_width=True, hide_index=True)
