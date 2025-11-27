# 🚀 Quick Start Guide

## Bước 1: Setup Environment (Bắt buộc)

### 1.1. Cài đặt DeepSeek API Key

**Bắt buộc** - Không có cái này thì không chạy được!

1. Lấy API key từ: https://platform.deepseek.com/
2. Mở file `.env` và thêm:
```env
DEEPSEEK_API_KEY=sk-your-key-here
```

Hoặc chạy script tự động:
```bash
python setup_env.py
```

### 1.2. Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

## Bước 2: Chạy ứng dụng

```bash
streamlit run main.py
```

Ứng dụng sẽ mở tại: http://localhost:8501

## Bước 3: Test các Agents

### ✅ Có thể dùng ngay (chỉ cần DeepSeek API):

1. **Chat Agent:**
   - "What is machine learning?"
   - "Explain LangGraph"

2. **ML Agent:**
   - "Create a sample salary dataset"
   - "Train a salary prediction model"
   - "Predict salary for 5 years experience"

### ⚙️ Cần setup thêm (tùy chọn):

3. **GitHub Agent** - Cần GitHub Token:
   - Xem SETUP.md phần "Setup GitHub"
   - Hoặc bỏ qua nếu không cần

4. **Drive Agent** - Cần Google Drive credentials:
   - Xem SETUP.md phần "Setup Google Drive"
   - Hoặc bỏ qua nếu không cần

5. **n8n Agent** - Cần n8n webhook URL:
   - Xem SETUP.md phần "Setup n8n"
   - Hoặc bỏ qua nếu không cần

## Checklist

- [ ] Đã có DeepSeek API key trong `.env`
- [ ] Đã cài đặt dependencies (`pip install -r requirements.txt`)
- [ ] Đã test chạy `streamlit run main.py`
- [ ] Đã test Chat Agent
- [ ] Đã test ML Agent (train model)
- [ ] (Tùy chọn) Setup GitHub token
- [ ] (Tùy chọn) Setup Google Drive
- [ ] (Tùy chọn) Setup n8n

## Troubleshooting

### Lỗi "DEEPSEEK_API_KEY is required"
→ Chưa thêm API key vào `.env`. Xem Bước 1.1

### Lỗi "Module not found"
→ Chưa cài dependencies. Chạy: `pip install -r requirements.txt`

### Lỗi "GitHub/Drive/n8n not configured"
→ Không sao! Các agents này là tùy chọn. Bạn vẫn dùng được Chat và ML agents.

## Next Steps

Sau khi chạy được cơ bản:
1. Thử train một ML model
2. Test các tính năng khác
3. Setup thêm GitHub/Drive/n8n nếu cần

