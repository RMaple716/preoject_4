# 旅游行程规划后端服务

基于 FastAPI 框架的后端服务，实现模块接口无缝对接。

启动服务：python src/index.py
运行任务分解测试脚本：python test_task_decompose.py（启动服务后需新开终端）
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
- `POST /api/v1/task/dispatch` - 分发任务到各智能体
- `GET /api/v1/task/{task_id}` - 获取任务状态

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

### 6. 校验接口
- `POST /api/v1/validate/itinerary` - 行程冲突检测
- `POST /api/v1/validate/time` - 时间冲突检测

### 7. 静态数据接口
- `GET /api/v1/static/attractions` - 获取景点列表
- `GET /api/v1/static/attractions/{city_name}` - 获取城市景点
- `GET /api/v1/static/cities` - 获取城市列表
- `GET /api/v1/static/locations/{city_name}` - 获取地点库