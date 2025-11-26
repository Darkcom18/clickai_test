"""Streamlit UI for Multi-Agent System."""

import streamlit as st
from orchestrator.graph import process_query
from utils.config import config

# Page config
st.set_page_config(
    page_title="Multi-Agent System",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "config_validated" not in st.session_state:
    try:
        config.validate()
        config.ensure_model_storage()
        st.session_state.config_validated = True
    except Exception as e:
        st.session_state.config_validated = False
        st.session_state.config_error = str(e)


def main():
    """Main Streamlit app."""
    
    st.title("🤖 Multi-Agent System")
    st.markdown("Hệ thống multi-agent với DeepSeek, GitHub, Drive, n8n, và ML models")
    
    # Check configuration
    if not st.session_state.config_validated:
        st.error(f"⚠️ Configuration Error: {st.session_state.config_error}")
        st.info("Vui lòng kiểm tra file .env và đảm bảo DEEPSEEK_API_KEY được cấu hình.")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.info("✅ Configuration valid")
        
        st.header("📋 Available Agents")
        st.markdown("""
        - **Chat Agent**: Trả lời câu hỏi đơn giản
        - **GitHub Agent**: Thao tác với GitHub
        - **Drive Agent**: Thao tác với Google Drive
        - **n8n Agent**: Trigger workflows
        - **ML Agent**: Train và predict với ML models
        """)
        
        st.header("💡 Examples")
        st.markdown("""
        **Chat:**
        - "What is machine learning?"
        
        **GitHub:**
        - "List my repositories"
        - "Create a new repo called test-project"
        
        **Drive:**
        - "List files in my Drive"
        - "Upload file.txt to Drive"
        
        **n8n:**
        - "Trigger workflow abc123"
        
        **ML:**
        - "Train a salary prediction model"
        - "Predict salary for 5 years experience"
        """)
    
    # Chat interface
    st.header("💬 Chat")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "agent_used" in message:
                st.caption(f"Agent: {message['agent_used']}")
    
    # Chat input
    if prompt := st.chat_input("Nhập câu hỏi hoặc yêu cầu của bạn..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process query
        with st.chat_message("assistant"):
            with st.spinner("Đang xử lý..."):
                try:
                    result = process_query(prompt)
                    
                    # Display result
                    response = result.get("result", "No response")
                    agent_used = result.get("agent_used", "unknown")
                    success = result.get("success", False)
                    
                    st.markdown(response)
                    st.caption(f"Agent: {agent_used} | Success: {success}")
                    
                    # Add to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "agent_used": agent_used,
                        "success": success,
                    })
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg,
                        "agent_used": "error",
                        "success": False,
                    })
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


if __name__ == "__main__":
    main()

