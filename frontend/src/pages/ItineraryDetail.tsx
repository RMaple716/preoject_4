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
  Col,
  Modal,
  Form,
  Input,
  InputNumber,
  Select,
  TimePicker,
  Popconfirm
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
  FileTextOutlined,
  EditOutlined,
  DeleteOutlined,
  PlusOutlined,
  SaveOutlined
} from '@ant-design/icons';
import { useNavigate, useParams } from 'react-router-dom';
import { itineraryApi, Itinerary, DayPlan } from '../services/itineraryApi';
import dayjs from 'dayjs';

const { Title, Paragraph, Text } = Typography;
const { TextArea } = Input;

// 景点类型定义
interface Attraction {
  name: string;
  visit_time?: string;
  visit_duration?: string;
  ticket_price?: number;
  location?: string;
  description?: string;
  rating?: number;
}

// 餐饮类型定义
interface Meal {
  name: string;
  meal_time?: string;
  restaurant_name?: string;
  cuisine_type?: string;
  price_per_person?: number;
  meal_type?: string; // breakfast/lunch/dinner
}

// 景点编辑表单组件
const AttractionForm: React.FC<{
  initialValues?: Attraction;
  onSubmit: (values: Attraction) => void;
  onCancel: () => void;
}> = ({ initialValues, onSubmit, onCancel }) => {
  const [form] = Form.useForm();

  useEffect(() => {
    if (initialValues) {
      form.setFieldsValue({
        ...initialValues,
        visit_time: initialValues.visit_time ? dayjs(initialValues.visit_time, 'HH:mm') : null,
      });
    }
  }, [initialValues, form]);

  const handleSubmit = () => {
    form.validateFields().then((values) => {
      const formattedValues = {
        ...values,
        visit_time: values.visit_time ? values.visit_time.format('HH:mm') : undefined,
      };
      onSubmit(formattedValues);
    });
  };

  return (
    <Form form={form} layout="vertical">
      <Form.Item
        name="name"
        label="景点名称"
        rules={[{ required: true, message: '请输入景点名称' }]}
      >
        <Input placeholder="例如：故宫博物院" />
      </Form.Item>
      
      <Form.Item
        name="visit_time"
        label="游览时间"
      >
        <TimePicker format="HH:mm" placeholder="选择时间" style={{ width: '100%' }} />
      </Form.Item>
      
      <Form.Item
        name="visit_duration"
        label="游览时长"
      >
        <Input placeholder="例如：2小时" />
      </Form.Item>
      
      <Form.Item
        name="ticket_price"
        label="门票价格（元）"
      >
        <InputNumber min={0} style={{ width: '100%' }} placeholder="0" />
      </Form.Item>
      
      <Form.Item
        name="location"
        label="地点"
      >
        <Input placeholder="例如：北京市东城区" />
      </Form.Item>
      
      <Form.Item
        name="description"
        label="描述"
      >
        <TextArea rows={2} placeholder="景点简介..." />
      </Form.Item>
      
      <Form.Item
        name="rating"
        label="评分"
      >
        <InputNumber min={0} max={5} step={0.1} style={{ width: '100%' }} placeholder="0-5" />
      </Form.Item>
      
      <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
        <Space>
          <Button onClick={onCancel}>取消</Button>
          <Button type="primary" onClick={handleSubmit}>
            确定
          </Button>
        </Space>
      </Form.Item>
    </Form>
  );
};

