import React, { useEffect, useRef, useState } from 'react';
import { Card, Button, Tag, Space, Typography, Collapse, Timeline, Spin, Empty, Alert } from 'antd';
import { CarOutlined, EnvironmentOutlined, ArrowRightOutlined, AimOutlined } from '@ant-design/icons';

const { Text } = Typography;

// 高德地图配置（建议通过环境变量管理，无环境变量时使用硬编码兜底）
const AMAP_JS_API_KEY = import.meta.env.VITE_AMAP_JS_API_KEY || '79e6fa00599f309662a90359d0dddda1';
const AMAP_SECURITY_JS_CODE = import.meta.env.VITE_AMAP_SECURITY_JS_CODE || '';

// 定义导航数据接口
interface NavigationStep {
  instruction: string;
  distance: number;
  duration: number;
  polyline?: string;
  type?: string;
  departure?: string;
  arrival?: string;
  via_num?: number;
}

interface NavigationData {
  from: string;
  to: string;
  type: string;
  distance: number;
  distance_text: string;
  duration: number;
  duration_text: string;
  steps: NavigationStep[];
  polyline?: string;
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

// ==================== 文字形式的导航详情组件 ====================
const NavigationTextDetail: React.FC<{ navigationData: NavigationData }> = ({ navigationData }) => {
  const formatStepDistance = (distance: number) => {
    if (distance >= 1000) return `${(distance / 1000).toFixed(1)}公里`;
    return `${distance}米`;
  };

  const formatStepDuration = (duration: number) => {
    const hours = Math.floor(duration / 3600);
    const minutes = Math.floor((duration % 3600) / 60);
    if (hours > 0) return `${hours}小时${minutes}分钟`;
    return `${minutes}分钟`;
  };

  const getTransportEmoji = (type: string) => {
    switch (type) {
      case 'walking': return '🚶';
      case 'driving': return '🚗';
      case 'transit': return '🚌';
      case 'bicycling': return '🚴';
      case 'subway': return '🚇';
      default: return '🚗';
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

  const getTransportTypeName = (type: string) => {
    switch (type) {
      case 'walking': return '步行';
      case 'driving': return '驾车';
      case 'transit': return '公交/地铁';
      case 'bicycling': return '骑行';
      default: return type;
    }
  };

  // 构建详细的时间线步骤
  const getTimelineItems = () => {
    const items: any[] = [];

    if (navigationData.steps && navigationData.steps.length > 0) {
      navigationData.steps.forEach((step, idx) => {
        const isWalking = step.type === 'walking' || 
          (step.instruction && step.instruction.includes('步行'));
        const isSubway = step.type === 'subway' || 
          (step.instruction && (step.instruction.includes('地铁') || step.instruction.includes('轨道交通')));
        const isBus = step.type === 'bus' || 
          (step.instruction && step.instruction.includes('公交'));
        
        items.push({
          color: isWalking ? 'blue' : isSubway ? 'green' : isBus ? 'orange' : 'default',
          children: (
            <div key={idx} style={{ padding: '4px 0' }}>
              <div style={{ marginBottom: 4 }}>
                {isWalking ? '🚶 ' : isSubway ? '🚇 ' : isBus ? '🚌 ' : '🚗 '}
                <Text strong>{step.instruction}</Text>
              </div>
              <Space size="middle">
                {step.distance > 0 && (
                  <Text type="secondary" style={{ fontSize: 12 }}>
                    📏 {formatStepDistance(step.distance)}
                  </Text>
                )}
                {step.duration > 0 && (
                  <Text type="secondary" style={{ fontSize: 12 }}>
                    ⏱ {formatStepDuration(step.duration)}
                  </Text>
                )}
                {step.departure && step.arrival && (
                  <Text type="secondary" style={{ fontSize: 12 }}>
                    🏷 {step.departure} → {step.arrival}
                  </Text>
                )}
                {step.via_num !== undefined && step.via_num > 0 && (
                  <Text type="secondary" style={{ fontSize: 12 }}>
                    🚏 经过 {step.via_num} 站
                  </Text>
                )}
              </Space>
            </div>
          )
        });
      });
    } else {
      // 没有详细步骤时显示简略信息
      items.push({
        color: 'gray',
        children: (
          <div style={{ padding: '4px 0' }}>
            <Text type="secondary">
              {getTransportEmoji(navigationData.type)} 
              从 {navigationData.from} 前往 {navigationData.to}
              {navigationData.distance_text && `（${navigationData.distance_text}）`}
            </Text>
          </div>
        )
      });
    }

    return items;
  };

  return (
    <div>
      {/* 路线概要 */}
      <div style={{ 
        background: '#f0f5ff', 
        borderRadius: 8, 
        padding: '12px 16px', 
        marginBottom: 12 
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
          <Tag icon={<CarOutlined />} color={getTransportTagColor(navigationData.type)}>
            {getTransportTypeName(navigationData.type)}
          </Tag>
          {navigationData.duration_text && (
            <Tag color="blue">⏱ {navigationData.duration_text}</Tag>
          )}
          {navigationData.distance_text && (
            <Tag color="green">📏 {navigationData.distance_text}</Tag>
          )}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
          <Text><EnvironmentOutlined style={{ color: '#52c41a' }} /> {navigationData.from}</Text>
          <ArrowRightOutlined style={{ color: '#1890ff' }} />
          <Text><EnvironmentOutlined style={{ color: '#ff4d4f' }} /> {navigationData.to}</Text>
        </div>
      </div>

      {/* 详细步骤 */}
      {navigationData.steps && navigationData.steps.length > 0 ? (
        <Collapse
          ghost
          defaultActiveKey={['1']}
          items={[{
            key: '1',
            label: <Text strong>📋 详细导航步骤 ({navigationData.steps.length} 步)</Text>,
            children: (
              <Timeline items={getTimelineItems()} />
            )
          }]}
        />
      ) : (
        <div style={{ textAlign: 'center', padding: 16 }}>
          <Text type="secondary">暂无详细的导航步骤数据</Text>
        </div>
      )}
    </div>
  );
};

// ==================== 地图展示组件（弹窗） ====================
const NavigationMapModal: React.FC<{
  visible: boolean;
  navigationData: NavigationData;
  allLocations?: LocationPoint[];
  onClose?: () => void;
}> = ({ visible, navigationData, allLocations }) => {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!visible || !mapRef.current) return;

    let cancelled = false;
    setLoading(true);
    setLoadError(null);

    const loadAMapScript = () => {
      return new Promise<void>((resolve, reject) => {
        if ((window as any).AMap && (window as any).AMap.Map) {
          const plugins = ['AMap.ToolBar', 'AMap.Driving', 'AMap.Walking', 'AMap.Transit', 'AMap.Riding'];
          const missingPlugins = plugins.filter(p => !(window as any).AMap[p]);
          if (missingPlugins.length === 0) {
            resolve();
          } else {
            (window as any).AMap.plugin(missingPlugins, () => {
              resolve();
            });
          }
          return;
        }

        if (AMAP_SECURITY_JS_CODE) {
          (window as any)._AMapSecurityConfig = {
            securityJsCode: AMAP_SECURITY_JS_CODE,
          };
        }

        const script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = `https://webapi.amap.com/maps?v=2.0&key=${AMAP_JS_API_KEY}&plugin=AMap.ToolBar,AMap.Driving,AMap.Walking,AMap.Transit,AMap.Riding`;
        script.onload = () => resolve();
        script.onerror = () => reject(new Error('高德地图API加载失败'));
        document.head.appendChild(script);
      });
    };

    const initMap = async () => {
      try {
        await loadAMapScript();

        if (cancelled) return;

        if (mapInstanceRef.current) {
          mapInstanceRef.current.destroy();
        }

        const map = new (window as any).AMap.Map(mapRef.current, {
          zoom: 14,
          center: [116.397428, 39.90923],
          viewMode: '2D'
        });
        mapInstanceRef.current = map;

        (window as any).AMap.plugin(['AMap.ToolBar'], function() {
          try {
            const toolbar = new (window as any).AMap.ToolBar();
            map.addControl(toolbar);
          } catch (e) {
            console.warn('ToolBar加载失败，不影响地图使用', e);
          }
        });

        const allMarkers: any[] = [];
        if (allLocations && allLocations.length > 0) {
          const colorMap: Record<string, string> = {
            attraction: '#1890ff',
            hotel: '#722ed1',
            restaurant: '#fa8c16',
            start: '#52c41a',
            end: '#ff4d4f',
          };
          const labelMap: Record<string, string> = {
            attraction: '🏛️',
            hotel: '🏨',
            restaurant: '🍽️',
            start: '🚩',
            end: '🏁',
          };

          allLocations.forEach((loc) => {
            const marker = new (window as any).AMap.Marker({
              position: [loc.lng, loc.lat],
              map: map,
              label: {
                content: `<div style="background:${colorMap[loc.type] || '#666'};color:white;padding:2px 6px;border-radius:4px;font-size:12px;white-space:nowrap">${labelMap[loc.type] || '📍'} ${loc.name}</div>`,
                direction: 'top',
              },
            });
            allMarkers.push(marker);
          });
        }

        if (navigationData.polyline) {
          try {
            const path = (window as any).AMap.GeometryUtil.decodePath(navigationData.polyline);
            if (path && path.length > 0) {
              const polylineObj = new (window as any).AMap.Polyline({
                path: path,
                borderWeight: 2,
                strokeColor: '#1890ff',
                lineWeight: 4,
                lineJoin: 'round'
              });
              map.add(polylineObj);

              if (!allLocations || allLocations.length === 0) {
                new (window as any).AMap.Marker({
                  position: path[0],
                  map: map,
                  label: { content: `<div style="background:#52c41a;color:white;padding:2px 6px;border-radius:4px;font-size:12px">起点: ${navigationData.from}</div>`, direction: 'top' }
                });
                new (window as any).AMap.Marker({
                  position: path[path.length - 1],
                  map: map,
                  label: { content: `<div style="background:#ff4d4f;color:white;padding:2px 6px;border-radius:4px;font-size:12px">终点: ${navigationData.to}</div>`, direction: 'top' }
                });
              }

              if (allMarkers.length > 0) {
                map.setFitView(allMarkers, false, [50, 50, 50, 50]);
              } else {
                map.setFitView();
              }
              if (!cancelled) setLoading(false);
              return;
            }
          } catch (e) {
            console.warn('polyline解码失败，尝试使用API搜索路线', e);
          }
        }

                const navigatorMap: Record<string, any> = {
          'walking': (window as any).AMap.Walking,
          'driving': (window as any).AMap.Driving,
          'transit': (window as any).AMap.Transit,
          'bicycling': (window as any).AMap.Riding,
        };

        const NavigatorClass = navigatorMap[navigationData.type] || (window as any).AMap.Driving;
        const navigator = new NavigatorClass({ map, panel: null, hideMarkers: false });

        navigator.search(navigationData.from, navigationData.to, (status: string, result: any) => {
          if (!cancelled) setLoading(false);
          if (status === 'complete') {
            console.log('路线规划成功');
            if (allMarkers.length > 0) {
              map.setFitView(allMarkers, false, [50, 50, 50, 50]);
            }
          } else {
            console.error('路线规划失败:', result);
            if (!cancelled) setLoadError(result?.info || '路线规划失败');
          }
        });

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
      if (mapInstanceRef.current) {
        mapInstanceRef.current.destroy();
        mapInstanceRef.current = null;
      }
    };
  }, [visible, navigationData, allLocations]);

      return (
    <div style={{ position: 'relative', minHeight: '200px' }}>
      {loading && (
        <div style={{ 
          position: 'absolute', 
          top: 0, left: 0, right: 0, bottom: 0,
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          background: '#f5f5f5',
          borderRadius: '8px',
          zIndex: 1
        }}>
          <Spin tip="加载地图中..." />
        </div>
      )}
      {loadError && !loading && (
        <Alert 
          message="地图加载提示" 
          description={loadError} 
          type="warning" 
          showIcon 
          style={{ marginBottom: 8, position: 'relative', zIndex: 1 }} 
          closable 
          onClose={() => setLoadError(null)}
        />
      )}
      <div
        ref={mapRef}
        style={{
          width: '100%',
          height: '500px',
          borderRadius: '8px',
          visibility: loading ? 'hidden' : 'visible',
          position: 'relative',
          zIndex: 0
        }}
      />
    </div>
  );
};
// ==================== 主组件 ====================
const NavigationMapView: React.FC<NavigationMapViewProps> = ({
  navigationData,
  allLocations  // ⬅️【修复】补上这个参数，之前被忽略了
}) => {
  const [showMap, setShowMap] = useState(false);

  if (!navigationData) {
    return (
      <Card size="small" style={{ marginBottom: 8 }}>
        <Empty 
          image={Empty.PRESENTED_IMAGE_SIMPLE} 
          description="暂无导航路线数据" 
        />
      </Card>
    );
  }

  return (
    <Card
      size="small"
      style={{ marginBottom: 8, border: '1px solid #d6e4ff' }}
      styles={{
        header: { backgroundColor: '#f0f5ff', padding: '8px 12px' }
      }}
      title={
        <Space>
          <CarOutlined style={{ color: '#1890ff' }} />
          <Text strong>导航路线</Text>
        </Space>
      }
      extra={
        <Space size="small">
          <Button 
            type="primary"
            size="small" 
            icon={<AimOutlined />}
            onClick={() => setShowMap(!showMap)}
          >
            {showMap ? '隐藏地图' : '显示地图'}
          </Button>
        </Space>
      }
    >
      {/* 文字导航详情 */}
      <NavigationTextDetail navigationData={navigationData} />

      {/* 地图展示（折叠式） */}
      {showMap && (
        <div style={{ marginTop: 12 }}>
          <NavigationMapModal 
            visible={showMap}
            navigationData={navigationData}
            allLocations={allLocations}  // ⬇️【新增】把坐标点传给地图弹窗
            onClose={() => setShowMap(false)}
          />
        </div>
      )}
    </Card>
  );
};

export { NavigationMapView, NavigationTextDetail };
export type { NavigationData, NavigationStep, LocationPoint };