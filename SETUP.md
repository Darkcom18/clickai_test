# Hướng dẫn Setup

## 1. Setup DeepSeek API (Bắt buộc)

DeepSeek API key là bắt buộc để hệ thống hoạt động.

1. Lấy API key từ: https://platform.deepseek.com/
2. Thêm vào file `.env`:
```env
DEEPSEEK_API_KEY=sk-your-key-here
```

## 2. Setup GitHub (Tùy chọn)

Nếu muốn sử dụng GitHub agent:

### Cách lấy GitHub Token:

1. Vào GitHub: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Đặt tên token (ví dụ: "Multi-Agent System")
4. Chọn scopes:
   - `repo` (full control) - để tạo repo, files, issues
   - `read:user` - để đọc thông tin user
5. Click "Generate token"
6. **Copy token ngay** (chỉ hiện 1 lần!)

### Thêm vào .env:
```env
GITHUB_TOKEN=ghp_your-token-here
GITHUB_USERNAME=your-username
```

**Lưu ý**: Nếu không có token, GitHub agent sẽ không hoạt động nhưng các agents khác vẫn chạy bình thường.

## 3. Setup Google Drive (Tùy chọn)

Nếu muốn sử dụng Drive agent:

### Bước 1: Tạo Google Cloud Project

1. Vào: https://console.cloud.google.com/
2. Tạo project mới hoặc chọn project có sẵn
3. Enable "Google Drive API":
   - Vào "APIs & Services" → "Library"
   - Tìm "Google Drive API"
   - Click "Enable"

### Bước 2: Tạo OAuth Credentials

1. Vào "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Nếu chưa có OAuth consent screen:
   - Chọn "External" → "Create"
   - Điền thông tin cơ bản
   - Save và Continue
4. Application type: Chọn "Desktop app"
5. Đặt tên (ví dụ: "Multi-Agent Drive")
6. Click "Create"
7. Download JSON file → đổi tên thành `credentials.json`
8. Đặt file vào thư mục gốc của project

### Bước 3: Chạy lần đầu

Khi chạy lần đầu, sẽ mở browser để authorize:
- Chọn Google account
- Cho phép quyền truy cập
- Token sẽ được lưu tự động vào `token.json`

**Lưu ý**: Nếu không setup, Drive agent sẽ không hoạt động nhưng các agents khác vẫn chạy bình thường.

## 4. Setup n8n (Tùy chọn)

Nếu muốn sử dụng n8n agent:

1. Có n8n instance đang chạy (local hoặc cloud)
2. Tạo webhook workflow trong n8n
3. Lấy webhook URL (ví dụ: `https://your-n8n.com/webhook/abc123`)
4. Thêm vào `.env`:
```env
N8N_WEBHOOK_BASE_URL=https://your-n8n.com/webhook
N8N_WEBHOOK_TOKEN=your-token-if-needed
```

**Lưu ý**: Nếu không có, n8n agent sẽ không hoạt động nhưng các agents khác vẫn chạy bình thường.

## 5. Setup ML Models (Tự động)

ML agent không cần setup đặc biệt, nhưng có thể cấu hình:

### Kaggle (Tùy chọn - để tìm dataset):
1. Vào: https://www.kaggle.com/settings
2. Scroll xuống "API" section
3. Click "Create New Token" → download `kaggle.json`
4. Extract username và key từ file JSON
5. Thêm vào `.env`:
```env
KAGGLE_USERNAME=your-username
KAGGLE_KEY=your-key
```

### HuggingFace (Tùy chọn):
1. Vào: https://huggingface.co/settings/tokens
2. Tạo token mới
3. Thêm vào `.env`:
```env
HUGGINGFACE_TOKEN=hf_your-token
```

## Tóm tắt file .env tối thiểu:

```env
# Bắt buộc
DEEPSEEK_API_KEY=sk-your-key-here

# Tùy chọn - chỉ thêm nếu muốn dùng
GITHUB_TOKEN=ghp_your-token
GITHUB_USERNAME=your-username

# Tùy chọn - chỉ thêm nếu muốn dùng
N8N_WEBHOOK_BASE_URL=https://your-n8n.com/webhook
N8N_WEBHOOK_TOKEN=your-token

# Tùy chọn - cho ML dataset discovery
KAGGLE_USERNAME=your-username
KAGGLE_KEY=your-key
HUGGINGFACE_TOKEN=hf_your-token
```

## Test sau khi setup:

1. **Chat Agent** (không cần token): Luôn hoạt động
2. **ML Agent** (không cần token): Có thể train model với sample data
3. **GitHub Agent**: Cần `GITHUB_TOKEN`
4. **Drive Agent**: Cần `credentials.json`
5. **n8n Agent**: Cần `N8N_WEBHOOK_BASE_URL`

## Troubleshooting

### Lỗi "GITHUB_TOKEN is required"
→ GitHub agent không được cấu hình. Bạn vẫn có thể dùng Chat và ML agents.

### Lỗi "Credentials file not found"
→ Google Drive chưa được setup. Bạn vẫn có thể dùng các agents khác.

### Lỗi "N8N_WEBHOOK_BASE_URL is required"
→ n8n chưa được cấu hình. Bạn vẫn có thể dùng các agents khác.

**Quan trọng**: Chỉ cần DeepSeek API key là có thể chạy được Chat và ML agents!

