import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import json
import base64
from PIL import Image

# Page Setup
st.set_page_config(page_title="Collection Tracker", page_icon="🌊", layout="wide")

# Custom CSS for Ocean Pastel Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=Nunito:ital,wght@0,400;0,700;1,700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #E8F4FD 0%, #D4EAF7 50%, #C5E3F5 100%);
    }
    
    h1 {
        font-family: 'Nunito', sans-serif !important;
        font-style: italic !important;
        font-weight: 700 !important;
        font-size: 36px !important;
        background: linear-gradient(135deg, #1B4F72 0%, #2980B9 50%, #5DADE2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
    
    h3 {
        font-family: 'Nunito', sans-serif !important;
        font-weight: 700 !important;
        font-size: 20px !important;
        color: #1B4F72 !important;
        text-align: center;
        margin-top: 0rem !important;
        margin-bottom: 0.5rem !important;
        border-bottom: 1px solid #85C1E9;
        display: inline-block;
        padding-bottom: 5px;
        width: 100%;
    }
    
    .custom-info-box {
        background: linear-gradient(135deg, #85C1E9 0%, #5DADE2 100%);
        padding: 0.8rem 1.2rem !important;
        border-radius: 15px;
        margin: 0.5rem 0 1.5rem 0 !important;
        color: white;
        font-family: 'Outfit', sans-serif;
        font-size: 14px;
        box-shadow: 0 4px 15px rgba(69, 179, 225, 0.2);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .custom-success-box {
        background: linear-gradient(135deg, #48C9B0 0%, #76D7C4 100%);
        padding: 1rem 1.5rem !important;
        border-radius: 15px;
        margin: 1rem 0 1rem 0 !important;
        color: white;
        font-family: 'Outfit', sans-serif;
        font-size: 18px;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 4px 15px rgba(72, 201, 176, 0.3);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .grand-total-box {
        background: linear-gradient(135deg, #1ABC9C 0%, #16A085 100%);
        padding: 1.2rem 1.8rem !important;
        border-radius: 20px;
        margin: 1rem 0 1rem 0 !important;
        color: white;
        font-family: 'Outfit', sans-serif;
        font-size: 20px;
        font-weight: 700;
        text-align: center;
        box-shadow: 0 6px 20px rgba(26, 188, 156, 0.4);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .grand-total-box small {
        font-size: 14px;
        font-weight: normal;
        opacity: 0.9;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1rem;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(41, 128, 185, 0.1);
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(133, 193, 233, 0.3);
        backdrop-filter: blur(5px);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(41, 128, 185, 0.2);
        border-color: #85C1E9;
    }
    
    .stTextInput input {
        border-radius: 30px !important;
        border: 2px solid #85C1E9 !important;
        padding: 0.7rem 1.2rem !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 16px !important;
        transition: all 0.3s;
        background: rgba(255,255,255,0.9) !important;
    }
    
    .stTextInput input:focus {
        border-color: #2980B9 !important;
        box-shadow: 0 0 0 3px rgba(41, 128, 185, 0.1) !important;
        background: white !important;
    }
    
    .stButton button {
        border-radius: 30px !important;
        background: linear-gradient(135deg, #5DADE2 0%, #2980B9 100%) !important;
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(41, 128, 185, 0.3);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B4F72 0%, #2471A3 50%, #2980B9 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        background: rgba(255,255,255,0.4);
        border-radius: 25px;
        margin: 1.5rem;
    }
    
    .welcome-box {
        background: linear-gradient(135deg, rgba(69, 179, 225, 0.1) 0%, rgba(133, 193, 233, 0.2) 100%);
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        margin-top: 2rem;
        border: 2px solid rgba(69, 179, 225, 0.3);
    }
    
    .welcome-title {
        font-family: 'Nunito', sans-serif;
        font-weight: 700;
        font-size: 20px;
        color: #1B4F72;
        text-align: center;
        margin-top: 0;
        margin-bottom: 0.5rem;
        display: inline-block;
        padding-bottom: 5px;
    }
    
    /* Welcome text styling - smaller line spacing */
    .welcome-text {
        font-size: 14px;
        color: #2980B9;
        margin: 0.25rem 0;
        line-height: 1.3;
    }
    
    .welcome-text-small {
        font-size: 14px;
        color: #2980B9;
        margin: 0.5rem 0;
        line-height: 1.2;
    }
    
    .error-box-notfound {
        background: linear-gradient(135deg, #FDEDEC 0%, #FADBD8 100%);
        padding: 1rem;
        border-radius: 15px;
        border-left: 4px solid #E74C3C;
        color: #C0392B;
        margin: 0.5rem 0;
    }
    
    .payment-form-container {
        background: rgba(255, 255, 255, 0.6);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(133, 193, 233, 0.4);
    }
    
    .info-badge {
        background: rgba(133, 193, 233, 0.3);
        border-radius: 20px;
        padding: 0.3rem 1rem;
        display: inline-block;
        font-size: 13px;
        color: #1B4F72;
        margin: 0 0.25rem;
    }
    
    .selected-method-badge {
        background: rgba(26, 188, 156, 0.2);
        border-radius: 15px;
        padding: 0.5rem 1rem;
        text-align: center;
        margin: 0.5rem 0;
        border: 1px solid rgba(26, 188, 156, 0.3);
    }
    
    .badge-container {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        margin-top: 0rem;
        margin-bottom: 0.5rem;
        flex-wrap: wrap;
    }
    
    hr {
        margin: 0.5rem 0;
        border-color: #85C1E9;
    }
    
    /* Responsive adjustments for different screen sizes */
    @media (max-width: 768px) {
        .badge-container {
            margin-top: -0.5rem;
        }
    }
    
    @media (min-width: 1200px) {
        .badge-container {
            margin-top: -0.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1>🌊 leehoney\'s mart collection tracker!</h1>', unsafe_allow_html=True)

# Function to save responses to Google Sheet
def save_to_google_sheet(data):
    try:
        # Check if secrets exist
        if "gcp_service_account" not in st.secrets:
            # Demo mode - save to session state
            if 'responses' not in st.session_state:
                st.session_state.responses = []
            st.session_state.responses.append(data)
            return True
        
        credentials_dict = {
            "type": st.secrets["gcp_service_account"]["type"],
            "project_id": st.secrets["gcp_service_account"]["project_id"],
            "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
            "private_key": st.secrets["gcp_service_account"]["private_key"],
            "client_email": st.secrets["gcp_service_account"]["client_email"],
            "client_id": st.secrets["gcp_service_account"]["client_id"],
            "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
            "token_uri": st.secrets["gcp_service_account"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"]
        }
        
        credentials = Credentials.from_service_account_info(
            credentials_dict, 
            scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        )
        
        client = gspread.authorize(credentials)
        
        # Create or open the response sheet
        try:
            sheet = client.open("Collection Responses")
        except:
            sheet = client.create("Collection Responses")
            # Share with your email
            sheet.share('ajelsss@gmail.com', perm_type='user', role='writer')
        
        worksheet = sheet.get_worksheet(0)
        
        # If empty, add headers
        if not worksheet.get_all_values():
            headers = ['Timestamp', 'Telegram Username', 'Collection Method', 'Specific Location', 
                      'Name', 'Phone Number', 'Address', 'Items to Collect', 
                      'Amount Paid', 'Transaction Proof', 'Note', 'Status']
            worksheet.append_row(headers)
        
        # Append data
        row = [
            data['timestamp'],
            data['username'],
            data['collection_method'],
            data['specific_location'],
            data['name'],
            data['phone'],
            data['address'],
            data['items'],
            data['amount_paid'],
            data['transaction_proof'],
            data['note'],
            'Pending'
        ]
        worksheet.append_row(row)
        return True
        
    except Exception as e:
        st.error(f"Error saving: {str(e)}")
        return False

# Load data function
@st.cache_data(ttl=300)
def load_data():
    try:
        try:
            credentials_dict = {
                "type": st.secrets["gcp_service_account"]["type"],
                "project_id": st.secrets["gcp_service_account"]["project_id"],
                "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
                "private_key": st.secrets["gcp_service_account"]["private_key"],
                "client_email": st.secrets["gcp_service_account"]["client_email"],
                "client_id": st.secrets["gcp_service_account"]["client_id"],
                "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
                "token_uri": st.secrets["gcp_service_account"]["token_uri"],
                "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
                "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"]
            }
            credentials = Credentials.from_service_account_info(credentials_dict, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
            client = gspread.authorize(credentials)
            sheet = client.open_by_key("1ZhOdFDh33lcIp7yzj9KoeaNdJhKziEXxUGDNHD3ISXQ")
            worksheet = sheet.get_worksheet(0)
            data = worksheet.get_all_records()
            return pd.DataFrame(data)
        except:
            csv_url = "https://docs.google.com/spreadsheets/d/1ZhOdFDh33lcIp7yzj9KoeaNdJhKziEXxUGDNHD3ISXQ/export?format=csv&gid=0"
            return pd.read_csv(csv_url)
    except Exception as e:
        st.error(f"Error loading data. Please contact @ajelsssss.")
        return None

# Function to get shipping cost
def get_shipping_cost(method):
    if method == "Tracked Envelope":
        return 3.00
    elif method == "Tracked Box":
        return 3.80
    else:
        return 0

# Search
st.markdown("### 🔍 Find Your Orders")
user_input = st.text_input("Username", placeholder="🐠 Enter telegram u/n (e.g: @ajelsssss)", label_visibility="collapsed")

# Initialize session state
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'collection_method' not in st.session_state:
    st.session_state.collection_method = None
if 'specific_location' not in st.session_state:
    st.session_state.specific_location = None
if 'show_all_orders' not in st.session_state:
    st.session_state.show_all_orders = False

if user_input and not st.session_state.submitted:
    with st.spinner("🌊 Diving in..."):
        df = load_data()
        
        if df is not None:
            df['Username'] = df['Username'].astype(str).str.strip()
            user_data = df[df['Username'].str.lower() == user_input.lower()].copy()

            if not user_data.empty:
                st.markdown(f"### 🐚 Order Summary for {user_input}")
                
                # Calculate totals for ALL orders
                user_data['Notification_Date'] = pd.to_datetime(user_data['Notification_Date'], dayfirst=True)
                today = datetime.now()
                user_data['Days_Since'] = (today - user_data['Notification_Date']).dt.days
                user_data['Late_Fee'] = user_data['Days_Since'].apply(lambda x: max(0, (x - 7) * 1) if pd.notnull(x) else 0)
                user_data['Second_Payment'] = pd.to_numeric(user_data['Second_Payment'], errors='coerce').fillna(0)
                user_data['Total_Due'] = user_data['Second_Payment'] + user_data['Late_Fee']
                
                total_2nd = user_data['Second_Payment'].sum()
                total_late = user_data['Late_Fee'].sum()
                total_due = user_data['Total_Due'].sum()
                
                # Filter based on Status column (ready for collection vs not)
                user_data['Status_Str'] = user_data['Status'].astype(str).str.lower().str.strip()
                ready_orders = user_data[user_data['Status_Str'] == 'ready for collection'].copy()
                pending_orders = user_data[user_data['Status_Str'] != 'ready for collection'].copy()
                
                # Show toggle button centered if there are pending orders
                if len(pending_orders) > 0:
                    # Centered See All Orders button with minimal spacing
                    col_empty1, col_btn, col_empty2 = st.columns([1, 2, 1])
                    with col_btn:
                        if not st.session_state.show_all_orders:
                            if st.button("🐙 See All Orders", use_container_width=True):
                                st.session_state.show_all_orders = True
                                st.rerun()
                        else:
                            if st.button("🐚 Show Ready Orders Only", use_container_width=True):
                                st.session_state.show_all_orders = False
                                st.rerun()
                    
                    # Centered badges below the button - responsive spacing
                    st.markdown(f"""
                        <div class="badge-container">
                            <span class="info-badge">✅ {len(ready_orders)} ready for collection</span>
                            <span class="info-badge">⏳ {len(pending_orders)} pending arrival</span>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Determine which data to display in table
                if st.session_state.show_all_orders:
                    display_data = user_data.copy()
                    if len(pending_orders) > 0:
                        st.info(f"🐙 Showing all {len(user_data)} orders")
                else:
                    display_data = ready_orders.copy()
                    if len(ready_orders) == 0 and len(pending_orders) > 0:
                        st.warning("🌊 No items are ready for collection yet! Click 'See All Orders' to view all your orders.")
                
                # 4. Table Display - Full table with all columns
                if len(display_data) > 0:
                    display_df = display_data.copy()
                    display_df['Notification_Date'] = display_df['Notification_Date'].dt.strftime('%d %b %Y')
                    
                    # Columns to display
                    desired_columns = ['Batch', 'Item_Name', 'Qty', 'Status', 'Notification_Date', 'Second_Payment', 'Late_Fee', 'Total_Due', 'Payment_Status','Remarks']
                    available_columns = [col for col in desired_columns if col in display_df.columns]
                    
                    clean_table = display_df[available_columns].rename(columns={
                        'Item_Name': 'Item Name',
                        'Notification_Date': 'Collection Notification',
                        'Second_Payment': '2nd Payment',
                        'Late_Fee': 'Late Fee',
                        'Total_Due': 'Total Due',
                        'Payment_Status': 'Payment Status',
                        'Status':'Item Status'
                    })
                    
                    # Format currency columns
                    for col in ['2nd Payment', 'Late Fee', 'Total Due']:
                        if col in clean_table.columns:
                            clean_table[col] = clean_table[col].apply(lambda x: f"${x:.2f}")
                    
                    st.dataframe(clean_table, use_container_width=True, hide_index=True)
                
                # Payment Summary (based on ALL orders)
                st.markdown("### 💰 Payment Summary")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div style="font-size: 14px; color: #1B4F72; margin-bottom: 10px;">💳 Total 2nd Payment</div>
                            <div style="font-size: 28px; font-weight: bold; color: #2471A3;">${total_2nd:.2f}</div>
                            <div style="font-size: 12px; color: #5DADE2; margin-top: 5px;">✨ pending payment</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    late_color = "#E74C3C" if total_late > 0 else "#27AE60"
                    late_text = "⚠️ overdue" if total_late > 0 else "✅ on time"
                    st.markdown(f"""
                        <div class="metric-card">
                            <div style="font-size: 14px; color: {late_color}; margin-bottom: 10px;">⚠️ Total Late Fee</div>
                            <div style="font-size: 28px; font-weight: bold; color: {late_color};">${total_late:.2f}</div>
                            <div style="font-size: 12px; color: #5DADE2; margin-top: 5px;">{late_text}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div style="font-size: 14px; color: #1ABC9C; margin-bottom: 10px;">🎯 Total Payment</div>
                            <div style="font-size: 28px; font-weight: bold; color: #1ABC9C;">${total_due:.2f}</div>
                            <div style="font-size: 12px; color: #5DADE2; margin-top: 5px;">💎 2nd Payment + Late Fee</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Only show collection method and form if there are ready orders
                if len(ready_orders) > 0:
                    # Collection Method Selection
                    st.markdown("---")
                    st.markdown("### 📮 Choose Collection Method")
                    
                    col_a, col_b, col_c, col_d = st.columns(4)
                    
                    with col_a:
                        if st.button("📩 Tracked Envelope\n+$3.00", use_container_width=True):
                            st.session_state.collection_method = "Tracked Envelope"
                            st.session_state.specific_location = None
                            st.rerun()
                    
                    with col_b:
                        if st.button("📦 Tracked Box\n+$3.80", use_container_width=True):
                            st.session_state.collection_method = "Tracked Box"
                            st.session_state.specific_location = None
                            st.rerun()
                    
                    with col_c:
                        if st.button("🏠 Self-Collect\n", use_container_width=True):
                            st.session_state.collection_method = "Self-Collect"
                            st.session_state.specific_location = None
                            st.rerun()
                    
                    with col_d:
                        if st.button("🤝 Meet-up\n", use_container_width=True):
                            st.session_state.collection_method = "Meet-up"
                            st.session_state.specific_location = None
                            st.rerun()
                    
                    # Show Grand Total Box if a collection method is selected
                    if st.session_state.collection_method:
                        shipping_cost = get_shipping_cost(st.session_state.collection_method)
                        grand_total = total_due + shipping_cost
                        
                        method_display = {
                            "Tracked Envelope": "📩 Tracked Envelope",
                            "Tracked Box": "📦 Tracked Box",
                            "Self-Collect": "🏠 Self-Collect",
                            "Meet-up": "🤝 Meet-up"
                        }.get(st.session_state.collection_method, st.session_state.collection_method)
                        
                        if shipping_cost > 0:
                            st.markdown(f"""
                                <div class="grand-total-box">
                                    🐠 <strong>GRAND TOTAL: ${grand_total:.2f}</strong> 🐚<br>
                                    <small>(Items: ${total_due:.2f} + {method_display}: ${shipping_cost:.2f})</small>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                                <div class="grand-total-box">
                                    🐠 <strong>GRAND TOTAL: ${grand_total:.2f}</strong> 🐚<br>
                                    <small>(Items: ${total_due:.2f} + {method_display}: Free)</small>
                                </div>
                            """, unsafe_allow_html=True)
                    
                    # Location Selection based on method
                    if st.session_state.collection_method == "Self-Collect":
                        st.markdown("#### 📍 Select Location")
                        st.markdown("""
                            <div style="background: rgba(133, 193, 233, 0.15); padding: 0.8rem; border-radius: 12px; margin-bottom: 1rem; font-size: 13px;">
                                <strong>📍 Collection Locations:</strong><br>
                                • NUS: 6 College Avenue East, 138614<br>
                                • Bishan: Block 142 Bishan Street 12 #09-528, 570142
                            </div>
                        """, unsafe_allow_html=True)
                        loc1, loc2 = st.columns(2)
                        with loc1:
                            if st.button("🏠 NUS", use_container_width=True):
                                st.session_state.specific_location = "NUS - 6 College Avenue East, 138614"
                                st.rerun()
                        with loc2:
                            if st.button("🏠 Bishan", use_container_width=True):
                                st.session_state.specific_location = "Bishan - Block 142 Bishan Street 12 #09-528, 570142"
                                st.rerun()
                    
                    elif st.session_state.collection_method == "Meet-up":
                        st.markdown("#### 🤝 Select MRT Station")
                        st.markdown("""
                            <div style="background: rgba(133, 193, 233, 0.15); padding: 0.8rem; border-radius: 12px; margin-bottom: 1rem; font-size: 13px;">
                                <strong>📍 Important Notes:</strong><br>
                                <em>Admin may choose locations near the MRT station.</em>
                            </div>
                        """, unsafe_allow_html=True)
                        loc1, loc2, loc3 = st.columns(3)
                        with loc1:
                            if st.button("🚉 Kent Ridge MRT", use_container_width=True):
                                st.session_state.specific_location = "Kent Ridge MRT"
                                st.rerun()
                        with loc2:
                            if st.button("🚉 Clementi MRT", use_container_width=True):
                                st.session_state.specific_location = "Clementi MRT"
                                st.rerun()
                        with loc3:
                            if st.button("🚉 Buona Vista MRT", use_container_width=True):
                                st.session_state.specific_location = "Buona Vista MRT"
                                st.rerun()
                    
                    # Show selected method badge
                    if st.session_state.collection_method and st.session_state.collection_method not in ["Self-Collect", "Meet-up"]:
                        st.markdown(f"""
                            <div class="selected-method-badge">
                                ✨ Selected: {st.session_state.collection_method} (+${get_shipping_cost(st.session_state.collection_method):.2f})
                            </div>
                        """, unsafe_allow_html=True)
                    elif st.session_state.collection_method and st.session_state.specific_location:
                        st.markdown(f"""
                            <div class="selected-method-badge">
                                ✨ Selected: {st.session_state.collection_method} - {st.session_state.specific_location}
                            </div>
                        """, unsafe_allow_html=True)
                    elif st.session_state.collection_method and st.session_state.collection_method in ["Self-Collect", "Meet-up"] and not st.session_state.specific_location:
                        st.info("👆 Please select a specific location above to continue.")
                    
                    # Show form if method and location selected (or method selected for mailing)
                    show_form = False
                    if st.session_state.collection_method in ["Tracked Envelope", "Tracked Box"]:
                        show_form = True
                    elif st.session_state.collection_method in ["Self-Collect", "Meet-up"] and st.session_state.specific_location:
                        show_form = True
                    
                    if show_form:
                        st.markdown("---")
                        st.markdown("### 📝 Complete Your Collection Request")
                        
                        # PayNow QR Code section
                        import base64
                        
                        # Read and encode the QR code image
                        try:
                            with open("qr_code.png", "rb") as image_file:
                                qr_base64 = base64.b64encode(image_file.read()).decode()
                            
                            st.markdown(f"""
                                <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 1rem; border-radius: 15px; text-align: center; margin-bottom: 1rem;">
                                    <p><strong>💰 PayNow/Paylah to: 80131019</strong></p>
                                    <p>or scan QR code:</p>
                                    <div style="display: flex; justify-content: center; margin-top:-15px">
                                        <img src="data:image/png;base64,{qr_base64}" width="150" style="border-radius: 10px;">
                                    </div>
                                    <p style="font-size: 12px; margin-top: 5px;">After payment, upload screenshot below</p>
                                </div>
                            """, unsafe_allow_html=True)
                        except:
                            st.warning("QR code image not found. Please add qr_code.png to the app folder.")
                        
                        with st.form(key="collection_form"):                            
                            # Pre-filled fields
                            st.text_input("Telegram Username", value=user_input, disabled=True)
                            st.text_input("Collection Method", value=st.session_state.collection_method, disabled=True)
                            if st.session_state.specific_location:
                                st.text_input("Selected Location", value=st.session_state.specific_location, disabled=True)
                            
                            # Required fields
                            name = st.text_input("Name *", placeholder="Enter your name")
                            phone = st.text_input("Phone Number *", placeholder="e.g., 91234567")
                            
                            # Address - required only for mailing
                            if st.session_state.collection_method in ["Tracked Envelope", "Tracked Box"]:
                                address = st.text_area("Full Delivery Address *", placeholder="Enter complete address with postal code", height=80)
                            else:
                                address = st.text_area("Address (For Mailing)", placeholder="Don't need to input if opted for self-collect/mailing", height=80)
                            
                            # Items to collect - ONLY ready for collection items
                            ready_items_list = "\n".join([f"- {row['Item_Name']} (Qty: {row['Qty']})" for _, row in ready_orders.iterrows()])
                            st.text_area("Items to Collect (Ready for Collection)", value=ready_items_list, disabled=True, height=120)
                            
                            # Payment fields - show the grand total again
                            shipping_cost = get_shipping_cost(st.session_state.collection_method)
                            amount_to_pay = total_due + shipping_cost
                            st.info(f"💰 **Total Amount to Pay: ${amount_to_pay:.2f}**")
                            
                            st.number_input("Amount Transferred ($)", value=float(amount_to_pay), min_value=0.0, step=0.5, key="amount_paid")
                            
                            # Transaction proof upload
                            if st.session_state.collection_method in ["Tracked Envelope", "Tracked Box"]:
                                proof_file = st.file_uploader("Upload Transaction Proof (Screenshot) *", type=['png', 'jpg', 'jpeg', 'pdf'])
                            else:
                                proof_file = st.file_uploader("Upload Transaction Proof", type=['png', 'jpg', 'jpeg', 'pdf'])
                            
                            # Note
                            note = st.text_area("Note (Optional)", placeholder="e.g., collecting with friend, special requests, etc.")
                            
                            # Acknowledgement
                            acknowledge = st.checkbox("I confirm that the information provided is accurate and I have made the payment (if applicable) *")
                            
                            submitted = st.form_submit_button("🐠 Submit Collection Request", use_container_width=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            if submitted:
                                if not name or not phone or not acknowledge:
                                    st.error("Please fill in all required fields (*)")
                                elif st.session_state.collection_method in ["Tracked Envelope", "Tracked Box"] and not address:
                                    st.error("Please provide your delivery address")
                                elif st.session_state.collection_method in ["Tracked Envelope", "Tracked Box"] and not proof_file:
                                    st.error("Please upload your transaction proof")
                                else:
                                    # Prepare data
                                    proof_info = f"{proof_file.name} - {datetime.now()}" if proof_file else "No proof needed (self-collect/meet-up)"
                                    
                                    response_data = {
                                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                        'username': user_input,
                                        'collection_method': st.session_state.collection_method,
                                        'specific_location': st.session_state.specific_location or "N/A",
                                        'name': name,
                                        'phone': phone,
                                        'address': address,
                                        'items': ready_items_list,
                                        'amount_paid': f"${amount_to_pay:.2f}",
                                        'transaction_proof': proof_info,
                                        'note': note if note else "None"
                                    }
                                    
                                    if save_to_google_sheet(response_data):
                                        st.session_state.submitted = True
                                        st.success("✅ Collection request submitted successfully!")
                                        st.balloons()
                                        st.info("Thank you for your submission!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to submit. Please contact @ajelsssss directly.")
                else:
                    st.info("🌊 No items are ready for collection yet. Check back later!")
                
            else:
                st.markdown(f"""
                    <div class="error-box-notfound">
                        <strong>🐠 Username '{user_input}' not found!</strong><br><br>
                        Possible reasons:<br>
                        • Incorrect username (check spelling and include "@")<br>
                        • Items not ready for collection yet<br><br>
                        Contact <strong>@ajelsssss</strong> for assistance.
                    </div>
                """, unsafe_allow_html=True)

elif st.session_state.submitted:
    st.markdown("""
        <div class="custom-success-box">
            🐠 <strong>Thank you for your submission!</strong>
        </div>
    """, unsafe_allow_html=True)
    if st.button("📋 Submit Another Request"):
        st.session_state.submitted = False
        st.session_state.collection_method = None
        st.session_state.specific_location = None
        st.session_state.show_all_orders = False
        st.rerun()

else:
    st.markdown("""
        <div class="welcome-box">
            <div style="font-size: 40px;">🐠 🌊 🐙</div>
            <div class="welcome-title">welcome to leehoney's mart.°•</div>
            <p class="welcome-text">check your order status and submit collection requests here!</p>
            <hr style="margin: 0.5rem 0;">
            <p class="welcome-text-small">𓇼 website works best with light mode! click on the 3 dots on the top right to adjust!</p>
            <p class="welcome-text-small">𓇼 please read details on the side bar first before filling up the form!</p>
            <p class="welcome-text-small">𓇼 please collect your items within 3 weeks of notification!</p>
            <p class="welcome-text-small">𓇼 consolidation limited to maximum 2 consecutive batches!</p>
            <p class="welcome-text-small">𓇼 late fee of $1/day applies after 3 weeks!</p>
        </div>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🌊 Quick Guide")
    st.markdown("---")
    st.markdown("**Collection Options:**")
    st.markdown("📩 Tracked Envelope: up to 33cm x 24cm ")
    st.markdown("📦 Tracked Box: 30cm x 19cm x 6.5cm **[more secure]**")
    st.markdown("🏠 Self-Collect: NUS | Bishan [for bulky items, only **self-collection** is allowed]")
    st.markdown("🤝 Meet-up at admin's convenience: Clementi | Buona Vista | Kent Ridge MRT")
    st.markdown("---")
    st.markdown("**About Mailing:**")
    st.markdown("🏠 Make sure you have entered your full address correctly")
    st.markdown("📍 Tracking codes will be sent together with address check!")
    st.markdown("💬 State your username in the comment when transferring!")
    st.markdown("---")
    st.markdown("**About Self-Collection:**")
    st.markdown("🏠 For Bishan, please fill in the form 1 week before coming down to collect!")
    st.markdown("📍 For NUS, please fill in the form 3 days before coming down to collect!")
    st.markdown("---")
    st.markdown("**About Late Fee(s):**")
    st.markdown("⏰ Late fee of $1/day applies for late collection")
    st.markdown("📩 For mailing, item(s) is/are considered collected once form is filled up!")
    st.markdown("🏠 For self-collection, item(s) is/are to be  collected within **3 weeks** from collection notification, after which late fee will also apply!!")
    st.markdown("---")
    st.markdown(f"**🕒 Last Updated**\n{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    st.markdown("---")
    st.markdown("*made with 🤍 by leehoney's mart*")
