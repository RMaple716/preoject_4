import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { message } from 'antd';

const apiClient = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 可以在这里添加token等认证信息
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // 添加请求日志（开发环境）
    if (import.meta.env.DEV) {
      console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`, config.data);
    }
    
    return config;
  },
  (error: AxiosError) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    const data = response.data;
    
    // 统一处理业务逻辑错误码
    if (data.code !== 200) {
      // 显示错误消息
      message.error(data.msg || '请求失败');
      
      // 特殊错误码处理
      if (data.code === 401) {
        // 未授权，跳转到登录页
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
      
      return Promise.reject(new Error(data.msg));
    }
    
    // 成功响应，返回完整数据
    return data;
  },
  (error: AxiosError) => {
    let errorMessage = '网络请求失败';
    
    if (error.response) {
      // 服务器返回错误状态码
      switch (error.response.status) {
        case 400:
          errorMessage = '请求参数错误';
          break;
        case 401:
          errorMessage = '未授权，请重新登录';
          localStorage.removeItem('token');
          window.location.href = '/login';
          break;
        case 403:
          errorMessage = '拒绝访问';
          break;
        case 404:
          errorMessage = '请求的资源不存在';
          break;
        case 500:
          errorMessage = (error.response.data as any)?.msg || '服务器内部错误';
          console.error('[500 Error Details]', error.response.data);
          break;
        case 502:
          errorMessage = '网关错误';
          break;
        case 503:
          errorMessage = '服务不可用';
          break;
        default:
          errorMessage = (error.response.data as any)?.msg || `请求失败 (${error.response.status})`;
      }
    } else if (error.request) {
      // 请求已发出但没有收到响应
      errorMessage = '网络连接超时，请检查网络设置';
    } else {
      // 其他错误
      errorMessage = error.message || '未知错误';
    }
    
    console.error('[API Response Error]', errorMessage, error);
    message.error(errorMessage);
    
    return Promise.reject(error);
  }
);

export default apiClient;