// 餐饮编辑表单组件
const MealForm: React.FC<{
  initialValues?: Meal;
  onSubmit: (values: Meal) => void;
  onCancel: () => void;
}> = ({ initialValues, onSubmit, onCancel }) => {
  const [form] = Form.useForm();

  useEffect(() => {
    if (initialValues) {
      form.setFieldsValue({
        ...initialValues,
        meal_time: initialValues.meal_time ? dayjs(initialValues.meal_time, 'HH:mm') : null,
      });
    }
  }, [initialValues, form]);

  const handleSubmit = () => {
    form.validateFields().then((values) => {
      const formattedValues = {
        ...values,
        meal_time: values.meal_time ? values.meal_time.format('HH:mm') : undefined,
      };
      onSubmit(formattedValues);
    });
  };

  return (
    <Form form={form} layout="vertical">
      <Form.Item
        name="name"
        label="餐厅名称"
        rules={[{ required: true, message: '请输入餐厅名称' }]}
      >
        <Input placeholder="例如：全聚德烤鸭店" />
      </Form.Item>
      
      <Form.Item
        name="meal_type"
        label="餐次"
      >
        <Select placeholder="选择餐次">
          <Select.Option value="breakfast">早餐</Select.Option>
          <Select.Option value="lunch">午餐</Select.Option>
          <Select.Option value="dinner">晚餐</Select.Option>
        </Select>
      </Form.Item>
      
      <Form.Item
        name="meal_time"
        label="用餐时间"
      >
        <TimePicker format="HH:mm" placeholder="选择时间" style={{ width: '100%' }} />
      </Form.Item>
      
      <Form.Item
        name="cuisine_type"
        label="菜系"
      >
        <Input placeholder="例如：北京菜" />
      </Form.Item>
      
      <Form.Item
        name="price_per_person"
        label="人均价格（元）"
      >
        <InputNumber min={0} style={{ width: '100%' }} placeholder="0" />
      </Form.Item>
      
      <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
        <Space>
          <Button onClick={onCancel}>取消</Button>
          <Button type="primary" onClick={handleSubmit}>
            确定
          </Button>
        </Space>
      </Form.Item>
    </Form>
  );
};

