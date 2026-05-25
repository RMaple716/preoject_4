import React, { useState } from 'react';
import { 
  Form, 
  Input, 
  InputNumber, 
  DatePicker, 
  Select, 
  Button, 
  Card, 
  Typography, 
  message,
  Space,
  Tag,
  Row,
  Col,
  Divider,
  Tooltip,
  Alert
} from 'antd';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import dayjs from 'dayjs';
import { 
  EnvironmentOutlined, 
  CalendarOutlined, 
  DollarOutlined,
  TeamOutlined,
  HeartOutlined,
  InfoCircleOutlined
} from '@ant-design/icons';
import { requirementApi, Requirement } from '../services/requirementApi';
import { setRequirement, setLoading } from '../store/slices/requirementSlice';

const { Title, Paragraph, Text } = Typography;
const { TextArea } = Input;

// 旅行偏好选项（更丰富的选择）
const travelPreferences = [
  { label: '历史古迹', value: '历史古迹', icon: '🏛️' },
  { label: '自然风光', value: '自然风光', icon: '🏞️' },
  { label: '美食探索', value: '美食探索', icon: '🍜' },
  { label: '购物休闲', value: '购物休闲', icon: '🛍️' },
  { label: '文化体验', value: '文化体验', icon: '🎭' },
  { label: '户外运动', value: '户外运动', icon: '🚴' },
  { label: '摄影打卡', value: '摄影打卡', icon: '📸' },
  { label: '亲子活动', value: '亲子活动', icon: '👨‍👩‍👧‍👦' },
  { label: '夜生活', value: '夜生活', icon: '🌃' },
  { label: '温泉度假', value: '温泉度假', icon: '♨️' },
];

// 出行类型选项
const travelTypes = [
  { label: '家庭出游', value: 'family', icon: '👨‍👩‍👧‍👦' },
  { label: '情侣出行', value: 'couple', icon: '💑' },
  { label: '朋友同行', value: 'friends', icon: '👥' },
  { label: '独自旅行', value: 'solo', icon: '🚶' },
  { label: '商务出差', value: 'business', icon: '💼' },
];

