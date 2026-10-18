import streamlit as st
import json
import os

st.set_page_config(page_title="Client Management System", page_icon="👥", layout="wide")

st.title("👥 Client Management System")
st.caption("Simple & Powerful Client Manager")

DATA_FILE = "clients_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

if "clients" not in st.session_state:
    st.session_state.clients = load_data()

# --------- Metrics ---------
total = len(st.session_state.clients)
active = len([c for c in st.session_state.clients if c["status"] == "Active"])
pending = len([c for c in st.session_state.clients if c["status"] == "Pending"])
completed = len([c for c in st.session_state.clients if c["status"] == "Completed"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Clients", total)
col2.metric("Active", active)
col3.metric("Pending", pending)
col4.metric("Completed", completed)

st.markdown("---")

# --------- Sidebar ---------
st.sidebar.title("Menu")
menu = st.sidebar.radio("Select Option:", 
                        ["Add Client", "Search Client", "View All", "Update Status", "Delete Client", "Download Data"])

# --------- Add Client ---------
if menu == "Add Client":
    st.header("➕ Add New Client")
    name = st.text_input("Client Name")
    status = st.selectbox("Status", ["Active", "Pending", "Completed"])
    
    if st.button("Add Client", type="primary"):
        if name.strip():
            st.session_state.clients.append({"name": name.strip(), "status": status})
            save_data(st.session_state.clients)
            st.success(f"✅ {name} successfully add ho gaya!")
            st.balloons()
            st.rerun()
        else:
            st.warning("Please enter a name.")

# --------- Search Client ---------
elif menu == "Search Client":
    st.header("🔍 Search Client")
    search_name = st.text_input("Enter name to search")
    
    if search_name:
        found = [c for c in st.session_state.clients if search_name.lower() in c["name"].lower()]
        if found:
            st.success(f"Found {len(found)} client(s)")
            st.write("### Search Result:")
            st.dataframe(found)   # یہ لائن اہم ہے
        else:
            st.warning("No client found.")

# --------- View All ---------
elif menu == "View All":
    st.header("📋 All Clients")
    if st.session_state.clients:
        st.table(st.session_state.clients)
    else:
        st.info("No clients added yet. Go to 'Add Client' to start.")

# --------- Update Status ---------
elif menu == "Update Status":
    st.header("✏️ Update Client Status")
    update_name = st.text_input("Enter client name")
    new_status = st.selectbox("New Status", ["Active", "Pending", "Completed"])
    
    if st.button("Update Status", type="primary"):
        found = False
        for client in st.session_state.clients:
            if client["name"].lower().strip() == update_name.lower().strip():
                client["status"] = new_status
                found = True
                break
        if found:
            save_data(st.session_state.clients)
            st.success(f"✅ {update_name} ka Status successfully update ho gaya!")
            st.balloons()
        else:
            st.error("Client not found. Please check the name.")

# --------- Delete Client ---------
elif menu == "Delete Client":
    st.header("🗑️ Delete Client")
    delete_name = st.text_input("Enter name to delete")
    
    if st.button("Delete Client", type="primary"):
        original = len(st.session_state.clients)
        st.session_state.clients = [
            c for c in st.session_state.clients 
            if c["name"].lower().strip() != delete_name.lower().strip()
        ]
        if len(st.session_state.clients) < original:
            save_data(st.session_state.clients)
            st.success("✅ Client deleted successfully!")
            st.rerun()
        else:
            st.error("Client not found. Please check the name.")

# --------- Download Data ---------
elif menu == "Download Data":
    st.header("📥 Download Data")
    if st.session_state.clients:
        json_data = json.dumps(st.session_state.clients, indent=4)
        st.download_button(
            label="Download JSON File",
            data=json_data,
            file_name="clients_data.json",
            mime="application/json"
        )
        st.success("Click the button above to download your data.")
    else:
        st.info("No data available to download.")