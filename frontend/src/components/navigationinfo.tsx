import React, { useState } from 'react';
import { Card, Timeline, Tag, Space, Typography, Button, Collapse } from 'antd';
import { CarOutlined, ClockCircleOutlined, EnvironmentOutlined, ArrowRightOutlined } from '@ant-design/icons';
import AMapNavigationDebug from './amapnavigationdebug';

const { Text, Paragraph } = Typography;
const { Panel } = Collapse;

interface Step {
  instruction: string;
  distance: number;
  duration: number;
  polyline?: string;
  station_name?: string;
  type?: string;
  departure?: string;
  arrival?: string;
  via_num?: number;
}

interface TransportOption {
  transport_id: string;
  type: string;
  from: string;
  to: string;
  distance: number;
  distance_text: string;
  duration: number;
  duration_text: string;
  steps: Step[];
  polyline?: string;
}

interface NavigationInfoProps {
  transport: TransportOption;
  onShowMap?: () => void;
}

const NavigationInfo: React.FC<NavigationInfoProps> = ({ transport, onShowMap }) => {
  const [mapVisible, setMapVisible] = useState(false);

  const handleShowMap = () => {
    setMapVisible(true);
  };

  const getTransportIcon = (type: string) => {
    switch (type) {
      case 'walking':
        return '🚶';
      case 'driving':
        return '🚗';
      case 'transit':
        return '🚌';
      case 'bicycling':
        return '🚴';
      default:
        return '🚗';
    }
  };

  const getTransportTypeText = (type: string) => {
    switch (type) {
      case 'walking':
        return '步行';
      case 'driving':
        return '驾车';
      case 'transit':
        return '公交';
      case 'bicycling':
        return '骑行';
      default:
        return '驾车';
    }
  };

  const formatStepDistance = (distance: number) => {
    if (distance >= 1000) {
      return `${(distance / 1000).toFixed(1)}公里`;
    }
    return `${distance}米`;
  };

  const formatStepDuration = (duration: number) => {
    const hours = Math.floor(duration / 3600);
    const minutes = Math.floor((duration % 3600) / 60);

    if (hours > 0) {
      return `${hours}小时${minutes}分钟`;
    }
    return `${minutes}分钟`;
  };

  return (
    <Card
      size="small"
      style={{ marginBottom: 8, backgroundColor: '#f0f5ff' }}
      bodyStyle={{ padding: '12px' }}
      extra={
        <Button
          type="link"
          size="small"
          onClick={handleShowMap}
        >
          查看地图
        </Button>
      }
    >
      <Space direction="vertical" size="small" style={{ width: '100%' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Text strong>
            <CarOutlined /> {getTransportTypeText(transport.type)}路线
            <span style={{ marginLeft: 8 }}>{getTransportIcon(transport.type)}</span>
          </Text>
          <Space size="small">
            <Tag icon={<ClockCircleOutlined />} color="blue">
              {transport.duration_text}
            </Tag>
            <Tag icon={<EnvironmentOutlined />} color="green">
              {transport.distance_text}
            </Tag>
          </Space>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Text>{transport.from}</Text>
          <ArrowRightOutlined style={{ color: '#1890ff' }} />
          <Text>{transport.to}</Text>
        </div>

        {transport.steps && transport.steps.length > 0 && (
          <Collapse
            ghost
            items={[
              {
                key: '1',
                label: '查看详细路线',
                children: (
                  <Timeline
                    items={transport.steps.map((step, index) => ({
                      key: index,
                      color: step.type === 'walking' ? 'blue' : step.type === 'subway' ? 'green' : 'orange',
                      children: (
                        <div>
                          <Paragraph style={{ marginBottom: 4 }}>
                            {step.type === 'walking' ? '🚶 ' : step.type === 'subway' ? '🚇 ' : '🚌 '}
                            {step.instruction}
                          </Paragraph>
                          <Space size="small">
                            <Text type="secondary" style={{ fontSize: 12 }}>
                              {formatStepDistance(step.distance)}
                            </Text>
                            <Text type="secondary" style={{ fontSize: 12 }}>
                              {formatStepDuration(step.duration)}
                            </Text>
                            {step.departure && step.arrival && (
                              <Text type="secondary" style={{ fontSize: 12 }}>
                                {step.departure} → {step.arrival}
                              </Text>
                            )}
                            {step.via_num !== undefined && step.via_num > 0 && (
                              <Text type="secondary" style={{ fontSize: 12 }}>
                                经过 {step.via_num} 站
                              </Text>
                            )}
                          </Space>
                        </div>
                      )
                    }))}
                  />
                )
              }
            ]}
          />
        )}
      </Space>
      <AMapNavigationDebug
        visible={mapVisible}
        onClose={() => setMapVisible(false)}
        polyline={transport.polyline}
        from={transport.from}
        to={transport.to}
        type={transport.type}
      />
    </Card>
  );
};

export default NavigationInfo;
