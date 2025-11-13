import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# ---------- Initialize Firebase ----------
cred = credentials.Certificate("lootloop-7c9b5-firebase-adminsdk-fbsvc-11c8db0312.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ---------- Streamlit App ----------
st.set_page_config(page_title="LootLoop Game", layout="wide")
st.title("🍔 LootLoop Game")

# --- Player Login / Selection ---
st.sidebar.header("Player Login")
username = st.sidebar.text_input("Enter your username:")

if username:
    # Check if player exists
    player_ref = db.collection("players").document(username)
    player_doc = player_ref.get()
    if player_doc.exists:
        player_data = player_doc.to_dict()
    else:
        # Create new player
        player_data = {"username": username, "coins": 100, "inventory": []}
        player_ref.set(player_data)

    st.subheader(f"🎮 Player: {username}")
    st.markdown(f"**Coins:** {player_data.get('coins', 0)}")
    st.markdown(f"**Inventory:** {', '.join(player_data.get('inventory', [])) if player_data.get('inventory') else 'Empty'}")

    # --- Restaurants Section ---
    st.subheader("🏪 Restaurants")
    stores = db.collection("stores").stream()
    cols = st.columns(3)  # 3-column layout

    for i, store in enumerate(stores):
        data = store.to_dict()
        col = cols[i % 3]
        col.markdown(f"### {data.get('name', 'Unnamed')}")
        items = data.get("items", [])
        for item in items:
            if col.button(f"Buy {item} ({data.get('prices', {}).get(item, 10)} coins)", key=f"{username}-{data.get('name')}-{item}"):
                price = data.get("prices", {}).get(item, 10)
                if player_data["coins"] >= price:
                    player_data["coins"] -= price
                    player_data["inventory"].append(item)
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# ---------- Firebase Setup ----------
cred = credentials.Certificate("lootloop-7c9b5-firebase-adminsdk-fbsvc-11c8db0312.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------- Streamlit App ----------
st.set_page_config(page_title="LootLoop", layout="wide")
st.title("🍔 LootLoop")

# --- Player Login ---
st.sidebar.header("Player Login")
username = st.sidebar.text_input("Enter your username:")

if username:
    player_ref = db.collection("players").document(username)
    player_doc = player_ref.get()
    if not player_doc.exists:
        player_data = {"username": username, "coins": 100, "inventory": []}
        player_ref.set(player_data)
    else:
        player_data = player_doc.to_dict()

    st.subheader(f"🎮 Player: {username}")
    st.write(f"**Coins:** {player_data['coins']}")
    st.write(f"**Inventory:** {', '.join(player_data['inventory']) if player_data['inventory'] else 'Empty'}")

    st.divider()

    # --- Restaurants Section ---
    st.subheader("🏪 Restaurants")

    # Preload sample restaurants if Firestore is empty
    if not db.collection("stores").get():
        sample_stores = [
            {"name": "Burger Blast", "items": ["Burger", "Fries", "Soda"], "prices": {"Burger": 15, "Fries": 10, "Soda": 5}},
            {"name": "Pizza Palace", "items": ["Pepperoni Pizza", "Cheese Pizza"], "prices": {"Pepperoni Pizza": 20, "Cheese Pizza": 15}},
            {"name": "Taco Town", "items": ["Taco", "Burrito"], "prices": {"Taco": 8, "Burrito": 12}}
        ]
        for s in sample_stores:
            db.collection("stores").add(s)

    stores = db.collection("stores").stream()
    cols = st.columns(3)
    for i, s in enumerate(stores):
        data = s.to_dict()
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# ---------- Firebase Setup ----------
cred = credentials.Certificate("lootloop-7c9b5-firebase-adminsdk-fbsvc-11c8db0312.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------- Streamlit App ----------
st.set_page_config(page_title="LootLoop", layout="wide")
st.title("🍔 LootLoop")

# --- Player Login ---
st.sidebar.header("Player Login")
username = st.sidebar.text_input("Enter your username:")

if username:
    player_ref = db.collection("players").document(username)
    player_doc = player_ref.get()
    if not player_doc.exists:
        player_data = {"username": username, "coins": 100, "inventory": []}
        player_ref.set(player_data)
    else:
        player_data = player_doc.to_dict()

    st.subheader(f"🎮 Player: {username}")
    st.write(f"**Coins:** {player_data['coins']}")
    st.write(f"**Inventory:** {', '.join(player_data['inventory']) if player_data['inventory'] else 'Empty'}")

    st.divider()

    # --- Restaurants Section ---
    st.subheader("🏪 Restaurants")

    # Preload sample restaurants if Firestore is empty
    if not db.collection("stores").get():
        sample_stores = [
            {"name": "Burger Blast", "items": ["Burger", "Fries", "Soda"], "prices": {"Burger": 15, "Fries": 10, "Soda": 5}},
            {"name": "Pizza Palace", "items": ["Pepperoni Pizza", "Cheese Pizza"], "prices": {"Pepperoni Pizza": 20, "Cheese Pizza": 15}},
            {"name": "Taco Town", "items": ["Taco", "Burrito"], "prices": {"Taco": 8, "Burrito": 12}}
        ]
        for s in sample_stores:
            db.collection("stores").add(s)

    stores = db.collection("stores").stream()
    cols = st.columns(3)
    for i, s in enumerate(stores):
        data = s.to_dict()
        col = cols[i % 3]
        col.markdown(f"### {data.get('name', 'Unnamed')}")
        for item in data.get("items", []):
            price = data["prices"].get(item, 0)
            if col.button(f"Buy {item} for {price} coins", key=f"{username}-{item}"):
                if player_data["coins"] >= price:
                    player_data["coins"] -= price
                    player_data["inventory"].append(item)
                    player_ref.set(player_data)
                    st.success(f"You bought a {item}!")
                    st.experimental_rerun()
                else:
                    st.warning("Not enough coins!")

else:
    st.info("Enter a username in the sidebar to start playing.")

