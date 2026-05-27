"""
高德地图导航API服务
"""
import httpx
from typing import Dict, Any, Optional, List
import os
import asyncio
from collections import defaultdict


class NavigationService:
    """高德地图导航API服务类"""

    def __init__(self, api_key: Optional[str] = None, min_interval: float = 1.0):
        """
        初始化导航服务

        Args:
            api_key: 高德地图API密钥,如果不提供则从环境变量AMAP_API_KEY读取
            min_interval: 最小查询间隔(秒),默认1秒
        """
        self.api_key = api_key or os.getenv('AMAP_API_KEY', '')
        self.base_url = "https://restapi.amap.com/v3"
        self.min_interval = min_interval
        self.last_query_time = defaultdict(float)
        self.query_lock = defaultdict(asyncio.Lock)

    async def geocode(self, address: str) -> Optional[str]:
        """
        将地址转换为经纬度坐标

        Args:
            address: 地址字符串

        Returns:
            坐标字符串，格式为 "经度,纬度"，如果失败返回 None
        """
        import logging
        logger = logging.getLogger(__name__)

        if not self.api_key:
            logger.warning("[Navigation] 未配置API密钥")
            return None

        url = f"{self.base_url}/geocode/geo"
        params = {
            'key': self.api_key,
            'address': address
        }

        try:
            logger.info(f"[Navigation] 调用地理编码API - 地址: {address}")
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                logger.info(f"[Navigation] 地理编码API返回: {data}")

                if data.get('status') == '1' and data.get('geocodes'):
                    location = data['geocodes'][0].get('location', '')
                    logger.info(f"[Navigation] 获取到坐标: {location}")
                    return location
                logger.warning(f"[Navigation] 地理编码失败 - 状态: {data.get('status')}, 信息: {data.get('info', '未知错误')}")
                return None
        except Exception as e:
            logger.error(f"[Navigation] 地理编码异常: {str(e)}")
            return None

    async def get_direction(
        self,
        origin: str,
        destination: str,
        mode: str = 'driving'
    ) -> Dict[str, Any]:
        """
        获取导航路线

        Args:
            origin: 起点地址或坐标
            destination: 终点地址或坐标
            mode: 导航模式
                - walking: 步行
                - driving: 驾车
                - transit: 公交
                - bicycling: 骑行

        Returns:
            导航信息字典
        """
        import logging
        logger = logging.getLogger(__name__)

        if not self.api_key:
            logger.warning("[Navigation] 未配置API密钥")
            return {
                'status': 'error',
                'message': '未配置高德地图API密钥'
            }

        logger.info(f"[Navigation] 调用导航API - 起点: {origin}, 终点: {destination}, 模式: {mode}")

        # 频率控制
        query_key = f"{origin}_{destination}_{mode}"
        async with self.query_lock[query_key]:
            current_time = asyncio.get_event_loop().time()
            last_time = self.last_query_time[query_key]
            elapsed = current_time - last_time

            if elapsed < self.min_interval:
                wait_time = self.min_interval - elapsed
                await asyncio.sleep(wait_time)

            self.last_query_time[query_key] = asyncio.get_event_loop().time()

        # 根据模式选择API
        if mode == 'walking':
            url = f"{self.base_url}/direction/walking"
        elif mode == 'driving':
            url = f"{self.base_url}/direction/driving"
        elif mode == 'transit':
            url = f"{self.base_url}/direction/transit/integrated"
        elif mode == 'bicycling':
            url = f"{self.base_url}/direction/bicycling"
        else:
            return {
                'status': 'error',
                'message': f'不支持的导航模式: {mode}'
            }

        params = {
            'key': self.api_key,
            'origin': origin,
            'destination': destination
        }

        try:
            logger.info(f"[Navigation] 请求URL: {url}")
            logger.info(f"[Navigation] 请求参数: {params}")
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                logger.info(f"[Navigation] 导航API返回: {data}")

                if data.get('status') == '1':
                    route_data = self._parse_route_data(data, mode)
                    logger.info(f"[Navigation] 解析后的路线数据: {route_data}")
                    return {
                        'status': 'success',
                        'data': route_data
                    }
                else:
                    logger.warning(f"[Navigation] 导航API返回错误 - 状态: {data.get('status')}, 信息: {data.get('info', '获取导航信息失败')}")
                    return {
                        'status': 'error',
                        'message': data.get('info', '获取导航信息失败')
                    }

        except httpx.TimeoutException:
            return {
                'status': 'error',
                'message': '请求超时'
            }
        except httpx.HTTPError as e:
            return {
                'status': 'error',
                'message': f'HTTP错误: {str(e)}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'未知错误: {str(e)}'
            }

    def _parse_route_data(self, data: Dict[str, Any], mode: str) -> Dict[str, Any]:
        """
        解析路线数据

        Args:
            data: API返回的原始数据
            mode: 导航模式

        Returns:
            解析后的路线数据
        """
        route_info = {
            'mode': mode,
            'distance': 0,
            'duration': 0,
            'steps': [],
            'polyline': ''
        }

        if mode in ['walking', 'driving', 'bicycling']:
            route = data.get('route', {})
            paths = route.get('paths', [])
            if paths:
                path = paths[0]
                # 确保distance和duration是数值类型
                distance = path.get('distance', 0)
                duration = path.get('duration', 0)
                try:
                    route_info['distance'] = int(float(str(distance))) if distance else 0
                except (ValueError, TypeError):
                    route_info['distance'] = 0
                try:
                    route_info['duration'] = int(float(str(duration))) if duration else 0
                except (ValueError, TypeError):
                    route_info['duration'] = 0
                route_info['polyline'] = path.get('polyline', '')

                # 解析步骤
                steps = path.get('steps', [])
                for step in steps:
                    step_distance = step.get('distance', 0)
                    step_duration = step.get('duration', 0)
                    try:
                        step_distance = int(float(str(step_distance))) if step_distance else 0
                    except (ValueError, TypeError):
                        step_distance = 0
                    try:
                        step_duration = int(float(str(step_duration))) if step_duration else 0
                    except (ValueError, TypeError):
                        step_duration = 0

                    route_info['steps'].append({
                        'instruction': step.get('instruction', ''),
                        'distance': step_distance,
                        'duration': step_duration,
                        'polyline': step.get('polyline', '')
                    })

        elif mode == 'transit':
            route = data.get('route', {})
            transits = route.get('transits', [])
            if transits:
                transit = transits[0]
                # 确保distance和duration是数值类型
                distance = transit.get('distance', 0)
                duration = transit.get('duration', 0)
                try:
                    route_info['distance'] = int(float(str(distance))) if distance else 0
                except (ValueError, TypeError):
                    route_info['distance'] = 0
                try:
                    route_info['duration'] = int(float(str(duration))) if duration else 0
                except (ValueError, TypeError):
                    route_info['duration'] = 0

                # 提取公交路线的polyline
                if 'polyline' in transit:
                    route_info['polyline'] = transit['polyline']

                # 解析公交路线
                segments = transit.get('segments', [])
                for segment in segments:
                    # 处理步行段
                    walking = segment.get('walking', {})
                    walking_distance = walking.get('distance', 0)
                    # 确保distance是数值类型
                    if walking_distance:
                        try:
                            walking_distance = int(float(str(walking_distance)))
                        except (ValueError, TypeError):
                            walking_distance = 0

                    if walking and walking_distance > 0:
                        route_info['steps'].append({
                            'type': 'walking',
                            'instruction': walking.get('instruction', '步行'),
                            'distance': walking_distance,
                            'duration': int(float(str(walking.get('duration', 0)))) if walking.get('duration') else 0,
                            'polyline': walking.get('polyline', '')
                        })

                    # 处理公交/地铁段
                    bus = segment.get('bus', {})
                    buslines = bus.get('buslines', [])
                    if bus and buslines:
                        for busline in buslines:
                            route_info['steps'].append({
                                'type': busline.get('type', 'bus'),
                                'instruction': f"乘坐{busline.get('name', '')}",
                                'distance': int(float(str(bus.get('distance', 0)))) if bus.get('distance') else 0,
                                'duration': int(float(str(bus.get('duration', 0)))) if bus.get('duration') else 0,
                                'departure': bus.get('departure', {}).get('name', ''),
                                'arrival': bus.get('arrival', {}).get('name', ''),
                                'via_num': int(float(str(busline.get('via_num', 0)))) if busline.get('via_num') else 0,
                                'polyline': bus.get('polyline', '')
                            })

        return route_info

    def format_distance(self, distance: int) -> str:
        """
        格式化距离

        Args:
            distance: 距离（米）

        Returns:
            格式化后的距离字符串
        """
        if distance >= 1000:
            return f"{distance / 1000:.1f}公里"
        return f"{distance}米"

    def format_duration(self, duration: int) -> str:
        """
        格式化时长

        Args:
            duration: 时长（秒）

        Returns:
            格式化后的时长字符串
        """
        hours = duration // 3600
        minutes = (duration % 3600) // 60

        if hours > 0:
            return f"{hours}小时{minutes}分钟"
        return f"{minutes}分钟"


# 创建全局实例
navigation_service = NavigationService()
