import React, { useEffect, useState } from 'react';
import { Typography, Button, Progress, Card, List, Tag, Spin, Alert } from 'antd';
import { useNavigate, useParams } from 'react-router-dom';
import { CheckCircleOutlined, ClockCircleOutlined, LoadingOutlined } from '@ant-design/icons';
import { taskApi } from '../services';

const { Title, Paragraph, Text } = Typography;

interface SubTask {
  task_id: string;
  agent: string;
  status: string;
  result?: any;
}

interface TaskInfo {
  task_id: string;
  batch_id: string;
  requirement_id: string;
  type: string;
  subtasks: string[];
  status: string;
  progress: number;
  created_at: string;
}

const TaskStatus: React.FC = () => {
  const navigate = useNavigate();
  const { taskId } = useParams();
  const [loading, setLoading] = useState(true);
  const [taskInfo, setTaskInfo] = useState<TaskInfo | null>(null);
  const [subTasks, setSubTasks] = useState<SubTask[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!taskId) return;

    const pollTaskStatus = async () => {
      try {
        const response = await taskApi.getById(taskId);

        if (response.code === 200) {
          const data = response.data;
          setTaskInfo(data);

          // 获取子任务状态
          if (data.subtasks && data.subtasks.length > 0) {
            const subTasksPromises = data.subtasks.map((subtaskId: string) =>
              taskApi.getById(subtaskId)
            );
            const subTasksResponses = await Promise.all(subTasksPromises);
            const subTasksData = subTasksResponses
              .filter(res => res.code === 200)
              .map(res => res.data);
            setSubTasks(subTasksData);
          }

          // 如果任务完成,停止轮询
          if (data.status === 'success' || data.status === 'completed' || data.status === 'failed') {
            setLoading(false);

            // 如果任务成功完成,跳转到行程详情页
            if (data.status === 'success' || data.status === 'completed') {
              setTimeout(() => {
                navigate(`/itinerary/${taskId}`);
              }, 1500);
            }
          }
        }
      } catch (err) {
        console.error('获取任务状态失败:', err);
        setError('获取任务状态失败');
        setLoading(false);
      }
    };

    // 立即执行一次
    pollTaskStatus();

    // 设置轮询
    const interval = setInterval(pollTaskStatus, 2000);

    return () => clearInterval(interval);
  }, [taskId, navigate]);

  const getAgentName = (agent: string) => {
    const agentNames: { [key: string]: string } = {
      attraction: '景点推荐',
      accommodation: '住宿推荐',
      food: '美食推荐',
      transport: '交通规划'
    };
    return agentNames[agent] || agent;
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
      case 'success':
        return <CheckCircleOutlined style={{ color: '#52c41a' }} />;
      case 'pending':
        return <ClockCircleOutlined style={{ color: '#faad14' }} />;
      case 'processing':
        return <LoadingOutlined style={{ color: '#1890ff' }} />;
      default:
        return null;
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'completed':
      case 'success':
        return '已完成';
      case 'pending':
        return '待处理';
      case 'processing':
        return '处理中';
      case 'failed':
        return '失败';
      default:
        return status;
    }
  };

  if (error) {
    return (
      <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
        <Alert
          message="错误"
          description={error}
          type="error"
          showIcon
          action={
            <Button size="small" onClick={() => navigate('/')}>
              返回首页
            </Button>
          }
        />
      </div>
    );
  }

  return (
    <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
      <Spin spinning={loading} tip="正在处理中...">
        <Card>
          <Title level={3}>智能规划进度</Title>

          {taskInfo && (
            <>
              <Paragraph>
                <Text strong>任务ID:</Text> {taskInfo.task_id}
              </Paragraph>

              <div style={{ margin: '24px 0' }}>
                <Progress
                  percent={typeof taskInfo.progress === 'number' ? (taskInfo.progress > 1 ? taskInfo.progress : taskInfo.progress * 100) : 0}
                  status={taskInfo.status === 'failed' ? 'exception' : 'active'}
                  strokeColor={{
                    '0%': '#108ee9',
                    '100%': '#87d068',
                  }}
                />
                <Paragraph style={{ marginTop: '8px' }}>
                  总体进度: {typeof taskInfo.progress === 'number' ? (taskInfo.progress > 1 ? taskInfo.progress : taskInfo.progress * 100) : 0}%
                </Paragraph>
              </div>

              {subTasks.length > 0 && (
                <div>
                  <Title level={4}>子任务状态</Title>
                  <List
                    dataSource={subTasks}
                    renderItem={(subTask) => (
                      <List.Item
                        actions={[
                          <Tag
                            color={
                              subTask.status === 'completed' || subTask.status === 'success'
                                ? 'success'
                                : subTask.status === 'processing'
                                ? 'processing'
                                : subTask.status === 'failed'
                                ? 'error'
                                : 'default'
                            }
                            icon={getStatusIcon(subTask.status)}
                          >
                            {getStatusText(subTask.status)}
                          </Tag>,
                        ]}
                      >
                        <List.Item.Meta
                          avatar={getStatusIcon(subTask.status)}
                          title={getAgentName(subTask.agent)}
                          description={`任务ID: ${subTask.task_id}`}
                        />
                      </List.Item>
                    )}
                  />
                </div>
              )}

              {(taskInfo.status === 'completed' || taskInfo.status === 'success') && (
                <Alert
                  message="规划完成"
                  description="正在跳转到行程详情页..."
                  type="success"
                  showIcon
                  style={{ marginTop: '24px' }}
                />
              )}

              {taskInfo.status === 'failed' && (
                <Alert
                  message="规划失败"
                  description="请检查网络连接后重试"
                  type="error"
                  showIcon
                  style={{ marginTop: '24px' }}
                  action={
                    <Button onClick={() => navigate('/requirement')}>
                      重新规划
                    </Button>
                  }
                />
              )}
            </>
          )}
        </Card>
      </Spin>
    </div>
  );
};

export default TaskStatus;