const RequirementForm: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [form] = Form.useForm();
  const [loading, setLoadingState] = useState(false);
  const [selectedPrefs, setSelectedPrefs] = useState<string[]>([]);

  const handleSubmit = async (values: any) => {
    try {
      setLoadingState(true);
      dispatch(setLoading(true));

      // 生成临时用户ID（实际项目中应从认证系统获取）
      const userId = `user_${Date.now()}`;

      const requirement: Requirement = {
        city_name: values.city_name,
        travel_days: values.travel_days,
        total_budget: values.total_budget,
        travel_date: values.travel_date.format('YYYY-MM-DD'),
        traveler_count: values.traveler_count,
        preferences: values.preferences || [],
        travel_type: values.travel_type,
        special_needs: values.special_needs,
      };

      console.log('提交需求:', requirement);

      const response = await requirementApi.submit({
        user_id: userId,
        requirement: {
          city_name: requirement.city_name,
          travel_days: requirement.travel_days,
          total_budget: requirement.total_budget,
          travel_type: requirement.travel_type,
          start_date: requirement.travel_date,
          preferences: requirement.preferences,
        }
      });
      const responseData = response.data;
      
      if (responseData?.code === 200) {
        message.success('✅ 需求提交成功！');
        
        const requirementId = responseData.data.requirement_id;
        dispatch(setRequirement({
          ...requirement,
          requirement_id: requirementId
        }));
        
        // 自动进行任务分解
        message.loading({ content: '正在智能规划行程...', key: 'decompose', duration: 0 });
        
        const decomposeResponse = await fetch('/api/v1/task/decompose', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            requirement_id: requirementId,
            structured_requirement: {
              city_name: requirement.city_name,
              travel_days: requirement.travel_days,
              total_budget: requirement.total_budget,
              travel_date: requirement.travel_date,
              traveler_count: requirement.traveler_count,
              preferences: requirement.preferences,
            }
          })
        });
        
        const decomposeData = await decomposeResponse.json();
        message.destroy('decompose');
        
        if (decomposeData.code === 200) {
          message.success('🎉 任务分解成功！正在生成专属行程...');
          setTimeout(() => {
            navigate(`/task/${decomposeData.data.task_id}`);
          }, 1500);
        } else {
          message.error(decomposeData.msg || '任务分解失败');
        }
      } else {
        message.error(responseData?.msg || '提交失败');
      }
    } catch (error) {
      console.error('提交失败:', error);
      message.error('❌ 提交失败，请检查网络连接后重试');
    } finally {
      setLoadingState(false);
      dispatch(setLoading(false));
    }
  };

  const handleReset = () => {
    form.resetFields();
    setSelectedPrefs([]);
    message.info('已重置表单');
  };

  return (
    <div style={{ padding: '24px', maxWidth: '900px', margin: '0 auto' }}>
      <Card variant="borderless">
        <Title level={2} style={{ textAlign: 'center', marginBottom: 8 }}>
          <EnvironmentOutlined style={{ color: '#1890ff', marginRight: 8 }} />
          定制您的专属行程
        </Title>
        <Paragraph type="secondary" style={{ textAlign: 'center', fontSize: 16 }}>
          填写旅行偏好，AI将为您智能规划完美行程
        </Paragraph>

        <Alert
          message="温馨提示"
          description="所有带 * 的字段为必填项，请如实填写以获得更精准的行程推荐"
          type="info"
          showIcon
          icon={<InfoCircleOutlined />}
          style={{ marginBottom: 24 }}
        />

        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          initialValues={{
            travel_days: 3,
            traveler_count: 2,
            total_budget: 5000,
            preferences: [],
          }}
          size="large"
        >
          <Divider orientation="left">
            <Text strong>基本信息</Text>
          </Divider>

          <Row gutter={16}>
            <Col xs={24} md={12}>
              <Form.Item
                label={
                  <Space>
                    <EnvironmentOutlined />
                    <span>目的地城市 <Text type="danger">*</Text></span>
                  </Space>
                }
                name="city_name"
                rules={[
                  { required: true, message: '请输入目的地城市' },
                  { min: 2, message: '城市名称至少2个字符' }
                ]}
                tooltip="请输入您想要前往的城市名称"
              >
                <Input 
                  placeholder="例如：北京、上海、杭州、成都" 
                  prefix={<EnvironmentOutlined />}
                  allowClear
                />
              </Form.Item>
            </Col>

            <Col xs={24} md={12}>
              <Form.Item
                label={
                  <Space>
                    <CalendarOutlined />
                    <span>出发日期 <Text type="danger">*</Text></span>
                  </Space>
                }
                name="travel_date"
                rules={[{ required: true, message: '请选择出发日期' }]}
                tooltip="选择您的旅行开始日期"
              >
                <DatePicker 
                  style={{ width: '100%' }} 
                  disabledDate={(current: dayjs.Dayjs) => current && current < dayjs().startOf('day')}
                  format="YYYY-MM-DD"
                  placeholder="选择出发日期"
                />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col xs={24} md={8}>
              <Form.Item
                label={
                  <Space>
                    <CalendarOutlined />
                    <span>旅行天数 <Text type="danger">*</Text></span>
                  </Space>
                }
                name="travel_days"
                rules={[
                  { required: true, message: '请输入旅行天数' },
                  { type: 'number', min: 1, max: 30, message: '天数范围为1-30天' }
                ]}
                tooltip="建议1-7天的短途旅行，或7-30天的长途旅行"
              >
                <Input.Group compact>
                  <InputNumber 
                    min={1} 
                    max={30} 
                    style={{ width: 'calc(100% - 40px)' }}
                    placeholder="例如：3"
                  />
                  <Input disabled style={{ width: '40px', textAlign: 'center' }} value="天" />
                </Input.Group>
              </Form.Item>
            </Col>

            <Col xs={24} md={8}>
              <Form.Item
                label={
                  <Space>
                    <TeamOutlined />
                    <span>出行人数 <Text type="danger">*</Text></span>
                  </Space>
                }
                name="traveler_count"
                rules={[
                  { required: true, message: '请输入出行人数' },
                  { type: 'number', min: 1, max: 20, message: '人数范围为1-20人' }
                ]}
                tooltip="包括您自己在内的总人数"
              >
                <Input.Group compact>
                  <InputNumber 
                    min={1} 
                    max={20} 
                    style={{ width: 'calc(100% - 40px)' }}
                    placeholder="例如：2"
                  />
                  <Input disabled style={{ width: '40px', textAlign: 'center' }} value="人" />
                </Input.Group>
              </Form.Item>
            </Col>

            <Col xs={24} md={8}>
              <Form.Item
                label={
                  <Space>
                    <DollarOutlined />
                    <span>总预算（元）<Text type="danger">*</Text></span>
                  </Space>
                }
                name="total_budget"
                rules={[
                  { required: true, message: '请输入总预算' },
                  { type: 'number', min: 1000, message: '最低预算1000元' }
                ]}
                tooltip="包含交通、住宿、餐饮、门票等所有费用"
              >
                <InputNumber 
                  min={1000} 
                  step={500}
                  style={{ width: '100%' }} 
                  placeholder="例如：5000"
                  addonBefore="¥"
                />
              </Form.Item>
            </Col>
          </Row>

          <Divider orientation="left">
            <Text strong>旅行偏好</Text>
          </Divider>

          <Form.Item
            label={
              <Space>
                <HeartOutlined />
                <span>出行类型</span>
              </Space>
            }
            name="travel_type"
            tooltip="选择适合您的出行方式"
          >
            <Select
              placeholder="选择出行类型（可选）"
              allowClear
              optionLabelProp="label"
            >
              {travelTypes.map(type => (
                <Select.Option key={type.value} value={type.value} label={`${type.icon} ${type.label}`}>
                  <Space>
                    <span>{type.icon}</span>
                    <span>{type.label}</span>
                  </Space>
                </Select.Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item
            label={
              <Space>
                <HeartOutlined />
                <span>旅行偏好（可多选）</span>
              </Space>
            }
            name="preferences"
            tooltip="选择您感兴趣的旅行活动类型"
          >
            <Select
              mode="multiple"
              placeholder="选择您的旅行偏好（最多选5个）"
              allowClear
              maxTagCount={5}
              onChange={(value: string[]) => setSelectedPrefs(value)}
            >
              {travelPreferences.map(pref => (
                <Select.Option key={pref.value} value={pref.value}>
                  <Space>
                    <span>{pref.icon}</span>
                    <span>{pref.label}</span>
                  </Space>
                </Select.Option>
              ))}
            </Select>
          </Form.Item>

          {selectedPrefs.length > 0 && (
            <div style={{ marginBottom: 16 }}>
              <Text type="secondary">已选择：</Text>
              <Space wrap>
                {selectedPrefs.map(pref => {
                  const prefObj = travelPreferences.find(p => p.value === pref);
                  return (
                    <Tag key={pref} color="blue">
                      {prefObj?.icon} {prefObj?.label}
                    </Tag>
                  );
                })}
              </Space>
            </div>
          )}

          <Form.Item
            label="特殊需求"
            name="special_needs"
            tooltip="如有特殊需求请在此说明，我们将尽力满足"
          >
            <TextArea 
              rows={4} 
              placeholder={'例如：\n- 需要无障碍设施\n- 携带儿童，需要亲子友好型景点\n- 有饮食禁忌（素食/清真/过敏等）\n- 希望安排一些自由活动时间'}
              maxLength={500}
              showCount
            />
          </Form.Item>

          <Divider />

          <Form.Item>
            <Space size="middle" style={{ width: '100%', justifyContent: 'center' }}>
              <Button 
                type="primary" 
                htmlType="submit" 
                loading={loading}
                size="large"
                style={{ minWidth: 150 }}
              >
                {loading ? '提交中...' : '🚀 开始智能规划'}
              </Button>
              <Button 
                onClick={handleReset}
                size="large"
                style={{ minWidth: 120 }}
              >
                重置
              </Button>
            </Space>
          </Form.Item>
        </Form>

        <Divider />

        <div style={{ textAlign: 'center' }}>
          <Text type="secondary" style={{ fontSize: 12 }}>
            💡 提示：填写越详细，生成的行程越符合您的期望
          </Text>
        </div>
      </Card>
    </div>
  );
};

export default RequirementForm;
