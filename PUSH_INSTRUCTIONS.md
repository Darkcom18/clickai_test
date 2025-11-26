# Hướng dẫn Push Code lên GitHub

## Vấn đề
Git đang dùng account `gavin-ancileo` nhưng repo là của `Darkcom18`, nên bị lỗi permission.

## Giải pháp

### Cách 1: Dùng Personal Access Token (Khuyến nghị)

1. **Tạo Personal Access Token:**
   - Vào: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Đặt tên: "clickai_test"
   - Chọn scopes: `repo` (full control)
   - Click "Generate token"
   - **Copy token ngay** (chỉ hiện 1 lần!)

2. **Push với token:**
```bash
git remote set-url origin https://YOUR_TOKEN@github.com/Darkcom18/clickai_test.git
git push -u origin main
```

Hoặc khi push, nhập username là `Darkcom18` và password là token.

### Cách 2: Dùng SSH (Nếu đã setup SSH key)

1. **Đổi remote sang SSH:**
```bash
git remote set-url origin git@github.com:Darkcom18/clickai_test.git
git push -u origin main
```

### Cách 3: Dùng GitHub CLI

```bash
gh auth login
git push -u origin main
```

## Kiểm tra

Sau khi push thành công, kiểm tra tại:
https://github.com/Darkcom18/clickai_test

