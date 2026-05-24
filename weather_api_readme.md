# 高德天气API配置说明

## 功能概述

项目已集成高德地图天气API,可以获取实时天气和天气预报信息。

## API接口

### 1. 获取实时天气

**接口地址**: `GET /api/v1/weather/current`

**请求参数**:
- `city`: 城市名称或adcode (必填)

**返回数据**:
```json
{
  "code": 200,
  "msg": "获取成功",
  "data": {
    "province": "北京",
    "city": "北京市",
    "adcode": "110000",
    "weather": "晴",
    "temperature": "20",
    "winddirection": "西",
    "windpower": "3",
    "humidity": "45",
    "reporttime": "2024-01-15 14:00:00"
  }
}
```

### 2. 获取天气预报

**接口地址**: `GET /api/v1/weather/forecast`

**请求参数**:
- `city`: 城市名称或adcode (必填)

**返回数据**:
```json
{
  "code": 200,
  "msg": "获取成功",
  "data": {
    "city": "北京市",
    "adcode": "110000",
    "province": "北京",
    "reporttime": "2024-01-15 14:00:00",
    "casts": [
      {
        "date": "2024-01-15",
        "week": "星期一",
        "dayweather": "晴",
        "nightweather": "晴",
        "daytemp": "20",
        "nighttemp": "5",
        "daywind": "西",
        "nightwind": "西",
        "daypower": "3",
        "nightpower": "3"
      }
    ]
  }
}
```

## 配置步骤

### 1. 获取高德地图API密钥

1. 访问[高德开放平台](https://lbs.amap.com/)
2. 注册/登录账号
3. 进入控制台,创建应用
4. 在应用中添加"Web服务"类型的Key
5. 记录下生成的Key

### 2. 配置环境变量

在项目根目录创建或编辑 `.env` 文件,添加以下内容:

```bash
AMAP_API_KEY=你的高德地图API密钥
```

### 3. 重启后端服务

```bash
cd E:\Important_File\coding
ew_project
python src/index.py
```

## 前端使用示例

```typescript
import { weatherApi } from '../services';

// 获取实时天气
const currentWeather = await weatherApi.getCurrent('北京');
console.log(currentWeather);

// 获取天气预报
const forecast = await weatherApi.getForecast('北京');
console.log(forecast);
```

## 注意事项

1. **API密钥安全**: 不要将API密钥提交到代码仓库,使用环境变量管理
2. **调用频率**: 高德地图API有调用频率限制,请注意控制调用次数
3. **城市名称**: 支持城市名称(如"北京")和adcode(如"110000")
4. **错误处理**: 如果未配置API密钥,API会返回错误信息

## 测试API

可以使用以下命令测试天气API:

```bash
# 获取实时天气
curl "http://127.0.0.1:9091/api/v1/weather/current?city=北京"

# 获取天气预报
curl "http://127.0.0.1:9091/api/v1/weather/forecast?city=北京"
```

## 集成建议

可以在以下场景中使用天气API:

1. **行程规划**: 在规划行程时显示目的地天气
2. **行程详情**: 在行程详情页面显示出行日期的天气
3. **智能推荐**: 根据天气情况推荐室内/室外活动
4. **出行提醒**: 根据天气预报提供出行建议

## 常见问题

### Q: 为什么返回"未配置高德地图API密钥"错误?

A: 请检查 `.env` 文件中是否正确配置了 `AMAP_API_KEY`。

### Q: 为什么获取不到天气信息?

A: 请检查:
1. API密钥是否正确
2. 城市名称是否正确
3. 网络连接是否正常
4. API调用次数是否超限

### Q: 如何获取城市的adcode?

A: 可以通过高德地图的地理编码API获取,或者直接使用城市名称,系统会自动识别。
