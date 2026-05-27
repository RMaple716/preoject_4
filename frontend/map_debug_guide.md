# 地图调试工具使用指南

## 概述

已创建地图调试工具和增强版地图组件，帮助您快速诊断和解决地图无法展示的问题。

## 文件说明

1. **mapDebugger.ts** - 地图调试工具
   - 位置：`frontend/src/utils/mapdebugger.ts`
   - 功能：系统化检查地图加载和渲染的各个环节

2. **AMapNavigationDebug.tsx** - 增强版地图组件
   - 位置：`frontend/src/components/amapnavigationdebug.tsx`
   - 功能：集成调试工具的地图组件

## 使用方法

### 方式1：使用调试版地图组件

将现有的地图组件替换为调试版：

```typescript
// 修改前
import AMapNavigation from './components/amapnavigation';

// 修改后
import AMapNavigationDebug from './components/amapnavigationdebug';

// 使用
<AMapNavigationDebug
  visible={visible}
  onClose={handleClose}
  polyline={polyline}
  from={from}
  to={to}
  type={type}
/>
```

### 方式2：手动运行诊断

在任何需要的地方导入并使用调试工具：

```typescript
import { mapDebugger } from '../utils/mapdebugger';

// 运行完整诊断
const debugResult = mapDebugger.diagnose({
  containerId: 'amap-container',
  mapInstance: mapInstance,
  polyline: polylineData,
  apiKey: 'your-api-key'
});

console.log('诊断结果:', debugResult);
```

## 诊断检查项

调试工具会自动检查以下内容：

### 1. 高德地图脚本加载
- ✅ 检查脚本是否已加载
- ✅ 检查脚本URL是否正确
- ✅ 检查window.AMap对象是否存在

### 2. 地图容器
- ✅ 检查容器元素是否存在
- ✅ 检查容器尺寸是否有效
- ✅ 检查容器CSS样式

### 3. 地图实例
- ✅ 检查地图实例是否创建
- ✅ 检查实例类型和方法

### 4. 路线数据
- ✅ 检查polyline数据是否存在
- ✅ 检查数据类型和长度
- ✅ 检查数据内容

### 5. API Key
- ✅ 检查API Key是否存在
- ✅ 检查Key长度和格式

## 诊断报告示例

运行诊断后，控制台会输出详细的诊断报告：

```
🗺️ 地图诊断报告
  开始诊断...

[地图调试] 脚本检查:
  已加载: true
  URL: https://webapi.amap.com/maps?v=2.0&key=...

[地图调试] 容器检查:
  容器存在: true
  宽度: 800
  高度: 600
  样式: {...}

[地图调试] 地图实例检查:
  实例存在: true
  实例类型: Map
  实例方法: [...]

[地图调试] 路线数据检查:
  数据存在: true
  数据类型: string
  数据长度: 1234
  数据内容: "..."

=== 诊断摘要 ===
✅ 脚本已加载
✅ 容器存在
✅ 容器尺寸有效
✅ 地图实例存在
✅ 路线数据存在
✅ API Key存在
❌ 无错误

=== 修复建议 ===
（如果有问题，会显示具体的修复建议）
```

## 常见问题及解决方案

### 问题1：高德地图脚本未加载

**症状**：
```
❌ 脚本已加载
```

**解决方案**：
1. 检查网络连接
2. 确认API Key有效
3. 检查脚本URL是否正确
4. 查看浏览器Network标签，确认脚本请求状态

### 问题2：地图容器不存在

**症状**：
```
❌ 容器存在
```

**解决方案**：
1. 确认容器ID正确
2. 检查组件是否正确渲染
3. 确认Modal已打开
4. 检查DOM结构

### 问题3：地图容器尺寸无效

**症状**：
```
❌ 容器尺寸有效
宽度: 0
高度: 0
```

**解决方案**：
1. 确保容器有明确的宽度和高度
2. 检查CSS样式
3. 确保容器在DOM中可见
4. 检查Modal是否已完全渲染

### 问题4：地图实例未创建

**症状**：
```
❌ 地图实例存在
```

**解决方案**：
1. 确认在组件挂载后初始化地图
2. 检查初始化代码是否执行
3. 查看控制台是否有JavaScript错误
4. 确认高德地图API已加载

### 问题5：路线数据缺失

**症状**：
```
❌ 路线数据存在
```

**解决方案**：
1. 检查后端API响应
2. 确认数据转换正确
3. 验证数据结构
4. 查看Network标签中的API响应

### 问题6：API Key无效

**症状**：
```
❌ API Key存在
```

**解决方案**：
1. 配置有效的API Key
2. 确认Key已开通Web端服务
3. 检查域名白名单
4. 联系高德地图客服

## 调试步骤

### 步骤1：打开浏览器控制台

按 F12 或右键选择"检查" → "Console" 标签

### 步骤2：运行诊断

点击地图Modal中的"运行诊断"按钮

### 步骤3：查看诊断报告

查看控制台输出的诊断报告，注意：
- ✅ 表示正常
- ❌ 表示有问题
- 黄色文字表示修复建议

### 步骤4：根据建议修复

根据诊断报告中的修复建议，逐一解决问题

### 步骤5：重新诊断

修复后，再次运行诊断，确认问题已解决

## 高级用法

### 自定义诊断

```typescript
import { mapDebugger } from '../utils/mapdebugger';

// 只检查脚本
mapDebugger.checkScriptLoaded();

// 只检查容器
mapDebugger.checkContainer('amap-container');

// 只检查地图实例
mapDebugger.checkMapInstance(mapInstance);

// 只检查路线数据
mapDebugger.checkPolylineData(polyline);

// 只检查API Key
mapDebugger.checkApiKey('your-api-key');
```

### 在组件中使用

```typescript
import { useEffect } from 'react';
import { mapDebugger } from '../utils/mapdebugger';

const MyComponent = () => {
  useEffect(() => {
    // 组件挂载后自动运行诊断
    mapDebugger.diagnose({
      containerId: 'map-container',
      mapInstance: mapInstance,
      polyline: polylineData,
      apiKey: 'your-api-key'
    });
  }, []);

  return <div>...</div>;
};
```

## 注意事项

1. **开发环境使用**：调试工具只在开发环境有效
2. **性能影响**：频繁运行诊断可能影响性能，建议在必要时使用
3. **敏感信息**：避免在生产环境输出API Key等敏感信息
4. **浏览器兼容性**：使用现代浏览器（Chrome、Firefox、Edge）

## 总结

地图调试工具提供了：
- 🗺️ 系统化的诊断流程
- ✅ 清晰的检查项
- 📋 详细的诊断报告
- 💡 具体的修复建议
- 🎯 快速定位问题

使用调试工具可以大大提升地图问题的排查效率，快速定位和解决问题。
