import streamlit as st

# --- INITIAL SETUP ---
st.set_page_config(page_title="Pizza People", layout="centered")

# Initialize "Mock Data" if it doesn't exist yet
if 'pizza_library' not in st.session_state:
    st.session_state.pizza_library = [
        {"name": "Neapolitan Margherita", "dough": "Neapolitan", "sauce": "Classic Red", "toppings": "Mozzarella, Basil, Olive Oil"},
        {"name": "Peach & Balsamic", "dough": "Neapolitan", "sauce": "White Base", "toppings": "Fresh Peaches, Balsamic Glaze, Goat Cheese"}
    ]

# --- HOME PAGE NAVIGATION ---
st.markdown("<h1 style='text-align: center;'>Pizza People</h1>", unsafe_allow_html=True)
st.write("---")

# Using columns for aesthetic navigation buttons
col1, col2, col3 = st.columns(3)

with col1:
    show_menu = st.button("See the Menu & Order", use_container_width=True)
with col2:
    make_dough = st.button("Make Some Dough", use_container_width=True)
with col3:
    add_library = st.button("Add to Pizza Library", use_container_width=True)

# --- MODULE 1: SEE THE MENU & ORDER ---
if show_menu:
    st.header("🍴 Digital Menu")
    for pizza in st.session_state.pizza_library:
        with st.container(border=True):
            st.subheader(pizza['name'])
            st.write(f"**Dough:** {pizza['dough']} | **Sauce:** {pizza['sauce']}")
            st.write(f"**Ingredients:** {pizza['toppings']}")
            if st.button(f"Order {pizza['name']}", key=pizza['name']):
                st.success(f"Added {pizza['name']} to your shopping list!")

# --- MODULE 2: MAKE SOME DOUGH ---
elif make_dough:
    st.header("🍞 The Dough Lab")
    style = st.selectbox("Select Style", ["Neapolitan", "New York Style", "Chicago Deep Dish", "Detroit Style", "Other"])
    
    # Logic for default ingredients based on style
    defaults = {"Neapolitan": 300, "Detroit": 500, "New York Style": 400}
    base_flour = defaults.get(style, 500)
    
    col_a, col_b = st.columns(2)
    with col_a:
        flour = st.number_input("Flour (g)", value=base_flour)
        salt = st.number_input("Salt (g)", value=int(flour * 0.03))
    with col_b:
        water = st.number_input("Water (g)", value=int(flour * 0.65))
        st.metric("Hydration", f"{(water/flour)*100:.1f}%")
        
    st.slider("Rate this bake (0-10)", 0, 10, 5)
    st.button("Log this Bake")

# --- MODULE 3: ADD TO THE LIBRARY ---
elif add_library:
    st.header("📚 Add New Creation")
    with st.form("new_pizza"):
        new_name = st.text_input("Pizza Name")
        new_dough = st.selectbox("Dough Base", ["Neapolitan", "New York Style", "Chicago Deep Dish", "Detroit Style"])
        new_sauce = st.text_input("Sauce Recipe Name")
        new_toppings = st.text_area("Ingredients List")
        
        if st.form_submit_button("Add to Library"):
            new_entry = {"name": new_name, "dough": new_dough, "sauce": new_sauce, "toppings": new_toppings}
            st.session_state.pizza_library.append(new_entry)
            st.balloons()
            st.success("Pizza Added!")
