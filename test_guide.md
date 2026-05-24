# 天气API测试指南

## 快速开始

### 方法一:使用测试脚本

1. **配置API密钥**

   在项目根目录创建 `.env` 文件,添加:
   ```bash
   AMAP_API_KEY=你的高德地图API密钥
   ```

2. **运行测试脚本**

   ```bash
   cd E:\Important_File\coding
ew_project
   python test_weather_api.py
   ```

3. **查看测试结果**

   脚本会测试以下城市的天气:
   - 北京
   - 上海
   - 西安

   每个城市会测试:
   - 实时天气
   - 未来3天天气预报

### 方法二:使用curl命令

1. **启动后端服务**

   ```bash
   cd E:\Important_File\coding
ew_project
   python src/index.py
   ```

2. **测试实时天气API**

   ```bash
   curl "http://127.0.0.1:9091/api/v1/weather/current?city=北京"
   ```

3. **测试天气预报API**

   ```bash
   curl "http://127.0.0.1:9091/api/v1/weather/forecast?city=北京"
   ```

### 方法三:使用浏览器

1. **启动后端服务**

   ```bash
   cd E:\Important_File\coding
ew_project
   python src/index.py
   ```

2. **访问API文档**

   打开浏览器访问: http://127.0.0.1:9091/docs

3. **测试天气API**

   在API文档页面找到 `/api/v1/weather/current` 和 `/api/v1/weather/forecast` 接口,点击"Try it out"进行测试。

## 获取API密钥

1. 访问[高德开放平台](https://lbs.amap.com/)
2. 注册/登录账号
3. 进入控制台
4. 创建应用
5. 添加"Web服务"类型的Key
6. 复制生成的Key

## 测试示例

### 成功响应示例

**实时天气**:
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

**天气预报**:
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

### 错误响应示例

**未配置API密钥**:
```json
{
  "code": 400,
  "msg": "未配置高德地图API密钥",
  "data": null
}
```

**城市名称错误**:
```json
{
  "code": 400,
  "msg": "获取天气信息失败",
  "data": null
}
```

## 常见问题

### Q: 测试脚本报错"未配置高德地图API密钥"

A: 请检查:
1. 是否创建了 `.env` 文件
2. `.env` 文件中是否正确配置了 `AMAP_API_KEY`
3. `.env` 文件是否在项目根目录

### Q: curl命令返回错误

A: 请检查:
1. 后端服务是否已启动
2. 端口9091是否被占用
3. API密钥是否已配置

### Q: 测试脚本运行很慢

A: 这是因为需要多次调用高德API,属于正常现象。如果特别慢,可能是网络问题。

## 下一步

测试成功后,可以:

1. 在前端页面中集成天气显示功能
2. 在行程规划时考虑天气因素
3. 根据天气情况推荐室内/室外活动
4. 提供出行建议和提醒

## 更多信息

详细的使用说明请参考 `WEATHER_API_README.md`
