# 🚀 Hướng dẫn Deploy lên Streamlit Cloud

## Bước 1: Chuẩn bị Repository

Đảm bảo code đã được push lên GitHub:
```bash
git add .
git commit -m "Prepare for Streamlit deployment"
git push
```

## Bước 2: Tạo file requirements.txt (Đã có sẵn)

File `requirements.txt` đã có trong project. Streamlit Cloud sẽ tự động cài đặt.

## Bước 3: Deploy lên Streamlit Cloud

### 3.1. Truy cập Streamlit Cloud

1. Vào: https://share.streamlit.io/
2. Đăng nhập bằng GitHub account
3. Click "New app"

### 3.2. Cấu hình App

- **Repository**: Chọn `Darkcom18/clickai_test`
- **Branch**: `main`
- **Main file path**: `main.py`
- **App URL**: Tự động tạo (ví dụ: `clickai-test.streamlit.app`)

### 3.3. Setup Secrets (Quan trọng!)

Click "Advanced settings" → "Secrets" và thêm các secrets sau:

```toml
DEEPSEEK_API_KEY = "sk-your-deepseek-key-here"
DEEPSEEK_API_BASE = "https://api.deepseek.com"

# Tùy chọn - chỉ thêm nếu cần
GITHUB_TOKEN = "ghp-your-token"
GITHUB_USERNAME = "Darkcom18"

N8N_WEBHOOK_BASE_URL = "https://your-n8n.com/webhook"
N8N_WEBHOOK_TOKEN = "your-token"

KAGGLE_USERNAME = "your-username"
KAGGLE_KEY = "your-key"

HUGGINGFACE_TOKEN = "hf-your-token"
```

**Lưu ý**: 
- Secrets được lưu an toàn và không hiển thị trong code
- Chỉ cần `DEEPSEEK_API_KEY` là có thể chạy được (Chat + ML agents)
- Các keys khác là tùy chọn

### 3.4. Deploy

Click "Deploy" và đợi build (thường 2-5 phút).

## Bước 4: Xử lý Google Drive (Nếu cần)

Google Drive cần `credentials.json` file, không thể setup qua secrets.

**Giải pháp:**

1. **Option 1**: Bỏ qua Drive agent (khuyến nghị cho deployment)
   - Drive agent sẽ tự động disable nếu không có credentials

2. **Option 2**: Upload credentials.json vào repo (không khuyến nghị vì security)
   - Thêm vào `.gitignore` nhưng có thể commit nếu cần
   - **Cảnh báo**: Không nên commit credentials vào public repo!

3. **Option 3**: Dùng Streamlit Secrets cho OAuth flow
   - Phức tạp hơn, cần custom code

## Bước 5: Kiểm tra sau khi Deploy

1. Truy cập URL app (ví dụ: `https://clickai-test.streamlit.app`)
2. Test Chat Agent: "What is machine learning?"
3. Test ML Agent: "Create a sample salary dataset"
4. Kiểm tra logs nếu có lỗi

## Troubleshooting

### Lỗi "DEEPSEEK_API_KEY is required"
→ Chưa thêm secret trong Streamlit Cloud. Vào Settings → Secrets và thêm.

### Lỗi "Module not found"
→ Kiểm tra `requirements.txt` đã có đủ packages chưa.

### Lỗi "GitHub/Drive/n8n not configured"
→ Không sao! Các agents này sẽ tự động disable. Bạn vẫn dùng được Chat và ML agents.

### App không load
→ Kiểm tra logs trong Streamlit Cloud dashboard.

## Tối ưu cho Production

1. **Environment Variables**: Dùng Streamlit Secrets thay vì file `.env`
2. **Error Handling**: Code đã có sẵn graceful handling cho missing configs
3. **Model Storage**: Models sẽ được lưu trong container (temporary)
   - Nếu cần persistent storage, dùng external storage (S3, etc.)

## Checklist trước khi Deploy

- [ ] Code đã push lên GitHub
- [ ] `requirements.txt` đã có đầy đủ
- [ ] `main.py` là entry point
- [ ] Đã thêm `DEEPSEEK_API_KEY` vào Streamlit Secrets
- [ ] (Tùy chọn) Đã thêm các secrets khác nếu cần
- [ ] Đã test local với `streamlit run main.py`

## Lưu ý quan trọng

1. **Secrets**: Không bao giờ commit API keys vào code!
2. **Google Drive**: Khó deploy vì cần file credentials.json
3. **Model Storage**: Models train trên Streamlit sẽ mất khi container restart
4. **Rate Limits**: Chú ý rate limits của DeepSeek API

## Alternative: Deploy với Docker

Nếu cần persistent storage hoặc custom setup, có thể deploy với Docker:

1. Tạo `Dockerfile`
2. Deploy lên Railway, Render, hoặc AWS
3. Setup environment variables tương tự

