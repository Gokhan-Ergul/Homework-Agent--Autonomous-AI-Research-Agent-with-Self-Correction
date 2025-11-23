import streamlit as st
import requests
import os
import json

st.set_page_config(page_title="AI Research Agent", page_icon="🤖", layout="wide")
st.title("🤖 Autonomous AI Research Assistant")

st.markdown("""
<style>
    .agent-box {
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 18px;
        border: 2px solid #444;
        background-color: #1E1E1E;
        color: #B0BEC5;
        transition: all 0.3s ease;
        position: relative;
        z-index: 2;
    }
    
    .active {
        background-color: #2E7D32;
        border-color: #69F0AE;
        color: white;
        box-shadow: 0 0 15px rgba(0, 230, 118, 0.6);
        transform: scale(1.05);
    }

    .sub-badge {
        margin-top: 10px;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        background-color: #37474F;
        color: #90A4AE;
        display: none;
        border: 1px dashed #546E7A;
        margin-left: auto;
        margin-right: auto;
        width: 80%;
    }

    .sub-active {
        display: block !important;
        background-color: #FF6F00;
        color: white;
        border: 1px solid #FFD180;
        box-shadow: 0 0 10px rgba(255, 167, 38, 0.6);
        animation: pulse 1.5s infinite;
    }

    .connector {
        height: 15px;
        width: 2px;
        background-color: #546E7A;
        margin: 0 auto;
        display: none;
    }
    .connector-active {
        display: block;
        background-color: #FFD180;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000/agent/events/start-research-stream"

def render_agents(current_node_name=None):
    node = str(current_node_name).lower().strip() if current_node_name else ""

    active_main_box = None
    active_sub_process = None

    if node == "researcher":
        active_main_box = "researcher"
    
    elif node == "run_tools":
        active_main_box = "researcher"
        active_sub_process = "Tools are running" 
        
    elif node == "compile_research":
        active_main_box = "researcher"
        active_sub_process = "Compiling the Text"

    elif node == "writer":
        active_main_box = "writer"
        
    elif node == "update_counter": 
        active_main_box = "writer"

    elif node == "controller":
        active_main_box = "controller"
        
    elif node == "formatter":
        active_main_box = "formatter"

    cols = st.columns(4)
    
    with cols[0]:
        is_active = "active" if active_main_box == "researcher" else ""
        
        tools_cls = "sub-active" if active_sub_process == "Tools are running" else ""
        tools_conn = "connector-active" if active_sub_process == "Tools are running" else ""
        
        comp_cls = "sub-active" if active_sub_process == "Compiling the Text" else ""
        comp_conn = "connector-active" if active_sub_process == "Compiling the Text" else ""

        st.markdown(f"""
            <div class="agent-box {is_active}">🔍 Researcher</div>
            
            <div class="connector {tools_conn}"></div>
            <div class="sub-badge {tools_cls}">🛠️ Running Tools</div>
            
            <div class="connector {comp_conn}"></div>
            <div class="sub-badge {comp_cls}">📑 Compiling</div>
        """, unsafe_allow_html=True)

    with cols[1]:
        is_active = "active" if active_main_box == "writer" else ""
        st.markdown(f"""<div class="agent-box {is_active}">✍️ Writer</div>""", unsafe_allow_html=True)

    with cols[2]:
        is_active = "active" if active_main_box == "controller" else ""
        st.markdown(f"""<div class="agent-box {is_active}">⚖️ Controller</div>""", unsafe_allow_html=True)

    with cols[3]:
        is_active = "active" if active_main_box == "formatter" else ""
        st.markdown(f"""<div class="agent-box {is_active}">📄 Formatter</div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    topic = st.text_area("Research Topic:", placeholder="E.g. The impact of AI on Healthcare...", height=250)
agent_placeholder = st.empty()

with agent_placeholder:
    render_agents(None)

if st.button("Start Research 🚀", type="primary"):
    if not topic:
        st.warning("Please enter a topic.")
    else:
        log_container = st.expander("Detailed Logs", expanded=True)
        
        try:
            payload = {"topic": topic}
            response = requests.post(API_URL, json=payload, stream=True)
            
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        
                        if "current_agent" in data:
                            agent_name = data["current_agent"]
                            
                            log_container.write(f"⚙️ Node: `{agent_name}`")
                            
                            with agent_placeholder:
                                render_agents(agent_name)
                        
                        if "status" in data and data["status"] == "completed":
                            st.success("✅ Research Completed Successfully!")
                            
                            with agent_placeholder:
                                render_agents("DONE") 
                            
                            raw_path = data.get('file_path') 
                            
                            clean_path = raw_path.replace("output/", "").replace("output\\", "")
                            
                            final_path = os.path.join("app", clean_path)
                            
                            if os.path.exists(final_path):
                                st.balloons() 
                                
                                with open(final_path, "rb") as file:
                                    st.download_button(
                                        label="📥 Download Report (.docx)",
                                        data=file,
                                        file_name=os.path.basename(final_path),
                                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                    )
                                
                                st.code(f"File saved locally at: {final_path}")
                            else:
                                st.error(f"🚨 File path returned ({final_path}), but file not found.")
                                st.warning("Hint: Check 'homework_agent/app/output' folder.")
                        
                    except json.JSONDecodeError:
                        continue
                        
        except Exception as e:
            st.error(f"Error: {e}")