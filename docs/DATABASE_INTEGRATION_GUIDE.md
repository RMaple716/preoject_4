# 数据库集成完整指南

## 📋 目录
- [问题背景](#问题背景)
- [解决方案](#解决方案)
- [实施步骤](#实施步骤)
- [功能验证](#功能验证)
- [API接口说明](#api接口说明)
- [常见问题](#常见问题)

---

## 问题背景

### ❌ 原有问题

1. **内存存储导致数据丢失**
   ```python
   requirements_store = {}  # 服务重启后清空
   tasks_store = {}         # 无法持久化
   itineraries_store = {}   # 收藏夹功能无法实现
   ```

2. **缺少真实基础数据**
   - 无景点、酒店、餐厅的真实数据
   - 所有推荐都来自硬编码示例
   - 无法支持智能体的真实推荐

3. **功能限制**
   - ❌ 无法保存行程到收藏夹
   - ❌ 无法查询历史行程
   - ❌ 无法统计分析用户行为

---

## 解决方案

### ✅ 已完成改造

#### 1. 数据库模型扩展（`src/models/db_models.py`）

新增3个业务数据表：

| 表名 | 说明 | 关键字段 |
|------|------|---------|
| `user_requirements` | 用户需求表 | requirement_id, user_id, requirement_data, status |
| `tasks` | 任务表 | task_id, batch_id, agent_type, status, result |
| `itineraries` | 行程表 | itinerary_id, user_id, day_plans, is_favorite ⭐ |

#### 2. 数据库服务层（`src/services/database_service.py`）

提供4个服务类：

- **RequirementService**: 需求CRUD操作
- **TaskService**: 任务管理、进度追踪
- **ItineraryService**: 行程管理、**收藏夹功能** ⭐
- **StaticDataService**: 基础数据查询（景点/酒店/餐厅）

#### 3. 路由改造

| 文件 | 改造内容 |
|------|---------|
| `src/routes/requirement.py` | 使用数据库替代 `requirements_store` |
| `src/routes/task.py` | 使用数据库替代 `tasks_store` |
| `src/routes/itinerary.py` | 实现完整的行程CRUD和**收藏功能** ⭐ |
| `src/routes/static_data.py` | 从数据库查询真实的景点/酒店/餐厅数据 |

#### 4. 数据库建表脚本（`database_schema.sql`）

包含8个表的完整DDL：
- 5个基础数据表（cities, attractions, locations, hotels, restaurants）
- 3个业务数据表（user_requirements, tasks, itineraries）

---

## 实施步骤

### 步骤1: 执行数据库建表脚本

```bash
# 连接到PostgreSQL
psql -U postgres -d travel_planner

# 执行建表脚本
\i d:/project/preoject_4/database_schema.sql

# 或直接一行命令
psql -U postgres -d travel_planner -f d:/project/preoject_4/database_schema.sql
```

**预期输出:**
```
=== 数据统计 ===
 table_name       | count 
------------------+-------
 Cities           |     5
 Attractions      |     5
 Locations        |     2
 Hotels           |     2
 Restaurants      |     2
 UserRequirements |     0
 Tasks            |     0
 Itineraries      |     0

✅ 数据库初始化完成！
已创建8个表（5个基础表 + 3个业务表）
已插入示例数据
```

### 步骤2: 安装依赖（如果需要）

```bash
pip install sqlalchemy psycopg2-binary
```

### 步骤3: 运行测试验证

```bash
python scripts/test_full_integration.py
```

**预期输出:**
```
======================================================================
🧪 开始测试数据库集成功能...
======================================================================

📍 测试1: 查询基础数据（城市、景点、酒店、餐厅）
✅ 找到 5 个城市
   - 北京 (beijing)
   - 上海 (shanghai)
   - 杭州 (hangzhou)
✅ 北京 有 2 个景点
✅ 北京 有 1 家酒店
✅ 北京 有 1 家餐厅

📍 测试2: 用户需求管理
✅ 创建需求成功: req_20260524160000_1234
   状态: pending
✅ 更新需求状态成功: parsed
✅ 查询需求成功: req_20260524160000_1234

📍 测试3: 任务管理
✅ 创建 4 个子任务成功
   - attraction: xxx-xxx-xxx
   - accommodation: xxx-xxx-xxx
   - food: xxx-xxx-xxx
   - transport: xxx-xxx-xxx
✅ 更新任务结果成功: xxx-xxx-xxx
✅ 批次进度: 1/4 完成

📍 测试4: 行程管理
✅ 创建行程成功: xxx-xxx-xxx
   标题: 北京三日游
   状态: draft
   收藏: False
✅ 切换收藏状态成功: 已收藏
✅ 保存行程成功: saved
✅ 发布行程成功: published
✅ 用户共有 1 个行程
✅ 用户收藏了 1 个行程

======================================================================
✨ 所有测试通过！数据库集成成功！
======================================================================

📊 测试结果总结:
  ✅ 基础数据查询正常（城市/景点/酒店/餐厅）
  ✅ 用户需求持久化存储
  ✅ 任务分解与进度追踪
  ✅ 行程CRUD操作
  ✅ 收藏夹功能 ⭐
  ✅ 服务重启后数据不丢失 ⭐
======================================================================
```

### 步骤4: 启动服务

```bash
python src/index.py
```

服务将在 `http://127.0.0.1:9091` 启动

---

## 功能验证

### 1. 基础数据查询

```bash
# 查询所有城市
curl http://127.0.0.1:9091/api/v1/static/cities

# 查询北京的景点
curl http://127.0.0.1:9091/api/v1/static/attractions/北京

# 查询北京的酒店
curl http://127.0.0.1:9091/api/v1/static/hotels/北京

# 查询北京的餐厅
curl http://127.0.0.1:9091/api/v1/static/restaurants/北京
```

### 2. 用户需求提交

```bash
curl -X POST "http://127.0.0.1:9091/api/v1/requirement/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "requirement": {
      "city_name": "北京",
      "travel_days": 3,
      "total_budget": 5000,
      "travel_date": "2026-06-01",
      "traveler_count": 2,
      "preferences": ["历史古迹", "美食"]
    }
  }'
```

### 3. 任务分解

```bash
curl -X POST "http://127.0.0.1:9091/api/v1/task/decompose" \
  -H "Content-Type: application/json" \
  -d '{
    "requirement_id": "req_xxx",
    "structured_requirement": {
      "city_name": "北京",
      "travel_days": 3,
      "total_budget": 5000,
      "travel_date": "2026-06-01",
      "traveler_count": 2,
      "preferences": ["历史古迹"]
    }
  }'
```

### 4. 行程管理与收藏 ⭐

```bash
# 创建行程
curl -X POST "http://127.0.0.1:9091/api/v1/itinerary/create" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "title": "北京三日游",
    "total_budget": 5000,
    "day_plans": [...]
  }'

# 收藏行程 ⭐ 新功能
curl -X POST "http://127.0.0.1:9091/api/v1/itinerary/{itinerary_id}/favorite"

# 查询收藏的行程 ⭐ 新功能
curl "http://127.0.0.1:9091/api/v1/itinerary/user/user_001?is_favorite=true"

# 保存行程为草稿 ⭐ 新功能
curl -X POST "http://127.0.0.1:9091/api/v1/itinerary/{itinerary_id}/save"

# 发布行程 ⭐ 新功能
curl -X POST "http://127.0.0.1:9091/api/v1/itinerary/{itinerary_id}/publish"
```

---

## API接口说明

### 新增/修改的接口

#### 1. 行程收藏接口 ⭐

**POST** `/api/v1/itinerary/{itinerary_id}/favorite`

切换行程的收藏状态

**响应:**
```json
{
  "code": 200,
  "msg": "行程已收藏",
  "data": {
    "itinerary_id": "xxx",
    "is_favorite": true
  }
}
```

#### 2. 查询收藏的行程 ⭐

**GET** `/api/v1/itinerary/user/{user_id}?is_favorite=true`

只返回用户收藏的行程

#### 3. 保存行程为草稿 ⭐

**POST** `/api/v1/itinerary/{itinerary_id}/save`

将行程状态改为 `saved`

#### 4. 发布行程 ⭐

**POST** `/api/v1/itinerary/{itinerary_id}/publish`

将行程状态改为 `published`

#### 5. 带过滤的酒店查询 ⭐

**GET** `/api/v1/static/hotels/{city_name}?min_star=4&max_price=1000&price_range=luxury`

支持星级、价格、价格区间过滤

#### 6. 带过滤的餐厅查询 ⭐

**GET** `/api/v1/static/restaurants/{city_name}?cuisine_type=川菜&max_price=100`

支持菜系类型、人均消费过滤

---

## 数据库表结构

### 业务数据表

#### user_requirements（用户需求表）

| 字段 | 类型 | 说明 |
|------|------|------|
| requirement_id | VARCHAR(50) | 主键，需求ID |
| user_id | VARCHAR(50) | 用户ID |
| requirement_data | JSONB | 需求数据JSON |
| status | VARCHAR(20) | 状态：pending/parsed/processing/completed |
| parsed_keywords | JSONB | 解析后的关键词 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

#### tasks（任务表）

| 字段 | 类型 | 说明 |
|------|------|------|
| task_id | VARCHAR(50) | 主键，任务ID |
| batch_id | VARCHAR(50) | 批次ID |
| requirement_id | VARCHAR(50) | 外键，关联需求 |
| agent_type | VARCHAR(50) | 智能体类型 |
| parameters | JSONB | 任务参数 |
| status | VARCHAR(20) | 状态：pending/running/success/failed |
| result | JSONB | 任务结果 |
| error | TEXT | 错误信息 |
| progress | FLOAT | 进度百分比 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

#### itineraries（行程表）⭐

| 字段 | 类型 | 说明 |
|------|------|------|
| itinerary_id | VARCHAR(50) | 主键，行程ID |
| user_id | VARCHAR(50) | 用户ID |
| requirement_id | VARCHAR(50) | 外键，关联需求 |
| title | VARCHAR(200) | 行程标题 |
| day_plans | JSONB | 每日计划JSON数组 |
| total_budget | DECIMAL(10,2) | 总预算 |
| actual_cost | DECIMAL(10,2) | 实际花费 |
| status | VARCHAR(20) | 状态：draft/saved/published |
| **is_favorite** | **BOOLEAN** | **是否收藏** ⭐ |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

---

## 常见问题

### Q1: 如何确认数据已存入数据库？

```sql
-- 连接数据库
psql -U postgres -d travel_planner

-- 查看各表数据量
SELECT 'UserRequirements' as table_name, COUNT(*) FROM user_requirements
UNION ALL SELECT 'Tasks', COUNT(*) FROM tasks
UNION ALL SELECT 'Itineraries', COUNT(*) FROM itineraries;
```

### Q2: 服务重启后数据还在吗？

✅ **是的！** 所有数据都存储在PostgreSQL数据库中，服务重启不会丢失。

可以通过以下测试验证：
1. 创建一个行程并收藏
2. 重启服务（Ctrl+C 停止，再运行 `python src/index.py`）
3. 再次查询该用户的收藏行程，数据依然存在

### Q3: 如何实现"保存到收藏夹"功能？

前端调用收藏接口即可：

```javascript
// 收藏行程
async function toggleFavorite(itineraryId) {
  const response = await fetch(
    `http://127.0.0.1:9091/api/v1/itinerary/${itineraryId}/favorite`,
    { method: 'POST' }
  );
  const data = await response.json();
  console.log('收藏状态:', data.data.is_favorite);
}

// 查询收藏的行程
async function getFavoriteItineraries(userId) {
  const response = await fetch(
    `http://127.0.0.1:9091/api/v1/itinerary/user/${userId}?is_favorite=true`
  );
  const data = await response.json();
  return data.data.itineraries;
}
```

### Q4: 如何添加更多真实数据？

编辑 `database_schema.sql` 文件，在"插入示例基础数据"部分添加更多INSERT语句，然后重新执行脚本。

或者编写Python脚本批量导入数据：

```python
from src.database import SessionLocal
from src.models.db_models import Attraction

db = SessionLocal()

# 批量插入景点
new_attraction = Attraction(
    attraction_id="beijing_summer_palace",
    name="颐和园",
    city_id="beijing",
    category="park",
    description="皇家园林博物馆",
    ticket_price=30.0,
    rating=4.7
)

db.add(new_attraction)
db.commit()
db.close()
```

### Q5: 数据库性能如何优化？

当前已实施的优化：
- ✅ 为常用查询字段创建索引
- ✅ 使用JSONB类型存储动态数据
- ✅ 使用全文搜索索引（GIN + tsvector）
- ✅ 外键约束保证数据完整性

后续可优化：
- 添加缓存层（Redis）
- 分页查询大数据集
- 定期清理过期数据

### Q6: 如何备份数据库？

```bash
# 备份
pg_dump -U postgres travel_planner > backup_$(date +%Y%m%d).sql

# 恢复
psql -U postgres -d travel_planner < backup_20260524.sql
```

---

## 下一步工作

### 已完成 ✅
- ✅ 数据库模型设计（8个表）
- ✅ 数据库服务层封装
- ✅ 路由改造（需求/任务/行程/静态数据）
- ✅ 收藏夹功能实现
- ✅ 基础数据导入（5城+景点+酒店+餐厅）
- ✅ 完整测试脚本

### 待完成 📋
- [ ] 智能体模块接入数据库（从数据库读取真实推荐数据）
- [ ] 前端页面集成收藏功能
- [ ] 行程分享功能
- [ ] 用户评价系统
- [ ] 数据统计分析面板

---

## 技术支持

如遇问题，请检查：
1. PostgreSQL服务是否启动
2. 数据库连接配置（`.env`文件）
3. 查看后端日志输出
4. 运行测试脚本定位问题

**相关文档:**
- `README.md` - 项目总览
- `docs/API_INTERFACES_COMPLETE.md` - API接口文档
- `scripts/test_full_integration.py` - 完整功能测试

---

**最后更新**: 2026-05-24  
**版本**: v2.0.0  
**状态**: ✅ 数据库集成完成，所有核心功能已实现