# 旅游行程规划后端服务

基于 FastAPI 框架的后端服务，实现模块接口无缝对接。

启动服务：python src/index.py
运行任务分解测试脚本：python test_task_decompose.py（启动服务后需新开终端）
运行时间冲突检测测试：python test_time_conflict.py（启动服务后需新开终端）
ps:注意路径！

## 接口规范

### 统一响应格式
```json
{
  "code": 200,
  "msg": "提示信息",
  "data": {}
}
```

### 命名规范
- 所有参数使用英文小写下划线命名
- 示例：`city_name`, `travel_days`, `total_budget`

### 时间格式
- 统一使用 `HH:mm` 格式（如 09:30, 14:00）
- 支持时间槽格式：上午/下午/晚上、morning/afternoon/evening

### 状态码说明
| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 接口列表

### 1. 健康检查
- `GET /api/v1/health` - 服务健康检查

### 2. 用户需求接口
- `POST /api/v1/requirement/submit` - 提交用户需求表单
- `POST /api/v1/requirement/parse` - 需求预处理（关键词提取）
- `GET /api/v1/requirement/{requirement_id}` - 获取需求详情

### 3. 任务分发接口
- `POST /api/v1/task/decompose` - **任务分解**（将结构化需求拆分为子任务）
- `POST /api/v1/task/dispatch` - 分发任务到各智能体（旧版，保留兼容）
- `GET /api/v1/task/{task_id}` - 获取任务状态（支持主任务和子任务）
- `POST /api/v1/task/update/{task_id}` - 更新任务结果（供智能体调用）

### 4. 智能体接口
- `POST /api/v1/agent/attractions` - 景点推荐智能体
- `POST /api/v1/agent/transport` - 交通推荐智能体
- `POST /api/v1/agent/hotel` - 住宿推荐智能体
- `POST /api/v1/agent/food` - 美食推荐智能体

### 5. 行程接口
- `POST /api/v1/itinerary/create` - 创建行程方案
- `GET /api/v1/itinerary/{itinerary_id}` - 获取行程详情
- `PUT /api/v1/itinerary/{itinerary_id}` - 更新行程
- `DELETE /api/v1/itinerary/{itinerary_id}` - 删除行程
- `GET /api/v1/itinerary/user/{user_id}` - 获取用户所有行程

### 6. 校验接口 ⭐ 新增
- `POST /api/v1/validation/time-conflict` - **时间冲突检测**
- `POST /api/v1/validation/itinerary` - **完整行程校验**（含预算检查）

### 7. 静态数据接口
- `GET /api/v1/static/attractions` - 获取景点列表
- `GET /api/v1/static/attractions/{city_name}` - 获取城市景点
- `GET /api/v1/static/cities` - 获取城市列表
- `GET /api/v1/static/locations/{city_name}` - 获取地点库

## 🆕 最新功能

### 任务分解模块 (Task Decomposition)
**文档**: `任务分解模块说明.md`  
**测试**: `test_task_decompose.py`

核心功能：
- ✅ 自动预算分配（住宿30%、餐饮25%、交通15%、门票20%、其他10%）
- ✅ 将结构化需求拆分为4个子任务（景点、住宿、美食、交通）
- ✅ 业务规则验证（天数、人数、最低预算）
- ✅ 任务状态追踪和进度计算

### 时间冲突检测算法 (Time Conflict Detection) ⭐ 新
**文档**: `时间冲突检测算法说明.md`、`时间冲突检测快速开始.md`  
**测试**: `test_time_conflict.py`

核心功能：
- ✅ 检测活动时间重叠
- ✅ 验证游览时长合理性
- ✅ 检查时间安排是否符合日常作息
- ✅ 控制每日行程总时长（不超过12小时）
- ✅ 预算超支检测
- ✅ 生成优化建议

支持的输入格式：
```json
{
  "start_time": "09:00",      // 精确时间
  "start_time": "上午",        // 中文时间槽
  "start_time": "morning",    // 英文时间槽
  "duration": "2小时",        // 时长描述
  "duration": "2-3小时"       // 时长范围
}
```

## 开发文档

### 核心文档
- `分工.md` - 团队分工方案
- `接口.md` - 完整接口文档
- `多智能体通信数据格式.md` - 智能体通信协议

