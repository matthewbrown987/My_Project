import streamlit as st
import json
import random

st.set_page_config(layout="centered")
st.image("meal_icon_cropped.png", width=110)

# ---------------------------
# FILE SETTINGS
# ---------------------------
RECIPES_FILE = "recipes.json"

# ---------------------------
# LOAD & SAVE FUNCTIONS
# ---------------------------
def load_recipes():
    try:
        with open(RECIPES_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        default_data = {
            "under_20_min": [],
            "30_min": [],
            "batch_cooking": []
        }
        save_recipes(default_data)
        return default_data

def save_recipes(data):
    with open(RECIPES_FILE, "w") as file:
        json.dump(data, file, indent=4)

# ---------------------------
# APP START
# ---------------------------
recipes = load_recipes()
days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

st.title("🍽️ Weekly Meal Planner")

# ---------------------------
# 1) WEEKLY PLANNER
# ---------------------------
st.subheader("📅 Plan Your Week")
st.write("Select a meal category for each day:")

cols = st.columns(2)
weekly_plan_selection = {}

for i, day in enumerate(days):
    with cols[i % 2]:
        weekly_plan_selection[day] = st.selectbox(
            day,
            options=list(recipes.keys()),
            key=f"select_{day}"
        )

if st.button("Generate Weekly Meal Plan"):
    st.subheader("🗓️ Your Weekly Meal Plan")

    weekly_plan = {}
    for day, meal_type in weekly_plan_selection.items():
        if recipes[meal_type]:
            weekly_plan[day] = random.choice(recipes[meal_type])
        else:
            weekly_plan[day] = {"name": "No recipes yet!"}

    for day, info in weekly_plan.items():
        st.write(f"**{day}:** {info['name']}")

st.divider()

# ---------------------------
# 2) ADD RECIPE
# ---------------------------
st.subheader("➕ Add a New Recipe")

category = st.selectbox("Select category", list(recipes.keys()), key="new_category")
recipe_name = st.text_input("Recipe name")
ingredients = st.text_area("Ingredients (comma-separated)", 
    placeholder="e.g., Chicken breast, Pasta, Olive oil")

if st.button("Add Recipe"):
    if recipe_name.strip() and ingredients.strip():
        ingredient_list = [i.strip() for i in ingredients.split(",")]
        recipes[category].append(
            {"name": recipe_name.strip(), "ingredients": ingredient_list}
        )
        save_recipes(recipes)
        st.success(f"🎉 Added **{recipe_name}** to **{category}**!")
        st.rerun()
    else:
        st.warning("⚠️ Please fill out both fields before adding.")

st.divider()

# ---------------------------
# 3) RECIPE MANAGER
# ---------------------------
st.subheader("📚 Recipe Manager (View, Edit or Delete)")

for cat, items in recipes.items():
    st.markdown(f"### 🍽️ {cat.replace('_',' ').title()}")

    if not items:
        st.write("🔎 No recipes yet.")
        continue

    for idx, recipe in enumerate(items):
        with st.expander(f"📖 {recipe['name']}"):
            st.write("**Ingredients:** " + ", ".join(recipe["ingredients"]))

            col1, col2 = st.columns(2)

            # --- EDIT BUTTON ---
            if col1.button("✏️ Edit", key=f"edit_{cat}_{idx}"):

                st.session_state.edit_key = (cat, idx)
                st.session_state.edit_name = recipe["name"]
                st.session_state.edit_ingredients = ", ".join(recipe["ingredients"])
                st.rerun()

            # --- DELETE BUTTON ---
            if col2.button("🗑️ Delete", key=f"delete_{cat}_{idx}"):
                recipes[cat].pop(idx)
                save_recipes(recipes)
                st.success("Recipe deleted!")
                st.rerun()

# ---------------------------
# 4) EDIT FORM (POPUP STYLE)
# ---------------------------
if "edit_key" in st.session_state:
    cat, idx = st.session_state.edit_key

    st.subheader("✏️ Edit Recipe")

    new_name = st.text_input("Recipe name", st.session_state.edit_name)
    new_ingredients = st.text_area("Ingredients (comma-separated)", 
                                    st.session_state.edit_ingredients)

    if st.button("Save Changes"):
        recipes[cat][idx]["name"] = new_name.strip()
        recipes[cat][idx]["ingredients"] = [i.strip() for i in new_ingredients.split(",")]
        save_recipes(recipes)

        del st.session_state.edit_key
        st.success("Recipe updated!")
        st.rerun()

    if st.button("Cancel Edit"):
        del st.session_state.edit_key
        st.rerun()
