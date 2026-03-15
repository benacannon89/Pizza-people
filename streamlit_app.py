    # --- STEP 2: PROCESS & BAKE ---
    with st.container(border=True):
        st.subheader("🔥 Step 2: Process & Bake")
        p1, p2, p3 = st.columns(3)
        
        with p1:
            st.write("**Fermentation**")
            ferm_type = st.radio("Type", ["Cold Ferment (Fridge)", "Room Temp"], horizontal=True)
            
            # --- DYNAMIC DEFAULTS LOGIC ---
            if selected_style == "Sourdough":
                if ferm_type == "Room Temp":
                    default_bulk = "8-12h"
                    default_ball = "2-4h"
                else:
                    default_bulk = "24-48h"
                    default_ball = "6h"
            else:
                # Defaults for commercial yeast styles
                if ferm_type == "Room Temp":
                    default_bulk = "4-8h"
                    default_ball = "2h"
                else:
                    default_bulk = "24h"
                    default_ball = "4-6h"

            if ferm_type == "Room Temp":
                st.number_input("Room Temp (°F)", value=72)
            
            bulk_time = st.text_input("Bulk Duration", value=default_bulk)
            ball_time = st.text_input("Ball Duration", value=default_ball)
            
        with p2:
            st.write("**Environment**")
            st.number_input("Floor Temp (°F)", value=850, step=25)
            st.number_input("Outside Air (°F)", value=72, step=1)
            
        with p3:
            st.write("**Results**")
            grade = st.slider("Final Grade", 0.0, 10.0, 8.0, step=0.1)

        st.text_area("Bake Notes")
        if st.button("Log This Experiment", use_container_width=True):
            st.success(f"Logged {selected_style} bake ({ferm_type})")
