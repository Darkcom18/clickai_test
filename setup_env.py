"""Script to setup .env file."""

import os
from pathlib import Path

def setup_env():
    """Setup .env file from user input."""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("⚠️  File .env đã tồn tại!")
        overwrite = input("Bạn có muốn ghi đè không? (y/n): ")
        if overwrite.lower() != 'y':
            print("Hủy bỏ.")
            return
    
    print("\n=== Setup .env file ===\n")
    print("Nhập các thông tin sau (Enter để bỏ qua):\n")
    
    # DeepSeek API Key (required)
    deepseek_key = input("DeepSeek API Key (BẮT BUỘC): ").strip()
    if not deepseek_key:
        print("❌ DeepSeek API Key là bắt buộc!")
        return
    
    # Optional configs
    github_token = input("GitHub Token (tùy chọn): ").strip()
    github_username = input("GitHub Username (tùy chọn): ").strip()
    n8n_url = input("n8n Webhook URL (tùy chọn): ").strip()
    n8n_token = input("n8n Webhook Token (tùy chọn): ").strip()
    kaggle_username = input("Kaggle Username (tùy chọn): ").strip()
    kaggle_key = input("Kaggle Key (tùy chọn): ").strip()
    hf_token = input("HuggingFace Token (tùy chọn): ").strip()
    
    # Read template
    template = ""
    if env_example.exists():
        with open(env_example, 'r', encoding='utf-8') as f:
            template = f.read()
    
    # Create .env content
    env_content = f"""# DeepSeek API Key
DEEPSEEK_API_KEY={deepseek_key}

# DeepSeek API Base URL
DEEPSEEK_API_BASE=https://api.deepseek.com

"""
    
    if github_token:
        env_content += f"""# GitHub Configuration
GITHUB_TOKEN={github_token}
GITHUB_USERNAME={github_username or ''}

"""
    
    if n8n_url:
        env_content += f"""# n8n Webhook Configuration
N8N_WEBHOOK_BASE_URL={n8n_url}
N8N_WEBHOOK_TOKEN={n8n_token or ''}

"""
    
    if kaggle_username:
        env_content += f"""# Kaggle API
KAGGLE_USERNAME={kaggle_username}
KAGGLE_KEY={kaggle_key or ''}

"""
    
    if hf_token:
        env_content += f"""# HuggingFace API
HUGGINGFACE_TOKEN={hf_token}

"""
    
    env_content += """# Google Drive Configuration (cần download credentials.json từ Google Cloud Console)
GOOGLE_DRIVE_CREDENTIALS_FILE=credentials.json
GOOGLE_DRIVE_TOKEN_FILE=token.json

# Model Storage
MODEL_STORAGE_PATH=ml_models/models
"""
    
    # Write .env file
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print(f"\n✅ Đã tạo file .env thành công!")
    print(f"\n📝 Lưu ý:")
    print("   - Chat Agent và ML Agent có thể chạy ngay")
    print("   - GitHub/Drive/n8n agents cần setup thêm (xem SETUP.md)")
    print("   - Google Drive cần download credentials.json từ Google Cloud Console")

if __name__ == "__main__":
    setup_env()

