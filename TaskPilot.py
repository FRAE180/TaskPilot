import streamlit as st
import pandas as pd
import openpyxl

# Excel-Datei laden
excel_file = 'todo_xlsx.xlsx'
df = pd.read_excel(excel_file, sheet_name='ToDo_Priorisiert', engine='openpyxl')

# Leere Zeilen entfernen
df.dropna(how='all', inplace=True)

# Spaltennamen bereinigen (z. B. \n entfernen)
df.columns = df.columns.str.replace('\n', ' ').str.strip()

# Fehlende Status-Werte auffüllen
df['Status'] = df['Status'].fillna('Unbekannt')

# Sidebar: Neue Aufgabe hinzufügen
st.sidebar.header("➕ Neue Aufgabe hinzufügen")
with st.sidebar.form("task_form"):
    erstellt = pd.Timestamp.now()
    kunde = st.text_input("Kunde oder Hersteller")
    aufgabe = st.text_input("Aufgabe")
    beschreibung = st.text_area("Beschreibung")
    deadline = st.date_input("Deadline")
    prioritaet = st.selectbox("Priorität", options=[1, 2, 3, 4, 5])
    status = st.selectbox("Status", options=["Bearbeitung", "Pausiert", "Abgeschlossen", "Unbekannt"])
    submitted = st.form_submit_button("Hinzufügen")

    if submitted:
        new_task = {
            'Erstellt': erstellt,
            'Kunde oder Hersteller': kunde,
            'Aufgabe': aufgabe,
            'Beschreibung': beschreibung,
            'Deadline': deadline,
            'Priorität': prioritaet,
            'Status': status
        }
        df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)
        st.success("✅ Aufgabe hinzugefügt!")

# Titel
st.title("📋 ToDo Kanban Board")

# Kanban-Spalten nach Status
statuses = df['Status'].unique()
columns = st.columns(len(statuses))

for i, status in enumerate(statuses):
    with columns[i]:
        st.subheader(status)
        for _, row in df[df['Status'] == status].iterrows():
            st.markdown(f"**{row.get('Aufgabe', '')}**")
            st.markdown(f"*{row.get('Kunde oder Hersteller', '')}*")
            st.markdown(f"{row.get('Beschreibung', '')}")
            st.markdown(f"📅 Deadline: {row.get('Deadline', '')}")
            st.markdown(f"🔥 Priorität: {row.get('Priorität', '')}")
            st.markdown("---")
