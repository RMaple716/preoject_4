/**
 * 地图调试工具
 * 用于诊断高德地图无法展示的问题
 */

interface MapDebugInfo {
  scriptLoaded: boolean;
  scriptUrl: string;
  containerExists: boolean;
  containerSize: { width: number; height: number };
  mapInstanceExists: boolean;
  polylineData: any;
  apiKey: string;
  errors: string[];
}

class MapDebugger {
  private debugInfo: MapDebugInfo = {
    scriptLoaded: false,
    scriptUrl: '',
    containerExists: false,
    containerSize: { width: 0, height: 0 },
    mapInstanceExists: false,
    polylineData: null,
    apiKey: '',
    errors: []
  };

  /**
   * 检查高德地图脚本是否加载
   */
  checkScriptLoaded(): boolean {
    const script = document.querySelector('script[src*="webapi.amap.com"]');
    this.debugInfo.scriptLoaded = !!window.AMap;
    this.debugInfo.scriptUrl = script?.getAttribute('src') || '';

    console.log('%c[地图调试] 脚本检查:', 'color: #1890ff; font-weight: bold;', {
      已加载: this.debugInfo.scriptLoaded,
      URL: this.debugInfo.scriptUrl
    });

    return this.debugInfo.scriptLoaded;
  }

  /**
   * 检查地图容器
   */
  checkContainer(containerId: string): boolean {
    const container = document.getElementById(containerId);
    this.debugInfo.containerExists = !!container;

    if (container) {
      this.debugInfo.containerSize = {
        width: container.offsetWidth,
        height: container.offsetHeight
      };

      console.log('%c[地图调试] 容器检查:', 'color: #1890ff; font-weight: bold;', {
        容器存在: this.debugInfo.containerExists,
        宽度: this.debugInfo.containerSize.width,
        高度: this.debugInfo.containerSize.height,
        样式: window.getComputedStyle(container)
      });

      if (this.debugInfo.containerSize.width === 0 || this.debugInfo.containerSize.height === 0) {
        this.addError(`容器尺寸无效: ${this.debugInfo.containerSize.width}x${this.debugInfo.containerSize.height}`);
      }
    } else {
      this.addError(`容器不存在: ${containerId}`);
    }

    return this.debugInfo.containerExists;
  }

  /**
   * 检查地图实例
   */
  checkMapInstance(mapInstance: any): boolean {
    this.debugInfo.mapInstanceExists = !!mapInstance;

    console.log('%c[地图调试] 地图实例检查:', 'color: #1890ff; font-weight: bold;', {
      实例存在: this.debugInfo.mapInstanceExists,
      实例类型: mapInstance?.constructor?.name,
      实例方法: mapInstance ? Object.keys(Object.getPrototypeOf(mapInstance)) : []
    });

    return this.debugInfo.mapInstanceExists;
  }

  /**
   * 检查路线数据
   */
  checkPolylineData(polyline: any): boolean {
    this.debugInfo.polylineData = polyline;

    console.log('%c[地图调试] 路线数据检查:', 'color: #1890ff; font-weight: bold;', {
      数据存在: !!polyline,
      数据类型: typeof polyline,
      数据长度: polyline?.length,
      数据内容: polyline
    });

    if (!polyline) {
      this.addError('路线数据不存在');
    }

    return !!polyline;
  }

  /**
   * 检查API Key
   */
  checkApiKey(key: string): boolean {
    this.debugInfo.apiKey = key;

    console.log('%c[地图调试] API Key检查:', 'color: #1890ff; font-weight: bold;', {
      Key存在: !!key,
      Key长度: key?.length,
      Key前缀: key?.substring(0, 10) + '...'
    });

    if (!key) {
      this.addError('API Key不存在');
    }

    return !!key;
  }

  /**
   * 添加错误信息
   */
  private addError(message: string) {
    this.debugInfo.errors.push(message);
    console.error(`%c[地图调试] 错误: ${message}`, 'color: #ff4d4f; font-weight: bold;');
  }

