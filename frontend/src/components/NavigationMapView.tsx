import React, { useEffect, useRef, useState, useCallback } from 'react';
import { Card, Button, Tag, Space, Typography, Spin, Empty, Alert } from 'antd';
import { CarOutlined, EnvironmentOutlined, ArrowRightOutlined, AimOutlined } from '@ant-design/icons';

const { Text } = Typography;

// 高德地图配置
const AMAP_JS_API_KEY = import.meta.env.VITE_AMAP_JS_API_KEY || '44d5a1d0ff67c65b57f1d9bb7291850d';
const AMAP_SECURITY_JS_CODE = import.meta.env.VITE_AMAP_SECURITY_JS_CODE || '15dc86f3be21a7853129ca4a5b76e58c';

// ==================== 类型定义 ====================

interface NavigationData {
  from: string;
  to: string;
  type: string;
  fromLocation?: { lat: number; lng: number } | null;
  toLocation?: { lat: number; lng: number } | null;
}

/** 多路段：一个路段表示从某地到某地的一段行程 */
interface RouteSegment {
  from: string;
  to: string;
  type: string;
  fromLocation?: { lat: number; lng: number } | null;
  toLocation?: { lat: number; lng: number } | null;
}

interface LocationPoint {
  name: string;
  lat: number;
  lng: number;
  type: 'attraction' | 'hotel' | 'restaurant' | 'start' | 'end';
  day?: number;
}

interface NavigationMapViewProps {
  navigationData: NavigationData | null;
  allLocations?: LocationPoint[];
}

/** 多路段地图组件的 Props */
interface MultiRouteMapProps {
  segments: RouteSegment[];
  allLocations?: LocationPoint[];
  visible: boolean;
  onClose?: () => void;
}

// ==================== 工具函数 ====================

const getTransportTypeName = (type: string) => {
  switch (type) {
    case 'walking': return '步行';
    case 'driving': return '驾车';
    case 'transit': return '公交/地铁';
    case 'bicycling': return '骑行';
    default: return type;
  }
};

const getTransportTagColor = (type: string) => {
  switch (type) {
    case 'walking': return 'blue';
    case 'driving': return 'orange';
    case 'transit': return 'green';
    case 'bicycling': return 'purple';
    default: return 'default';
  }
};

const getTransportIcon = (type: string) => {
  switch (type) {
    case 'walking': return '🚶';
    case 'driving': return '🚗';
    case 'transit': return '🚇';
    case 'bicycling': return '🚴';
    default: return '🚗';
  }
};

