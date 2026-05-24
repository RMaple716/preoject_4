import React, { useEffect, useState } from 'react';
import { 
  Typography, 
  Button, 
  Card, 
  Timeline, 
  Tag, 
  Space, 
  Descriptions,
  Divider,
  Spin,
  Empty,
  message,
  Statistic,
  Row,
  Col
} from 'antd';
import { 
  ArrowLeftOutlined,
  EnvironmentOutlined,
  CalendarOutlined,
  DollarOutlined,
  ClockCircleOutlined,
  CarOutlined,
  HomeOutlined,
  RestOutlined,
  CameraOutlined,
  FileTextOutlined
} from '@ant-design/icons';
import { useNavigate, useParams } from 'react-router-dom';
import { itineraryApi, Itinerary } from '../services/itineraryApi';

const { Title, Paragraph, Text } = Typography;

// 景点卡片组件
const AttractionCard: React.FC<{ attraction: any }> = ({ attraction }) => (
  <Card 
    size="small" 
    style={{ marginBottom: 8 }}
    bodyStyle={{ padding: '12px' }}
  >
    <Space direction="vertical" size="small" style={{ width: '100%' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Text strong>{attraction.name}</Text>
        {attraction.rating && (
          <Tag color="gold">⭐ {attraction.rating}</Tag>
        )}
      </div>
      {attraction.description && (
        <Text type="secondary" style={{ fontSize: 12 }}>
          {attraction.description}
        </Text>
      )}
      <Space size="small">
        {attraction.visit_duration && (
          <Tag icon={<ClockCircleOutlined />}>
            {attraction.visit_duration}
          </Tag>
        )}
        {attraction.ticket_price && (
          <Tag icon={<DollarOutlined />} color="green">
            ¥{attraction.ticket_price}
          </Tag>
        )}
        {attraction.location && (
          <Tag icon={<EnvironmentOutlined />}>
            {attraction.location}
          </Tag>
        )}
      </Space>
    </Space>
  </Card>
);

// 餐饮卡片组件
const MealCard: React.FC<{ meal: any }> = ({ meal }) => (
  <Card 
    size="small" 
    style={{ marginBottom: 8 }}
    bodyStyle={{ padding: '12px' }}
  >
    <Space direction="vertical" size="small" style={{ width: '100%' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Text strong>{meal.restaurant_name || meal.name}</Text>
        {meal.meal_type && (
          <Tag color="orange">{meal.meal_type}</Tag>
        )}
      </div>
      {meal.cuisine_type && (
        <Text type="secondary" style={{ fontSize: 12 }}>
          {meal.cuisine_type}
        </Text>
      )}
      {meal.price_per_person && (
        <Tag icon={<DollarOutlined />} color="green">
          ¥{meal.price_per_person}/人
        </Tag>
      )}
    </Space>
  </Card>
);

// 交通信息组件
const TransportInfo: React.FC<{ transport: any }> = ({ transport }) => (
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

// 住宿信息组件
const HotelInfo: React.FC<{ hotel: any }> = ({ hotel }) => (
  <Card 
    size="small"
    style={{ marginBottom: 8, backgroundColor: '#f6ffed' }}
    bodyStyle={{ padding: '12px' }}
  >
    <Space direction="vertical" size="small" style={{ width: '100%' }}>
      <Text strong><HomeOutlined /> 住宿安排</Text>
      <Text>{hotel.name}</Text>
      {hotel.address && (
        <Text type="secondary">{hotel.address}</Text>
      )}
      {hotel.price_per_night && (
        <Text type="secondary">¥{hotel.price_per_night}/晚</Text>
      )}
      {hotel.rating && (
        <Tag color="gold">⭐ {hotel.rating}</Tag>
      )}
    </Space>
  </Card>
);

// 每日行程内容组件
const DayPlanContent: React.FC<{ dayPlan: any }> = ({ dayPlan }) => {
  const timelineItems = [];

  // 添加交通（如果有）
  if (dayPlan.transport) {
    timelineItems.push({
      color: 'blue',
      children: <TransportInfo transport={dayPlan.transport} />
    });
  }

  // 添加景点
  if (dayPlan.attractions && dayPlan.attractions.length > 0) {
    timelineItems.push({
      color: 'green',
      dot: <CameraOutlined />,
      children: (
        <div>
          <Text strong><CameraOutlined /> 景点游览</Text>
          <div style={{ marginTop: 8 }}>
            {dayPlan.attractions.map((attraction: any, idx: number) => (
              <AttractionCard key={idx} attraction={attraction} />
            ))}
          </div>
        </div>
      )
    });
  }

  // 添加餐饮
  if (dayPlan.meals && dayPlan.meals.length > 0) {
    timelineItems.push({
      color: 'orange',
      dot: <RestOutlined />,
      children: (
        <div>
          <Text strong><RestOutlined /> 餐饮安排</Text>
          <div style={{ marginTop: 8 }}>
            {dayPlan.meals.map((meal: any, idx: number) => (
              <MealCard key={idx} meal={meal} />
            ))}
          </div>
        </div>
      )
    });
  }

  // 添加住宿（如果有）
  if (dayPlan.hotel) {
    timelineItems.push({
      color: 'purple',
      children: <HotelInfo hotel={dayPlan.hotel} />
    });
  }

  // 添加备注
  if (dayPlan.notes) {
    timelineItems.push({
      color: 'gray',
      dot: <FileTextOutlined />,
      children: (
        <Card size="small" bodyStyle={{ padding: '12px' }}>
          <Text type="secondary"><FileTextOutlined /> 备注：{dayPlan.notes}</Text>
        </Card>
      )
    });
  }

  return <Timeline items={timelineItems} />;
};

const ItineraryDetail: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [loading, setLoading] = useState(false);
  const [itinerary, setItinerary] = useState<Itinerary | null>(null);

  useEffect(() => {
    if (id) {
      fetchItineraryDetail(id);
    }
  }, [id]);

  const fetchItineraryDetail = async (itineraryId: string) => {
    try {
      setLoading(true);
      const response = await itineraryApi.getById(itineraryId);
      
      if (response.data?.code === 200) {
        setItinerary(response.data.data);
      } else {
        message.error(response.data?.msg || '获取行程详情失败');
      }
    } catch (error) {
      console.error('获取行程详情失败:', error);
      message.error('获取行程详情失败');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ padding: '48px', textAlign: 'center' }}>
        <Spin size="large" tip="加载行程详情..." />
      </div>
    );
  }

  if (!itinerary) {
    return (
      <div style={{ padding: '48px' }}>
        <Empty description="行程不存在或已被删除">
          <Button type="primary" onClick={() => navigate('/itineraries')}>
            返回行程列表
          </Button>
        </Empty>
      </div>
    );
  }

  return (
    <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
      {/* 返回按钮 */}
      <Button 
        icon={<ArrowLeftOutlined />} 
        onClick={() => navigate('/itineraries')}
        style={{ marginBottom: 16 }}
      >
        返回列表
      </Button>

      {/* 行程基本信息卡片 */}
      <Card style={{ marginBottom: 24 }}>
        <Row gutter={[16, 16]}>
          <Col xs={24} md={16}>
            <Title level={3} style={{ margin: 0 }}>
              {itinerary.title || `${itinerary.city_name} ${itinerary.travel_days}日游`}
            </Title>
            <Paragraph type="secondary" style={{ marginTop: 8 }}>
              创建于 {itinerary.created_at ? new Date(itinerary.created_at).toLocaleDateString() : '未知'}
            </Paragraph>
          </Col>
          <Col xs={24} md={8}>
            <Row gutter={[8, 8]}>
              <Col span={12}>
                <Statistic
                  title="总预算"
                  value={itinerary.total_budget}
                  prefix="¥"
                  valueStyle={{ fontSize: 18 }}
                />
              </Col>
              <Col span={12}>
                <Statistic
                  title="天数"
                  value={itinerary.travel_days}
                  suffix="天"
                  valueStyle={{ fontSize: 18 }}
                />
              </Col>
            </Row>
          </Col>
        </Row>
        
        <Divider style={{ margin: '16px 0' }} />
        
        <Descriptions column={{ xs: 1, sm: 2, md: 3 }} size="small">
          <Descriptions.Item label={<><EnvironmentOutlined /> 目的地</>}>
            {itinerary.city_name}
          </Descriptions.Item>
          <Descriptions.Item label={<><CalendarOutlined /> 行程天数</>}>
            {itinerary.travel_days} 天
          </Descriptions.Item>
          <Descriptions.Item label={<><DollarOutlined /> 总预算</>}>
            ¥{itinerary.total_budget}
          </Descriptions.Item>
          <Descriptions.Item label="状态">
            <Tag color={
              itinerary.status === 'completed' ? 'green' :
              itinerary.status === 'draft' ? 'blue' : 'default'
            }>
              {itinerary.status === 'completed' ? '已完成' :
               itinerary.status === 'draft' ? '草稿' : itinerary.status}
            </Tag>
          </Descriptions.Item>
        </Descriptions>
      </Card>

      {/* 每日行程时间轴 */}
      <Title level={4}>
        <CalendarOutlined /> 每日行程安排
      </Title>
      
      {itinerary.day_plans && itinerary.day_plans.length > 0 ? (
        itinerary.day_plans.map((dayPlan: any, index: number) => (
          <Card 
            key={index}
            title={
              <Space>
                <Tag color="blue">第{dayPlan.day}天</Tag>
                <Text>{dayPlan.date}</Text>
              </Space>
            }
            style={{ marginBottom: 16 }}
            headStyle={{ backgroundColor: '#fafafa' }}
          >
            <DayPlanContent dayPlan={dayPlan} />
          </Card>
        ))
      ) : (
        <Empty description="暂无行程安排" />
      )}

      {/* 底部操作按钮 */}
      <Divider />
      <Space>
        <Button type="primary" onClick={() => navigate('/itineraries')}>
          返回行程列表
        </Button>
        <Button danger>删除行程</Button>
      </Space>
    </div>
  );
};

export default ItineraryDetail;
