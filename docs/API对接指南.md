# API对接指南

## 目录
- [概述](#概述)
- [快速开始](#快速开始)
- [API模块说明](#api模块说明)
- [使用示例](#使用示例)
- [错误处理](#错误处理)
- [最佳实践](#最佳实践)

## 概述

本项目采用前后端分离架构，前端通过RESTful API与后端FastAPI服务进行通信。所有API接口已封装在`src/services`目录下，可直接在组件中使用。

### 技术栈
- **HTTP客户端**: Axios
- **基础URL**: `/api/v1` (通过Vite代理转发到 `http://127.0.0.1:9091`)
- **响应格式**: 统一的JSON格式 `{ code, msg, data }`
- **认证方式**: Bearer Token (可选)

## 快速开始

### 1. 导入API服务

```typescript
// 方式一：按需导入（推荐）
import { requirementApi, itineraryApi } from '@/services';

// 方式二：从索引文件导入
import { requirementApi } from '@/services/index';
```

### 2. 调用API

```typescript
const handleSubmit = async () => {
  try {
    const response = await requirementApi.submit({
      user_id: 'user_123',
      requirement: {
        city_name: '北京',
        travel_days: 3,
        total_budget: 5000,
        travel_type: 'family',
        start_date: '2026-05-20',
        preferences: ['历史古迹', '美食探索']
      }
    });
    
    if (response.code === 200) {
      console.log('提交成功:', response.data);
    }
  } catch (error) {
    console.error('提交失败:', error);
  }
};
```

## API模块说明

### 1. 用户需求模块 (`requirementApi`)

管理用户旅行需求的提交和查询。

#### API方法

| 方法 | 路径 | 说明 |
|------|------|------|
| `submit` | POST `/requirement/submit` | 提交旅行需求 |
| `parse` | POST `/requirement/parse` | 解析需求关键词 |
| `getById` | GET `/requirement/:id` | 获取需求详情 |

#### 使用示例

```typescript
import { requirementApi } from '@/services';

// 提交需求
const response = await requirementApi.submit({
  user_id: 'user_123',
  requirement: {
    city_name: '杭州',
    travel_days: 2,
    total_budget: 3000,
    travel_type: 'couple',
    start_date: '2026-06-01',
    preferences: ['自然风光', '摄影打卡']
  }
});

// 解析需求
await requirementApi.parse(requirementId);

// 获取详情
const detail = await requirementApi.getById(requirementId);
```

### 2. 任务分解模块 (`taskApi`)

负责任务的分解、状态查询和结果更新。

#### API方法

| 方法 | 路径 | 说明 |
|------|------|------|
| `decompose` | POST `/task/decompose` | 任务分解 |
| `getById` | GET `/task/:taskId` | 查询任务状态 |
| `update` | POST `/task/update/:taskId` | 更新任务结果 |

#### 使用示例

```typescript
import { taskApi } from '@/services';

// 任务分解
const decomposeResponse = await taskApi.decompose(
  requirementId,
  {
    city_name: '成都',
    travel_days: 3,
    total_budget: 4000,
    travel_date: '2026-07-15',
    traveler_count: 2,
    preferences: ['美食探索', '文化体验']
  }
);

const taskId = decomposeResponse.data.task_id;

// 轮询任务状态
const checkTaskStatus = async () => {
  const status = await taskApi.getById(taskId);
  console.log('任务进度:', status.data.progress);
  
  if (status.data.status === 'success') {
    console.log('任务完成');
  } else if (status.data.status === 'failed') {
    console.error('任务失败');
  }
};
```

### 3. 行程管理模块 (`itineraryApi`)

管理行程的创建、查询、更新和删除。

#### API方法

| 方法 | 路径 | 说明 |
|------|------|------|
| `create` | POST `/itinerary/create` | 创建行程 |
| `getById` | GET `/itinerary/:id` | 获取行程详情 |
| `update` | PUT `/itinerary/:id` | 更新行程 |
| `delete` | DELETE `/itinerary/:id` | 删除行程 |
| `getByUser` | GET `/itinerary/user/:userId` | 获取用户所有行程 |

#### 使用示例

```typescript
import { itineraryApi } from '@/services';

// 创建行程
const itinerary = await itineraryApi.create({
  user_id: 'user_123',
  requirement_id: 'req_456',
  title: '北京三日游',
  city_name: '北京',
  travel_days: 3,
  total_budget: 5000,
  day_plans: [...]
});

// 获取行程详情
const detail = await itineraryApi.getById(itineraryId);

// 获取用户所有行程
const userItineraries = await itineraryApi.getByUser('user_123');

// 更新行程
await itineraryApi.update(itineraryId, {
  title: '北京四日游（修改版）',
  day_plans: [...]
});

// 删除行程
await itineraryApi.delete(itineraryId);
```

### 4. 行程校验模块 (`validationApi`)

提供时间冲突检测和完整行程校验功能。

#### API方法

| 方法 | 路径 | 说明 |
|------|------|------|
| `checkTimeConflict` | POST `/validation/time-conflict` | 时间冲突检测 |
| `validateItinerary` | POST `/validation/itinerary` | 完整行程校验 |

#### 使用示例

```typescript
import { validationApi } from '@/services';

// 时间冲突检测
const conflictResult = await validationApi.checkTimeConflict({
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

if (conflictResult.data.has_conflict) {
  console.warn('发现时间冲突:', conflictResult.data.conflicts);
}

// 完整行程校验
const validationResult = await validationApi.validateItinerary({
  day_plans: [...],
  structured_requirement: {
    total_budget: 5000
  }
});

console.log('校验结果:', validationResult.data.valid);
console.log('建议:', validationResult.data.suggestions);
```

### 5. 静态数据模块 (`staticDataApi`)

提供城市、景点等基础数据查询。

#### API方法

| 方法 | 路径 | 说明 |
|------|------|------|
| `getAttractions` | GET `/static/attractions` | 获取所有景点 |
| `getAttractionsByCity` | GET `/static/attractions/:cityName` | 获取城市景点 |
| `getCities` | GET `/static/cities` | 获取城市列表 |
| `getLocations` | GET `/static/locations/:cityName` | 获取地点库 |

#### 使用示例

```typescript
import { staticDataApi } from '@/services';

// 获取所有城市
const cities = await staticDataApi.getCities();

// 获取北京的景点
const beijingAttractions = await staticDataApi.getAttractionsByCity('北京');

// 获取所有景点（可筛选）
const allAttractions = await staticDataApi.getAttractions();
```

### 6. 智能体模块 (`agentApi`)

调用四大智能体获取专业推荐。

#### API方法

| 方法 | 路径 | 说明 |
|------|------|------|
| `getAttractions` | POST `/agent/attractions` | 景点推荐 |
| `getTransport` | POST `/agent/transport` | 交通推荐 |
| `getHotels` | POST `/agent/hotel` | 住宿推荐 |
| `getFood` | POST `/agent/food` | 美食推荐 |

#### 使用示例

```typescript
import { agentApi } from '@/services';

// 景点推荐
const attractions = await agentApi.getAttractions({
  city_name: '西安',
  travel_days: 2,
  preferences: ['历史古迹'],
  ticket_budget: 500,
  traveler_count: 2
});

// 住宿推荐
const hotels = await agentApi.getHotels({
  city_name: '西安',
  check_in_date: '2026-08-01',
  check_out_date: '2026-08-03',
  nights: 2,
  budget_per_night: 300,
  traveler_count: 2
});

// 美食推荐
const restaurants = await agentApi.getFood({
  city_name: '西安',
  travel_days: 2,
  budget_per_person: 100,
  cuisine_preference: '本地特色',
  preferences: ['美食探索']
});

// 交通推荐
const transport = await agentApi.getTransport({
  city_name: '西安',
  travel_days: 2,
  budget: 200,
  mode_preference: 'transit'
});
```

## 错误处理

### 统一错误处理

API客户端已配置全局错误拦截器，会自动显示错误消息。如需自定义处理：

```typescript
try {
  const response = await requirementApi.submit(data);
  // 成功处理
} catch (error) {
  // 错误已在拦截器中显示message
  // 这里可以进行额外处理
  console.error('详细错误信息:', error);
  
  // 可以根据错误类型做不同处理
  if (error.response?.status === 400) {
    // 参数错误
  } else if (error.response?.status === 401) {
    // 未授权，跳转到登录页
  }
}
```

### 常见错误码

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| 200 | 成功 | - |
| 400 | 请求参数错误 | 检查参数格式 |
| 401 | 未授权 | 重新登录 |
| 404 | 资源不存在 | 检查ID是否正确 |
| 500 | 服务器内部错误 | 联系后端开发 |

### 业务错误码

后端可能返回特定的业务错误码：

- `400001`: 出行天数超出范围（1-30天）
- `400002`: 预算过低

## 最佳实践

### 1. 使用TypeScript类型

```typescript
// ✅ 推荐：使用类型定义
import type { Requirement } from '@/services';

const requirement: Requirement = {
  city_name: '北京',
  travel_days: 3,
  // ... TypeScript会提供智能提示
};
```

### 2. 添加加载状态

```typescript
const [loading, setLoading] = useState(false);

const handleSubmit = async () => {
  setLoading(true);
  try {
    await requirementApi.submit(data);
    message.success('提交成功');
  } catch (error) {
    // 错误已由拦截器处理
  } finally {
    setLoading(false);
  }
};
```

### 3. 避免重复请求

```typescript
const [submitting, setSubmitting] = useState(false);

const handleSubmit = async () => {
  if (submitting) return; // 防止重复提交
  
  setSubmitting(true);
  try {
    await requirementApi.submit(data);
  } finally {
    setSubmitting(false);
  }
};
```

### 4. 使用React Query或SWR（可选）

对于需要缓存和自动刷新的数据，可以考虑使用React Query：

```typescript
import { useQuery } from '@tanstack/react-query';
import { itineraryApi } from '@/services';

const { data, isLoading, error } = useQuery({
  queryKey: ['itinerary', itineraryId],
  queryFn: () => itineraryApi.getById(itineraryId)
});
```

### 5. 日志记录

开发环境下会自动打印请求日志：

```
[API Request] POST /requirement/submit { user_id: 'user_123', ... }
```

生产环境可通过环境变量控制：

```typescript
// .env.production
VITE_ENABLE_API_LOG=false
```

## 完整流程示例

```typescript
import { requirementApi, taskApi, itineraryApi } from '@/services';
import { message } from 'antd';

const createTravelPlan = async () => {
  try {
    // 1. 提交需求
    message.loading('正在提交需求...');
    const reqResponse = await requirementApi.submit({
      user_id: 'user_123',
      requirement: {
        city_name: '成都',
        travel_days: 3,
        total_budget: 4000,
        travel_type: 'friends',
        start_date: '2026-09-01',
        preferences: ['美食探索', '文化体验']
      }
    });
    
    const requirementId = reqResponse.data.requirement_id;
    message.success('需求提交成功');
    
    // 2. 任务分解
    message.loading('正在智能规划行程...');
    const taskResponse = await taskApi.decompose(requirementId, {
      city_name: '成都',
      travel_days: 3,
      total_budget: 4000,
      travel_date: '2026-09-01',
      traveler_count: 2,
      preferences: ['美食探索', '文化体验']
    });
    
    const taskId = taskResponse.data.task_id;
    message.success('任务分解成功');
    
    // 3. 轮询任务状态
    const pollInterval = setInterval(async () => {
      const status = await taskApi.getById(taskId);
      
      if (status.data.status === 'success') {
        clearInterval(pollInterval);
        message.success('行程生成完成！');
        
        // 4. 创建行程
        const itinerary = await itineraryApi.create({
          user_id: 'user_123',
          requirement_id: requirementId,
          // ... 从任务结果中提取行程数据
        });
        
        // 跳转到行程详情页
        navigate(`/itinerary/${itinerary.data.itinerary_id}`);
      } else if (status.data.status === 'failed') {
        clearInterval(pollInterval);
        message.error('行程生成失败');
      }
    }, 2000);
    
  } catch (error) {
    message.error('操作失败，请重试');
  }
};
```

## 常见问题

### Q: 如何修改API基础URL？

A: 修改 `vite.config.ts` 中的代理配置：

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:9091',
      changeOrigin: true
    }
  }
}
```

### Q: 如何添加认证Token？

A: Token已自动从localStorage读取并添加到请求头：

```typescript
localStorage.setItem('token', 'your_token_here');
```

### Q: 如何调试API请求？

A: 
1. 打开浏览器开发者工具
2. 查看Network标签页
3. 过滤XHR请求
4. 查看请求和响应的详细信息

### Q: 后端服务未启动怎么办？

A: 
1. 确保后端服务运行在 `http://127.0.0.1:9091`
2. 在项目根目录执行：`npm run dev` 或 `python src/index.py`
3. 访问 `http://127.0.0.1:9091/docs` 确认API文档可访问

## 相关文档

- [后端API文档](http://127.0.0.1:9091/docs)
- [前端项目结构](../README.md)
- [Git开发流程](./Git开发新功能流程说明.md)
