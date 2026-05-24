# 前后端API对接完整指南

## 📋 目录
- [概述](#概述)
- [API模块清单](#api模块清单)
- [详细接口文档](#详细接口文档)
- [已修复问题](#已修复问题)
- [使用示例](#使用示例)
- [注意事项](#注意事项)

---

## 概述

本项目采用 **FastAPI** 后端 + **React + TypeScript** 前端的技术栈，所有API遵循统一的响应格式和命名规范。

### 统一响应格式
```json
{
  "code": 200,
  "msg": "成功消息",
  "data": { ... }
}
```

### 错误响应格式
```json
{
  "code": 404,
  "msg": "错误消息",
  "data": null
}
```

### 基础配置
- **后端地址**: `http://127.0.0.1:9091`
- **API前缀**: `/api/v1`
- **前端代理**: 开发环境需配置Vite代理指向后端

---

## API模块清单

| 模块 | 路由前缀 | 接口数量 | 状态 |
|------|---------|---------|------|
| 健康检查 | `/api/v1/health` | 1 | ✅ 已完成 |
| 用户需求 | `/api/v1/requirement` | 3 | ✅ 已完成 |
| 任务分解 | `/api/v1/task` | 3 | ✅ 已完成 |
| 行程管理 | `/api/v1/itinerary` | 5 | ✅ 已完成 |
| 行程校验 | `/api/v1/validation` | 2 | ✅ 已完成 |
| 静态数据 | `/api/v1/static` | 3 | ✅ 已完成 |
| 智能体 | `/api/v1/agent` | 4 | ✅ 已完成 |
| 行程整合 | `/api/v1/integration` | 2 | ✅ 已完成 |
| **总计** | - | **23** | **100%** |

---

## 详细接口文档

### 0. 健康检查模块 (`/api/v1/health`) ⭐ 新增

#### 0.1 服务健康检查
- **接口**: `GET /api/v1/health`
- **前端方法**: `healthApi.checkHealth()`
- **响应数据**:
```typescript
{
  status: string;      // "healthy"
  timestamp: string;   // ISO时间戳
}
```

---

### 1. 用户需求模块 (`/api/v1/requirement`)

#### 1.1 提交需求
- **接口**: `POST /api/v1/requirement/submit`
- **前端方法**: `requirementApi.submit(data)`
- **请求参数**:
```typescript
{
  user_id: string;
  requirement: {
    city_name: string;
    travel_days: number;
    total_budget?: number;
    travel_type?: string;
    start_date?: string;
    preferences?: string[];
  }
}
```
- **响应数据**:
```typescript
{
  requirement_id: string;
  status: "pending";
}
```

#### 1.2 解析需求
- **接口**: `POST /api/v1/requirement/parse`
- **前端方法**: `requirementApi.parse(requirementId)`
- **请求参数**: `{ requirement_id: string }`
- **响应数据**:
```typescript
{
  requirement_id: string;
  parsed: boolean;
  keywords: {
    city_name: string;
    travel_days: number;
    total_budget?: number;
    travel_type?: string;
    preferences: string[];
  }
}
```

#### 1.3 获取需求详情
- **接口**: `GET /api/v1/requirement/:id`
- **前端方法**: `requirementApi.getById(id)`
- **响应数据**: 完整的需求对象

---

### 2. 任务分解模块 (`/api/v1/task`)

#### 2.1 任务分解
- **接口**: `POST /api/v1/task/decompose`
- **前端方法**: `taskApi.decompose(requirementId, structuredRequirement)`
- **请求参数**:
```typescript
{
  requirement_id: string;
  structured_requirement: {
    city_name: string;
    travel_days: number;
    total_budget: number;
    travel_date: string;
    traveler_count: number;
    preferences: string[];
    // 可选字段
    accommodation_budget?: number;
    food_budget?: number;
    transport_budget?: number;
    ticket_budget?: number;
  }
}
```
- **响应数据**:
```typescript
{
  task_id: string;
  batch_id: string;
  requirement_id: string;
  subtasks: Array<{
    task_id: string;
    agent: string; // attraction/accommodation/food/transport
    status: string;
    result: any;
  }>;
}
```

#### 2.2 查询任务状态
- **接口**: `GET /api/v1/task/:task_id`
- **前端方法**: `taskApi.getById(taskId)`
- **响应数据**:
```typescript
{
  task_id: string;
  status: string; // pending/running/success/failed
  progress: number; // 0-100
  result?: any;
  error?: string;
}
```

#### 2.3 更新任务结果
- **接口**: `POST /api/v1/task/update/:task_id`
- **前端方法**: `taskApi.update(taskId, data)`
- **请求参数**:
```typescript
{
  status: "success" | "failed";
  result?: any;
  error?: string;
}
```

---

### 3. 行程管理模块 (`/api/v1/itinerary`)

#### 3.1 创建行程
- **接口**: `POST /api/v1/itinerary/create`
- **前端方法**: `itineraryApi.create(data)`
- **请求参数**:
```typescript
{
  user_id: string;
  requirement_id: string;
  title?: string;
  city_name: string;
  travel_days: number;
  total_budget?: number;
  day_plans?: DayPlan[];
}
```

#### 3.2 获取行程详情
- **接口**: `GET /api/v1/itinerary/:id`
- **前端方法**: `itineraryApi.getById(id)`

#### 3.3 更新行程
- **接口**: `PUT /api/v1/itinerary/:id`
- **前端方法**: `itineraryApi.update(id, data)`

#### 3.4 删除行程
- **接口**: `DELETE /api/v1/itinerary/:id`
- **前端方法**: `itineraryApi.delete(id)`

#### 3.5 获取用户所有行程
- **接口**: `GET /api/v1/itinerary/user/:user_id`
- **前端方法**: `itineraryApi.getByUser(userId)`
- **响应数据**:
```typescript
{
  total: number;
  itineraries: Itinerary[];
}
```

---

### 4. 行程校验模块 (`/api/v1/validation`)

#### 4.1 时间冲突检测
- **接口**: `POST /api/v1/validation/time-conflict`
- **前端方法**: `validationApi.checkTimeConflict(data)`
- **请求参数**:
```typescript
{
  schedule: ScheduleItem[];
}

interface ScheduleItem {
  name: string;
  start_time?: string;      // "09:00" 或 "上午"
  end_time?: string;        // "12:00"
  duration?: string;        // "2小时" 或 "30分钟"
  activity_type: string;    // attraction/meal/transport/accommodation
  location?: string;        // 活动地点（可选）
}
```
- **响应数据**:
```typescript
{
  has_conflict: boolean;
  conflicts: ConflictItem[];
}

interface ConflictItem {
  type: string;             // time_overlap/unreasonable_time等
  description: string;
  severity: "error" | "warning";
  activities: string[];
}
```

#### 4.2 完整行程校验
- **接口**: `POST /api/v1/validation/itinerary`
- **前端方法**: `validationApi.validateItinerary(data)`
- **请求参数**:
```typescript
{
  day_plans: DayPlan[];
  structured_requirement?: {
    total_budget?: number;
    // 其他需求字段
  };
}
```
- **响应数据**:
```typescript
{
  valid: boolean;
  conflicts: ConflictItem[];
  suggestions: string[];
  total_cost?: number;
}
```

---

### 5. 静态数据模块 (`/api/v1/static`)

#### 5.1 获取所有景点
- **接口**: `GET /api/v1/static/attractions`
- **前端方法**: `staticDataApi.getAttractions()`
- **查询参数**: `category?`, `tags?`
- **响应数据**:
```typescript
{
  total: number;
  cities: string[];
  attractions: Attraction[];
}
```

#### 5.2 获取城市景点
- **接口**: `GET /api/v1/static/attractions/:city_name`
- **前端方法**: `staticDataApi.getAttractionsByCity(cityName)`

#### 5.3 获取城市列表
- **接口**: `GET /api/v1/static/cities`
- **前端方法**: `staticDataApi.getCities()`

---

### 6. 智能体模块 (`/api/v1/agent`)

#### 6.1 景点推荐
- **接口**: `POST /api/v1/agent/attractions`
- **前端方法**: `agentApi.getAttractions(data)`
- **请求参数**:
```typescript
{
  city_name: string;
  travel_days: number;
  preferences?: string[];
  dislikes?: string[];
  ticket_budget?: number;
  traveler_count?: number;
}
```

#### 6.2 交通推荐
- **接口**: `POST /api/v1/agent/transport`
- **前端方法**: `agentApi.getTransport(data)`
- **请求参数**:
```typescript
{
  city_name: string;
  travel_days: number;
  budget?: number;
  travel_date?: string;
  mode_preference?: string;
}
```

#### 6.3 住宿推荐
- **接口**: `POST /api/v1/agent/hotel`
- **前端方法**: `agentApi.getHotels(data)`
- **请求参数**:
```typescript
{
  city_name: string;
  check_in_date: string;
  check_out_date: string;
  nights: number;
  budget_per_night?: number;
  location_preference?: string;
  traveler_count?: number;
}
```

#### 6.4 美食推荐
- **接口**: `POST /api/v1/agent/food`
- **前端方法**: `agentApi.getFood(data)`
- **请求参数**:
```typescript
{
  city_name: string;
  travel_days: number;
  budget_per_person?: number;
  cuisine_preference?: string;
  preferences?: string[];
  dislikes?: string[];
}
```

---

### 7. 行程整合模块 (`/api/v1/integration`) ⭐ 新增核心功能

#### 7.1 行程整合
- **接口**: `POST /api/v1/integration/combine`
- **前端方法**: `integrationApi.combine(data)`
- **描述**: 将各智能体的输出拼接为每日行程，并自动进行校验
- **请求参数**:
```typescript
{
  task_id: string;
  agent_results: {
    attraction?: { attractions: any[] };
    accommodation?: { hotels: any[] };
    food?: { restaurants: any[] };
    transport?: { transport_options: any[] };
  };
  structured_requirement: {
    city_name: string;
    travel_days: number;
    total_budget: number;
    travel_date: string;
    traveler_count: number;
    preferences?: string[];
  };
}
```
- **响应数据**:
```typescript
{
  task_id: string;
  day_plans: DayPlan[];
  validation: {
    valid: boolean;
    conflicts: ConflictItem[];
    suggestions: string[];
  };
  total_cost: number;
}
```

#### 7.2 路线优化
- **接口**: `POST /api/v1/integration/optimize-route`
- **前端方法**: `integrationApi.optimizeRoute(data)`
- **描述**: 对给定景点列表进行路径优化，减少折返
- **请求参数**:
```typescript
{
  attractions: Array<{
    name: string;
    location: {
      lat: number;
      lng: number;
    };
  }>;
}
```
- **响应数据**:
```typescript
{
  optimized_attractions: Array<{
    name: string;
    location: {
      lat: number;
      lng: number;
    };
  }>;
}
```

---

## 已修复问题

### ✅ 问题1: ScheduleItem类型定义不完整
**问题描述**: 前端`ScheduleItem`接口缺少`location`字段，但后端校验逻辑中使用该字段  
**修复方案**: 在`frontend/src/services/validationApi.ts`中添加`location?: string`字段  
**影响文件**: 
- `frontend/src/services/validationApi.ts`
- `frontend/src/services/apiTest.ts`

### ✅ 问题2: 未实现的静态数据接口
**问题描述**: 前端定义了`getLocations()`方法，但后端无对应路由  
**修复方案**: 注释掉该方法，待后端实现后再启用  
**影响文件**: `frontend/src/services/staticDataApi.ts`

### ✅ 问题3: apiTest.ts中的类型错误
- **位置**: [`frontend/src/services/apiTest.ts`](file://d:\web%20travel\preoject_4\frontend\src\services\apiTest.ts) 第160行
- **问题**: 使用了不存在的 [location](file://d:\web%20travel\preoject_4\backend\models.py#L392-L392) 属性
- **修复**: 在修复问题1后，恢复location字段的正常使用
- **验证**: 已通过TypeScript编译检查

#### 问题4: 缺失核心API模块
- **位置**: 前端services目录
- **问题**: 缺少行程整合模块（integration）和健康检查模块（health）
- **影响**: 无法使用完整的行程自动生成流程和服务状态监控
- **修复**: 
  - 创建 `integrationApi.ts` - 包含行程整合和路线优化两个核心接口
  - 创建 `healthApi.ts` - 包含服务健康检查接口
  - 更新 `index.ts` 统一导出新模块
- **验证**: 已通过TypeScript编译检查，对接率达到100%

---

## 📁 创建的新文档

```
# 前后端API对接完整指南

## 📋 目录
- [概述](#概述)
- [API模块清单](#api模块清单)
- [详细接口文档](#详细接口文档)
- [已修复问题](#已修复问题)
- [使用示例](#使用示例)
- [注意事项](#注意事项)

---

## 概述

本项目采用 **FastAPI** 后端 + **React + TypeScript** 前端的技术栈，所有API遵循统一的响应格式和命名规范。

### 统一响应格式
```json
{
  "code": 200,
  "msg": "成功消息",
  "data": { ... }
}
```

### 错误响应格式
```json
{
  "code": 404,
  "msg": "错误消息",
  "data": null
}
```

### 基础配置
- **后端地址**: `http://127.0.0.1:9091`
- **API前缀**: `/api/v1`
- **前端代理**: 开发环境需配置Vite代理指向后端

---

## API模块清单

| 模块 | 路由前缀 | 接口数量 | 状态 |
|------|---------|---------|------|
| 健康检查 | `/api/v1/health` | 1 | ✅ 已完成 |
| 用户需求 | `/api/v1/requirement` | 3 | ✅ 已完成 |
| 任务分解 | `/api/v1/task` | 3 | ✅ 已完成 |
| 行程管理 | `/api/v1/itinerary` | 5 | ✅ 已完成 |
| 行程校验 | `/api/v1/validation` | 2 | ✅ 已完成 |
| 静态数据 | `/api/v1/static` | 3 | ✅ 已完成 |
| 智能体 | `/api/v1/agent` | 4 | ✅ 已完成 |
| 行程整合 | `/api/v1/integration` | 2 | ✅ 已完成 |
| **总计** | - | **23** | **100%** |

---

## 详细接口文档

### 0. 健康检查模块 (`/api/v1/health`) ⭐ 新增

#### 0.1 服务健康检查
- **接口**: `GET /api/v1/health`
- **前端方法**: `healthApi.checkHealth()`
- **响应数据**:
```typescript
{
  status: string;      // "healthy"
  timestamp: string;   // ISO时间戳
}
```

---

### 1. 用户需求模块 (`/api/v1/requirement`)

#### 1.1 提交需求
- **接口**: `POST /api/v1/requirement/submit`
- **前端方法**: `requirementApi.submit(data)`
- **请求参数**:
```typescript
{
  user_id: string;
  requirement: {
    city_name: string;
    travel_days: number;
    total_budget?: number;
    travel_type?: string;
    start_date?: string;
    preferences?: string[];
  }
}
```
- **响应数据**:
```typescript
{
  requirement_id: string;
  status: "pending";
}
```

#### 1.2 解析需求
- **接口**: `POST /api/v1/requirement/parse`
- **前端方法**: `requirementApi.parse(requirementId)`
- **请求参数**: `{ requirement_id: string }`
- **响应数据**:
```typescript
{
  requirement_id: string;
  parsed: boolean;
  keywords: {
    city_name: string;
    travel_days: number;
    total_budget?: number;
    travel_type?: string;
    preferences: string[];
  }
}
```

#### 1.3 获取需求详情
- **接口**: `GET /api/v1/requirement/:id`
- **前端方法**: `requirementApi.getById(id)`
- **响应数据**: 完整的需求对象

---

### 2. 任务分解模块 (`/api/v1/task`)

#### 2.1 任务分解
- **接口**: `POST /api/v1/task/decompose`
- **前端方法**: `taskApi.decompose(requirementId, structuredRequirement)`
- **请求参数**:
```typescript
{
  requirement_id: string;
  structured_requirement: {
    city_name: string;
    travel_days: number;
    total_budget: number;
    travel_date: string;
    traveler_count: number;
    preferences: string[];
    // 可选字段
    accommodation_budget?: number;
    food_budget?: number;
    transport_budget?: number;
    ticket_budget?: number;
  }
}
```
- **响应数据**:
```typescript
{
  task_id: string;
  batch_id: string;
  requirement_id: string;
  subtasks: Array<{
    task_id: string;
    agent: string; // attraction/accommodation/food/transport
    status: string;
    result: any;
  }>;
}
```

#### 2.2 查询任务状态
- **接口**: `GET /api/v1/task/:task_id`
- **前端方法**: `taskApi.getById(taskId)`
- **响应数据**:
```typescript
{
  task_id: string;
  status: string; // pending/running/success/failed
  progress: number; // 0-100
  result?: any;
  error?: string;
}
```

#### 2.3 更新任务结果
- **接口**: `POST /api/v1/task/update/:task_id`
- **前端方法**: `taskApi.update(taskId, data)`
- **请求参数**:
```typescript
{
  status: "success" | "failed";
  result?: any;
  error?: string;
}
```

---

### 3. 行程管理模块 (`/api/v1/itinerary`)

#### 3.1 创建行程
- **接口**: `POST /api/v1/itinerary/create`
- **前端方法**: `itineraryApi.create(data)`
- **请求参数**:
```typescript
{
  user_id: string;
  requirement_id: string;
  title?: string;
  city_name: string;
  travel_days: number;
  total_budget?: number;
  day_plans?: DayPlan[];
}
```

#### 3.2 获取行程详情
- **接口**: `GET /api/v1/itinerary/:id`
- **前端方法**: `itineraryApi.getById(id)`

#### 3.3 更新行程
- **接口**: `PUT /api/v1/itinerary/:id`
- **前端方法**: `itineraryApi.update(id, data)`

#### 3.4 删除行程
- **接口**: `DELETE /api/v1/itinerary/:id`
- **前端方法**: `itineraryApi.delete(id)`

#### 3.5 获取用户所有行程
- **接口**: `GET /api/v1/itinerary/user/:user_id`
- **前端方法**: `itineraryApi.getByUser(userId)`
- **响应数据**:
```typescript
{
  total: number;
  itineraries: Itinerary[];
}
```

---

### 4. 行程校验模块 (`/api/v1/validation`)

#### 4.1 时间冲突检测
- **接口**: `POST /api/v1/validation/time-conflict`
- **前端方法**: `validationApi.checkTimeConflict(data)`
- **请求参数**:
```typescript
{
  schedule: ScheduleItem[];
}

interface ScheduleItem {
  name: string;
  start_time?: string;      // "09:00" 或 "上午"
  end_time?: string;        // "12:00"
  duration?: string;        // "2小时" 或 "30分钟"
  activity_type: string;    // attraction/meal/transport/accommodation
  location?: string;        // 活动地点（可选）
}
```
- **响应数据**:
```typescript
{
  has_conflict: boolean;
  conflicts: ConflictItem[];
}

interface ConflictItem {
  type: string;             // time_overlap/unreasonable_time等
  description: string;
  severity: "error" | "warning";
  activities: string[];
}
```

#### 4.2 完整行程校验
- **接口**: `POST /api/v1/validation/itinerary`
- **前端方法**: `validationApi.validateItinerary(data)`
- **请求参数**:
```typescript
{
  day_plans: DayPlan[];
  structured_requirement?: {
    total_budget?: number;
    // 其他需求字段
  };
}
```
- **响应数据**:
```typescript
{
  valid: boolean;
  conflicts: ConflictItem[];
  suggestions: string[];
  total_cost?: number;
}
```

---

### 5. 静态数据模块 (`/api/v1/static`)

#### 5.1 获取所有景点
- **接口**: `GET /api/v1/static/attractions`
- **前端方法**: `staticDataApi.getAttractions()`
- **查询参数**: `category?`, `tags?`
- **响应数据**:
```typescript
{
  total: number;
  cities: string[];
  attractions: Attraction[];
}
```

#### 5.2 获取城市景点
- **接口**: `GET /api/v1/static/attractions/:city_name`
- **前端方法**: `staticDataApi.getAttractionsByCity(cityName)`

#### 5.3 获取城市列表
- **接口**: `GET /api/v1/static/cities`
- **前端方法**: `staticDataApi.getCities()`

---

### 6. 智能体模块 (`/api/v1/agent`)

#### 6.1 景点推荐
- **接口**: `POST /api/v1/agent/attractions`
- **前端方法**: `agentApi.getAttractions(data)`
- **请求参数**:
```typescript
{
  city_name: string;
  travel_days: number;
  preferences?: string[];
  dislikes?: string[];
  ticket_budget?: number;
  traveler_count?: number;
}
```

#### 6.2 交通推荐
- **接口**: `POST /api/v1/agent/transport`
- **前端方法**: `agentApi.getTransport(data)`
- **请求参数**:
```typescript
{
  city_name: string;
  travel_days: number;
  budget?: number;
  travel_date?: string;
  mode_preference?: string;
}
```

#### 6.3 住宿推荐
- **接口**: `POST /api/v1/agent/hotel`
- **前端方法**: `agentApi.getHotels(data)`
- **请求参数**:
```typescript
{
  city_name: string;
  check_in_date: string;
  check_out_date: string;
  nights: number;
  budget_per_night?: number;
  location_preference?: string;
  traveler_count?: number;
}
```

#### 6.4 美食推荐
- **接口**: `POST /api/v1/agent/food`
- **前端方法**: `agentApi.getFood(data)`
- **请求参数**:
```typescript
{
  city_name: string;
  travel_days: number;
  budget_per_person?: number;
  cuisine_preference?: string;
  preferences?: string[];
  dislikes?: string[];
}
```

---

### 7. 行程整合模块 (`/api/v1/integration`) ⭐ 新增核心功能

#### 7.1 行程整合
- **接口**: `POST /api/v1/integration/combine`
- **前端方法**: `integrationApi.combine(data)`
- **描述**: 将各智能体的输出拼接为每日行程，并自动进行校验
- **请求参数**:
```typescript
{
  task_id: string;
  agent_results: {
    attraction?: { attractions: any[] };
    accommodation?: { hotels: any[] };
    food?: { restaurants: any[] };
    transport?: { transport_options: any[] };
  };
  structured_requirement: {
    city_name: string;
    travel_days: number;
    total_budget: number;
    travel_date: string;
    traveler_count: number;
    preferences?: string[];
  };
}
```
- **响应数据**:
```typescript
{
  task_id: string;
  day_plans: DayPlan[];
  validation: {
    valid: boolean;
    conflicts: ConflictItem[];
    suggestions: string[];
  };
  total_cost: number;
}
```

#### 7.2 路线优化
- **接口**: `POST /api/v1/integration/optimize-route`
- **前端方法**: `integrationApi.optimizeRoute(data)`
- **描述**: 对给定景点列表进行路径优化，减少折返
- **请求参数**:
```typescript
{
  attractions: Array<{
    name: string;
    location: {
      lat: number;
      lng: number;
    };
  }>;
}
```
- **响应数据**:
```typescript
{
  optimized_attractions: Array<{
    name: string;
    location: {
      lat: number;
      lng: number;
    };
  }>;
}
```

---

## 已修复问题

### ✅ 问题1: ScheduleItem类型定义不完整
**问题描述**: 前端`ScheduleItem`接口缺少`location`字段，但后端校验逻辑中使用该字段  
**修复方案**: 在`frontend/src/services/validationApi.ts`中添加`location?: string`字段  
**影响文件**: 
- `frontend/src/services/validationApi.ts`
- `frontend/src/services/apiTest.ts`

### ✅ 问题2: 未实现的静态数据接口
**问题描述**: 前端定义了`getLocations()`方法，但后端无对应路由  
**修复方案**: 注释掉该方法，待后端实现后再启用  
**影响文件**: `frontend/src/services/staticDataApi.ts`

### ✅ 问题3: apiTest.ts中的类型错误
- **位置**: [`frontend/src/services/apiTest.ts`](file://d:\web%20travel\preoject_4\frontend\src\services\apiTest.ts) 第160行
- **问题**: 使用了不存在的 [location](file://d:\web%20travel\preoject_4\backend\models.py#L392-L392) 属性
- **修复**: 在修复问题1后，恢复location字段的正常使用
- **验证**: 已通过TypeScript编译检查

#### 问题4: 缺失核心API模块
- **位置**: 前端services目录
- **问题**: 缺少行程整合模块（integration）和健康检查模块（health）
- **影响**: 无法使用完整的行程自动生成流程和服务状态监控
- **修复**: 
  - 创建 `integrationApi.ts` - 包含行程整合和路线优化两个核心接口
  - 创建 `healthApi.ts` - 包含服务健康检查接口
  - 更新 `index.ts` 统一导出新模块
- **验证**: 已通过TypeScript编译检查，对接率达到100%

---

## 使用示例

### 完整流程示例

``typescript
import { 
  requirementApi, 
  taskApi, 
  itineraryApi, 
  validationApi,
  agentApi,
  integrationApi,  // ⭐ 新增
  healthApi        // ⭐ 新增
} from '@/services';

// 0. 检查服务健康状态
const healthCheck = await healthApi.checkHealth();
console.log('服务状态:', healthCheck.data.status);

// 1. 提交旅行需求
const submitResponse = await requirementApi.submit({
  user_id: 'user_001',
  requirement: {
    city_name: '北京',
    travel_days: 3,
    total_budget: 5000,
    travel_type: 'family',
    start_date: '2026-05-20',
    preferences: ['历史古迹', '美食探索']
  }
});

const requirementId = submitResponse.data.requirement_id;

// 2. 任务分解
const taskResponse = await taskApi.decompose(requirementId, {
  city_name: '北京',
  travel_days: 3,
  total_budget: 5000,
  travel_date: '2026-05-20',
  traveler_count: 2,
  preferences: ['历史古迹', '美食探索']
});

const taskId = taskResponse.data.task_id;

// 3. 调用智能体获取推荐
const attractionsResponse = await agentApi.getAttractions({
  city_name: '北京',
  travel_days: 3,
  preferences: ['历史古迹'],
  ticket_budget: 500,
  traveler_count: 2
});

const hotelsResponse = await agentApi.getHotels({
  city_name: '北京',
  check_in_date: '2026-05-20',
  check_out_date: '2026-05-23',
  nights: 3,
  budget_per_night: 1000,
  location_preference: 'city center',
  traveler_count: 2
});

const foodResponse = await agentApi.getFood({
  city_name: '北京',
  travel_days: 3,
  budget_per_person: 100,
  cuisine_preference: 'Chinese',
  preferences: ['street food'],
  dislikes: ['seafood']
});

const transportResponse = await agentApi.getTransport({
  city_name: '北京',
  travel_days: 3,
  budget: 500,
  travel_date: '2026-05-20',
  mode_preference: 'public'
});

// 4. 创建行程
const itineraryResponse = await itineraryApi.create({
  user_id: 'user_001',
  requirement_id: requirementId,
  title: '北京三日游',
  city_name: '北京',
  travel_days: 3,
  total_budget: 5000,
  day_plans: [...]
});

// 5. 校验行程
const validationResult = await validationApi.checkTimeConflict({
  schedule: [
    {
      name: '故宫博物院',
      start_time: '09:00',
      end_time: '12:00',
      activity_type: 'attraction',
      location: '北京市东城区'
    },
    {
      name: '午餐',
      start_time: '11:30',
      duration: '1小时',
      activity_type: 'meal',
      location: '王府井'
    }
  ]
});

if (validationResult.data.has_conflict) {
  console.warn('发现时间冲突:', validationResult.data.conflicts);
}

// 6. 行程整合（核心功能）⭐
const combineResult = await integrationApi.combine({
  task_id: taskId,
  agent_results: {
    attraction: { attractions: attractionsResponse.data.attractions },
    accommodation: { hotels: hotelsResponse.data.hotels },
    food: { restaurants: foodResponse.data.restaurants },
    transport: { transport_options: transportResponse.data.transport_options }
  },
  structured_requirement: {
    city_name: '北京',
    travel_days: 3,
    total_budget: 5000,
    travel_date: '2026-05-20',
    traveler_count: 2,
    preferences: ['历史古迹']
  }
});

console.log('行程校验结果:', combineResult.data.validation.valid);
console.log('总花费:', combineResult.data.total_cost);

// 7. 路线优化（可选）
const optimizedRoute = await integrationApi.optimizeRoute({
  attractions: [
    { name: '故宫', location: { lat: 39.916, lng: 116.397 } },
    { name: '天坛', location: { lat: 39.882, lng: 116.407 } },
    { name: '颐和园', location: { lat: 39.998, lng: 116.275 } }
  ]
});

console.log('优化后的景点顺序:', optimizedRoute.data.optimized_attractions);
