# Multi-Agent System với DeepSeek

Hệ thống multi-agent sử dụng DeepSeek API, LangChain/LangGraph để điều phối các agents chuyên biệt cho GitHub, Google Drive, n8n, và Machine Learning.

## 🎯 Tính năng

- **Chat Agent**: Trả lời câu hỏi đơn giản
- **GitHub Agent**: Thao tác với GitHub (list repos, create repo, create files, etc.)
- **Drive Agent**: Thao tác với Google Drive (upload, download, list files, etc.)
- **n8n Agent**: Trigger workflows qua webhook
- **ML Agent**: Tự động tìm dataset, train model, và predict (ví dụ: dự đoán lương)

## 🏗️ Kiến trúc

```
User Query
    ↓
Orchestrator (LangGraph) - Routing logic
    ↓
Agents (LangChain) - Specialized agents
    ↓
MCP Servers - External service integrations
    ↓
External APIs (GitHub/Drive/n8n/ML)
```

## 📋 Yêu cầu

- Python 3.9+
- DeepSeek API key
- (Optional) GitHub token, Google Drive credentials, n8n webhook URL

## 🚀 Cài đặt

1. **Clone repository:**
```bash
git clone <repository-url>
cd clickai
```

2. **Tạo virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows
```

3. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

4. **Cấu hình environment variables:**

**Cách 1: Dùng script tự động (khuyến nghị):**
```bash
python setup_env.py
```

**Cách 2: Tạo thủ công:**
```bash
cp env.example .env
# Chỉnh sửa file .env và thêm API keys
```

**Xem [SETUP.md](SETUP.md) để biết cách lấy tokens.**

**Tối thiểu chỉ cần DeepSeek API key:**
```env
DEEPSEEK_API_KEY=sk-your-deepseek-api-key-here
```

Các tokens khác (GitHub, Drive, n8n) là tùy chọn - xem SETUP.md để biết cách setup.

5. **Setup Google Drive (nếu cần):**
- Tải credentials.json từ Google Cloud Console
- Đặt vào thư mục gốc của project
- Chạy lần đầu sẽ tự động tạo token.json

## 🎮 Sử dụng

### Chạy Streamlit UI:
```bash
streamlit run main.py
```

### Sử dụng trong code:
```python
from orchestrator.graph import process_query

result = process_query("List my GitHub repositories")
print(result)
```

## 🔐 OAuth & Credentials Setup

### Quick OAuth Helpers

**GitHub Token:**
```bash
python get_github_token.py
```
Script này sẽ mở browser và hướng dẫn bạn lấy GitHub token.

**Google Drive OAuth:**
```bash
python setup_drive_oauth.py
```
Script này sẽ giúp bạn authorize Google Drive và lấy token.json.

**OAuth Helper (Tất cả services):**
```bash
python oauth_helper.py
```
Interactive tool để hướng dẫn setup cho tất cả services.

### Hoặc nhập trực tiếp trong Streamlit App

1. Mở Streamlit app
2. Click nút **"🔧 Settings"** trong sidebar
3. Nhập GitHub token hoặc n8n webhook URL
4. Click **"💾 Save"**

## 📖 Ví dụ sử dụng

### Chat Agent
```
"What is machine learning?"
"How does LangGraph work?"
```

### GitHub Agent
```
"List my repositories"
"Create a new repository called my-project"
"List files in username/repo-name"
"Create a file test.py with content 'print(hello)'"
```

### Drive Agent
```
"List files in my Drive"
"Upload file.txt to Drive"
"Create a folder named 'Projects'"
```

### n8n Agent
```
"Trigger workflow abc123"
"Test n8n connection"
```

### ML Agent
```
"Train a salary prediction model"
"Create a sample salary dataset"
"Predict salary for 5 years experience, Master degree"
"List all trained models"
```

## 🔧 Cấu trúc thư mục

```
clickai/
├── main.py                 # Streamlit UI
├── requirements.txt        # Dependencies
├── .env                    # Environment variables
├── orchestrator/           # LangGraph orchestrator
│   ├── graph.py           # StateGraph definition
│   └── nodes.py           # Agent nodes
├── agents/                 # Agent implementations
│   ├── chat_agent.py
│   ├── github_agent.py
│   ├── drive_agent.py
│   ├── n8n_agent.py
│   └── ml_agent.py
├── mcp_servers/           # MCP server implementations
│   ├── github_mcp.py
│   ├── drive_mcp.py
│   ├── n8n_mcp.py
│   └── ml_mcp.py
├── ml_models/             # ML utilities
│   ├── dataset_finder.py
│   ├── trainer.py
│   ├── model_manager.py
│   └── models/            # Saved models
└── utils/                 # Utilities
    ├── config.py
    └── llm.py
```

## 🤖 ML Model Features

ML Agent hỗ trợ:
- **Tự động tìm dataset**: Tìm kiếm từ Kaggle, HuggingFace
- **Tự động train**: Tự động detect task type (regression/classification) và train model
- **Model management**: Lưu, load, list models
- **Prediction**: Sử dụng models đã train để predict

Ví dụ train model dự đoán lương:
```python
# Tạo sample dataset
ml_mcp = get_ml_mcp()
dataset_path = ml_mcp.create_sample_salary_dataset()

# Train model
result = ml_mcp.train_model(
    dataset_path=dataset_path,
    target_column="salary",
    model_name="salary_predictor"
)

# Predict
prediction = ml_mcp.predict(
    model_name="salary_predictor",
    features={
        "experience_years": 5,
        "education_level": "Master",
        "company_size": "Large",
        "location": "Urban"
    }
)
```

## 🔐 Security

- Không commit file `.env` vào git
- Lưu trữ API keys an toàn
- Google Drive credentials cần được bảo vệ

## 📝 License

MIT

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

Nếu có vấn đề, vui lòng tạo issue trên GitHub.