  /**
   * 执行完整诊断
   */
  diagnose(options: {
    containerId?: string;
    mapInstance?: any;
    polyline?: any;
    apiKey?: string;
  }) {
    console.group('%c🗺️ 地图诊断报告', 'color: #722ed1; font-weight: bold; font-size: 14px;');

    console.log('%c开始诊断...', 'color: #1890ff; font-weight: bold;');

    // 1. 检查脚本
    this.checkScriptLoaded();

    // 2. 检查容器
    if (options.containerId) {
      this.checkContainer(options.containerId);
    }

    // 3. 检查地图实例
    if (options.mapInstance) {
      this.checkMapInstance(options.mapInstance);
    }

    // 4. 检查路线数据
    if (options.polyline !== undefined) {
      this.checkPolylineData(options.polyline);
    }

    // 5. 检查API Key
    if (options.apiKey) {
      this.checkApiKey(options.apiKey);
    }

    // 6. 输出诊断结果
    this.printSummary();

    console.groupEnd();

    return this.debugInfo;
  }

  /**
   * 输出诊断摘要
   */
  private printSummary() {
    console.log('%c=== 诊断摘要 ===', 'color: #722ed1; font-weight: bold;');

    const status = {
      '✅ 脚本已加载': this.debugInfo.scriptLoaded,
      '✅ 容器存在': this.debugInfo.containerExists,
      '✅ 容器尺寸有效': this.debugInfo.containerSize.width > 0 && this.debugInfo.containerSize.height > 0,
      '✅ 地图实例存在': this.debugInfo.mapInstanceExists,
      '✅ 路线数据存在': !!this.debugInfo.polylineData,
      '✅ API Key存在': !!this.debugInfo.apiKey,
      '❌ 无错误': this.debugInfo.errors.length === 0
    };

    Object.entries(status).forEach(([key, value]) => {
      const icon = value ? '✅' : '❌';
      const color = value ? '#52c41a' : '#ff4d4f';
      console.log(`%c${icon} ${key}`, `color: ${color}; font-weight: bold;`);
    });

    if (this.debugInfo.errors.length > 0) {
      console.log('%c发现的问题:', 'color: #ff4d4f; font-weight: bold;');
      this.debugInfo.errors.forEach((error, index) => {
        console.log(`%c${index + 1}. ${error}`, 'color: #ff4d4f;');
      });
    }

    // 7. 提供建议
    this.provideSuggestions();
  }

  /**
   * 提供修复建议
   */
  private provideSuggestions() {
    console.log('%c=== 修复建议 ===', 'color: #722ed1; font-weight: bold;');

    if (!this.debugInfo.scriptLoaded) {
      console.log('%c1. 高德地图脚本未加载', 'color: #faad14; font-weight: bold;');
      console.log('   解决方案:');
      console.log('   - 检查网络连接');
      console.log('   - 确认API Key有效');
      console.log('   - 检查脚本URL是否正确');
    }

    if (!this.debugInfo.containerExists) {
      console.log('%c2. 地图容器不存在', 'color: #faad14; font-weight: bold;');
      console.log('   解决方案:');
      console.log('   - 确认容器ID正确');
      console.log('   - 检查组件是否正确渲染');
    }

    if (this.debugInfo.containerExists && 
        (this.debugInfo.containerSize.width === 0 || this.debugInfo.containerSize.height === 0)) {
      console.log('%c3. 地图容器尺寸无效', 'color: #faad14; font-weight: bold;');
      console.log('   解决方案:');
      console.log('   - 确保容器有明确的宽度和高度');
      console.log('   - 检查CSS样式');
      console.log('   - 确保容器在DOM中可见');
    }

    if (!this.debugInfo.mapInstanceExists) {
      console.log('%c4. 地图实例未创建', 'color: #faad14; font-weight: bold;');
      console.log('   解决方案:');
      console.log('   - 确认在组件挂载后初始化地图');
      console.log('   - 检查初始化代码是否执行');
      console.log('   - 查看控制台是否有JavaScript错误');
    }

    if (!this.debugInfo.polylineData) {
      console.log('%c5. 路线数据缺失', 'color: #faad14; font-weight: bold;');
      console.log('   解决方案:');
      console.log('   - 检查后端API响应');
      console.log('   - 确认数据转换正确');
      console.log('   - 验证数据结构');
    }

    if (!this.debugInfo.apiKey) {
      console.log('%c6. API Key缺失', 'color: #faad14; font-weight: bold;');
      console.log('   解决方案:');
      console.log('   - 配置有效的API Key');
      console.log('   - 确认Key已开通Web端服务');
      console.log('   - 检查域名白名单');
    }
  }
}

export const mapDebugger = new MapDebugger();
