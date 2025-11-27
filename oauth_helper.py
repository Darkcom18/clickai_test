"""OAuth Helper Tool - Run this locally to get tokens for GitHub/Google Drive."""

import os
import sys
from pathlib import Path

def github_oauth_helper():
    """Helper to guide user through GitHub OAuth."""
    print("\n" + "="*60)
    print("🔐 GitHub OAuth Helper")
    print("="*60)
    print("\nCó 2 cách để lấy GitHub token:\n")
    
    print("CÁCH 1: Personal Access Token (Đơn giản nhất)")
    print("-" * 60)
    print("1. Vào: https://github.com/settings/tokens")
    print("2. Click 'Generate new token' → 'Generate new token (classic)'")
    print("3. Đặt tên: 'Multi-Agent System'")
    print("4. Chọn scopes:")
    print("   ✅ repo (full control)")
    print("   ✅ read:user")
    print("5. Click 'Generate token'")
    print("6. COPY TOKEN NGAY (chỉ hiện 1 lần!)")
    print("\nToken sẽ có dạng: ghp_xxxxxxxxxxxxxxxxxxxx")
    
    print("\n" + "-" * 60)
    print("CÁCH 2: GitHub OAuth App (Nâng cao)")
    print("-" * 60)
    print("1. Vào: https://github.com/settings/developers")
    print("2. Click 'New OAuth App'")
    print("3. Điền thông tin:")
    print("   - Application name: Multi-Agent System")
    print("   - Homepage URL: https://your-app.streamlit.app")
    print("   - Authorization callback URL: https://your-app.streamlit.app")
    print("4. Click 'Register application'")
    print("5. Copy Client ID và Client Secret")
    print("6. Tạo authorization URL và lấy token")
    print("\n⚠️  Lưu ý: OAuth App phức tạp hơn, khuyến nghị dùng Cách 1")
    
    print("\n" + "="*60)
    token = input("\nNhập GitHub token của bạn (hoặc Enter để bỏ qua): ").strip()
    
    if token:
        print(f"\n✅ Token đã nhận: {token[:10]}...")
        print("\nBạn có thể:")
        print("1. Copy token này vào Streamlit app (Settings → GitHub)")
        print("2. Hoặc thêm vào .env file: GITHUB_TOKEN=your-token")
        return token
    else:
        print("\n⚠️  Bỏ qua. Bạn có thể thêm token sau trong Streamlit app.")
        return None


def google_drive_oauth_helper():
    """Helper to guide user through Google Drive OAuth."""
    print("\n" + "="*60)
    print("🔐 Google Drive OAuth Helper")
    print("="*60)
    print("\nGoogle Drive cần OAuth flow phức tạp hơn.\n")
    
    print("BƯỚC 1: Tạo Google Cloud Project")
    print("-" * 60)
    print("1. Vào: https://console.cloud.google.com/")
    print("2. Tạo project mới hoặc chọn project có sẵn")
    print("3. Enable 'Google Drive API':")
    print("   - Vào 'APIs & Services' → 'Library'")
    print("   - Tìm 'Google Drive API'")
    print("   - Click 'Enable'")
    
    print("\nBƯỚC 2: Tạo OAuth Credentials")
    print("-" * 60)
    print("1. Vào 'APIs & Services' → 'Credentials'")
    print("2. Click 'Create Credentials' → 'OAuth client ID'")
    print("3. Nếu chưa có OAuth consent screen:")
    print("   - Chọn 'External' → 'Create'")
    print("   - Điền thông tin cơ bản")
    print("   - Save và Continue")
    print("4. Application type: Chọn 'Desktop app'")
    print("5. Đặt tên: 'Multi-Agent Drive'")
    print("6. Click 'Create'")
    print("7. Download JSON file → đổi tên thành 'credentials.json'")
    
    print("\nBƯỚC 3: Authorize và lấy token")
    print("-" * 60)
    print("1. Đặt file 'credentials.json' vào thư mục project")
    print("2. Chạy script này để authorize:")
    print("   python -c \"from mcp_servers.drive_mcp import get_drive_mcp; get_drive_mcp()\"")
    print("3. Browser sẽ mở để bạn authorize")
    print("4. Token sẽ được lưu vào 'token.json'")
    
    print("\n" + "="*60)
    creds_file = input("\nĐường dẫn đến credentials.json (hoặc Enter để bỏ qua): ").strip()
    
    if creds_file and Path(creds_file).exists():
        print(f"\n✅ Tìm thấy credentials.json")
        print("\nBây giờ chạy lệnh sau để authorize:")
        print(f"   python -c \"import sys; sys.path.insert(0, '.'); from mcp_servers.drive_mcp import get_drive_mcp; get_drive_mcp()\"")
        return creds_file
    else:
        print("\n⚠️  Bỏ qua. Bạn có thể setup sau.")
        return None


def main():
    """Main OAuth helper."""
    print("\n" + "="*60)
    print("🔐 OAuth Helper Tool")
    print("="*60)
    print("\nTool này giúp bạn lấy tokens cho GitHub và Google Drive.")
    print("Tokens có thể được dùng trong Streamlit app.\n")
    
    print("Chọn service:")
    print("1. GitHub")
    print("2. Google Drive")
    print("3. Cả hai")
    print("4. Thoát")
    
    choice = input("\nLựa chọn (1-4): ").strip()
    
    results = {}
    
    if choice == "1" or choice == "3":
        results['github'] = github_oauth_helper()
    
    if choice == "2" or choice == "3":
        results['drive'] = google_drive_oauth_helper()
    
    if choice == "4":
        print("\n👋 Tạm biệt!")
        return
    
    # Summary
    print("\n" + "="*60)
    print("📋 Tóm tắt")
    print("="*60)
    
    if results.get('github'):
        print(f"\n✅ GitHub Token: {results['github'][:10]}...")
        print("   → Copy vào Streamlit app (Settings → GitHub)")
    
    if results.get('drive'):
        print(f"\n✅ Google Drive: {results['drive']}")
        print("   → Chạy authorize script để lấy token.json")
    
    print("\n💡 Tip: Bạn có thể nhập tokens trực tiếp trong Streamlit app")
    print("   (Click nút '🔧 Settings' trong sidebar)")


if __name__ == "__main__":
    main()

