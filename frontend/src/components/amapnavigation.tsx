import React, { useEffect, useRef } from 'react';
import { Modal } from 'antd';

interface AMapNavigationProps {
  visible: boolean;
  onClose: () => void;
  polyline?: string; // 路线编码
  from: string; // 起点
  to: string; // 终点
  type?: string; // 交通模式: walking/driving/transit/bicycling
}

const AMapNavigation: React.FC<AMapNavigationProps> = ({
  visible,
  onClose,
  polyline,
  from,
  to,
  type = 'driving'
}) => {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);

  useEffect(() => {
    if (!visible || !mapRef.current) return;

    // 动态加载高德地图API
    const loadAMapScript = () => {
      return new Promise<void>((resolve, reject) => {
        if (window.AMap) {
          resolve();
          return;
        }

        const script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = `https://webapi.amap.com/maps?v=2.0&key=68d86f708336a0eb7f8777ab1d5989e8&plugin=AMap.Driving,AMap.Walking,AMap.Transit,AMap.Riding`;
        script.onload = () => resolve();
        script.onerror = () => reject(new Error('Failed to load AMap'));
        document.head.appendChild(script);
      });
    };

    const initMap = async () => {
      try {
        await loadAMapScript();

        if (!mapInstanceRef.current) {
          // 创建地图实例
          const map = new window.AMap.Map(mapRef.current, {
            zoom: 13,
            center: [116.397428, 39.90923],
            viewMode: '2D'
          });

          mapInstanceRef.current = map;

          // 添加工具条
          const toolbar = new window.AMap.ToolBar();
          map.addControl(toolbar);

          // 添加比例尺
          const scale = new window.AMap.Scale();
          map.addControl(scale);
        }

        const map = mapInstanceRef.current;

        // 清除之前的标记和路线
        map.clearMap();

        // 如果有路线编码，绘制路线
        if (polyline) {
          try {
            const path = window.AMap.GeometryUtil.decodePath(polyline);
            const polylineObj = new window.AMap.Polyline({
              path: path,
              borderWeight: 2,
              strokeColor: '#1890ff',
              lineJoin: 'round'
            });
            map.add(polylineObj);

            // 添加起点和终点标记
            const startMarker = new window.AMap.Marker({
              position: path[0],
              title: from,
              label: {
                content: from,
                direction: 'top'
              }
            });
            const endMarker = new window.AMap.Marker({
              position: path[path.length - 1],
              title: to,
              label: {
                content: to,
                direction: 'top'
              }
            });
            map.add([startMarker, endMarker]);

            // 设置地图视野以包含整个路线
            map.setFitView();
          } catch (error) {
            console.error('绘制路线失败:', error);
          }
        } else {
          // 如果没有路线编码，根据交通模式调用相应的API
          let navigator;
          
          switch (type) {
            case 'walking':
              navigator = new window.AMap.Walking({
                map: map,
                panel: null
              });
              break;
            case 'transit':
              navigator = new window.AMap.Transit({
                map: map,
                panel: null
              });
              break;
            case 'bicycling':
              navigator = new window.AMap.Riding({
                map: map,
                panel: null
              });
              break;
            case 'driving':
            default:
              navigator = new window.AMap.Driving({
                map: map,
                panel: null
              });
              break;
          }

          navigator.search(from, to, (status: string, result: any) => {
            if (status === 'complete') {
              console.log('路线规划成功:', result);
            } else {
              console.error('路线规划失败:', result);
            }
          });
        }

      } catch (error) {
        console.error('地图初始化失败:', error);
      }
    };

    initMap();

    return () => {
      // 组件卸载时清理
      if (mapInstanceRef.current) {
        mapInstanceRef.current.destroy();
        mapInstanceRef.current = null;
      }
    };
  }, [visible, polyline, from, to]);

  return (
    <Modal
      title="导航路线"
      open={visible}
      onCancel={onClose}
      footer={null}
      width={800}
      style={{ top: 20 }}
    >
      <div
        ref={mapRef}
        style={{
          width: '100%',
          height: '600px',
          borderRadius: '8px'
        }}
      />
    </Modal>
  );
};

export default AMapNavigation;
