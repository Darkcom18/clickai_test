"""Quick script to get GitHub token via OAuth or guide user."""

import webbrowser
import urllib.parse

def open_github_token_page():
    """Open GitHub token creation page."""
    url = "https://github.com/settings/tokens/new"
    print("🌐 Đang mở trang tạo GitHub token...")
    webbrowser.open(url)
    print("\n📋 Hướng dẫn:")
    print("1. Đặt tên token: 'Multi-Agent System'")
    print("2. Chọn expiration: 90 days hoặc No expiration")
    print("3. Chọn scopes:")
    print("   ✅ repo (full control)")
    print("   ✅ read:user")
    print("4. Click 'Generate token'")
    print("5. COPY TOKEN và paste vào đây:\n")
    
    token = input("GitHub Token: ").strip()
    
    if token:
        print(f"\n✅ Token đã nhận: {token[:10]}...")
        print("\nBạn có thể:")
        print(f"1. Copy token này: {token}")
        print("2. Vào Streamlit app → Settings → GitHub → Paste token")
        print("3. Hoặc thêm vào .env: GITHUB_TOKEN=your-token")
        return token
    else:
        print("\n⚠️  Không có token. Bạn có thể thêm sau.")
        return None


if __name__ == "__main__":
    token = open_github_token_page()
    if token:
        print(f"\n💾 Token của bạn: {token}")
        print("   (Lưu ý: Token này chỉ hiện 1 lần, hãy lưu lại!)")

