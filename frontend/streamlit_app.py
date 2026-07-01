"""
Streamlit frontend for Customer Churn Intelligence Platform.
"""
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import uuid

import os

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="Customer Churn Intelligence Platform",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Session state initialization
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False


# Sidebar
with st.sidebar:
    st.markdown("# 🏦 Churn Intelligence")
    st.markdown("---")
    
    st.markdown("### Session Info")
    st.info(f"Session ID: {st.session_state.session_id[:8]}...")
    
    st.markdown("### Navigation")
    page = st.radio(
        "Select Page",
        ["💬 AI Chat", "📊 Dashboard", "📁 Data Upload", "📜 History", "⚙️ Settings"]
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This platform uses multi-agent AI to analyze customer churn patterns and generate retention recommendations.
    """)


# Main content
st.markdown('<div class="main-header">Customer Churn Intelligence Platform</div>', unsafe_allow_html=True)


# Page: AI Chat
if page == "💬 AI Chat":
    st.markdown('<div class="sub-header">AI-Powered Churn Analysis</div>', unsafe_allow_html=True)
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about customer churn, risk factors, or retention strategies..."):
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing with multi-agent system..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/query",
                            json={
                                "session_id": st.session_state.session_id,
                                "user_query": prompt,
                                "context": ""
                            },
                            timeout=120
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            ai_response = result["response"]
                            st.markdown(ai_response)
                            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                        else:
                            st.error(f"Error: {response.status_code}")
                            st.error(response.text)
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection error: {str(e)}")
                        st.error("Make sure the backend API is running on http://localhost:8000")

    # Export option at the bottom
    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### Export & Reports")
        if st.button("📥 Generate and Export PDF report", key="export_pdf_button"):
            with st.spinner("Preparing executive summary style PDF..."):
                try:
                    report_resp = requests.post(f"{API_URL}/generate-report", json={"session_id": st.session_state.session_id})
                    if report_resp.status_code == 200:
                        pdf_resp = requests.get(f"{API_URL}/download-report/{st.session_state.session_id}")
                        if pdf_resp.status_code == 200:
                            st.download_button(
                                label="Download Executive PDF",
                                data=pdf_resp.content,
                                file_name=f"BNP_ChurnReport_{st.session_state.session_id[:8]}.pdf",
                                mime="application/pdf"
                            )
                            st.success("Executive PDF generated successfully! Click the button above to download.")
                        else:
                            st.error(f"Failed to fetch PDF report: {pdf_resp.text}")
                    else:
                        st.error(f"Failed to compile report: {report_resp.text}")
                except Exception as e:
                    st.error(f"Error exporting report: {e}")



# Page: Dashboard
elif page == "📊 Dashboard":
    st.markdown('<div class="sub-header">Analytics Dashboard</div>', unsafe_allow_html=True)
    
    # Try to load existing dataset to populate dashboard dynamically
    import os
    dataset_file = "datasets/BNPParibas_Data.csv"
    df_loaded = None
    if os.path.exists(dataset_file):
        try:
            df_loaded = pd.read_csv(dataset_file)
            df_loaded = df_loaded.dropna()
            df_loaded = df_loaded[df_loaded['age'] > 0]
            df_loaded = df_loaded[df_loaded['tenure_months'] >= 0]
        except Exception:
            pass
            
    # Metrics columns
    col1, col2, col3, col4 = st.columns(4)
    
    if df_loaded is not None and not df_loaded.empty:
        total_cust = len(df_loaded)
        churn_rate_val = df_loaded['churn'].mean()
        high_risk_cust = len(df_loaded[(df_loaded['churn'] == 1) | (df_loaded['support_tickets'] > 3)])
        retention_rate_val = 1.0 - churn_rate_val
        
        with col1:
            st.metric("Total Customers", f"{total_cust}")
        with col2:
            st.metric("Churn Rate", f"{churn_rate_val * 100:.1f}%")
        with col3:
            st.metric("High Risk Customers", f"{high_risk_cust}")
        with col4:
            st.metric("Retention Goal", f"{retention_rate_val * 100:.1f}%")
            
        st.markdown("---")
        
        # Real statistics charts
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Churn Rate by Contract Type (%)")
            contract_churn = df_loaded.groupby('contract_type')['churn'].mean() * 100
            st.bar_chart(contract_churn)
        with c2:
            st.subheader("Customer Status Count")
            status_df = pd.DataFrame({
                "Count": df_loaded['churn'].value_counts().values
            }, index=["Active (0)", "Churned (1)"])
            st.bar_chart(status_df)
    else:
        with col1:
            st.metric("Total Customers", "0", "N/A")
        with col2:
            st.metric("Churn Rate", "0%", "N/A")
        with col3:
            st.metric("High Risk", "0", "N/A")
        with col4:
            st.metric("Retention Rate", "0%", "N/A")
            
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Churn Distribution")
            st.info("Upload dataset to view churn distribution")
        with col2:
            st.subheader("Customer Segments")
            st.info("Upload dataset to view customer segments")
            
    st.markdown("---")
    st.subheader("Recent Analysis")
    if st.session_state.chat_history:
        st.write(f"Active session chat history contains {len(st.session_state.chat_history)} messages.")
    else:
        st.info("No recent analysis available in this session. Start a chat to see analysis results.")



# Page: Data Upload
elif page == "📁 Data Upload":
    st.markdown('<div class="sub-header">Upload Customer Dataset</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Upload your customer churn dataset (CSV format) to enable AI-powered analysis.
    
    Expected columns:
    - customer_id
    - age
    - tenure_months
    - monthly_charges
    - total_charges
    - contract_type
    - internet_service
    - support_tickets
    - payment_method
    - churn (0/1)
    """)
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload a CSV file with customer data"
    )
    
    if uploaded_file is not None:
        # Display file info
        file_details = {
            "Filename": uploaded_file.name,
            "File type": uploaded_file.type,
            "File size": f"{uploaded_file.size / 1024:.2f} KB"
        }
        st.json(file_details)
        
        # Preview data
        try:
            df = pd.read_csv(uploaded_file)
            st.subheader("Data Preview")
            st.dataframe(df.head())
            
            st.subheader("Data Summary")
            st.write(df.describe())
            
            # Upload button
            if st.button("Upload to ChromaDB", type="primary"):
                with st.spinner("Processing and uploading data..."):
                    try:
                        uploaded_file.seek(0) # Reset file pointer before sending
                        files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}
                        response = requests.post(
                            f"{API_URL}/upload",
                            files=files,
                            timeout=300
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.markdown('<div class="success-box">✅ Dataset uploaded successfully!</div>', unsafe_allow_html=True)
                            st.json(result)
                            st.session_state.uploaded = True
                        else:
                            st.markdown(f'<div class="error-box">❌ Upload failed: {response.status_code}</div>', unsafe_allow_html=True)
                            st.error(response.text)
                    except requests.exceptions.RequestException as e:
                        st.markdown(f'<div class="error-box">❌ Connection error: {str(e)}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error reading CSV: {str(e)}")


# Page: History
elif page == "📜 History":
    st.markdown('<div class="sub-header">Conversation History</div>', unsafe_allow_html=True)
    
    try:
        response = requests.get(
            f"{API_URL}/history/{st.session_state.session_id}",
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            history = result["history"]
            
            if history:
                for i, entry in enumerate(history, 1):
                    with st.expander(f"Q{i}: {entry['user_query'][:50]}..."):
                        st.markdown(f"**User:** {entry['user_query']}")
                        st.markdown(f"**Assistant:** {entry['agent_response']}")
                        st.caption(f"Timestamp: {entry.get('created_at', 'N/A')}")
            else:
                st.info("No conversation history yet. Start chatting to build history.")
        else:
            st.error(f"Error fetching history: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")


# Page: Settings
elif page == "⚙️ Settings":
    st.markdown('<div class="sub-header">Settings</div>', unsafe_allow_html=True)
    
    st.markdown("### Session Management")
    
    if st.button("Start New Session"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.chat_history = []
        st.success("New session started!")
    
    st.markdown("---")
    st.markdown("### API Configuration")
    st.markdown(f"**API URL:** {API_URL}")
    
    st.markdown("---")
    st.markdown("### System Status")
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            st.success("✅ Backend API is running")
        else:
            st.error("❌ Backend API is not responding correctly")
    except requests.exceptions.RequestException:
        st.error("❌ Cannot connect to Backend API")
        st.warning("Make sure the backend is running: `uvicorn backend.api.app:app --reload`")


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8rem;'>
    Customer Churn Intelligence Platform | Powered by CrewAI Multi-Agent System
</div>
""", unsafe_allow_html=True)
