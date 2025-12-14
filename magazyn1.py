import streamlit as st
import pandas as pd # Wymagany do wyświetlania DataFrame

# --- Definicja Stanu (RESETUJE SIĘ PO INTERAKCJI) ---
# Format: [{'index': 100001, 'name': 'Laptop Służbowy', 'quantity': 15}, ...]
INVENTORY = [
    {'index': 100001, 'name': 'Laptop Służbowy', 'quantity': 15},
    {'index': 100002, 'name': 'Smartfon Firmowy', 'quantity': 50},
    {'index': 100003, 'name': 'Zestaw Słuchawkowy', 'quantity': 120},
]

# --- Ustawienia Strony ---
st.set_page_config(
    page_title="Prosty Magazyn z Ilościami",
    layout="wide",
    initial_sidebar_state="expanded"
)

## --- Funkcje Logiki Magazynu ---

def get_next_index():
    """Generuje kolejny sześciocyfrowy numer katalogowy."""
    if INVENTORY:
        max_index = max(item['index'] for item in INVENTORY)
        return max_index + 1
    return 100001 # Startowa wartość

def add_item(item_name, item_quantity):
    """Dodaje nowy przedmiot z unikalnym indeksem i ilością."""
    # UWAGA: Ta zmiana nie będzie trwała!
    if not item_name or item_quantity <= 0:
        st.toast("❌ Nazwa nie może być pusta, a ilość musi być większa niż 0.")
        return

    # Sprawdzamy, czy nazwa już istnieje
    existing_names = [item['name'] for item in INVENTORY]
    if item_name in existing_names:
        st.toast(f"⚠️ Przedmiot '{item_name}' jest już na liście. Użyj funkcji edycji do zmiany ilości.")
        return

    new_index = get_next_index()
    
    # Tworzenie nowego rekordu
    new_item = {'index': new_index, 'name': item_name, 'quantity': item_quantity}
    INVENTORY.append(new_item)
    
    st.toast(f"✅ Dodano: '{item_name}' ({item_quantity} szt.) z indeksem {new_index} (zaraz zniknie).")

def remove_item(index_to_remove):
    """Usuwa cały przedmiot na podstawie numeru indeksu."""
    # UWAGA: Ta zmiana nie będzie trwała!
    global INVENTORY
    
    initial_length = len(INVENTORY)
    
    # Usuwamy element z listy
    INVENTORY = [item for item in INVENTORY if item['index'] != index_to_remove]
    
    if len(INVENTORY) < initial_length:
        st.toast(f"🗑️ Usunięto cały towar (Indeks: {index_to_remove}).")
    else:
        st.toast(f"❌ Błąd: Indeks {index_to_remove} nie został znaleziony.")

## --- Interfejs Użytkownika Streamlit ---

st.title("🔢 Prosty Magazyn z Ilościami")
st.warning("⚠️ **UWAGA:** Stan magazynu jest **nietrwały** i resetuje się po każdej interakcji.")

# Utwórz dwie kolumny
col1, col2 = st.columns([1, 2])

# Kolumna 1: Dodawanie/Usuwanie
with col1:
    st.header("➕ Dodaj Towar")

    # Dodawanie Towaru z Ilością
    new_item_name = st.text_input("Nazwa nowego towaru", key="new_name")
    new_item_quantity = st.number_input(
        "Ilość sztuk na start", 
        min_value=1, 
        step=1, 
        value=1, 
        key="new_quantity"
    )
    
    if st.button("Dodaj do Magazynu", type="primary"):
        add_item(new_item_name, new_item_quantity)

    st.markdown("---")

    # Usuwanie Towaru
    st.header("➖ Usuń Towar (Cały Rekord)")
    
    if INVENTORY:
        current_indices_names = {item['index']: item['name'] for item in INVENTORY}
        
        # Tworzymy opcje wyświetlające Indeks i Nazwę, ale zwracające Indeks
        index_options = [f"{idx} - {name}" for idx, name in current_indices_names.items()]
        
        item_to_remove_str = st.selectbox(
            "Wybierz Indeks Towaru do usunięcia",
            index_options,
        )
        
        # Wyodrębnienie numeru indeksu z wybranego stringa
        index_to_remove_select = int(item_to_remove_str.split(' - ')[0])
        
        if st.button("Usuń Cały Towar", type="secondary"):
            remove_item(index_to_remove_select)
    else:
        st.info("Lista jest pusta.")

# Kolumna 2: Stan Magazynu
with col2:
    st.header("📊 Aktualny Stan Magazynu")

    if INVENTORY:
        # Obliczanie sumy ilości
        total_items_count = sum(item['quantity'] for item in INVENTORY)
        st.metric(
            label="Łączna Liczba Sztuk w Magazynie", 
            value=total_items_count, 
            delta=f"Towarów: {len(INVENTORY)}"
        )
        
        # Wyświetlanie danych w DataFrame
        df = pd.DataFrame(INVENTORY)
        df.columns = ["Numer Katalogowy", "Nazwa Towaru", "Ilość Sztuk"]
        
        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("Lista jest pusta.")
