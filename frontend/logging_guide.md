# 前端日志系统使用指南

## 概述

本项目集成了一个强大的前端日志系统，帮助开发者直观地查看和分析前端运行过程中的数据流、API调用、组件生命周期等关键信息。

## 日志工具位置

```
frontend/src/utils/logger.ts
```

## 日志类型

### 1. 基础日志

#### Info（信息日志）
```typescript
logger.info('ComponentName', '操作描述', data);
```
- 用途：记录常规操作和信息
- 颜色：蓝色
- 示例：
```typescript
logger.info('AMapNavigation', '开始初始化地图', { from: '起点', to: '终点' });
```

#### Success（成功日志）
```typescript
logger.success('ComponentName', '操作成功', data);
```
- 用途：记录成功的操作
- 颜色：绿色
- 示例：
```typescript
logger.success('AMapNavigation', '地图实例创建成功');
```

#### Warn（警告日志）
```typescript
logger.warn('ComponentName', '警告信息', data);
```
- 用途：记录需要注意但不影响运行的情况
- 颜色：黄色
- 示例：
```typescript
logger.warn('AMapNavigation', '组件未显示或容器未就绪', { visible: false });
```

#### Error（错误日志）
```typescript
logger.error('ComponentName', '错误信息', error);
```
- 用途：记录错误和异常
- 颜色：红色
- 示例：
```typescript
logger.error('AMapNavigation', '绘制路线失败', error);
```

### 2. 专用日志

#### 数据流日志
```typescript
logger.dataFlow('ComponentName', '步骤名称', data);
```
- 用途：记录数据在组件间的流动
- 特点：自动显示数据类型、内容、长度等信息
- 示例：
```typescript
logger.dataFlow('NavigationInfo', '接收交通数据', transportData);
```

#### API调用日志
```typescript
logger.apiCall('ComponentName', 'HTTP方法', 'URL', data);
```
- 用途：记录API调用
- 示例：
```typescript
logger.apiCall('ItineraryAPI', 'GET', '/api/v1/itinerary/123');
```

#### API响应日志
```typescript
logger.apiResponse('ComponentName', status, data);
```
- 用途：记录API响应
- 示例：
```typescript
logger.apiResponse('ItineraryAPI', 200, itineraryData);
```

#### 组件生命周期日志
```typescript
logger.componentLifecycle('ComponentName', '阶段', props);
```
- 用途：记录组件生命周期
- 阶段：mount（挂载）、update（更新）、unmount（卸载）
- 示例：
```typescript
logger.componentLifecycle('AMapNavigation', 'mount', { visible, polyline });
```

## 使用示例

### 示例1：地图组件日志

```typescript
import { logger } from '../utils/logger';

const AMapNavigation: React.FC<AMapNavigationProps> = ({ visible, polyline, from, to }) => {
  useEffect(() => {
    // 记录组件挂载
    logger.componentLifecycle('AMapNavigation', 'mount', { visible, polyline });

    // 记录地图初始化
    logger.info('AMapNavigation', '开始初始化地图');

    try {
      // 记录路线解码
      const path = window.AMap.GeometryUtil.decodePath(polyline);
      logger.info('AMapNavigation', '路线解码成功', { 
        pathLength: path.length,
        startPoint: path[0],
        endPoint: path[path.length - 1]
      });

      // 记录成功
      logger.success('AMapNavigation', '路线绘制完成');
    } catch (error) {
      // 记录错误
      logger.error('AMapNavigation', '路线绘制失败', error);
    }
  }, [visible, polyline]);

  return <div>...</div>;
};
```

### 示例2：API调用日志

```typescript
import { logger } from '../utils/logger';

const fetchItinerary = async (id: string) => {
  try {
    // 记录API调用
    logger.apiCall('ItineraryAPI', 'GET', `/api/v1/itinerary/${id}`);

    const response = await fetch(`/api/v1/itinerary/${id}`);
    const data = await response.json();

    // 记录API响应
    logger.apiResponse('ItineraryAPI', response.status, data);

    // 记录数据流
    logger.dataFlow('ItineraryAPI', '接收行程数据', data);

    return data;
  } catch (error) {
    logger.error('ItineraryAPI', '获取行程失败', error);
    throw error;
  }
};
```

### 示例3：数据转换日志

```typescript
import { logger } from '../utils/logger';

const transformTransport = (transport: any) => {
  logger.dataFlow('DataTransformer', '开始转换交通数据', transport);

  const transformed = {
    id: transport.transport_id,
    from: transport.from,
    to: transport.to,
    type: transport.type,
    polyline: transport.polyline,
    steps: transport.steps
  };

  logger.dataFlow('DataTransformer', '转换完成', transformed);

  return transformed;
};
```

## 浏览器控制台查看日志

### Chrome DevTools

1. 打开浏览器开发者工具（F12）
2. 切换到 Console 标签
3. 查看彩色日志输出

### 日志分组

日志系统使用 `console.group` 对相关日志进行分组，可以展开/折叠查看详细信息：

- 📊 数据流日志（紫色）
- 🌐 API调用日志（青色）
- 📥 API响应日志（绿色/红色）
- 🔄 组件生命周期日志（绿色/蓝色/红色）

### 过滤日志

在控制台过滤框中输入关键词可以过滤特定日志：

```
AMapNavigation  // 只显示地图相关日志
API            // 只显示API相关日志
ERROR          // 只显示错误日志
```

## 开发环境控制

日志系统只在开发环境（NODE_ENV=development）中输出，生产环境自动禁用。

### 环境配置

```bash
# 开发环境
NODE_ENV=development npm start

# 生产环境
NODE_ENV=production npm run build
```

## 最佳实践

1. **合理使用日志级别**
   - 使用 `info` 记录常规操作
   - 使用 `success` 记录成功的关键操作
   - 使用 `warn` 记录需要注意的情况
   - 使用 `error` 记录错误和异常

2. **使用专用日志**
   - 数据流动使用 `dataFlow`
   - API调用使用 `apiCall` 和 `apiResponse`
   - 组件生命周期使用 `componentLifecycle`

3. **提供上下文信息**
   - 在日志中包含相关的数据
   - 使用有意义的标签和消息

4. **避免过度日志**
   - 不要在循环中输出大量日志
   - 避免记录敏感信息

## 故障排查

### 问题：日志不显示

**解决方案**：
1. 确认 NODE_ENV=development
2. 检查浏览器控制台是否打开
3. 确认没有过滤规则屏蔽日志

### 问题：日志颜色不显示

**解决方案**：
1. 确认使用的是现代浏览器
2. 检查控制台设置是否启用了颜色输出

### 问题：日志分组无法展开

**解决方案**：
1. 点击分组标题左侧的箭头
2. 确认浏览器支持 console.group

## 总结

本日志系统提供了强大的调试和问题排查能力，通过合理使用可以：
- 快速定位问题
- 追踪数据流
- 监控API调用
- 了解组件生命周期
- 提升开发效率

建议在开发过程中充分利用日志系统，特别是在处理复杂的数据流和API交互时。
