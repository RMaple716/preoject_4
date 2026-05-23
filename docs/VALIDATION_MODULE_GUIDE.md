# 规划校验模块使用指南

## 📋 模块概述

规划校验模块负责检查旅游行程的合理性，包括：
1. ✅ **时间冲突检测** - 检查活动时间是否重叠
2. ✅ **预算校验** - 检查总花费是否超出预算限制
3. ✅ **景点开放时间校验** - 检查游览时间是否在景点开放时间内

## 🎯 核心功能

### 1. 时间冲突检测

**功能**: 检测同一时间段内的活动是否存在时间重叠

**检测项**:
- ⏰ 活动时间重叠（错误级别）
- ⏰ 开始时间过早（早于6:00，警告级别）
- ⏰ 结束时间过晚（晚于23:00，警告级别）
- ⏰ 景点游览时长过短（少于30分钟，警告级别）
- ⏰ 景点游览时长过长（超过8小时，警告级别）
- ⏰ 每日总时长超限（超过12小时，警告级别）

**支持的时间格式**:
- `HH:MM` 格式：`"09:30"`, `"14:00"`
- 时间槽格式：`"上午"`, `"中午"`, `"下午"`, `"晚上"`
- 英文时间槽：`"morning"`, `"afternoon"`, `"evening"`

**支持的时长格式**:
- `"2小时"` → 120分钟
- `"30分钟"` → 30分钟
- `"2-3小时"` → 150分钟（取平均值）
- `"半天"` → 240分钟
- `"全天"` → 480分钟

### 2. 预算校验

**功能**: 计算行程总花费并与用户预算进行对比

**费用计算**:
```
总花费 = 景点门票总和 + 餐饮费用总和 + 交通费用总和
```

**校验规则**:
- 如果 `总花费 > 总预算`，生成错误级别冲突
- 提供调整建议："建议调整部分景点或选择更经济的餐厅"

### 3. 景点开放时间校验 ⭐ 新增

**功能**: 检查计划游览时间是否在景点开放时间内

**支持的开放时间格式**:
- `"08:30-17:00"` - 标准格式
- `"全天开放"` - 全天开放
- `"不开放"` / `"关闭"` - 不开放（跳过检查）

**检测类型**:
1. **完全超出开放时间** (error级别)
   - 游览时间完全在开放时间之外
   - 示例：景点08:30-17:00开放，计划07:00-09:00游览

2. **部分超出开放时间** (warning级别)
   - 游览时间部分在开放时间之外
   - 示例：景点08:30-17:00开放，计划08:00-10:00游览

**容错处理**:
- 如果景点没有 `opening_hours` 字段，自动跳过该景点的检查
- 如果开放时间格式无法解析，跳过该景点的检查

## 🔌 API接口

### 接口1: 时间冲突检测

**URL**: `POST /api/v1/validation/time-conflict`

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

### 接口2: 完整行程校验

**URL**: `POST /api/v1/validation/itinerary`

**请求参数**:
```json
{
  "day_plans": [
    {
      "day": 1,
      "date": "2026-05-20",
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
    "travel_date": "2026-05-20",
    "traveler_count": 2
  }
}
```

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
        "date": "2026-05-20"
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

## 🧪 测试方法

### 运行测试脚本

```bash
python test_opening_hours_validation.py
```

### 测试用例

1. **测试1**: 景点开放时间超出检测
   - 验证：游览时间早于开放时间能被正确检测

2. **测试2**: 正常开放时间无冲突
   - 验证：游览时间在开放范围内不会误报

3. **测试3**: 预算+开放时间综合测试
   - 验证：同时检测预算超出和开放时间冲突

4. **测试4**: 缺少开放时间信息
   - 验证：没有opening_hours字段的景点会被跳过

## 💡 使用示例

### Python调用示例

```python
import requests

# 完整行程校验
url = "http://127.0.0.1:9091/api/v1/validation/itinerary"

payload = {
    "day_plans": [...],
    "structured_requirement": {
        "total_budget": 5000,
        ...
    }
}

response = requests.post(url, json=payload)
result = response.json()

if result['code'] == 200:
    data = result['data']
    if not data['valid']:
        print("行程存在问题:")
        for conflict in data['conflicts']:
            print(f"  [{conflict['severity']}] {conflict['description']}")
        
        if data['suggestions']:
            print("\n建议:")
            for suggestion in data['suggestions']:
                print(f"  - {suggestion}")
    else:
        print("✓ 行程安排合理，无冲突")
```

### 前端集成示例

```typescript
// services/validationApi.ts
import api from './api';

export const validateItinerary = async (dayPlans: any[], structuredRequirement: any) => {
  const response = await api.post('/validation/itinerary', {
    day_plans: dayPlans,
    structured_requirement: structuredRequirement
  });
  
  return response.data;
};

// 在组件中使用
const validationResult = await validateItinerary(dayPlans, requirement);

if (!validationResult.data.valid) {
  // 显示冲突信息
  validationResult.data.conflicts.forEach(conflict => {
    message.warning(conflict.description);
  });
}
```

## 📊 冲突严重程度

| 严重程度 | 说明 | 处理方式 |
|---------|------|---------|
| `error` | 严重问题，必须修复 | 阻止行程保存，要求用户修改 |
| `warning` | 建议性问题 | 提示用户，但允许继续 |

## 🔍 冲突类型列表

### 时间相关
- `time_overlap` - 活动时间重叠 (error)
- `unreasonable_time` - 时间不合理 (warning)
- `too_short_duration` - 游览时间过短 (warning)
- `too_long_duration` - 游览时间过长 (warning)
- `overloaded_day` - 当日行程过载 (warning)

### 预算相关
- `budget_exceeded` - 预算超出 (error)

### 开放时间相关 ⭐ 新增
- `outside_opening_hours` - 完全超出开放时间 (error)
- `partial_outside_opening_hours` - 部分超出开放时间 (warning)

## 🚀 最佳实践

1. **数据完整性**: 尽量为景点提供 `opening_hours` 字段，以获得完整的校验
2. **时间格式**: 优先使用 `HH:MM` 格式，比时间槽更精确
3. **预算设置**: 设置合理的 `total_budget`，避免过于宽松或严格
4. **冲突处理**: 
   - 对 `error` 级别的冲突必须修复
   - 对 `warning` 级别的冲突可以根据实际情况决定是否调整
5. **建议参考**: 关注 `suggestions` 字段中的优化建议

## 📝 注意事项

1. **开放时间格式**: 目前仅支持 `HH:MM-HH:MM` 格式，复杂格式（如"周一闭馆"）暂不支持
2. **默认值**: 
   - 如果没有指定开始时间，默认为 09:00
   - 如果没有指定持续时间，默认为 2小时
   - 如果没有开放时间信息，跳过该景点的开放时间检查
3. **性能考虑**: 对于多天行程，校验会逐天进行，建议单次校验不超过10天
4. **时区问题**: 所有时间均按当地时间处理，不考虑时区转换

## 🔄 版本历史

- **v1.0** (2026-05-23): 初始版本，包含时间冲突检测和预算校验
- **v1.1** (2026-05-23): 新增景点开放时间校验功能

---

**相关文件**:
- 核心代码: `src/routes/validate.py`
- 测试脚本: `test_opening_hours_validation.py`
- 数据模型: `src/models/request.py`, `src/models/static_data.py`
