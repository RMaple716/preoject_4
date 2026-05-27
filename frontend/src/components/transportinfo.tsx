import React from 'react';
import { Card, Space, Typography } from 'antd';
import { CarOutlined } from '@ant-design/icons';
import NavigationInfo from './NavigationInfo';

const { Text } = Typography;

interface TransportInfoProps {
  transport: any;
}

const TransportInfo: React.FC<TransportInfoProps> = ({ transport }) => {
  // 检查是否是新的导航格式
  if (transport.data && transport.data.items && transport.data.items.length > 0) {
    return <NavigationInfo transport={transport.data.items[0]} />;
  }
  
  // 检查是否是直接的导航格式
  if (transport.type && transport.steps) {
    return <NavigationInfo transport={transport} />;
  }

  // 旧格式保持不变
  return (
    <Card
      size="small"
      style={{ marginBottom: 8, backgroundColor: '#f0f5ff' }}
      bodyStyle={{ padding: '12px' }}
    >
      <Space direction="vertical" size="small" style={{ width: '100%' }}>
        <Text strong><CarOutlined /> 交通安排</Text>
        {transport.mode && (
          <Text>方式：{transport.mode}</Text>
        )}
        {transport.from_location && transport.to_location && (
          <Text>
            {transport.from_location} → {transport.to_location}
          </Text>
        )}
        {transport.duration && (
          <Text type="secondary">时长：{transport.duration}</Text>
        )}
        {transport.cost && (
          <Text type="secondary">费用：¥{transport.cost}</Text>
        )}
      </Space>
    </Card>
  );
};

export default TransportInfo;
