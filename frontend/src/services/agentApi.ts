import apiClient from './api';

// 景点推荐接口
export interface AttractionsRequest {
  city_name: string;
  travel_days: number;
  preferences?: string[];
  dislikes?: string[];
  ticket_budget?: number;
  traveler_count?: number;
}

export interface Attraction {
  name: string;
  duration: string;
  fee: number;
  location: string;
  description?: string;
  rating?: number;
  opening_hours?: string;
}

export interface AttractionsResponse {
  attractions: Attraction[];
}

// 交通推荐接口
export interface TransportRequest {
  city_name: string;
  travel_days: number;
  budget?: number;
  travel_date?: string;
  mode_preference?: string;
}

export interface TransportOption {
  type: string;
  departure_time: string;
  arrival_time: string;
  price: number;
  duration?: string;
}

export interface TransportResponse {
  transport_options: TransportOption[];
}

// 住宿推荐接口
export interface HotelRequest {
  city_name: string;
  check_in_date: string;
  check_out_date: string;
  nights: number;
  budget_per_night?: number;
  location_preference?: string;
  traveler_count?: number;
}

export interface Hotel {
  name: string;
  address: string;
  price_per_night: number;
  rating: number;
  amenities?: string[];
}

export interface HotelResponse {
  hotels: Hotel[];
}

// 美食推荐接口
export interface FoodRequest {
  city_name: string;
  travel_days: number;
  budget_per_person?: number;
  cuisine_preference?: string;
  preferences?: string[];
  dislikes?: string[];
}

export interface Restaurant {
  name: string;
  cuisine: string;
  avg_price: number;
  rating: number;
  address?: string;
  specialties?: string[];
}

export interface FoodResponse {
  restaurants: Restaurant[];
}

export const agentApi = {
  // 景点推荐
  getAttractions: (data: AttractionsRequest) => 
    apiClient.post('/agent/attractions', data),
  
  // 交通推荐
  getTransport: (data: TransportRequest) => 
    apiClient.post('/agent/transport', data),
  
  // 住宿推荐
  getHotels: (data: HotelRequest) => 
    apiClient.post('/agent/hotel', data),
  
  // 美食推荐
  getFood: (data: FoodRequest) => 
    apiClient.post('/agent/food', data),
};
