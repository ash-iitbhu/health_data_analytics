import streamlit as st
import requests
import json
import pandas as pd
import os

API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="GenAI Health Analyst",
    layout="wide"
)
with st.sidebar:
    st.title("🏥 Health Analytics System")
    st.markdown("---")
    st.subheader("Available Datasets")
    with st.expander("View Data Schema"):
        st.markdown("""
        **Dataset 1: Health Metrics**
        - `Blood_Pressure_Abnormality`: 0/1
        - `BMI`, `Age`, `Hemoglobin`, `Stress`
        - `Chronic_kidney_disease`: 0/1
        
        **Dataset 2: Activity (Longitudinal)**
        - `Physical_activity` (steps)
        - `Day_Number` (1-10)
        """)

st.title("🧬 Intelligent Health Data Analyst")
st.markdown(
    """
    Ask complex questions about patient demographics, lifestyle factors, and disease outcomes. 
    *The system performs real-time statistical analysis on the fly.*
    """
)

#sample queries
sample_queries = [
    "How many people who smoke have chronic kidney disease?",
    "What is the correlation between BMI and Stress Level?",
    "Does physical activity in the last 10 days differ for patients with Kidney Disease?"
]

query = st.text_area("Enter your analytical question:", height=100, placeholder="e.g., " + sample_queries[0])

cols = st.columns(len(sample_queries))

if st.button("🔍 Analyze Data", type="primary"):
    if not query:
        st.warning("Please enter a question first.")
    else:
        st.markdown(f"**running analysis for:** _{query}_")
        
        status_container = st.empty()
        
        try:
            with st.spinner("Orchestrating Agents..."):
                payload = {"query": query}
                FULL_URL = f"{API_URL}/analyze"
                response = requests.post(FULL_URL, json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    final_answer = result.get("response", "No response provided.")
                    trace_logs = result.get("trace", [])
                    
                    st.success("### Analysis Result")
                    st.markdown(final_answer)
                    
                    with st.expander("🛠️ View Agent 'Thought Process' & Code Execution"):
                        for log in trace_logs:
                            if "Data_Analyst" in log:
                                st.markdown(f"**👨‍💻 Analyst:**")
                                st.code(log.replace("Data_Analyst:", "").strip())
                            elif "Supervisor" in log:
                                st.markdown(f"**👮 Supervisor:** {log.replace('Supervisor:', '').strip()}")
                            elif "Tool" in log:
                                st.markdown(f"**⚙️ Tool Output:**")
                                st.caption(log)
                            else:
                                st.text(log)
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
                    
        except requests.exceptions.ConnectionError:
            st.error("🚨 Connection Error: Ensure the FastAPI backend is running on port 8000.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

st.markdown("---")
st.caption("POC Implementation | Powered by LangChain, LangGraph, FastAPI & Grok")