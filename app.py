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

st.title("🍽️ Weekly Meal Planner & Recipe Manager")

# ---------------------------
# 1) WEEKLY PLANNER (TOP + COMPACT)
# ---------------------------
st.subheader("📅 Plan Your Week")
st.write("Select a meal category for each day:")

cols = st.columns(2)  # 2-column dropdown layout
weekly_plan_selection = {}

for i, day in enumerate(days):
    with cols[i % 2]:  # alternate between columns
        weekly_plan_selection[day] = st.selectbox(
            day,
            options=list(recipes.keys()),
            key=f"select_{day}"
        )

st.write("")  # spacing

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
# 2) ADD RECIPE SECTION
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
            {
                "name": recipe_name.strip(),
                "ingredients": ingredient_list
            }
        )
        save_recipes(recipes)
        st.success(f"🎉 Added **{recipe_name}** to **{category}**!")
    else:
        st.warning("⚠️ Please fill out both fields before adding.")

st.divider()

# ---------------------------
# 3) RECIPE MANAGER (VIEW / EDIT / DELETE)
# ---------------------------
st.subheader("📚 Recipe Manager (View, Edit or Delete)")

for cat, items in recipes.items():
    st.markdown(f"### 🍽️ {cat.replace('_',' ').title()}")
    if not items:
        st.write("🔎 No recipes yet.")
    else:
        for idx, recipe in enumerate(items):
            st.write(f"**{recipe['name']}**")
