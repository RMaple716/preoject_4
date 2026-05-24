-- ============================================================
-- 旅游行程规划系统 - PostgreSQL 完整建表脚本（含业务表）
-- 版本: 2.0.0
-- 日期: 2026-05-24
-- 说明: 包含基础数据表和业务数据表
-- ============================================================

-- 启用必要的扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ============================================================
-- 第一部分：基础数据表（城市、景点、酒店、餐厅、地点）
-- ============================================================

-- 1. 城市表 (cities)
CREATE TABLE IF NOT EXISTS cities (
    city_id VARCHAR(50) PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    province VARCHAR(100),
    country VARCHAR(100) DEFAULT '中国',
    description TEXT,
    tags JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cities_city_name ON cities USING gin(to_tsvector('simple', city_name));
CREATE INDEX idx_cities_province ON cities(province);
CREATE INDEX idx_cities_tags ON cities USING gin(tags);

COMMENT ON TABLE cities IS '城市基础信息表';

-- 2. 景点表 (attractions)
CREATE TABLE IF NOT EXISTS attractions (
    attraction_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    city_id VARCHAR(50) NOT NULL REFERENCES cities(city_id) ON DELETE CASCADE,
    category VARCHAR(50) NOT NULL CHECK (category IN ('scenic_spot', 'museum', 'park', 'beach', 'mountain', 'temple')),
    description TEXT,
    address VARCHAR(500),
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    opening_hours VARCHAR(200),
    ticket_price DECIMAL(10, 2) DEFAULT 0,
    recommended_duration VARCHAR(50),
    tags JSONB DEFAULT '[]'::jsonb,
    rating DECIMAL(3, 2) CHECK (rating >= 0 AND rating <= 5),
    images JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_attractions_name ON attractions USING gin(to_tsvector('simple', name));
CREATE INDEX idx_attractions_city_id ON attractions(city_id);
CREATE INDEX idx_attractions_category ON attractions(category);
CREATE INDEX idx_attractions_rating ON attractions(rating DESC);

COMMENT ON TABLE attractions IS '旅游景点基础数据表';

-- 3. 地点表 (locations)
CREATE TABLE IF NOT EXISTS locations (
    location_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    city_id VARCHAR(50) NOT NULL REFERENCES cities(city_id) ON DELETE CASCADE,
    category VARCHAR(50) NOT NULL CHECK (category IN ('airport', 'train_station', 'bus_station', 'metro', 'shopping', 'food')),
    address VARCHAR(500),
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_locations_name ON locations USING gin(to_tsvector('simple', name));
CREATE INDEX idx_locations_city_id ON locations(city_id);
CREATE INDEX idx_locations_category ON locations(category);

COMMENT ON TABLE locations IS '地点基础数据表（交通枢纽、商业区等）';

-- 4. 酒店表 (hotels)
CREATE TABLE IF NOT EXISTS hotels (
    hotel_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    city_id VARCHAR(50) NOT NULL REFERENCES cities(city_id) ON DELETE CASCADE,
    address VARCHAR(500),
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    star_rating INTEGER CHECK (star_rating >= 1 AND star_rating <= 5),
    price_range VARCHAR(50) CHECK (price_range IN ('budget', 'mid-range', 'luxury')),
    min_price DECIMAL(10, 2),
    max_price DECIMAL(10, 2),
    amenities JSONB DEFAULT '[]'::jsonb,
    description TEXT,
    rating DECIMAL(3, 2) CHECK (rating >= 0 AND rating <= 5),
    images JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_hotels_name ON hotels USING gin(to_tsvector('simple', name));
CREATE INDEX idx_hotels_city_id ON hotels(city_id);
CREATE INDEX idx_hotels_star_rating ON hotels(star_rating);
CREATE INDEX idx_hotels_price_range ON hotels(price_range);
CREATE INDEX idx_hotels_rating ON hotels(rating DESC);

COMMENT ON TABLE hotels IS '酒店住宿基础数据表';

-- 5. 餐厅表 (restaurants)
CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    city_id VARCHAR(50) NOT NULL REFERENCES cities(city_id) ON DELETE CASCADE,
    cuisine_type VARCHAR(100),
    address VARCHAR(500),
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    price_level VARCHAR(50) CHECK (price_level IN ('$', '$$', '$$$', '$$$$')),
    avg_price DECIMAL(10, 2),
    specialties JSONB DEFAULT '[]'::jsonb,
    description TEXT,
    rating DECIMAL(3, 2) CHECK (rating >= 0 AND rating <= 5),
    opening_hours VARCHAR(200),
    images JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_restaurants_name ON restaurants USING gin(to_tsvector('simple', name));
CREATE INDEX idx_restaurants_city_id ON restaurants(city_id);
CREATE INDEX idx_restaurants_cuisine_type ON restaurants(cuisine_type);
CREATE INDEX idx_restaurants_price_level ON restaurants(price_level);
CREATE INDEX idx_restaurants_rating ON restaurants(rating DESC);

COMMENT ON TABLE restaurants IS '餐厅美食基础数据表';


-- ============================================================
-- 第二部分：业务数据表（需求、任务、行程）
-- ============================================================

-- 6. 用户需求表 (user_requirements)
CREATE TABLE IF NOT EXISTS user_requirements (
    requirement_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    requirement_data JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'parsed', 'processing', 'completed')),
    parsed_keywords JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_requirements_user_id ON user_requirements(user_id);
CREATE INDEX idx_user_requirements_status ON user_requirements(status);

COMMENT ON TABLE user_requirements IS '用户需求表';
COMMENT ON COLUMN user_requirements.requirement_id IS '需求唯一标识';
COMMENT ON COLUMN user_requirements.user_id IS '用户ID';
COMMENT ON COLUMN user_requirements.requirement_data IS '需求数据JSON';
COMMENT ON COLUMN user_requirements.status IS '状态：pending/parsed/processing/completed';
COMMENT ON COLUMN user_requirements.parsed_keywords IS '解析后的关键词';

-- 7. 任务表 (tasks)
CREATE TABLE IF NOT EXISTS tasks (
    task_id VARCHAR(50) PRIMARY KEY,
    batch_id VARCHAR(50) NOT NULL,
    requirement_id VARCHAR(50) NOT NULL REFERENCES user_requirements(requirement_id) ON DELETE CASCADE,
    agent_type VARCHAR(50) NOT NULL CHECK (agent_type IN ('attraction', 'accommodation', 'food', 'transport')),
    parameters JSONB,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'success', 'failed')),
    result JSONB,
    error TEXT,
    progress FLOAT DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_batch_id ON tasks(batch_id);
CREATE INDEX idx_tasks_requirement_id ON tasks(requirement_id);
CREATE INDEX idx_tasks_agent_type ON tasks(agent_type);
CREATE INDEX idx_tasks_status ON tasks(status);

COMMENT ON TABLE tasks IS '任务表';
COMMENT ON COLUMN tasks.task_id IS '任务唯一标识';
COMMENT ON COLUMN tasks.batch_id IS '批次ID';
COMMENT ON COLUMN tasks.requirement_id IS '关联的需求ID';
COMMENT ON COLUMN tasks.agent_type IS '智能体类型';
COMMENT ON COLUMN tasks.parameters IS '任务参数';
COMMENT ON COLUMN tasks.status IS '任务状态';
COMMENT ON COLUMN tasks.result IS '任务结果';
COMMENT ON COLUMN tasks.error IS '错误信息';
COMMENT ON COLUMN tasks.progress IS '进度百分比';

-- 8. 行程表 (itineraries)
CREATE TABLE IF NOT EXISTS itineraries (
    itinerary_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    requirement_id VARCHAR(50) REFERENCES user_requirements(requirement_id) ON DELETE SET NULL,
    title VARCHAR(200),
    day_plans JSONB NOT NULL,
    total_budget DECIMAL(10, 2),
    actual_cost DECIMAL(10, 2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'saved', 'published')),
    is_favorite BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_itineraries_user_id ON itineraries(user_id);
CREATE INDEX idx_itineraries_requirement_id ON itineraries(requirement_id);
CREATE INDEX idx_itineraries_status ON itineraries(status);
CREATE INDEX idx_itineraries_is_favorite ON itineraries(is_favorite);

COMMENT ON TABLE itineraries IS '行程表';
COMMENT ON COLUMN itineraries.itinerary_id IS '行程唯一标识';
COMMENT ON COLUMN itineraries.user_id IS '用户ID';
COMMENT ON COLUMN itineraries.requirement_id IS '关联的需求ID';
COMMENT ON COLUMN itineraries.title IS '行程标题';
COMMENT ON COLUMN itineraries.day_plans IS '每日计划JSON数组';
COMMENT ON COLUMN itineraries.total_budget IS '总预算';
COMMENT ON COLUMN itineraries.actual_cost IS '实际花费';
COMMENT ON COLUMN itineraries.status IS '状态：draft/saved/published';
COMMENT ON COLUMN itineraries.is_favorite IS '是否收藏';


-- ============================================================
-- 创建自动更新 updated_at 的触发器函数
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 为所有表添加更新触发器
CREATE TRIGGER trigger_update_cities_updated_at BEFORE UPDATE ON cities FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_update_attractions_updated_at BEFORE UPDATE ON attractions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_update_locations_updated_at BEFORE UPDATE ON locations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_update_hotels_updated_at BEFORE UPDATE ON hotels FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_update_restaurants_updated_at BEFORE UPDATE ON restaurants FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_update_user_requirements_updated_at BEFORE UPDATE ON user_requirements FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_update_tasks_updated_at BEFORE UPDATE ON tasks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trigger_update_itineraries_updated_at BEFORE UPDATE ON itineraries FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


-- ============================================================
-- 插入示例基础数据
-- ============================================================

-- 城市数据
INSERT INTO cities (city_id, city_name, province, country, description, tags) VALUES
('beijing', '北京', '北京市', '中国', '中国首都，历史文化名城，拥有众多世界文化遗产', '["历史", "文化", "古都", "政治中心"]'),
('shanghai', '上海', '上海市', '中国', '国际化大都市，中国经济金融中心', '["现代", "繁华", "国际", "金融"]'),
('hangzhou', '杭州', '浙江省', '中国', '人间天堂，西湖美景，历史文化名城', '["自然", "园林", "休闲", "西湖"]'),
('chengdu', '成都', '四川省', '中国', '天府之国，美食之都，大熊猫故乡', '["美食", "熊猫", "休闲", "文化"]'),
('xian', '西安', '陕西省', '中国', '十三朝古都，兵马俑故乡', '["历史", "古都", "文化", "文物"]')
ON CONFLICT (city_id) DO NOTHING;

-- 景点数据（部分示例）
INSERT INTO attractions (attraction_id, name, city_id, category, description, address, latitude, longitude, opening_hours, ticket_price, recommended_duration, tags, rating, images) VALUES
('beijing_gugong', '故宫博物院', 'beijing', 'museum', '明清两代皇家宫殿，世界文化遗产', '北京市东城区景山前街4号', 39.916345, 116.397155, '08:30-17:00', 60.00, '3小时', '["历史", "建筑", "文化", "世界遗产"]', 4.8, '["https://example.com/gugong1.jpg"]'),
('beijing_tiantan', '天坛公园', 'beijing', 'park', '明清皇帝祭天祈谷的场所，世界文化遗产', '北京市东城区天坛路甲1号', 39.882197, 116.406632, '06:00-22:00', 15.00, '2小时', '["历史", "公园", "文化"]', 4.6, '["https://example.com/tiantan1.jpg"]'),
('hangzhou_xihu', '西湖风景名胜区', 'hangzhou', 'scenic_spot', '杭州标志性景点，世界文化遗产', '浙江省杭州市西湖区', 30.242928, 120.148832, '全天开放', 0.00, '4小时', '["自然", "湖泊", "风景", "世界遗产"]', 4.9, '["https://example.com/xihu1.jpg"]'),
('chengdu_panda', '成都大熊猫繁育研究基地', 'chengdu', 'park', '全球最大的大熊猫人工繁育研究基地', '四川省成都市成华区熊猫大道1375号', 30.733333, 104.150000, '07:30-18:00', 55.00, '3小时', '["动物", "熊猫", "自然", "科普"]', 4.8, '["https://example.com/panda1.jpg"]'),
('xian_terracotta', '秦始皇兵马俑博物馆', 'xian', 'museum', '世界第八大奇迹，世界文化遗产', '陕西省西安市临潼区秦陵北路', 34.383333, 109.273056, '08:30-18:00', 120.00, '3小时', '["历史", "文物", "世界遗产", "考古"]', 4.9, '["https://example.com/terracotta1.jpg"]')
ON CONFLICT (attraction_id) DO NOTHING;

-- 酒店数据（部分示例）
INSERT INTO hotels (hotel_id, name, city_id, address, latitude, longitude, star_rating, price_range, min_price, max_price, amenities, description, rating, images) VALUES
('beijing_hotel_001', '北京王府井希尔顿酒店', 'beijing', '北京市东城区王府井东街8号', 39.914500, 116.412000, 5, 'luxury', 1200.00, 3000.00, '["WiFi", "游泳池", "健身房", "餐厅", "停车场"]', '位于王府井商业区的豪华酒店', 4.7, '["https://example.com/hotel1.jpg"]'),
('hangzhou_hotel_001', '杭州西湖国宾馆', 'hangzhou', '浙江省杭州市西湖区杨公堤18号', 30.245678, 120.135432, 5, 'luxury', 1500.00, 4000.00, '["WiFi", "湖景", "餐厅", "停车场", "花园"]', '西湖边的豪华度假酒店，环境优美', 4.8, '["https://example.com/hotel2.jpg"]')
ON CONFLICT (hotel_id) DO NOTHING;

-- 餐厅数据（部分示例）
INSERT INTO restaurants (restaurant_id, name, city_id, cuisine_type, address, latitude, longitude, price_level, avg_price, specialties, description, rating, opening_hours, images) VALUES
('beijing_rest_001', '全聚德烤鸭店', 'beijing', '北京菜', '北京市东城区前门大街30号', 39.898765, 116.398765, '$$$', 200.00, '["烤鸭", "京味小吃"]', '百年老字号，正宗北京烤鸭', 4.5, '11:00-22:00', '["https://example.com/restaurant1.jpg"]'),
('hangzhou_rest_001', '楼外楼', 'hangzhou', '杭帮菜', '浙江省杭州市西湖区孤山路30号', 30.250123, 120.142345, '$$', 150.00, '["西湖醋鱼", "龙井虾仁"]', '西湖边著名餐厅，正宗杭帮菜', 4.6, '10:30-21:30', '["https://example.com/restaurant2.jpg"]')
ON CONFLICT (restaurant_id) DO NOTHING;

-- 地点数据（部分示例）
INSERT INTO locations (location_id, name, city_id, category, address, latitude, longitude, description) VALUES
('beijing_airport_capital', '北京首都国际机场', 'beijing', 'airport', '北京市顺义区天竺地区', 40.079908, 116.603119, '北京主要国际机场'),
('beijing_station', '北京站', 'beijing', 'train_station', '北京市东城区毛家湾胡同甲13号', 39.902265, 116.428503, '北京主要火车站之一')
ON CONFLICT (location_id) DO NOTHING;


-- ============================================================
-- 验证数据
-- ============================================================
SELECT '=== 数据统计 ===' as info;
SELECT 'Cities' as table_name, COUNT(*) as count FROM cities
UNION ALL SELECT 'Attractions', COUNT(*) FROM attractions
UNION ALL SELECT 'Locations', COUNT(*) FROM locations
UNION ALL SELECT 'Hotels', COUNT(*) FROM hotels
UNION ALL SELECT 'Restaurants', COUNT(*) FROM restaurants
UNION ALL SELECT 'UserRequirements', COUNT(*) FROM user_requirements
UNION ALL SELECT 'Tasks', COUNT(*) FROM tasks
UNION ALL SELECT 'Itineraries', COUNT(*) FROM itineraries;

SELECT '✅ 数据库初始化完成！' as status,
       '已创建8个表（5个基础表 + 3个业务表）' as tables,
       '已插入示例数据' as data_status;