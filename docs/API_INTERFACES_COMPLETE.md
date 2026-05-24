# 旅游行程规划系统 - 完整API接口文档

## 📋 目录

- [1. 健康检查](#1-健康检查)
- [2. 用户需求接口](#2-用户需求接口)
- [3. 任务分发接口](#3-任务分发接口)
- [4. 智能体接口](#4-智能体接口)
- [5. 行程接口](#5-行程接口)
- [6. 校验接口](#6-校验接口)
- [7. 静态数据接口](#7-静态数据接口)
- [8. 行程整合接口](#8-行程整合接口)

---

## 基础信息

**Base URL**: `http://127.0.0.1:9091/api/v1`

**统一响应格式**:
```json
{
  "code": 200,
  "msg": "提示信息",
  "data": {}
}
```

**状态码说明**:
| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 1. 健康检查

### 1.1 服务健康检查

**接口**: `GET /api/v1/health`

**描述**: 检查服务是否正常运行

**请求参数**: 无

**响应示例**:
```json
{
  "code": 200,
  "msg": "服务正常",
  "data": {
    "status": "healthy",
    "timestamp": "2026-05-23T22:00:00"
  }
}
```

---

## 2. 用户需求接口

### 2.1 提交用户需求表单

**接口**: `POST /api/v1/requirement/submit`

**描述**: 用户提交旅行需求表单

**请求参数**:
```json
{
  "user_id": "user_001",
  "requirement": {
    "city_name": "北京",
    "travel_days": 3,
    "total_budget": 5000,
    "travel_date": "2026-06-01",
    "traveler_count": 2,
    "preferences": ["历史古迹", "美食探索"],
    "dislikes": ["爬山"],
    "travel_type": "休闲游"
  }
}
```

**响应示例**:
```json
{
  "code": 200,
  "msg": "需求提交成功",
  "data": {
    "requirement_id": "req_xxx",
    "status": "pending"
  }
}
```

### 2.2 需求预处理（关键词提取）

**接口**: `POST /api/v1/requirement/parse`

**描述**: 对已提交的需求进行解析，提取关键词

**请求参数**:
```json
{
  "requirement_id": "req_xxx"
}
```

**响应示例**:
```json
{
  "code": 200,
  "msg": "需求解析成功",
  "data": {
    "requirement_id": "req_xxx",
    "parsed": true,
    "keywords": {
      "city_name": "北京",
      "travel_days": 3,
      "total_budget": 5000,
      "travel_type": "休闲游",
      "preferences": ["历史古迹", "美食探索"]
    }
  }
}
```

### 2.3 获取需求详情

**接口**: `GET /api/v1/requirement/{requirement_id}`

**描述**: 根据ID获取需求详细信息

**路径参数**:
- `requirement_id`: 需求ID

**响应示例**:
```json
{
  "code": 200,
  "msg": "获取成功",
  "data": {
    "requirement_id": "req_xxx",
    "user_id": "user_001",
    "requirement": {...},
    "status": "parsed",
    "created_at": "2026-05-23T22:00:00"
  }
}
```

---

## 3. 任务分发接口

### 3.1 任务分解 ⭐ 核心接口

**接口**: `POST /api/v1/task/decompose`

**描述**: 将结构化需求拆分为各智能体的子任务，自动分配预算

**请求参数**:
```json
{
  "requirement_id": "req_xxx",
  "structured_requirement": {
    "city_name": "北京",
    "travel_days": 3,
    "total_budget": 5000,
    "travel_date": "2026-06-01",
    "traveler_count": 2,
    "preferences": ["历史古迹", "美食"],
    "dislikes": ["爬山"]
  }
}
```

**业务规则**:
- 出行天数: 1-30天
- 出行人数: 1-20人
- 最低预算: 每人每天100元

**预算分配算法**:
- 住宿: 30%
- 餐饮: 25%
- 交通: 15%
- 门票: 20%
- 其他: 10%

**响应示例**:
```json
{
  "code": 200,
  "msg": "任务分解成功",
  "data": {
    "task_id": "batch_xxx",
    "batch_id": "batch_xxx",
    "requirement_id": "req_xxx",
    "subtasks": [
      {
        "task_id": "task_attraction_xxx",
        "agent": "attraction",
        "status": "pending",
        "result": null
      },
      {
        "task_id": "task_accommodation_xxx",
        "agent": "accommodation",
        "status": "pending",
        "result": null
      },
      {
        "task_id": "task_food_xxx",
        "agent": "food",
        "status": "pending",
        "result": null
      },
      {
        "task_id": "task_transport_xxx",
        "agent": "transport",
        "status": "pending",
        "result": null
      }
    ]
  }
}
```

### 3.2 获取任务状态

**接口**: `GET /api/v1/task/{task_id}`

**描述**: 获取任务执行状态（支持主任务和子任务）

**路径参数**:
- `task_id`: 任务ID（可以是batch_id或子任务ID）

**响应示例（主任务）**:
```json
{
  "code": 200,
  "msg": "获取成功",
  "data": {
    "task_id": "batch_xxx",
    "status": "running",
    "progress": 50.0,
    "failed_subtasks": [],
    "message": "已完成 2/4 个子任务"
  }
}
```

**响应示例（子任务）**:
```json
{
  "code": 200,
  "msg": "获取成功",
  "data": {
    "task_id": "task_attraction_xxx",
    "agent": "attraction",
    "status": "success",
    "result": {
      "attractions": [...]
    },
    "error": null
  }
}
```

### 3.3 更新任务结果

**接口**: `POST /api/v1/task/update/{task_id}`

**描述**: 智能体调用此接口更新任务执行结果

**路径参数**:
- `task_id`: 子任务ID

**请求参数**:
```json
{
  "status": "success",
  "result": {
    "attractions": [
      {"name": "故宫", "ticket_price": 60, ...}
    ]
  },
  "error": null
}
```

**响应示例**:
```json
{
  "code": 200,
  "msg": "任务结果更新成功",
  "data": {
    "task_id": "task_attraction_xxx",
    "status": "success"
  }
}
```

---

## 4. 智能体接口

### 4.1 景点推荐智能体

**接口**: `POST /api/v1/agent/attractions`

**描述**: 根据城市、偏好等条件推荐景点

**请求参数**:
```json
{
  "city_name": "北京",
  "travel_days": 3,
  "preferences": ["历史古迹", "文化体验"],
  "dislikes": ["爬山"],
  "ticket_budget": 1000,
  "traveler_count": 2
}
```

**响应示例**:
```json
{
  "code": 200,
  "msg": "景点推荐成功",
  "data": {
    "attractions": [
      {
        "name": "故宫博物院",
        "duration": "2-3小时",
        "fee": 60.0,
        "location": "北京市东城区",
        "opening_hours": "08:30-17:00",
        "rating": 4.8
      }
    ]
  }
}
```

### 4.2 交通推荐智能体

**接口**: `POST /api/v1/agent/transport`

**描述**: 推荐城市内或城市间交通方案

**请求参数**:
```json
{
  "from_city": "北京",
  "to_city": "上海",
  "travel_date": "2026-06-01",
  "transport_type": "train"
}
```

**响应示例**:
```json
{
  "code": 200,
  "msg": "交通推荐成功",
  "data": {
    "transport_options": [
      {
        "type": "高铁",
        "departure_time": "08:00",
        "arrival_time": "12:30",
        "price": 500.0,
        "duration": "4.5小时"
      }
    ]
  }
}
```

### 4.3 住宿推荐智能体

**接口**: `POST /api/v1/agent/hotel`

**描述**: 根据预算、位置等条件推荐酒店

**请求参数**:
```json
{
  "city_name": "北京",
  "check_in_date": "2026-06-01",
  "check_out_date": "2026-06-04",
  "budget_per_night": 500,
  "location_preference": "靠近景点"
}
```

**响应示例**:
```json
{
  "code": 200,
  "msg": "住宿推荐成功",
  "data": {
    "hotels": [
      {
        "name": "北京王府井酒店",
        "address": "北京市东城区王府井大街",
        "price_per_night": 450.0,
        "rating": 4.5,
        "distance_to_attractions": "500米"
      }
    ]
  }
}
```

### 4.4 美食推荐智能体

**接口**: `POST /api/v1/agent/food`

**描述**: 根据城市、预算、口味等条件推荐餐厅

**请求参数**:
```json
{
  "city_name": "北京",
  "budget_per_meal": 100,
  "cuisine_type": "本地特色"
}
```

**响应示例**:
```json
{
  "code": 200,
  "msg": "美食推荐成功",
  "data": {
    "restaurants": [
      {
        "name": "全聚德烤鸭店",
        "cuisine": "北京菜",
        "avg_price": 120.0,
        "rating": 4.6,
        "address": "北京市东城区前门大街"
      }
    ]
  }
}
```

---

## 5. 行程接口

### 5.1 创建行程方案

**接口**: `POST /api/v1/itinerary/create`

**描述**: 创建新的行程方案

**请求参数**:
```json
{
  "user_id": "user_001",
  "requirement_id": "req_xxx",
  "title": "北京三日游",
  "city_name": "北京",
  "travel_days": 3,
  "total_budget": 5000,
  "day_plans": [
    {
      "day": 1,
      "date": "2026-06-01",
      "attractions": [
        {
          "name": "故宫博物院",
          "start_time": "09:00",
          "visit_duration": "3小时",
          "opening_hours": "08:30-17:00",
          "ticket_price": 60
        }
      ],
      "meals": [
        {
          "name": "午餐",
          "time": "12:00",
          "avg_price_per_person": 80
        }
      ],
      "transport": {
        "from": "酒店",
        "to": "故宫",
        "departure_time": "08:30",
        "cost": 20
      },
      "hotel": {
        "name": "北京酒店",
        "price_per_night": 450
      },
      "notes": "第一天行程安排"
    }
  ]
}
```

**响应示例**:
```json
{
  "code": 200,
  "msg": "行程创建成功",
  "data": {
    "itinerary_id": "itin_xxx",
    "user_id": "user_001",
    "requirement_id": "req_xxx",
    "title": "北京三日游",
    "city_name": "北京",
    "travel_days": 3,
    "total_budget": 5000,
    "day_plans": [...],
    "status": "draft",
    "created_at": "2026-05-23T22:00:00",
    "updated_at": "2026-05-23T22:00:00"
  }
}
```

### 5.2 获取行程详情

**接口**: `GET /api/v1/itinerary/{itinerary_id}`

**描述**: 根据ID获取行程详细信息

**路径参数**:
- `itinerary_id`: 行程ID

**响应示例**:
```json
{
  "code": 200,
  "msg": "获取成功",
  "data": {
    "itinerary_id": "itin_xxx",
    "title": "北京三日游",
    "day_plans": [...],
    "status": "draft"
  }
}
```

### 5.3 更新行程

**接口**: `PUT /api/v1/itinerary/{itinerary_id}`

**描述**: 更新行程信息（标题或每日计划）

**路径参数**:
- `itinerary_id`: 行程ID

**请求参数**:
```json
{
  "title": "北京三日游（修改版）",
  "day_plans": [...]
}
```

**响应示例**:
```json
{
  "code": 200,
  "msg": "行程更新成功",
  "data": {
    "itinerary_id": "itin_xxx",
    "title": "北京三日游（修改版）",
    "updated_at": "2026-05-23T22:30:00"
  }
}
```

### 5.4 删除行程

**接口**: `DELETE /api/v1/itinerary/{itinerary_id}`

**描述**: 删除指定行程

**路径参数**:
- `itinerary_id`: 行程ID

**响应示例**:
```json
{
  "code": 200,
  "msg": "行程删除成功",
  "data": {
    "deleted": true
  }
}
```

### 5.5 获取用户所有行程

**接口**: `GET /api/v1/itinerary/user/{user_id}`

**描述**: 获取指定用户的所有行程列表

**路径参数**:
- `user_id`: 用户ID

**响应示例**:
```json
{
  "code": 200,
  "msg": "获取成功",
  "data": {
    "total": 3,
    "itineraries": [
      {
        "itinerary_id": "itin_xxx",
        "title": "北京三日游",
        "status": "draft"
      }
    ]
  }
}
```

---

## 6. 校验接口 ⭐ 新增功能

### 6.1 时间冲突检测

**接口**: `POST /api/v1/validation/time-conflict`

**描述**: 检测活动时间是否存在重叠

**请求参数**:
```json
{
  "schedule": [
    {
      "name": "故宫博物院",
      "start_time": "09:00",
      "end_time": "12:00",
      "activity_type": "attraction",
      "location": "北京市东城区"
    },
    {
      "name": "午餐",
      "start_time": "11:30",
      "duration": "1小时",
      "activity_type": "meal",
      "location": "王府井"
    }
  ]
}
```

**响应示例**:
```json
{
  "code": 200,
  "msg": "时间冲突检测完成",
  "data": {
    "has_conflict": true,
    "conflicts": [
      {
        "type": "time_overlap",
        "description": "'故宫博物院' (09:00-12:00) 与 '午餐' (11:30-12:30) 时间重叠",
        "severity": "error",
        "activities": ["故宫博物院", "午餐"]
      }
    ]
  }
}
```

### 6.2 完整行程校验 ⭐ 包含开放时间检查

**接口**: `POST /api/v1/validation/itinerary`

**描述**: 对完整行程进行多维度校验（时间冲突 + 预算 + 景点开放时间）

**请求参数**:
```json
{
  "day_plans": [
    {
      "day": 1,
      "date": "2026-06-01",
      "attractions": [
        {
          "name": "故宫博物院",
          "start_time": "09:00",
          "visit_duration": "3小时",
          "opening_hours": "08:30-17:00",
          "ticket_price": 60,
          "address": "北京市东城区"
        }
      ],
      "meals": [
        {
          "name": "午餐",
          "time": "12:00",
          "duration": "1小时",
          "avg_price_per_person": 80
        }
      ],
      "transport": {
        "from": "酒店",
        "to": "故宫",
        "departure_time": "08:30",
        "duration": "30分钟",
        "cost": 20
      }
    }
  ],
  "structured_requirement": {
    "city_name": "北京",
    "travel_days": 1,
    "total_budget": 5000,
    "travel_date": "2026-06-01",
    "traveler_count": 2
  }
}
```

**校验内容**:
1. ✅ 时间冲突检测
2. ✅ 预算校验
3. ✅ 景点开放时间检查（新增）
4. ✅ 游览时长合理性检查
5. ✅ 每日总时长检查

**响应示例**:
```json
{
  "code": 200,
  "msg": "行程校验完成",
  "data": {
    "valid": false,
    "conflicts": [
      {
        "type": "outside_opening_hours",
        "description": "'故宫博物院' 不在开放时间内（开放时间: 08:30-17:00）",
        "severity": "error",
        "activities": ["故宫博物院"],
        "day": 1,
        "date": "2026-06-01"
      },
      {
        "type": "budget_exceeded",
        "description": "总花费 6000 元超出预算 5000 元",
        "severity": "error",
        "activities": []
      }
    ],
    "suggestions": [
      "建议调整部分景点或选择更经济的餐厅"
    ]
  }
}
```

**冲突类型说明**:

| 类型 | 严重程度 | 说明 |
|------|---------|------|
| `time_overlap` | error | 活动时间重叠 |
| `unreasonable_time` | warning | 时间不合理（过早/过晚） |
| `too_short_duration` | warning | 游览时间过短（<30分钟） |
| `too_long_duration` | warning | 游览时间过长（>8小时） |
| `overloaded_day` | warning | 当日行程过载（>12小时） |
| `budget_exceeded` | error | 预算超出 |
| `outside_opening_hours` | error | 完全超出开放时间 |
| `partial_outside_opening_hours` | warning | 部分超出开放时间 |

---

## 7. 静态数据接口

### 7.1 获取所有景点列表

**接口**: `GET /api/v1/static/attractions`

**描述**: 获取所有景点列表，支持按分类和标签筛选

**查询参数**:
- `category`: 景点分类（可选）
- `tags`: 标签列表（可选，多个用逗号分隔）

**响应示例**:
```json
{
  "code": 200,
  "msg": "获取成功",
  "data": {
    "total": 6,
    "cities": ["北京", "上海", "成都", "杭州", "西安"],
    "attractions": [
      {
        "attraction_id": "a001",
        "name": "故宫",
        "city_name": "北京",
        "category": "scenic_spot",
        "ticket_price": 60.0,
        "rating": 4.8,
        "tags": ["历史", "建筑"]
      }
    ]
  }
}
```

### 7.2 获取城市景点

**接口**: `GET /api/v1/static/attractions/{city_name}`

**描述**: 获取指定城市的所有景点

**路径参数**:
- `city_name`: 城市名称

**响应示例**:
```json
{
  "code": 200,
  "msg": "获取成功",
  "data": {
    "city_name": "北京",
    "total": 2,
    "attractions": [
      {
        "attraction_id": "a001",
        "name": "故宫",
        "city_name": "北京",
        "category": "scenic_spot",
        "ticket_price": 60.0
      }
    ]
  }
}
```

### 7.3 获取城市列表

**接口**: `GET /api/v1/static/cities`

**描述**: 获取所有支持的城市列表

**响应示例**:
```json
{
  "code": 200,
  "msg": "获取成功",
  "data": {
    "total": 5,
    "cities": [
      {
        "city_id": "c001",
        "city_name": "北京",
        "province": "北京",
        "country": "中国",
        "description": "中国的首都",
        "tags": ["历史文化", "政治中心"]
      }
    ]
  }
}
```

---

## 8. 行程整合接口

### 8.1 行程整合

**接口**: `POST /api/v1/integration/combine`

**描述**: 将各智能体的输出拼接为每日行程，并自动进行校验

**请求参数**:
```json
{
  "task_id": "batch_xxx",
  "agent_results": {
    "attraction": {
      "attractions": [
        {"name": "故宫", "ticket_price": 60, "visit_time_slot": "morning"}
      ]
    },
    "accommodation": {
      "hotels": [
        {"name": "北京酒店", "price_per_night": 450}
      ]
    },
    "food": {
      "restaurants": [
        {"name": "餐厅A", "avg_price_per_person": 80}
      ]
    },
    "transport": {
      "transport_options": []
    }
  },
  "structured_requirement": {
    "city_name": "北京",
    "travel_days": 3,
    "total_budget": 5000,
    "travel_date": "2026-06-01",
    "traveler_count": 2
  }
}
```

**响应示例**:
```json
{
  "code": 200,
  "msg": "行程整合成功",
  "data": {
    "task_id": "batch_xxx",
    "day_plans": [
      {
        "day": 1,
        "date": "2026-06-01",
        "attractions": [...],
        "meals": [...],
        "transport": {...},
        "hotel": {...},
        "daily_cost": 650.0,
        "notes": "第1天行程安排"
      }
    ],
    "validation": {
      "valid": true,
      "conflicts": [],
      "suggestions": ["行程安排合理，无时间冲突"]
    },
    "total_cost": 1950.0
  }
}
```

### 8.2 路线优化

**接口**: `POST /api/v1/integration/optimize-route`

**描述**: 对给定景点列表进行路径优化，减少折返

**请求参数**:
```json
{
  "attractions": [
    {"name": "故宫", "location": {"lat": 39.916, "lng": 116.397}},
    {"name": "颐和园", "location": {"lat": 39.998, "lng": 116.275}},
    {"name": "天坛", "location": {"lat": 39.882, "lng": 116.407}}
  ]
}
```

**响应示例**:
```json
{
  "code": 200,
  "msg": "路线优化完成",
  "data": {
    "optimized_attractions": [
      {"name": "天坛", "location": {"lat": 39.882, "lng": 116.407}},
      {"name": "故宫", "location": {"lat": 39.916, "lng": 116.397}},
      {"name": "颐和园", "location": {"lat": 39.998, "lng": 116.275}}
    ]
  }
}
```

---

## 🔌 前端集成示例

### TypeScript/React 调用示例

```typescript
// services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:9091/api/v1',
  timeout: 30000
});

// 任务分解
export const decomposeTask = async (requirementId: string, structuredRequirement: any) => {
  const response = await api.post('/task/decompose', {
    requirement_id: requirementId,
    structured_requirement: structuredRequirement
  });
  return response.data;
};

// 完整行程校验
export const validateItinerary = async (dayPlans: any[], structuredRequirement: any) => {
  const response = await api.post('/validation/itinerary', {
    day_plans: dayPlans,
    structured_requirement: structuredRequirement
  });
  return response.data;
};

// 获取任务状态
export const getTaskStatus = async (taskId: string) => {
  const response = await api.get(`/task/${taskId}`);
  return response.data;
};
```

### Python 调用示例

```python
import requests

BASE_URL = "http://127.0.0.1:9091/api/v1"

# 任务分解
def decompose_task(requirement_id, structured_requirement):
    response = requests.post(
        f"{BASE_URL}/task/decompose",
        json={
            "requirement_id": requirement_id,
            "structured_requirement": structured_requirement
        }
    )
    return response.json()

# 完整行程校验
def validate_itinerary(day_plans, structured_requirement):
    response = requests.post(
        f"{BASE_URL}/validation/itinerary",
        json={
            "day_plans": day_plans,
            "structured_requirement": structured_requirement
        }
    )
    return response.json()

# 获取任务状态
def get_task_status(task_id):
    response = requests.get(f"{BASE_URL}/task/{task_id}")
    return response.json()
```

---

## 📊 API接口统计

| 模块 | 接口数量 | 核心功能 |
|------|---------|---------|
| 健康检查 | 1 | 服务状态检查 |
| 用户需求 | 3 | 提交、解析、查询 |
| 任务分发 | 3 | 分解、查询、更新 |
| 智能体 | 4 | 景点/交通/住宿/美食推荐 |
| 行程管理 | 5 | CRUD操作 + 用户查询 |
| 校验 | 2 | 时间冲突 + 完整校验 |
| 静态数据 | 3 | 景点/城市查询 |
| 行程整合 | 2 | 整合 + 路线优化 |
| **总计** | **25个接口** | **完整覆盖所有功能** |

---

## 🚀 快速开始

### 1. 启动后端服务

```bash
cd d:\project\preoject_4
python src/index.py
```

服务将在 `http://127.0.0.1:9091` 启动

### 2. 访问API文档

- Swagger UI: http://127.0.0.1:9091/docs
- ReDoc: http://127.0.0.1:9091/redoc

### 3. 测试接口

```bash
# 健康检查
curl http://127.0.0.1:9091/api/v1/health

# 查看API文档
open http://127.0.0.1:9091/docs
```

---

## 📝 注意事项

1. **时间格式**: 所有时间使用 `HH:mm` 格式（如 `09:30`, `14:00`）
2. **日期格式**: 使用 `YYYY-MM-DD` 格式（如 `2026-06-01`）
3. **预算单位**: 所有金额单位为人民币元（CNY）
4. **分页**: 当前版本暂不支持分页，返回全部数据
5. **认证**: 当前版本暂不需要认证，生产环境需添加JWT
6. **CORS**: 已配置允许跨域请求，前端可直接调用

---

## 🔄 版本历史

- **v1.0** (2026-05-23): 初始版本，包含25个完整API接口
  - ✅ 用户需求管理
  - ✅ 任务分解与分发
  - ✅ 多智能体协作
  - ✅ 行程CRUD操作
  - ✅ 完整校验功能（含开放时间检查）
  - ✅ 静态数据管理
  - ✅ 行程整合与优化

---

**相关文档**:
- 项目架构: `ARCHITECTURE.md`
- 快速开始: `QUICKSTART.md`
- 校验模块指南: `VALIDATION_MODULE_GUIDE.md`
- 测试脚本: `test_time_conflict.py`, `test_opening_hours_validation.py`