const formatTime = (seconds: number): string => {
  if (!seconds || seconds <= 0) return '';
  const hours = Math.floor(seconds / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  if (hours > 0) return `${hours}小时${mins}分钟`;
  return `${mins}分钟`;
};

const formatDistance = (meters: number): string => {
  if (!meters || meters <= 0) return '';
  if (meters >= 1000) return `${(meters / 1000).toFixed(1)}公里`;
  return `${meters}米`;
};

// ==================== 高德地图 SDK 加载（单例） ====================
let amapLoadPromise: Promise<void> | null = null;

function loadAMapSDK(): Promise<void> {
  if (amapLoadPromise) return amapLoadPromise;
  amapLoadPromise = new Promise((resolve, reject) => {
    if ((window as any).AMap && (window as any).AMap.Map) { resolve(); return; }
    if (AMAP_SECURITY_JS_CODE) {
      (window as any)._AMapSecurityConfig = { securityJsCode: AMAP_SECURITY_JS_CODE };
    }
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = `https://webapi.amap.com/maps?v=2.0&key=${AMAP_JS_API_KEY}&plugin=AMap.ToolBar,AMap.Scale,AMap.Driving,AMap.Walking,AMap.Riding,AMap.Transfer`;
    script.onload = () => resolve();
    script.onerror = () => { amapLoadPromise = null; reject(new Error('高德地图API加载失败')); };
    document.head.appendChild(script);
  });
  return amapLoadPromise;
}

// ==================== 创建路线规划器 ====================
function createNavigator(mode: string, map: any, panelEl?: HTMLElement | string): any {
  const options: any = { map, panel: panelEl || null, hideMarkers: false };
  switch (mode) {
    case 'walking': return new (window as any).AMap.Walking(options);
    case 'riding':
    case 'bicycling': return new (window as any).AMap.Riding(options);
    case 'transit':
      options.city = '北京';
      options.policy = (window as any).AMap.TransferPolicy?.LEAST_TIME || 0;
      return new (window as any).AMap.Transfer(options);
    case 'driving':
    default:
      options.policy = (window as any).AMap.DrivingPolicy?.LEAST_TIME || 0;
      options.showTraffic = true;
      return new (window as any).AMap.Driving(options);
  }
}

// 获取起点终点
function getOriginDest(segment: RouteSegment) {
  return {
    origin: segment.fromLocation ? [segment.fromLocation.lng, segment.fromLocation.lat] : segment.from,
    destination: segment.toLocation ? [segment.toLocation.lng, segment.toLocation.lat] : segment.to,
  };
}

// 添加标记点
function addMarkers(map: any, allLocations: LocationPoint[]): any[] {
  const markers: any[] = [];
  const colorMap: Record<string, string> = {
    attraction: '#1890ff', hotel: '#722ed1', restaurant: '#fa8c16', start: '#52c41a', end: '#ff4d4f',
  };
  const labelMap: Record<string, string> = {
    attraction: '🏛️', hotel: '🏨', restaurant: '🍽️', start: '🚩', end: '🏁',
  };
  allLocations.forEach((loc) => {
    const marker = new (window as any).AMap.Marker({
      position: [loc.lng, loc.lat], map: map,
      label: {
        content: `<div style="background:${colorMap[loc.type] || '#666'};color:white;padding:2px 6px;border-radius:4px;font-size:12px;white-space:nowrap">${labelMap[loc.type] || '📍'} ${loc.name}</div>`,
        direction: 'top',
      },
    });
    markers.push(marker);
  });
  return markers;
}

// ==================== 🆕 多路段地图组件（带时间轴+详细面板） ====================
const MultiRouteMapModal: React.FC<MultiRouteMapProps> = ({
  visible,
  segments,
  allLocations
}) => {
  const mapRef = useRef<HTMLDivElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);
  const currentRouteRef = useRef<any>(null);
  const backgroundPolylinesRef = useRef<any[]>([]);
  const markersRef = useRef<any[]>([]);
  const cancelledRef = useRef(false);

  const [loadError, setLoadError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeIndex, setActiveIndex] = useState(0);
  const [routeSummary, setRouteSummary] = useState<{ distance: string; duration: string; mode: string } | null>(null);

      const highlightSegment = useCallback((map: any, segment: RouteSegment, panelEl?: HTMLElement | null) => {
    // 清除之前的高亮
    if (currentRouteRef.current && currentRouteRef.current.clear) {
      currentRouteRef.current.clear();
      currentRouteRef.current = null;
    }

    // 🆕 清空 panel 内容，避免旧内容残留
    if (panelEl) {
      panelEl.innerHTML = '<div style="padding: 12px 16px; color: #999; text-align: center;">⏳ 正在加载路线详情...</div>';
    }

    const { origin, destination } = getOriginDest(segment);
    const navigator = createNavigator(segment.type, map, panelEl || undefined);
    currentRouteRef.current = navigator;

    setRouteSummary(null);

    // 🆕 执行路线规划
    navigator.search(origin, destination, (status: string, result: any) => {
      if (cancelledRef.current) return;

      if (status === 'complete') {
        map.setFitView();
        if (result.routes && result.routes[0]) {
          const route = result.routes[0];
          setRouteSummary({
            distance: formatDistance(route.distance),
            duration: formatTime(route.time),
            mode: getTransportTypeName(segment.type),
          });
        }
      } else {
        console.warn(`路段 ${activeIndex} 规划失败:`, result?.info || status);
      }
    });
  }, [activeIndex]);
  // 绘制背景层路线（灰色半透明）


  // 初始化地图
  useEffect(() => {
    if (!visible || !mapRef.current || segments.length === 0) return;

    let localCancelled = false;
    cancelledRef.current = false;
    setLoading(true);
    setLoadError(null);
    setActiveIndex(0);

    const initMap = async () => {
      try {
        await loadAMapSDK();
        if (localCancelled) return;

        // 销毁旧实例
        if (mapInstanceRef.current) {
          mapInstanceRef.current.destroy();
          mapInstanceRef.current = null;
        }
        backgroundPolylinesRef.current = [];
        markersRef.current = [];

        // 创建地图
        const map = new (window as any).AMap.Map(mapRef.current, {
          viewMode: '3D', zoom: 12, center: [116.397428, 39.90923], resizeEnable: true,
        });
        mapInstanceRef.current = map;

        // 控件
        (window as any).AMap.plugin(['AMap.ToolBar', 'AMap.Scale'], () => {
          try {
            map.addControl(new (window as any).AMap.ToolBar({ position: 'RT' }));
            map.addControl(new (window as any).AMap.Scale({ position: 'LB' }));
          } catch (e) { /* ignore */ }
        });

        // 标记点
        if (allLocations && allLocations.length > 0) {
          markersRef.current = addMarkers(map, allLocations);
        }

        // 高亮第一个路段
        const panelEl = panelRef.current;
        highlightSegment(map, segments[0], panelEl);

        // 如果有多段，异步绘制其他路段的背景层
        if (segments.length > 1) {
          // 逐个处理其他路段（用规划器绘制到地图上）
          for (let i = 1; i < segments.length; i++) {
            if (localCancelled) break;
            const { origin, destination } = getOriginDest(segments[i]);
            const navigator = createNavigator(segments[i].type, map);
            navigator.search(origin, destination, () => {});
          }
        }

        if (!localCancelled) setLoading(false);

      } catch (error) {
        if (!localCancelled) {
          setLoading(false);
          setLoadError(`地图加载失败: ${(error as Error).message}`);
        }
      }
    };

    initMap();

    return () => {
      localCancelled = true;
      cancelledRef.current = true;
      if (currentRouteRef.current && currentRouteRef.current.clear) {
        currentRouteRef.current.clear();
        currentRouteRef.current = null;
      }
      if (mapInstanceRef.current) {
        mapInstanceRef.current.destroy();
        mapInstanceRef.current = null;
      }
    };
  }, [visible]); // 只在 visible 变化时重建地图

  // 切换路段时重新高亮
  useEffect(() => {
    if (!mapInstanceRef.current || !visible || segments.length === 0) return;
    const map = mapInstanceRef.current;
    const panelEl = panelRef.current;
    highlightSegment(map, segments[activeIndex], panelEl);
  }, [activeIndex, visible]);

  if (segments.length === 0) {
    return <Empty description="暂无路线数据" />;
  }

  return (
    <div>
      {/* 🆕 路段选择时间轴 */}
      {segments.length > 1 && (
        <div style={{
          marginBottom: 12,
          padding: '8px 12px',
          background: '#fafafa',
          borderRadius: 8,
          border: '1px solid #f0f0f0',
        }}>
          <Text strong style={{ fontSize: 13, marginBottom: 8, display: 'block' }}>
            📍 选择路段查看详细导航
          </Text>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            {segments.map((seg, idx) => (
              <div
                key={idx}
                onClick={() => setActiveIndex(idx)}
                style={{
                  cursor: 'pointer',
                  padding: '6px 12px',
                  borderRadius: 6,
                  background: idx === activeIndex ? '#e6f7ff' : '#fff',
                  border: idx === activeIndex ? '1.5px solid #1890ff' : '1px solid #d9d9d9',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 6,
                  fontSize: 12,
                  transition: 'all 0.2s',
                  flex: '1 1 auto',
                  minWidth: 120,
                }}
              >
                <Tag color={getTransportTagColor(seg.type)} style={{ margin: 0, fontSize: 11 }}>
                  {getTransportIcon(seg.type)} {getTransportTypeName(seg.type)}
                </Tag>
                <Text style={{ fontSize: 12 }}>
                  {seg.from} → {seg.to}
                </Text>
                {idx === activeIndex && (
                  <Tag color="blue" style={{ margin: 0, fontSize: 10 }}>当前</Tag>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 🆕 当前路段的摘要信息 */}
      {routeSummary && (
        <div style={{
          background: '#f0f5ff',
          borderRadius: 8,
          padding: '8px 16px',
          marginBottom: 8,
          display: 'flex',
          gap: 16,
          alignItems: 'center',
          flexWrap: 'wrap',
        }}>
          <Text>
            <EnvironmentOutlined style={{ color: '#52c41a' }} /> {segments[activeIndex].from}
          </Text>
          <ArrowRightOutlined style={{ color: '#1890ff', fontSize: 12 }} />
          <Text>
            <EnvironmentOutlined style={{ color: '#ff4d4f' }} /> {segments[activeIndex].to}
          </Text>
          <Tag color={getTransportTagColor(segments[activeIndex].type)}>
            {getTransportIcon(segments[activeIndex].type)} {routeSummary.mode}
          </Tag>
          {routeSummary.distance && <Tag color="green">📏 {routeSummary.distance}</Tag>}
          {routeSummary.duration && <Tag color="blue">⏱ {routeSummary.duration}</Tag>}
        </div>
      )}

      {/* 地图区域 */}
      <div style={{ position: 'relative', minHeight: '200px' }}>
        {loading && (
          <div style={{
            position: 'absolute', top: 0, left: 0, right: 0, bottom: 0,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            background: '#f5f5f5', borderRadius: '8px', zIndex: 1,
          }}>
            <Spin tip="加载地图中..." />
          </div>
        )}
        {loadError && !loading && (
          <Alert message="地图加载提示" description={loadError} type="warning" showIcon
            style={{ marginBottom: 8, position: 'relative', zIndex: 1 }}
            closable onClose={() => setLoadError(null)} />
        )}
        <div ref={mapRef} style={{
          width: '100%', height: '400px', borderRadius: '8px',
          visibility: loading ? 'hidden' : 'visible',
          position: 'relative', zIndex: 0,
        }} />
      </div>

      {/* 🆕 高德自动填充的详细导航面板 */}
      <div
        ref={panelRef}
        id="route-panel-content"
        style={{
          marginTop: 12,
          maxHeight: '300px',
          overflowY: 'auto',
          background: '#fff',
          borderRadius: 8,
          border: '1px solid #f0f0f0',
          fontSize: 13,
        }}
      >
        {!loading && !loadError && (
          <div style={{ padding: '12px 16px', color: '#999', textAlign: 'center' }}>
            ⏳ 路线规划中，详细步骤将显示在此处...
          </div>
        )}
        {/* 高德会自动填充 panel 内容到这里 */}
      </div>
    </div>
  );
};

// ==================== 单路段地图组件（兼容原有 NavigationData） ====================
const SingleRouteMapModal: React.FC<{
  visible: boolean;
  navigationData: NavigationData;
  allLocations?: LocationPoint[];
  onClose?: () => void;
}> = ({ visible, navigationData, allLocations }) => {
  const mapRef = useRef<HTMLDivElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);
  const currentRouteRef = useRef<any>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [routeSummary, setRouteSummary] = useState<{ distance: string; duration: string; mode: string } | null>(null);

  useEffect(() => {
    if (!visible || !mapRef.current) return;

    let cancelled = false;
    setLoading(true);
    setLoadError(null);

    const initMap = async () => {
      try {
        await loadAMapSDK();
        if (cancelled) return;

        if (mapInstanceRef.current) {
          mapInstanceRef.current.destroy();
          mapInstanceRef.current = null;
        }

        const map = new (window as any).AMap.Map(mapRef.current, {
          viewMode: '3D', zoom: 12, center: [116.397428, 39.90923], resizeEnable: true,
        });
        mapInstanceRef.current = map;

        (window as any).AMap.plugin(['AMap.ToolBar', 'AMap.Scale'], () => {
          try {
            map.addControl(new (window as any).AMap.ToolBar({ position: 'RT' }));
            map.addControl(new (window as any).AMap.Scale({ position: 'LB' }));
          } catch (e) { /* ignore */ }
        });

        if (allLocations && allLocations.length > 0) {
          addMarkers(map, allLocations);
        }

        // 规划路线
        const { origin, destination } = {
          origin: navigationData.fromLocation
            ? [navigationData.fromLocation.lng, navigationData.fromLocation.lat]
            : navigationData.from,
          destination: navigationData.toLocation
            ? [navigationData.toLocation.lng, navigationData.toLocation.lat]
            : navigationData.to,
        };

        const navigator = createNavigator(navigationData.type, map, panelRef.current || undefined);
        currentRouteRef.current = navigator;

        setRouteSummary(null);

        navigator.search(origin, destination, (status: string, result: any) => {
          if (cancelled) return;
          setLoading(false);

          if (status === 'complete') {
            map.setFitView();
            if (result.routes && result.routes[0]) {
              const route = result.routes[0];
              setRouteSummary({
                distance: formatDistance(route.distance),
                duration: formatTime(route.time),
                mode: getTransportTypeName(navigationData.type),
              });
            }
          } else {
            if (allLocations && allLocations.length > 0) {
              setTimeout(() => map.setFitView(), 500);
              setLoadError('路线规划失败，但已显示景点位置');
            } else {
              setLoadError(result?.info || '路线规划失败');
            }
          }
        });

        if (!cancelled) setTimeout(() => setLoading(false), 1000);

      } catch (error) {
        if (!cancelled) {
          setLoading(false);
          setLoadError(`地图加载失败: ${(error as Error).message}`);
        }
      }
    };

    initMap();

    return () => {
      cancelled = true;
      if (currentRouteRef.current && currentRouteRef.current.clear) {
        currentRouteRef.current.clear();
        currentRouteRef.current = null;
      }
      if (mapInstanceRef.current) {
        mapInstanceRef.current.destroy();
        mapInstanceRef.current = null;
      }
    };
  }, [visible, navigationData, allLocations]);

  return (
    <div>
      {/* 摘要信息 */}
      {routeSummary && (
        <div style={{
          background: '#f0f5ff', borderRadius: 8, padding: '8px 16px',
          marginBottom: 8, display: 'flex', gap: 16, alignItems: 'center', flexWrap: 'wrap',
        }}>
          <Text><EnvironmentOutlined style={{ color: '#52c41a' }} /> {navigationData.from}</Text>
          <ArrowRightOutlined style={{ color: '#1890ff', fontSize: 12 }} />
          <Text><EnvironmentOutlined style={{ color: '#ff4d4f' }} /> {navigationData.to}</Text>
          <Tag color={getTransportTagColor(navigationData.type)}>
            {getTransportIcon(navigationData.type)} {routeSummary.mode}
          </Tag>
          {routeSummary.distance && <Tag color="green">📏 {routeSummary.distance}</Tag>}
          {routeSummary.duration && <Tag color="blue">⏱ {routeSummary.duration}</Tag>}
        </div>
      )}

      {/* 地图 */}
      <div style={{ position: 'relative', minHeight: '200px' }}>
        {loading && (
          <div style={{
            position: 'absolute', top: 0, left: 0, right: 0, bottom: 0,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            background: '#f5f5f5', borderRadius: '8px', zIndex: 1,
          }}>
            <Spin tip="加载地图中..." />
          </div>
        )}
        {loadError && !loading && (
          <Alert message="地图加载提示" description={loadError} type="warning" showIcon
            style={{ marginBottom: 8, position: 'relative', zIndex: 1 }}
            closable onClose={() => setLoadError(null)} />
        )}
        <div ref={mapRef} style={{
          width: '100%', height: '400px', borderRadius: '8px',
          visibility: loading ? 'hidden' : 'visible', position: 'relative', zIndex: 0,
        }} />
      </div>

      {/* 详细导航面板 */}
      <div
        ref={panelRef}
        style={{
          marginTop: 12, maxHeight: '300px', overflowY: 'auto',
          background: '#fff', borderRadius: 8, border: '1px solid #f0f0f0', fontSize: 13,
        }}
      >
        {!loading && !loadError && (
          <div style={{ padding: '12px 16px', color: '#999', textAlign: 'center' }}>
            ⏳ 路线规划中，详细步骤将显示在此处...
          </div>
        )}
      </div>
    </div>
  );
};

// ==================== 主组件（判断使用单路段还是多路段） ====================
const NavigationMapView: React.FC<NavigationMapViewProps> = ({
  navigationData,
  allLocations
}) => {
  const [showMap, setShowMap] = useState(false);

  if (!navigationData) {
    return (
      <Card size="small" style={{ marginBottom: 8 }}>
        <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description="暂无导航路线数据" />
      </Card>
    );
  }

  return (
    <Card
      size="small"
      style={{ marginBottom: 8, border: '1px solid #d6e4ff' }}
      styles={{ header: { backgroundColor: '#f0f5ff', padding: '8px 12px' } }}
      title={
        <Space>
          <CarOutlined style={{ color: '#1890ff' }} />
          <Text strong>导航路线</Text>
        </Space>
      }
      extra={
        <Button type="primary" size="small" icon={<AimOutlined />}
          onClick={() => setShowMap(!showMap)}>
          {showMap ? '隐藏地图' : '显示地图'}
        </Button>
      }
    >
      {/* 路线概要（用格式化保护） */}
      <div style={{ background: '#f0f5ff', borderRadius: 8, padding: '12px 16px', marginBottom: 12 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
          <Tag icon={<CarOutlined />} color={getTransportTagColor(navigationData.type)}>
            {getTransportTypeName(navigationData.type)}
          </Tag>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
          <Text><EnvironmentOutlined style={{ color: '#52c41a' }} /> {String(navigationData.from)}</Text>
          <ArrowRightOutlined style={{ color: '#1890ff' }} />
          <Text><EnvironmentOutlined style={{ color: '#ff4d4f' }} /> {String(navigationData.to)}</Text>
        </div>
      </div>

      {/* 地图 */}
      {showMap && (
        <div style={{ marginTop: 12 }}>
          <SingleRouteMapModal
            visible={showMap}
            navigationData={navigationData}
            allLocations={allLocations}
            onClose={() => setShowMap(false)}
          />
        </div>
      )}
    </Card>
  );
};

export { NavigationMapView, MultiRouteMapModal };
export type { NavigationData, LocationPoint, RouteSegment };