### 模块文档
- `任务分解模块说明.md` - 任务分解功能详解
- `任务分解测试示例.md` - 任务分解API测试示例
- `时间冲突检测算法说明.md` - 时间冲突检测算法详解 ⭐
- `时间冲突检测快速开始.md` - 5分钟上手指南 ⭐
- `时间冲突检测开发总结.md` - 开发成果总结 ⭐

### Git协作规范
- `docs/规范.md` - 小组协作编程规范
- `Git开发新功能流程说明.md` - Git操作流程

## 技术栈

- **框架**: FastAPI
- **数据验证**: Pydantic
- **服务器**: Uvicorn
- **测试**: requests + pytest（可选）

## 项目结构

```
preoject_4/
├── src/
│   ├── routes/
│   │   ├── task.py          # 任务分解与分发
│   │   ├── validate.py      # 行程校验（时间冲突检测）⭐
│   │   ├── agent.py         # 智能体接口
│   │   ├── requirement.py   # 需求处理
│   │   ├── itinerary.py     # 行程管理
│   │   └── ...
│   ├── models/
│   │   ├── request.py       # 请求模型
│   │   └── response.py      # 响应模型
│   └── index.py             # 主入口
├── test_task_decompose.py   # 任务分解测试
├── test_time_conflict.py    # 时间冲突检测测试 ⭐
└── docs/
    └── 规范.md              # 协作规范
```

## 快速开始

### 1. 安装依赖
```bash
pip install fastapi uvicorn pydantic requests
```

### 2. 启动服务
```bash
cd preoject_4
python src/index.py
```

服务将在 `http://127.0.0.1:9091` 启动

### 3. 访问文档
打开浏览器访问：`http://127.0.0.1:9091/docs`

### 4. 运行测试
```bash
# 任务分解测试
python test_task_decompose.py

# 时间冲突检测测试 ⭐
python test_time_conflict.py
```

## API 使用示例

### 任务分解
```bash
curl -X POST "http://127.0.0.1:9091/api/v1/task/decompose" \
  -H "Content-Type: application/json" \
  -d '{
    "requirement_id": "req_001",
    "structured_requirement": {
      "city_name": "北京",
      "travel_days": 3,
      "total_budget": 5000,
      "travel_date": "2026-05-20",
      "traveler_count": 3,
      "preferences": ["历史古迹", "美食"]
    }
  }'
```

### 时间冲突检测 ⭐
```bash
curl -X POST "http://127.0.0.1:9091/api/v1/validation/time-conflict" \
  -H "Content-Type: application/json" \
  -d '{
    "schedule": [
      {
        "name": "故宫博物院",
        "start_time": "09:00",
        "end_time": "12:00",
        "activity_type": "attraction"
      },
      {
        "name": "午餐",
        "start_time": "11:30",
        "duration": "1小时",
        "activity_type": "meal"
      }
    ]
  }'
```

## 团队协作

### 分支管理
- 主分支：`main`
- 功能分支：`feature/<功能名>`
- 修复分支：`fix/<问题名>`

详见：`docs/规范.md`

### 提交规范
遵循 Conventional Commits：
```
feat: 新增功能
fix: 修复bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试相关
chore: 构建/工具配置
```

## 常见问题

### Q1: 如何测试时间冲突检测功能？
A: 运行 `python test_time_conflict.py`，会自动执行7个测试用例。

### Q2: 时间冲突检测支持哪些时间格式？
A: 支持 "HH:MM"、"上午/下午/晚上"、"morning/afternoon/evening" 等多种格式。

### Q3: 如何集成到我的模块中？
A: 参考 `时间冲突检测快速开始.md` 中的实际应用场景章节。

### Q4: 检测到冲突后如何处理？
A: 根据 `severity` 字段判断：
- `error`: 必须修复后才能继续
- `warning`: 可以忽略，但建议优化

## 更新日志

### v1.1.0 (2026-05-19)
- ✨ 新增时间冲突检测算法模块
- ✨ 新增完整行程校验接口
- 📝 新增3份详细文档
- 🧪 新增7个测试用例

### v1.0.0 (2026-05-18)
- ✨ 初始版本发布
- ✨ 任务分解模块
- ✨ 智能体接口
- ✨ 基础行程管理

## 联系方式

如有问题，请参考相关文档或在团队群组中提问。

---

**最后更新**: 2026-05-19  
**版本**: v1.1.0
