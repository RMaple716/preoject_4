# 数据格式更新说明

## 更新日期
2024-01-01

## 更新概述
为了确保智能体输出与前端数据模型的一致性,我们对以下内容进行了更新:

### 1. 后端智能体输出格式

#### 景点智能体 (AttractionsAgent)
```json
{
  "attractions": [
    {
      "attraction_id": "att_001",
      "name": "景点名称",
      "city_name": "城市名称",
      "location": "景点地址",
      "description": "景点描述",
      "recommended_duration": "游览时长",
      "visit_time_slot": "morning/afternoon/evening",
      "ticket_price": 门票价格,
      "rating": 评分,
      "opening_hours": "营业时间",
      "tags": ["标签1", "标签2"]
    }
  ]
}
```

#### 住宿智能体 (HotelAgent)
```json
{
  "hotels": [
    {
      "hotel_id": "hotel_001",
      "name": "酒店名称",
      "city_name": "城市名称",
      "location": "详细地址",
      "price_per_night": 每晚价格,
      "rating": 评分,
      "amenities": ["设施1", "设施2"]
    }
  ]
}
```

#### 美食智能体 (FoodAgent)
```json
{
  "restaurants": [
    {
      "restaurant_id": "rest_001",
      "name": "餐厅名称",
      "city_name": "城市名称",
      "location": "餐厅地址",
      "cuisine_type": "菜系类型",
      "avg_price": 人均消费,
      "rating": 评分,
      "specialties": ["特色菜1", "特色菜2"]
    }
  ]
}
```

#### 交通智能体 (TransportAgent)
```json
{
  "transport_options": [
    {
      "transport_id": "trans_001",
      "type": "flight/train/bus/subway/taxi",
      "from": "起点名称",
      "to": "终点名称",
      "departure_time": "出发时间",
      "arrival_time": "到达时间",
      "duration": "预计时长",
      "price": 价格
    }
  ]
}
```

### 2. 前端类型定义更新

#### 景点类型 (Attraction)
- 新增 `attraction_id` 字段
- 新增 `city_name` 字段
- 新增 `visit_time_slot` 字段
- 新增 `tags` 字段
- `location` 改为必填字段
- `ticket_price` 改为可选字段

#### 酒店类型 (Hotel)
- 新增 `hotel_id` 字段
- 新增 `city_name` 字段
- `location` 改为必填字段
- 所有字段改为可选

#### 餐厅类型 (Restaurant)
- 新增 `restaurant_id` 字段
- 新增 `city_name` 字段
- 新增 `specialties` 字段
- 新增 `meal_type` 字段
- 新增 `meal_time` 字段
- 新增 `time` 字段
- 新增 `start_time` 字段
- 新增 `end_time` 字段
- 新增 `duration` 字段
- `location` 改为必填字段

#### 交通类型 (Transport)
- 新增 `transport_id` 字段
- `type` 改为枚举类型
- 新增 `from` 和 `to` 字段
- 所有字段改为可选

### 3. 数据转换工具

创建了 `frontend/src/utils/dataTransformers.ts` 文件,包含以下转换函数:
- `transformAttraction` - 转换单个景点
- `transformHotel` - 转换单个酒店
- `transformRestaurant` - 转换单个餐厅
- `transformTransport` - 转换单个交通
- `transformAttractions` - 批量转换景点
- `transformHotels` - 批量转换酒店
- `transformRestaurants` - 批量转换餐厅
- `transformTransports` - 批量转换交通
- `transformDayPlan` - 转换单日行程
- `transformDayPlans` - 批量转换每日行程

### 4. 行程整合模块更新

#### integration.py
- 为景点、酒店、餐厅数据自动添加 `city_name` 字段
- 更新费用计算逻辑:
  - 餐饮价格字段从 `avg_price_per_person` 改为 `avg_price`
  - 交通价格字段从 `cost` 改为 `price`

### 5. 前端组件更新

#### ItineraryDetail.tsx
- 更新景点类型定义,添加新字段
- 更新餐饮类型定义,添加新字段
- 更新住宿信息组件:
  - 显示酒店设施列表
  - 使用 `location` 字段替代 `address`
- 更新餐饮卡片显示逻辑:
  - 显示餐厅位置
  - 显示评分
  - 使用 `avg_price` 字段

## 兼容性处理

为了确保向后兼容,数据转换工具会自动处理旧格式的数据:
- 支持旧字段名到新字段名的映射
- 支持可选字段的默认值设置
- 支持字段类型的自动转换

## 使用建议

1. **新开发**: 直接使用新的数据格式和类型定义
2. **旧代码**: 使用数据转换工具处理旧格式的数据
3. **API调用**: 确保前端API调用使用新的请求参数格式

## 测试建议

1. 测试各智能体的输出是否符合新格式
2. 测试前端组件是否能正确显示新格式的数据
3. 测试数据转换工具是否能正确处理旧格式数据
4. 测试行程整合功能是否正常工作

## 后续优化方向

1. 添加数据验证逻辑
2. 添加数据格式转换的错误处理
3. 优化数据转换性能
4. 添加单元测试
