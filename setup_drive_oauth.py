"""Setup Google Drive OAuth - Run this to authorize and get token.json."""

from pathlib import Path
from mcp_servers.drive_mcp import get_drive_mcp
from utils.config import config

def main():
    """Setup Google Drive OAuth."""
    print("\n" + "="*60)
    print("🔐 Google Drive OAuth Setup")
    print("="*60)
    
    creds_file = Path(config.GOOGLE_DRIVE_CREDENTIALS_FILE)
    
    if not creds_file.exists():
        print(f"\n❌ Không tìm thấy file: {creds_file}")
        print("\n📋 Hướng dẫn:")
        print("1. Vào: https://console.cloud.google.com/")
        print("2. Tạo OAuth credentials (Desktop app)")
        print("3. Download JSON file")
        print(f"4. Đổi tên thành '{creds_file}' và đặt vào thư mục project")
        print("\nXem SETUP.md để biết chi tiết.")
        return
    
    print(f"\n✅ Tìm thấy credentials.json")
    print("\n🔄 Đang khởi tạo OAuth flow...")
    print("   (Browser sẽ mở để bạn authorize)")
    
    try:
        # This will trigger OAuth flow
        drive_mcp = get_drive_mcp()
        
        if drive_mcp.initialized:
            print("\n✅ Google Drive đã được authorize thành công!")
            print(f"   Token đã được lưu vào: {config.GOOGLE_DRIVE_TOKEN_FILE}")
            print("\n💡 Bây giờ bạn có thể dùng Drive agent trong Streamlit app.")
        else:
            print("\n⚠️  Authorization không thành công.")
            print("   Kiểm tra lại credentials.json và thử lại.")
    
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        print("\n💡 Tips:")
        print("   - Đảm bảo credentials.json đúng format")
        print("   - Kiểm tra Google Cloud Console đã enable Drive API")
        print("   - Thử chạy lại script này")


if __name__ == "__main__":
    main()

