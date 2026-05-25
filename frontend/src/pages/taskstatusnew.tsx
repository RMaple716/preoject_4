import React, { useEffect, useState } from 'react';
import { Typography, Button, Progress, Card, Spin, Alert } from 'antd';
import { useNavigate, useParams } from 'react-router-dom';
import { taskApi } from '../services';

const { Title, Paragraph, Text } = Typography;

interface TaskInfo {
  task_id: string;
  status: string;
  progress: number;
  failed_subtasks: string[];
  message: string;
  itinerary_id?: string;  // 添加行程ID字段
}

const TaskStatus: React.FC = () => {
  const navigate = useNavigate();
  const { taskId } = useParams();
  const [loading, setLoading] = useState(true);
  const [taskInfo, setTaskInfo] = useState<TaskInfo | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!taskId) return;

    const pollTaskStatus = async () => {
      try {
        const response = await taskApi.getById(taskId);

        if (response.code === 200) {
          const data = response.data;
          setTaskInfo(data);

          // 如果任务完成,停止轮询
          if (data.status === 'success' || data.status === 'failed') {
            setLoading(false);

            // 如果任务成功完成,跳转到行程详情页
            if (data.status === 'success') {
              setTimeout(() => {
                // 使用行程ID进行跳转,如果没有行程ID则使用任务ID
                const itineraryId = data.itinerary_id || taskId;
                navigate(`/itinerary/${itineraryId}`);
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
                  percent={taskInfo.progress}
                  status={taskInfo.status === 'failed' ? 'exception' : 'active'}
                  strokeColor={{
                    '0%': '#108ee9',
                    '100%': '#87d068',
                  }}
                />
                <Paragraph style={{ marginTop: '8px' }}>
                  {taskInfo.message}
                </Paragraph>
                {taskInfo.failed_subtasks && taskInfo.failed_subtasks.length > 0 && (
                  <Paragraph style={{ color: '#ff4d4f' }}>
                    失败的子任务: {taskInfo.failed_subtasks.length} 个
                  </Paragraph>
                )}
              </div>

              {taskInfo.status === 'success' && (
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
