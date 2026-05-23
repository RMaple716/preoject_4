# API接口快速参考手册

## 📌 基础信息

- **Base URL**: `http://127.0.0.1:9091/api/v1`
- **响应格式**: `{"code": 200, "msg": "...", "data": {...}}`
- **时间格式**: `HH:mm` (如 `09:30`)
- **日期格式**: `YYYY-MM-DD` (如 `2026-06-01`)

---

## 🔗 接口清单（共25个）

### 1️⃣ 健康检查（1个）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 服务健康检查 |

---

### 2️⃣ 用户需求（3个）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/requirement/submit` | 提交需求表单 |
| POST | `/requirement/parse` | 解析需求关键词 |
| GET | `/requirement/{id}` | 获取需求详情 |

---

### 3️⃣ 任务分发（3个）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/task/decompose` | ⭐ 任务分解（核心） |
| GET | `/task/{id}` | 获取任务状态 |
| POST | `/task/update/{id}` | 更新任务结果 |

---

### 4️⃣ 智能体（4个）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/agent/attractions` | 景点推荐 |
| POST | `/agent/transport` | 交通推荐 |
| POST | `/agent/hotel` | 住宿推荐 |
| POST | `/agent/food` | 美食推荐 |

---

### 5️⃣ 行程管理（5个）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/itinerary/create` | 创建行程 |
| GET | `/itinerary/{id}` | 获取行程详情 |
| PUT | `/itinerary/{id}` | 更新行程 |
| DELETE | `/itinerary/{id}` | 删除行程 |
| GET | `/itinerary/user/{user_id}` | 获取用户行程列表 |

---

### 6️⃣ 校验接口（2个）⭐ 新增

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/validation/time-conflict` | 时间冲突检测 |
| POST | `/validation/itinerary` | ⭐ 完整行程校验（含开放时间检查） |

---

### 7️⃣ 静态数据（3个）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/static/attractions` | 获取所有景点 |
| GET | `/static/attractions/{city}` | 获取城市景点 |
| GET | `/static/cities` | 获取城市列表 |

---

### 8️⃣ 行程整合（2个）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/integration/combine` | 行程整合+自动校验 |
| POST | `/integration/optimize-route` | 路线优化 |

---

## 🚀 常用调用示例

### Python示例

```python
import requests

BASE_URL = "http://127.0.0.1:9091/api/v1"

# 1. 提交需求
req_response = requests.post(f"{BASE_URL}/requirement/submit", json={
    "user_id": "user_001",
    "requirement": {
        "city_name": "北京",
        "travel_days": 3,
        "total_budget": 5000,
        "travel_date": "2026-06-01",
        "traveler_count": 2
    }
})
requirement_id = req_response.json()['data']['requirement_id']

# 2. 任务分解
task_response = requests.post(f"{BASE_URL}/task/decompose", json={
    "requirement_id": requirement_id,
    "structured_requirement": {
        "city_name": "北京",
        "travel_days": 3,
        "total_budget": 5000,
        "travel_date": "2026-06-01",
        "traveler_count": 2
    }
})
task_id = task_response.json()['data']['task_id']

# 3. 完整行程校验
validation_response = requests.post(f"{BASE_URL}/validation/itinerary", json={
    "day_plans": [...],
    "structured_requirement": {...}
})
is_valid = validation_response.json()['data']['valid']
```

### TypeScript/React示例

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:9091/api/v1'
});

// 任务分解
const { data } = await api.post('/task/decompose', {
  requirement_id: reqId,
  structured_requirement: requirement
});

// 完整行程校验
const { data } = await api.post('/validation/itinerary', {
  day_plans: plans,
  structured_requirement: req
});
```

---

## 📊 核心业务流程

```mermaid
graph LR
    A[提交需求] --> B[解析需求]
    B --> C[任务分解]
    C --> D[智能体执行]
    D --> E[行程整合]
    E --> F[行程校验]
    F --> G[创建行程]
```

**步骤说明**:
1. 用户提交需求 → `/requirement/submit`
2. 解析需求关键词 → `/requirement/parse`
3. 任务分解为子任务 → `/task/decompose`
4. 各智能体执行 → `/agent/*`
5. 整合为每日行程 → `/integration/combine`
6. 校验行程合理性 → `/validation/itinerary`
7. 保存行程 → `/itinerary/create`

---

## ⚠️ 注意事项

1. **必填字段验证**:
   - 任务分解: `city_name`, `travel_days`, `total_budget`, `travel_date`, `traveler_count`
   - 出行天数: 1-30天
   - 出行人数: 1-20人
   - 最低预算: 每人每天100元

2. **预算分配算法**（自动）:
   - 住宿: 30%
   - 餐饮: 25%
   - 交通: 15%
   - 门票: 20%
   - 其他: 10%

3. **校验规则**:
   - 时间重叠 → error
   - 预算超出 → error
   - 开放时间冲突 → error/warning
   - 游览时长不合理 → warning

4. **开放时间格式**:
   - 标准: `"08:30-17:00"`
   - 全天: `"全天开放"`
   - 关闭: `"不开放"` 或 `"关闭"`

---

## 🔍 调试技巧

### 1. 查看API文档
```bash
# Swagger UI
open http://127.0.0.1:9091/docs

# ReDoc
open http://127.0.0.1:9091/redoc
```

### 2. 测试服务状态
```bash
curl http://127.0.0.1:9091/api/v1/health
```

### 3. 运行完整测试
```bash
python test_all_api_interfaces.py
```

### 4. 测试开放时间校验
```bash
python test_opening_hours_validation.py
```

---

## 📞 常见问题

**Q: 如何获取完整的接口文档？**  
A: 访问 `http://127.0.0.1:9091/docs` 查看Swagger UI

**Q: 任务分解后如何知道任务完成？**  
A: 轮询调用 `GET /task/{task_id}` 查看进度

**Q: 如何检查行程是否有问题？**  
A: 调用 `POST /validation/itinerary` 进行完整校验

**Q: 景点开放时间在哪里设置？**  
A: 在景点数据的 `opening_hours` 字段中设置

**Q: 预算超出怎么办？**  
A: 校验接口会返回 `budget_exceeded` 冲突，调整景点或餐厅即可

---

## 📚 相关文档

- [完整API文档](./API_INTERFACES_COMPLETE.md)
- [校验模块指南](./VALIDATION_MODULE_GUIDE.md)
- [项目架构](../frontend/ARCHITECTURE.md)
- [快速开始](../frontend/QUICKSTART.md)

---

**最后更新**: 2026-05-23  
**版本**: v1.0  
**接口总数**: 25个
