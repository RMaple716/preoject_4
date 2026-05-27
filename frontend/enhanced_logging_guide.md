# 增强日志系统使用指南

## 概述

已为前端项目添加了增强的日志系统，可以直观地查看API请求、响应和数据流。

## 快速开始

### 1. 使用增强的API客户端

将现有的 `api.ts` 替换为 `api_enhanced.ts`：

```typescript
// 修改前
import apiClient from './services/api';

// 修改后
import apiClient from './services/api_enhanced';
```

### 2. 在组件中使用日志

```typescript
import { logger } from '../utils/logger';

const MyComponent = () => {
  useEffect(() => {
    // 记录组件挂载
    logger.componentLifecycle('MyComponent', 'mount');

    // 记录数据流
    logger.dataFlow('MyComponent', '接收数据', someData);

    // 记录信息
    logger.info('MyComponent', '操作描述', { key: 'value' });

    // 记录成功
    logger.success('MyComponent', '操作成功');

    // 记录警告
    logger.warn('MyComponent', '警告信息', { warning: 'details' });

    // 记录错误
    logger.error('MyComponent', '错误信息', error);
  }, []);

  return <div>...</div>;
};
```

## 日志类型说明

### 1. API调用日志 🌐

自动记录所有API请求：

```
🌐 API调用 - API
  方法: GET
  URL: /api/v1/itinerary/xxx
  请求数据: undefined
```

### 2. API响应日志 📥

自动记录所有API响应：

```
📥 API响应 - API (绿色表示成功，红色表示失败)
  状态码: 200
  响应数据: {...}
```

### 3. 数据流日志 📊

记录数据在组件间的流动：

```
📊 数据流 - ComponentName - 步骤名称
  数据类型: object
  数据内容: {...}
  对象键: ['key1', 'key2', ...]
```

### 4. 组件生命周期日志 🔄

记录组件的生命周期：

```
🔄 组件生命周期 - ComponentName (绿色=挂载，蓝色=更新，红色=卸载)
  阶段: mount
  Props: {...}
```

## 查看日志

### 1. 打开浏览器控制台

按 F12 或右键选择"检查" → "Console" 标签

### 2. 日志分组

日志会自动分组，可以展开/折叠：
- 点击分组标题左侧的箭头展开/折叠
- 不同类型的日志使用不同的颜色和图标

### 3. 过滤日志

在控制台过滤框中输入关键词：
```
API          // 只显示API相关日志
MyComponent  // 只显示特定组件的日志
ERROR        // 只显示错误日志
```

## 实际示例

### 示例1：查看API请求流程

1. 打开浏览器控制台
2. 执行一个API请求
3. 查看以下日志：
   - 🌐 API调用 - 请求开始
   - 📥 API响应 - 响应结果
   - 📊 数据流 - 数据传递

### 示例2：调试组件

```typescript
const MyComponent = ({ data }) => {
  useEffect(() => {
    logger.componentLifecycle('MyComponent', 'mount', { data });

    // 处理数据
    const processed = processData(data);
    logger.dataFlow('MyComponent', '数据处理完成', processed);

    // API调用
    fetchData().then(result => {
      logger.success('MyComponent', '数据获取成功', result);
    }).catch(error => {
      logger.error('MyComponent', '数据获取失败', error);
    });
  }, [data]);

  return <div>...</div>;
};
```

### 示例3：追踪数据流

```typescript
// 在数据转换函数中
const transformData = (rawData) => {
  logger.dataFlow('DataTransformer', '原始数据', rawData);

  const transformed = {
    id: rawData.id,
    name: rawData.name,
    // ...其他转换
  };

  logger.dataFlow('DataTransformer', '转换后数据', transformed);

  return transformed;
};
```

## 日志级别

### INFO（蓝色）
- 常规操作信息
- API调用
- 组件状态变化

### SUCCESS（绿色）
- 成功的操作
- API成功响应
- 数据处理完成

### WARN（黄色）
- 需要注意但不影响运行的情况
- 缺失某些可选数据
- 降级方案触发

### ERROR（红色）
- 错误和异常
- API失败
- 数据处理错误

## 最佳实践

1. **在关键步骤添加日志**
   - API调用前后
   - 数据转换
   - 组件生命周期

2. **提供有用的上下文**
   ```typescript
   // 好的做法
   logger.info('Component', '操作描述', { 
     id: data.id, 
     status: data.status 
   });

   // 不好的做法
   logger.info('Component', '操作');
   ```

3. **使用合适的日志级别**
   - 常规信息用 info
   - 成功用 success
   - 警告用 warn
   - 错误用 error

4. **避免过度日志**
   - 不要在循环中输出大量日志
   - 避免记录敏感信息
   - 生产环境自动禁用

## 故障排查

### 问题：看不到日志

**检查清单**：
1. 确认在开发环境（NODE_ENV=development）
2. 检查浏览器控制台是否打开
3. 确认没有过滤规则屏蔽日志
4. 检查logger是否正确导入

### 问题：日志颜色不显示

**解决方案**：
1. 使用现代浏览器（Chrome、Firefox、Edge）
2. 检查控制台设置是否启用颜色
3. 清除浏览器缓存

### 问题：日志太多

**解决方案**：
1. 使用控制台过滤功能
2. 只在关键位置添加日志
3. 使用日志级别过滤

## 总结

增强的日志系统提供了：
- 🌐 API请求/响应的完整追踪
- 📊 数据流的可视化
- 🔄 组件生命周期的监控
- 🎨 彩色和分组的日志输出
- 🔍 便于调试和问题排查

合理使用日志系统可以大大提升开发效率和问题定位速度。
