import streamlit as st

# --- Definicja Stanu (RESETUJE SIĘ PO INTERAKCJI) ---
# Ponieważ nie używamy st.session_state, ta lista zostanie zresetowana
# za każdym razem, gdy użytkownik kliknie przycisk lub wprowadzi dane.
# Jest to celowe w tym przykładzie, aby pokazać działanie bez stanu sesji.
INVENTORY = [
    "Laptop Służbowy",
    "Smartfon Firmowy",
    "Zestaw Słuchawkowy",
]

# --- Ustawienia Strony ---
st.set_page_config(
    page_title="Prosty Magazyn (Bez Sesji)",
    layout="wide",
    initial_sidebar_state="expanded"
)

## --- Funkcje Logiki Magazynu ---

def add_item(item_name):
    """Próbuje dodać przedmiot, ale tylko do bieżącej instancji listy."""
    # UWAGA: Ta zmiana nie będzie trwała!
    if item_name and item_name not in INVENTORY:
        INVENTORY.append(item_name)
        st.toast(f"✅ Dodano: '{item_name}' (tylko w tej chwili, zaraz zniknie).")
    elif item_name in INVENTORY:
        st.toast(f"⚠️ Przedmiot '{item_name}' jest już na liście.")
    else:
        st.toast("❌ Nazwa przedmiotu nie może być pusta.")

def remove_item(item_name):
    """Próbuje usunąć przedmiot, ale tylko z bieżącej instancji listy."""
    # UWAGA: Ta zmiana nie będzie trwała!
    try:
        INVENTORY.remove(item_name)
        st.toast(f"🗑️ Usunięto: '{item_name}' (tylko w tej chwili, zaraz powróci).")
    except ValueError:
        st.toast(f"❌ Błąd: Przedmiot '{item_name}' nie został znaleziony.")

## --- Interfejs Użytkownika Streamlit ---

st.title("👻 Prosty Magazyn (Stan Nietrwały)")
st.warning("⚠️ **UWAGA:** Ten system **NIE** używa `st.session_state`. Każda interakcja (np. dodanie/usunięcie) spowoduje zresetowanie listy do jej początkowego stanu.")

# Utwórz dwie kolumny dla lepszego układu
col1, col2 = st.columns([1, 2])

# Kolumna 1: Dodawanie/Usuwanie
with col1:
    st.header("➕ Dodaj / ➖ Usuń")

    # Dodawanie Towaru
    st.subheader("Dodaj Nowy Towar")
    new_item = st.text_input("Nazwa nowego towaru")
    
    # Wywołanie funkcji przyciskiem (resetuje stan)
    if st.button("Dodaj do Magazynu", type="primary"):
        add_item(new_item)

    st.markdown("---")

    # Usuwanie Towaru
    st.subheader("Usuń Towar")
    if INVENTORY:
        # Selectbox z aktualną listą przedmiotów
        # UWAGA: Po kliknięciu przycisku 'Usuń', ta lista powróci do stanu początkowego.
        item_to_remove = st.selectbox(
            "Wybierz towar do usunięcia",
            INVENTORY,
        )
        
        # Wywołanie funkcji przyciskiem (resetuje stan)
        if st.button("Usuń Wybrany Towar", type="secondary"):
            remove_item(item_to_remove)
    else:
        st.info("Lista jest pusta.")

# Kolumna 2: Stan Magazynu
with col2:
    st.header("📊 Aktualny Stan Magazynu")

    # Wyświetl listę zaimportowaną na początku skryptu
    if INVENTORY:
        st.metric(label="Łączna Liczba Towarów", value=len(INVENTORY))
        
        st.dataframe(
            {"Indeks": range(1, len(INVENTORY) + 1), "Nazwa Towaru": INVENTORY},
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("Lista jest pusta.")
