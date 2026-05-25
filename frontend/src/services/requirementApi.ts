import apiClient from './api';

export interface UserRequirement {
  city_name: string;
  travel_days: number;
  total_budget?: number;
  travel_type?: string;
  travel_date?: string;
  preferences?: string[];
}

export interface RequirementSubmitRequest {
  user_id: string;
  requirement: UserRequirement;
}

export interface Requirement {
  requirement_id?: string;
  city_name: string;
  travel_days: number;
  total_budget: number;
  travel_date: string;
  traveler_count: number;
  preferences: string[];
  travel_type?: string;
  special_needs?: string;
}

export interface StructuredRequirement {
  city_name: string;
  travel_days: number;
  total_budget: number;
  travel_date: string;
  traveler_count: number;
  preferences: string[];
}

export const requirementApi = {
  // 提交需求
  submit: (data: RequirementSubmitRequest) => 
    apiClient.post('/requirement/submit', data),
  
  // 解析需求
  parse: (requirementId: string) => 
    apiClient.post('/requirement/parse', { requirement_id: requirementId }),
  
  // 获取需求详情
  getById: (id: string) => 
    apiClient.get(`/requirement/${id}`),
};
