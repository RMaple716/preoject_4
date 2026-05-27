import React, { useEffect, useRef } from 'react';
import { Modal, Button } from 'antd';
import { logger } from '../utils/logger';
import { mapDebugger } from '../utils/mapdebugger';

interface AMapNavigationProps {
  visible: boolean;
  onClose: () => void;
  polyline?: string;
  from: string;
  to: string;
  type?: string;
}

const AMapNavigationDebug: React.FC<AMapNavigationProps> = ({
  visible,
  onClose,
  polyline,
  from,
  to,
  type = 'driving'
}) => {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);
  const containerId = 'amap-container-' + Date.now();

  useEffect(() => {
    logger.componentLifecycle('AMapNavigation', 'mount', { visible, polyline, from, to, type });

    if (!visible || !mapRef.current) {
      logger.warn('AMapNavigation', '组件未显示或容器未就绪', { visible, hasContainer: !!mapRef.current });
      return;
    }

    logger.info('AMapNavigation', '开始初始化地图');

    // 动态加载高德地图API
    const loadAMapScript = () => {
      logger.info('AMapNavigation', '开始加载高德地图API');
      return new Promise<void>((resolve, reject) => {
        if (window.AMap) {
          logger.success('AMapNavigation', '高德地图API已加载');
          resolve();
          return;
        }

        const script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = `https://webapi.amap.com/maps?v=2.0&key=68d86f708336a0eb7f8777ab1d5989e8&plugin=AMap.Driving,AMap.Walking,AMap.Transit,AMap.Riding`;
        script.onload = () => {
          logger.success('AMapNavigation', '高德地图API加载成功');
          resolve();
        };
        script.onerror = () => {
          logger.error('AMapNavigation', '高德地图API加载失败');
          reject(new Error('Failed to load AMap'));
        };
        document.head.appendChild(script);
      });
    };

    const initMap = async () => {
      try {
        logger.info('AMapNavigation', '开始初始化地图实例');
        await loadAMapScript();

        if (!mapInstanceRef.current) {
          logger.info('AMapNavigation', '创建新的地图实例');

          // 检查容器
          if (!mapRef.current) {
            logger.error('AMapNavigation', '地图容器不存在');
            return;
          }

          const container = mapRef.current;
          logger.info('AMapNavigation', '容器尺寸', {
            width: container.offsetWidth,
            height: container.offsetHeight
          });

          // 创建地图实例
          const map = new window.AMap.Map(container, {
            zoom: 13,
            center: [116.397428, 39.90923],
            viewMode: '2D'
          });

          mapInstanceRef.current = map;
          logger.success('AMapNavigation', '地图实例创建成功');

          // 添加工具条
          const toolbar = new window.AMap.ToolBar();
          map.addControl(toolbar);
          logger.info('AMapNavigation', '工具条已添加');

          // 添加比例尺
          const scale = new window.AMap.Scale();
          map.addControl(scale);
          logger.info('AMapNavigation', '比例尺已添加');
        } else {
          logger.info('AMapNavigation', '使用已存在的地图实例');
        }

        const map = mapInstanceRef.current;

        // 清除之前的标记和路线
        map.clearMap();
        logger.info('AMapNavigation', '已清除之前的标记和路线');

        // 如果有路线编码，绘制路线
        if (polyline) {
          logger.info('AMapNavigation', '开始绘制路线', { 
            polylineLength: polyline.length,
            from, 
            to,
            type 
          });

          try {
            const path = window.AMap.GeometryUtil.decodePath(polyline);
            logger.info('AMapNavigation', '路线解码成功', { 
              pathLength: path.length,
              startPoint: path[0],
              endPoint: path[path.length - 1]
            });

            const polylineObj = new window.AMap.Polyline({
              path: path,
              borderWeight: 2,
              strokeColor: '#1890ff',
              lineJoin: 'round'
            });
            map.add(polylineObj);
            logger.success('AMapNavigation', '路线对象已添加到地图');

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
            logger.success('AMapNavigation', '起点和终点标记已添加', {
              start: from,
              end: to
            });

            // 设置地图视野以包含整个路线
            map.setFitView();
            logger.success('AMapNavigation', '地图视野已调整');
          } catch (error) {
            logger.error('AMapNavigation', '绘制路线失败', error);
          }
        } else {
          // 如果没有路线编码，根据交通模式调用相应的API
          logger.info('AMapNavigation', '使用API规划路线', { from, to, type });

          let navigator;

          switch (type) {
            case 'walking':
              logger.info('AMapNavigation', '使用步行导航API');
              navigator = new window.AMap.Walking({
                map: map,
                panel: null
              });
              break;
            case 'transit':
              logger.info('AMapNavigation', '使用公交导航API');
              navigator = new window.AMap.Transit({
                map: map,
                panel: null
              });
              break;
            case 'bicycling':
              logger.info('AMapNavigation', '使用骑行导航API');
              navigator = new window.AMap.Riding({
                map: map,
                panel: null
              });
              break;
            case 'driving':
            default:
              logger.info('AMapNavigation', '使用驾车导航API');
              navigator = new window.AMap.Driving({
                map: map,
                panel: null
              });
              break;
          }

          logger.info('AMapNavigation', '开始搜索路线', { from, to });
          navigator.search(from, to, (status: string, result: any) => {
            if (status === 'complete') {
              logger.success('AMapNavigation', '路线规划成功', {
                status,
                hasResult: !!result,
                resultType: result?.type
              });
            } else {
              logger.error('AMapNavigation', '路线规划失败', {
                status,
                result,
                info: result?.info,
                message: result?.message
              });
            }
          });
        }

      } catch (error) {
        logger.error('AMapNavigation', '地图初始化失败', error);
      }
    };

    initMap();

    return () => {
      logger.componentLifecycle('AMapNavigation', 'unmount');
      if (mapInstanceRef.current) {
        mapInstanceRef.current.destroy();
        mapInstanceRef.current = null;
      }
    };
  }, [visible, polyline, from, to, type]);

  const runDiagnostics = () => {
    mapDebugger.diagnose({
      containerId: containerId,
      mapInstance: mapInstanceRef.current,
      polyline: polyline,
      apiKey: '68d86f708336a0eb7f8777ab1d5989e8'
    });
  };

  return (
    <Modal
      title={
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>导航路线</span>
          <Button type="primary" size="small" onClick={runDiagnostics}>
            运行诊断
          </Button>
        </div>
      }
      open={visible}
      onCancel={onClose}
      footer={null}
      width={800}
      style={{ top: 20 }}
    >
      <div
        id={containerId}
        ref={mapRef}
        style={{
          width: '100%',
          height: '600px',
          borderRadius: '8px',
          backgroundColor: '#f0f0f0'
        }}
      />
    </Modal>
  );
};

export default AMapNavigationDebug;