// 景点卡片组件（带编辑功能）
const AttractionCard: React.FC<{ 
  attraction: any; 
  index: number;
  dayIndex: number;
  onEdit: (dayIndex: number, attractionIndex: number) => void;
  onDelete: (dayIndex: number, attractionIndex: number) => void;
}> = ({ attraction, index, dayIndex, onEdit, onDelete }) => (
  <Card 
    size="small" 
    style={{ marginBottom: 8 }}
    bodyStyle={{ padding: '12px' }}
    extra={
      <Space size="small">
        <Button 
          type="text" 
          size="small" 
          icon={<EditOutlined />}
          onClick={() => onEdit(dayIndex, index)}
        />
        <Popconfirm
          title="确定删除此景点吗？"
          onConfirm={() => onDelete(dayIndex, index)}
          okText="确定"
          cancelText="取消"
        >
          <Button 
            type="text" 
            size="small" 
            danger
            icon={<DeleteOutlined />}
          />
        </Popconfirm>
      </Space>
    }
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
        {attraction.visit_time && (
          <Tag icon={<ClockCircleOutlined />} color="blue">
            {attraction.visit_time}
          </Tag>
        )}
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

// 餐饮卡片组件（带编辑功能）
const MealCard: React.FC<{ 
  meal: any; 
  index: number;
  dayIndex: number;
  onEdit: (dayIndex: number, mealIndex: number) => void;
  onDelete: (dayIndex: number, mealIndex: number) => void;
}> = ({ meal, index, dayIndex, onEdit, onDelete }) => (
  <Card 
    size="small" 
    style={{ marginBottom: 8 }}
    bodyStyle={{ padding: '12px' }}
    extra={
      <Space size="small">
        <Button 
          type="text" 
          size="small" 
          icon={<EditOutlined />}
          onClick={() => onEdit(dayIndex, index)}
        />
        <Popconfirm
          title="确定删除此餐饮吗？"
          onConfirm={() => onDelete(dayIndex, index)}
          okText="确定"
          cancelText="取消"
        >
          <Button 
            type="text" 
            size="small" 
            danger
            icon={<DeleteOutlined />}
          />
        </Popconfirm>
      </Space>
    }
  >
    <Space direction="vertical" size="small" style={{ width: '100%' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Text strong>{meal.restaurant_name || meal.name}</Text>
        {meal.meal_type && (
          <Tag color="orange">
            {meal.meal_type === 'breakfast' ? '早餐' : 
             meal.meal_type === 'lunch' ? '午餐' : '晚餐'}
          </Tag>
        )}
      </div>
      {meal.cuisine_type && (
        <Text type="secondary" style={{ fontSize: 12 }}>
          {meal.cuisine_type}
        </Text>
      )}
      <Space size="small">
        {meal.meal_time && (
          <Tag icon={<ClockCircleOutlined />} color="blue">
            {meal.meal_time}
          </Tag>
        )}
        {meal.price_per_person && (
          <Tag icon={<DollarOutlined />} color="green">
            ¥{meal.price_per_person}/人
          </Tag>
        )}
      </Space>
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

// 每日行程内容组件（带编辑功能）
const DayPlanContent: React.FC<{ 
  dayPlan: any;
  dayIndex: number;
  onEditAttraction: (dayIndex: number, attractionIndex: number) => void;
  onDeleteAttraction: (dayIndex: number, attractionIndex: number) => void;
  onAddAttraction: (dayIndex: number) => void;
  onEditMeal: (dayIndex: number, mealIndex: number) => void;
  onDeleteMeal: (dayIndex: number, mealIndex: number) => void;
  onAddMeal: (dayIndex: number) => void;
  onEditNotes: (dayIndex: number) => void;
}> = ({ 
  dayPlan, 
  dayIndex,
  onEditAttraction,
  onDeleteAttraction,
  onAddAttraction,
  onEditMeal,
  onDeleteMeal,
  onAddMeal,
  onEditNotes
}) => {
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
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
            <Text strong><CameraOutlined /> 景点游览</Text>
            <Button 
              type="dashed" 
              size="small" 
              icon={<PlusOutlined />}
              onClick={() => onAddAttraction(dayIndex)}
            >
              添加景点
            </Button>
          </div>
          <div style={{ marginTop: 8 }}>
            {dayPlan.attractions.map((attraction: any, idx: number) => (
              <AttractionCard 
                key={idx} 
                attraction={attraction} 
                index={idx}
                dayIndex={dayIndex}
                onEdit={onEditAttraction}
                onDelete={onDeleteAttraction}
              />
            ))}
          </div>
        </div>
      )
    });
  } else {
    // 没有景点时显示添加按钮
    timelineItems.push({
      color: 'green',
      dot: <CameraOutlined />,
      children: (
        <Button 
          type="dashed" 
          block
          icon={<PlusOutlined />}
          onClick={() => onAddAttraction(dayIndex)}
        >
          添加景点
        </Button>
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
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
            <Text strong><RestOutlined /> 餐饮安排</Text>
            <Button 
              type="dashed" 
              size="small" 
              icon={<PlusOutlined />}
              onClick={() => onAddMeal(dayIndex)}
            >
              添加餐饮
            </Button>
          </div>
          <div style={{ marginTop: 8 }}>
            {dayPlan.meals.map((meal: any, idx: number) => (
              <MealCard 
                key={idx} 
                meal={meal} 
                index={idx}
                dayIndex={dayIndex}
                onEdit={onEditMeal}
                onDelete={onDeleteMeal}
              />
            ))}
          </div>
        </div>
      )
    });
  } else {
    // 没有餐饮时显示添加按钮
    timelineItems.push({
      color: 'orange',
      dot: <RestOutlined />,
      children: (
        <Button 
          type="dashed" 
          block
          icon={<PlusOutlined />}
          onClick={() => onAddMeal(dayIndex)}
        >
          添加餐饮
        </Button>
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
  timelineItems.push({
    color: 'gray',
    dot: <FileTextOutlined />,
    children: (
      <Card size="small" bodyStyle={{ padding: '12px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <Text type="secondary"><FileTextOutlined /> 备注：</Text>
          <Button 
            type="text" 
            size="small" 
            icon={<EditOutlined />}
            onClick={() => onEditNotes(dayIndex)}
          />
        </div>
        <div style={{ marginTop: 4 }}>
          {dayPlan.notes ? (
            <Text>{dayPlan.notes}</Text>
          ) : (
            <Text type="secondary">暂无备注</Text>
          )}
        </div>
      </Card>
    )
  });

  return <Timeline items={timelineItems} />;
};

const ItineraryDetail: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [itinerary, setItinerary] = useState<Itinerary | null>(null);
  
  // 编辑状态
  const [editAttractionModal, setEditAttractionModal] = useState<{
    visible: boolean;
    dayIndex: number;
    attractionIndex?: number;
    initialValues?: Attraction;
  }>({ visible: false, dayIndex: -1 });
  
  const [editMealModal, setEditMealModal] = useState<{
    visible: boolean;
    dayIndex: number;
    mealIndex?: number;
    initialValues?: Meal;
  }>({ visible: false, dayIndex: -1 });
  
  const [editNotesModal, setEditNotesModal] = useState<{
    visible: boolean;
    dayIndex: number;
    notes?: string;
  }>({ visible: false, dayIndex: -1 });

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

  // 保存行程
  const saveItinerary = async () => {
    if (!itinerary || !id) return;
    
    try {
      setSaving(true);
      const response = await itineraryApi.update(id, {
        title: itinerary.title,
        day_plans: itinerary.day_plans,
      });
      
      if (response.data?.code === 200) {
        message.success('保存成功');
        setItinerary(response.data.data);
      } else {
        message.error(response.data?.msg || '保存失败');
      }
    } catch (error) {
      console.error('保存失败:', error);
      message.error('保存失败');
    } finally {
      setSaving(false);
    }
  };

  // 景点编辑处理
  const handleEditAttraction = (dayIndex: number, attractionIndex: number) => {
    const attraction = itinerary?.day_plans?.[dayIndex]?.attractions?.[attractionIndex];
    setEditAttractionModal({
      visible: true,
      dayIndex,
      attractionIndex,
      initialValues: attraction,
    });
  };

  const handleAddAttraction = (dayIndex: number) => {
    setEditAttractionModal({
      visible: true,
      dayIndex,
    });
  };

  const handleDeleteAttraction = (dayIndex: number, attractionIndex: number) => {
    if (!itinerary || !itinerary.day_plans) return;
    
    const newDayPlans = [...itinerary.day_plans];
    const attractions = [...(newDayPlans[dayIndex].attractions || [])];
    attractions.splice(attractionIndex, 1);
    newDayPlans[dayIndex] = {
      ...newDayPlans[dayIndex],
      attractions,
    };
    
    setItinerary({
      ...itinerary,
      day_plans: newDayPlans,
    });
    
    message.success('已删除景点');
  };

  const handleSubmitAttraction = (values: Attraction) => {
    if (!itinerary || !itinerary.day_plans) return;
    
    const newDayPlans = [...itinerary.day_plans];
    const attractions = [...(newDayPlans[editAttractionModal.dayIndex].attractions || [])];
    
    if (editAttractionModal.attractionIndex !== undefined) {
      // 编辑现有景点
      attractions[editAttractionModal.attractionIndex] = values;
    } else {
      // 添加新景点
      attractions.push(values);
    }
    
    newDayPlans[editAttractionModal.dayIndex] = {
      ...newDayPlans[editAttractionModal.dayIndex],
      attractions,
    };
    
    setItinerary({
      ...itinerary,
      day_plans: newDayPlans,
    });
    
    setEditAttractionModal({ visible: false, dayIndex: -1 });
    message.success(editAttractionModal.attractionIndex !== undefined ? '修改成功' : '添加成功');
  };

  // 餐饮编辑处理
  const handleEditMeal = (dayIndex: number, mealIndex: number) => {
    const meal = itinerary?.day_plans?.[dayIndex]?.meals?.[mealIndex];
    setEditMealModal({
      visible: true,
      dayIndex,
      mealIndex,
      initialValues: meal,
    });
  };

  const handleAddMeal = (dayIndex: number) => {
    setEditMealModal({
      visible: true,
      dayIndex,
    });
  };

  const handleDeleteMeal = (dayIndex: number, mealIndex: number) => {
    if (!itinerary || !itinerary.day_plans) return;
    
    const newDayPlans = [...itinerary.day_plans];
    const meals = [...(newDayPlans[dayIndex].meals || [])];
    meals.splice(mealIndex, 1);
    newDayPlans[dayIndex] = {
      ...newDayPlans[dayIndex],
      meals,
    };
    
    setItinerary({
      ...itinerary,
      day_plans: newDayPlans,
    });
    
    message.success('已删除餐饮');
  };

  const handleSubmitMeal = (values: Meal) => {
    if (!itinerary || !itinerary.day_plans) return;
    
    const newDayPlans = [...itinerary.day_plans];
    const meals = [...(newDayPlans[editMealModal.dayIndex].meals || [])];
    
    if (editMealModal.mealIndex !== undefined) {
      // 编辑现有餐饮
      meals[editMealModal.mealIndex] = values;
    } else {
      // 添加新餐饮
      meals.push(values);
    }
    
    newDayPlans[editMealModal.dayIndex] = {
      ...newDayPlans[editMealModal.dayIndex],
      meals,
    };
    
    setItinerary({
      ...itinerary,
      day_plans: newDayPlans,
    });
    
    setEditMealModal({ visible: false, dayIndex: -1 });
    message.success(editMealModal.mealIndex !== undefined ? '修改成功' : '添加成功');
  };

  // 备注编辑处理
  const handleEditNotes = (dayIndex: number) => {
    const notes = itinerary?.day_plans?.[dayIndex]?.notes;
    setEditNotesModal({
      visible: true,
      dayIndex,
      notes,
    });
  };

  const handleSubmitNotes = () => {
    if (!itinerary || !itinerary.day_plans) return;
    
    const form = document.querySelector('#notesForm') as HTMLFormElement;
    if (form) {
      const formData = new FormData(form);
      const notes = formData.get('notes') as string;
      
      const newDayPlans = [...itinerary.day_plans];
      newDayPlans[editNotesModal.dayIndex] = {
        ...newDayPlans[editNotesModal.dayIndex],
        notes,
      };
      
      setItinerary({
        ...itinerary,
        day_plans: newDayPlans,
      });
      
      setEditNotesModal({ visible: false, dayIndex: -1 });
      message.success('备注已更新');
    }
  };

  // 删除行程
  const handleDeleteItinerary = async () => {
    if (!id) return;
    
    try {
      const response = await itineraryApi.delete(id);
      if (response.data?.code === 200) {
        message.success('行程已删除');
        navigate('/itineraries');
      } else {
        message.error(response.data?.msg || '删除失败');
      }
    } catch (error) {
      console.error('删除失败:', error);
      message.error('删除失败');
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
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <Title level={4} style={{ margin: 0 }}>
          <CalendarOutlined /> 每日行程安排
        </Title>
        <Button 
          type="primary" 
          icon={<SaveOutlined />} 
          onClick={saveItinerary}
          loading={saving}
        >
          保存修改
        </Button>
      </div>
      
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
            <DayPlanContent 
              dayPlan={dayPlan} 
              dayIndex={index}
              onEditAttraction={handleEditAttraction}
              onDeleteAttraction={handleDeleteAttraction}
              onAddAttraction={handleAddAttraction}
              onEditMeal={handleEditMeal}
              onDeleteMeal={handleDeleteMeal}
              onAddMeal={handleAddMeal}
              onEditNotes={handleEditNotes}
            />
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
        <Popconfirm
          title="确定删除此行程吗？"
          description="删除后无法恢复"
          onConfirm={handleDeleteItinerary}
          okText="确定"
          cancelText="取消"
          okButtonProps={{ danger: true }}
        >
          <Button danger>删除行程</Button>
        </Popconfirm>
      </Space>

      {/* 景点编辑弹窗 */}
      <Modal
        title={editAttractionModal.attractionIndex !== undefined ? '编辑景点' : '添加景点'}
        open={editAttractionModal.visible}
        onCancel={() => setEditAttractionModal({ visible: false, dayIndex: -1 })}
        footer={null}
        width={600}
      >
        <AttractionForm
          initialValues={editAttractionModal.initialValues}
          onSubmit={handleSubmitAttraction}
          onCancel={() => setEditAttractionModal({ visible: false, dayIndex: -1 })}
        />
      </Modal>

      {/* 餐饮编辑弹窗 */}
      <Modal
        title={editMealModal.mealIndex !== undefined ? '编辑餐饮' : '添加餐饮'}
        open={editMealModal.visible}
        onCancel={() => setEditMealModal({ visible: false, dayIndex: -1 })}
        footer={null}
        width={600}
      >
        <MealForm
          initialValues={editMealModal.initialValues}
          onSubmit={handleSubmitMeal}
          onCancel={() => setEditMealModal({ visible: false, dayIndex: -1 })}
        />
      </Modal>

      {/* 备注编辑弹窗 */}
      <Modal
        title="编辑备注"
        open={editNotesModal.visible}
        onOk={handleSubmitNotes}
        onCancel={() => setEditNotesModal({ visible: false, dayIndex: -1 })}
        okText="保存"
        cancelText="取消"
      >
        <Form id="notesForm" layout="vertical">
          <Form.Item name="notes" initialValue={editNotesModal.notes}>
            <TextArea rows={4} placeholder="输入备注信息..." />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default ItineraryDetail;
