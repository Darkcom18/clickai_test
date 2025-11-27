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
        
        # Settings button
        if st.button("🔧 Settings", use_container_width=True):
            st.session_state.show_settings = not st.session_state.get("show_settings", False)
        
        # Settings panel
        if st.session_state.get("show_settings", False):
            st.divider()
            st.subheader("🔐 Credentials Settings")
            
            # Status indicators
            st.markdown("**Agent Status:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                github_status = "✅" if (st.session_state.get("user_GITHUB_TOKEN") or config.GITHUB_TOKEN) else "❌"
                st.markdown(f"GitHub: {github_status}")
            with col2:
                n8n_status = "✅" if (st.session_state.get("user_N8N_WEBHOOK_BASE_URL") or config.N8N_WEBHOOK_BASE_URL) else "❌"
                st.markdown(f"n8n: {n8n_status}")
            with col3:
                drive_status = "⚠️"  # Complex setup
                st.markdown(f"Drive: {drive_status}")
            
            with st.expander("GitHub", expanded=False):
                st.markdown("""
                **How to get GitHub Token:**
                1. Go to: https://github.com/settings/tokens
                2. Click "Generate new token" → "Generate new token (classic)"
                3. Select scopes: `repo` (full control)
                4. Copy token and paste below
                """)
                github_token = st.text_input(
                    "GitHub Token",
                    value=st.session_state.get("user_GITHUB_TOKEN", config.GITHUB_TOKEN or ""),
                    type="password",
                    help="Get token from: https://github.com/settings/tokens"
                )
                github_username = st.text_input(
                    "GitHub Username",
                    value=st.session_state.get("user_GITHUB_USERNAME", config.GITHUB_USERNAME or ""),
                    help="Your GitHub username"
                )
                if st.button("💾 Save GitHub", use_container_width=True):
                    st.session_state.user_GITHUB_TOKEN = github_token
                    st.session_state.user_GITHUB_USERNAME = github_username
                    # Force reload by clearing cache
                    import mcp_servers.github_mcp as github_mcp_module
                    github_mcp_module._github_mcp = None
                    github_mcp_module._last_github_token = None
                    st.success("GitHub credentials saved! Try using GitHub agent now.")
                    st.rerun()
            
            with st.expander("n8n Webhook", expanded=False):
                st.markdown("""
                **How to get n8n Webhook URL:**
                1. Open your n8n workflow
                2. Add a "Webhook" node
                3. Copy the webhook URL (e.g., `https://your-n8n.com/webhook/abc123`)
                4. Paste below
                """)
                n8n_url = st.text_input(
                    "n8n Webhook URL",
                    value=st.session_state.get("user_N8N_WEBHOOK_BASE_URL", config.N8N_WEBHOOK_BASE_URL or ""),
                    help="Example: https://your-n8n.com/webhook/abc123",
                    placeholder="https://your-n8n.com/webhook/..."
                )
                n8n_token = st.text_input(
                    "n8n Token (optional)",
                    value=st.session_state.get("user_N8N_WEBHOOK_TOKEN", config.N8N_WEBHOOK_TOKEN or ""),
                    type="password",
                    help="Optional authentication token"
                )
                if st.button("💾 Save n8n", use_container_width=True):
                    st.session_state.user_N8N_WEBHOOK_BASE_URL = n8n_url
                    st.session_state.user_N8N_WEBHOOK_TOKEN = n8n_token
                    # Force reload by clearing cache
                    import mcp_servers.n8n_mcp as n8n_mcp_module
                    n8n_mcp_module._n8n_mcp = None
                    n8n_mcp_module._last_n8n_url = None
                    st.success("n8n credentials saved! Try using n8n agent now.")
                    st.rerun()
            
            with st.expander("Google Drive", expanded=False):
                st.markdown("""
                **Google Drive OAuth Setup:**
                
                Google Drive cần OAuth flow phức tạp. Có 2 cách:
                """)
                
                st.markdown("""
                **Cách 1: Setup Local (Khuyến nghị)**
                1. Download `credentials.json` từ Google Cloud Console
                2. Đặt vào thư mục project
                3. Chạy: `python setup_drive_oauth.py`
                4. Browser sẽ mở để authorize
                5. Token sẽ được lưu vào `token.json`
                
                **Cách 2: Upload credentials.json (Temporary)**
                - Upload file credentials.json
                - ⚠️ Lưu ý: Trong Streamlit Cloud, file chỉ tồn tại trong session
                """)
                
                uploaded_file = st.file_uploader(
                    "Upload credentials.json",
                    type=["json"],
                    help="Upload your Google Drive credentials.json file"
                )
                if uploaded_file is not None:
                    import json
                    try:
                        creds_data = json.load(uploaded_file)
                        st.success("✅ File credentials.json đã được upload!")
                        st.info("⚠️ Lưu ý: File này chỉ tồn tại trong session hiện tại.")
                        st.json(creds_data)
                        st.markdown("""
                        **Tiếp theo:**
                        - File đã được nhận nhưng cần authorize để lấy token
                        - Chạy `python setup_drive_oauth.py` local để authorize
                        - Hoặc xem hướng dẫn trong SETUP.md
                        """)
                    except Exception as e:
                        st.error(f"❌ Lỗi đọc file: {str(e)}")
                
                st.markdown("---")
                st.markdown("""
                **Quick Helper:**
                - Chạy `python oauth_helper.py` để được hướng dẫn chi tiết
                - Hoặc `python get_github_token.py` để lấy GitHub token nhanh
                """)
            
            with st.expander("Clear All Settings", expanded=False):
                st.warning("This will clear all user-entered credentials from this session.")
                if st.button("🗑️ Clear All", use_container_width=True):
                    keys_to_clear = [
                        "user_GITHUB_TOKEN", "user_GITHUB_USERNAME",
                        "user_N8N_WEBHOOK_BASE_URL", "user_N8N_WEBHOOK_TOKEN"
                    ]
                    for key in keys_to_clear:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.success("Settings cleared!")
                    st.rerun()
            
            st.divider()
        
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

