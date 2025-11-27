# 🏗️ Kiến trúc Multi-Agent System

## Tổng quan

Multi-agent system sử dụng **LangGraph** để điều phối 5 agents chuyên biệt. Hệ thống tự động route query đến agent phù hợp dựa trên keywords.

## 📊 Flow Diagram

```
User Query (main.py)
    ↓
Orchestrator (orchestrator/graph.py)
    ├── Router Node (phân tích keywords)
    │   ├── "github" → GitHub Agent
    │   ├── "drive" → Drive Agent  
    │   ├── "n8n" → n8n Agent
    │   ├── "train/predict" → ML Agent
    │   └── default → Chat Agent
    ↓
Agent Nodes (orchestrator/nodes.py)
    ├── chat_node → agents/chat_agent.py
    ├── github_node → agents/github_agent.py
    ├── drive_node → agents/drive_agent.py
    ├── n8n_node → agents/n8n_agent.py
    └── ml_node → agents/ml_agent.py
    ↓
MCP Servers (mcp_servers/)
    ├── github_mcp.py
    ├── drive_mcp.py
    ├── n8n_mcp.py
    └── ml_mcp.py
    ↓
External APIs / Services
```

## 📁 Cấu trúc Multi-Agent

### 1. **Orchestrator** (Điều phối viên) - `orchestrator/`

Đây là **trái tim** của multi-agent system:

- **`orchestrator/graph.py`**: 
  - Tạo LangGraph StateGraph
  - Router node phân tích query và quyết định agent nào xử lý
  - Quản lý state và flow giữa các agents

- **`orchestrator/nodes.py`**:
  - 5 node functions, mỗi node gọi một agent tương ứng
  - `chat_node()`, `github_node()`, `drive_node()`, `n8n_node()`, `ml_node()`

**Ví dụ routing logic:**
```python
# orchestrator/graph.py - router_node()
if "github" in query → github_node
if "drive" in query → drive_node  
if "train" in query → ml_node
else → chat_node
```

### 2. **Agents** (Các agents chuyên biệt) - `agents/`

Mỗi agent là một LLM-powered entity với tools riêng:

- **`agents/chat_agent.py`**: Trả lời câu hỏi đơn giản
- **`agents/github_agent.py`**: GitHub operations (dùng GitHub MCP)
- **`agents/drive_agent.py`**: Drive operations (dùng Drive MCP)
- **`agents/n8n_agent.py`**: n8n workflows (dùng n8n MCP)
- **`agents/ml_agent.py`**: ML operations (dùng ML MCP)

**Mỗi agent có:**
- LangChain AgentExecutor với tools
- DeepSeek LLM để hiểu intent
- Tools từ MCP servers để thực thi actions

### 3. **MCP Servers** (Model Context Protocol) - `mcp_servers/`

Cung cấp functions/tools để tương tác với external services:

- **`mcp_servers/github_mcp.py`**: GitHub API functions
- **`mcp_servers/drive_mcp.py`**: Google Drive API functions
- **`mcp_servers/n8n_mcp.py`**: n8n webhook functions
- **`mcp_servers/ml_mcp.py`**: ML model functions (train, predict, etc.)

### 4. **Entry Point** - `main.py`

Streamlit UI gọi orchestrator:
```python
from orchestrator.graph import process_query
result = process_query(user_input)
```

## 🔄 Luồng xử lý một query

1. **User nhập query** trong Streamlit UI (`main.py`)
2. **Orchestrator nhận query** (`orchestrator/graph.py::process_query()`)
3. **Router phân tích** keywords và quyết định agent
4. **Agent được gọi** qua node tương ứng (`orchestrator/nodes.py`)
5. **Agent sử dụng LLM** để hiểu intent và quyết định actions
6. **Agent gọi MCP functions** để thực thi
7. **Kết quả trả về** qua orchestrator → UI

## 🎯 Ví dụ cụ thể

### Query: "List my GitHub repositories"

```
1. main.py → process_query("List my GitHub repositories")
2. orchestrator/graph.py → router_node() 
   → Phát hiện "github" → agent_type = "github"
3. orchestrator/nodes.py → github_node()
   → Gọi agents/github_agent.py
4. github_agent.py → AgentExecutor với tools
   → Tool: list_repos() từ mcp_servers/github_mcp.py
5. github_mcp.py → GitHub API → Trả về repos
6. Kết quả đi ngược lại → UI hiển thị
```

### Query: "Train a salary prediction model"

```
1. main.py → process_query("Train a salary prediction model")
2. orchestrator/graph.py → router_node()
   → Phát hiện "train" → agent_type = "ml"
3. orchestrator/nodes.py → ml_node()
   → Gọi agents/ml_agent.py
4. ml_agent.py → AgentExecutor
   → Tool: train_model() từ mcp_servers/ml_mcp.py
5. ml_mcp.py → ml_models/trainer.py → Train model
6. Kết quả trả về → UI hiển thị
```

## 🔑 Điểm quan trọng

1. **Orchestrator** (`orchestrator/`) là trung tâm điều phối
2. **Agents** (`agents/`) là các chuyên gia xử lý từng domain
3. **MCP Servers** (`mcp_servers/`) cung cấp tools/functions
4. **LangGraph** quản lý state và flow giữa các nodes

## 📝 Tóm tắt vị trí

- **Multi-agent orchestrator**: `orchestrator/graph.py` + `orchestrator/nodes.py`
- **Các agents**: `agents/*.py`
- **MCP servers**: `mcp_servers/*.py`
- **Entry point**: `main.py` (gọi `orchestrator/graph.py::process_query()`)

