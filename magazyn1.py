import streamlit as st

# --- Definicja Stanu (RESETUJE SIĘ PO INTERAKCJI) ---
# Używamy słowników, aby przechowywać zarówno numer indeksu, jak i nazwę towaru.
# Format: [{'index': 100001, 'name': 'Laptop Służbowy'}, ...]
INVENTORY = [
    {'index': 100001, 'name': 'Laptop Służbowy'},
    {'index': 100002, 'name': 'Smartfon Firmowy'},
    {'index': 100003, 'name': 'Zestaw Słuchawkowy'},
]
# Licznik do generowania kolejnych numerów katalogowych (indeksów)
LAST_INDEX = 100003

# --- Ustawienia Strony ---
st.set_page_config(
    page_title="Prosty Magazyn (Sześciocyfrowe Indeksy)",
    layout="wide",
    initial_sidebar_state="expanded"
)

## --- Funkcje Logiki Magazynu ---

def get_next_index():
    """Generuje kolejny sześciocyfrowy numer katalogowy."""
    # UWAGA: Ponieważ nie używamy stanu sesji, ta wartość jest resetowana!
    if INVENTORY:
        # Znajdujemy największy aktualny indeks
        max_index = max(item['index'] for item in INVENTORY)
        return max_index + 1
    return 100001 # Startowa wartość

def add_item(item_name):
    """Dodaje nowy przedmiot z unikalnym indeksem."""
    # UWAGA: Ta zmiana nie będzie trwała!
    if not item_name:
        st.toast("❌ Nazwa przedmiotu nie może być pusta.")
        return

    # Sprawdzamy, czy nazwa już istnieje
    existing_names = [item['name'] for item in INVENTORY]
    if item_name in existing_names:
        st.toast(f"⚠️ Przedmiot '{item_name}' jest już na liście.")
        return

    new_index = get_next_index()
    
    # Tworzenie nowego rekordu i dodanie do nietrwałej listy
    new_item = {'index': new_index, 'name': item_name}
    INVENTORY.append(new_item)
    
    st.toast(f"✅ Dodano: '{item_name}' z indeksem {new_index} (zaraz zniknie).")

def remove_item(index_to_remove):
    """Usuwa przedmiot na podstawie numeru indeksu."""
    # UWAGA: Ta zmiana nie będzie trwała!
    global INVENTORY
    
    # Filtrujemy listę, zachowując tylko te elementy, których indeks nie pasuje
    initial_length = len(INVENTORY)
    
    # Tworzenie nowej listy bez usuniętego elementu
    new_inventory = [item for item in INVENTORY if item['index'] != index_to_remove]
    
    if len(new_inventory) < initial_length:
        # Uaktualniamy listę globalną
        INVENTORY = new_inventory 
        st.toast(f"🗑️ Usunięto indeks: {index_to_remove} (zaraz powróci).")
    else:
        st.toast(f"❌ Błąd: Indeks {index_to_remove} nie został znaleziony.")

## --- Interfejs Użytkownika Streamlit ---

st.title("🔢 Prosty Magazyn (Sześciocyfrowe Indeksy)")
st.warning("⚠️ **UWAGA:** Stan magazynu jest **nietrwały** i resetuje się do listy początkowej po każdej interakcji.")

# Utwórz dwie kolumny
col1, col2 = st.columns([1, 2])

# Kolumna 1: Dodawanie/Usuwanie
with col1:
    st.header("➕ Dodaj / ➖ Usuń")

    # Dodawanie Towaru
    st.subheader("Dodaj Nowy Towar")
    new_item_name = st.text_input("Nazwa nowego towaru")
    
    if st.button("Dodaj do Magazynu", type="primary"):
        add_item(new_item_name)

    st.markdown("---")

    # Usuwanie Towaru
    st.subheader("Usuń Towar (wg Indeksu)")
    
    # Tworzenie listy indeksów do wyboru
    if INVENTORY:
        current_indices = [item['index'] for item in INVENTORY]
        
        index_to_remove_select = st.selectbox(
            "Wybierz Indeks Towaru do usunięcia",
            current_indices,
        )
        
        if st.button("Usuń Wybrany Towar", type="secondary"):
            # Używamy index_to_remove_select do wywołania funkcji
            remove_item(index_to_remove_select)
    else:
        st.info("Lista jest pusta.")

# Kolumna 2: Stan Magazynu
with col2:
    st.header("📊 Aktualny Stan Magazynu")

    if INVENTORY:
        st.metric(label="Łączna Liczba Towarów", value=len(INVENTORY))
        
        # Wyświetlanie danych w DataFrame
        import pandas as pd
        df = pd.DataFrame(INVENTORY)
        df.columns = ["Numer Katalogowy", "Nazwa Towaru"]
        
        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("Lista jest pusta.")
