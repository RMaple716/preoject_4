-- ============================================================
-- 旅游行程规划系统 - 业务数据表建表脚本
-- 版本: 1.0.0
-- 日期: 2026-05-24
-- 说明: 创建用户需求、任务、行程等业务数据表
-- ============================================================

-- 启用必要的扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- 业务数据表
-- ============================================================

-- 1. 用户需求表 (user_requirements)
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

-- 2. 任务表 (tasks)
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

-- 3. 行程表 (itineraries)
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

-- 为业务表添加更新触发器
DROP TRIGGER IF EXISTS trigger_update_user_requirements_updated_at ON user_requirements;
CREATE TRIGGER trigger_update_user_requirements_updated_at 
    BEFORE UPDATE ON user_requirements 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS trigger_update_tasks_updated_at ON tasks;
CREATE TRIGGER trigger_update_tasks_updated_at 
    BEFORE UPDATE ON tasks 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS trigger_update_itineraries_updated_at ON itineraries;
CREATE TRIGGER trigger_update_itineraries_updated_at 
    BEFORE UPDATE ON itineraries 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================================
-- 验证表创建
-- ============================================================
SELECT '=== 业务数据表统计 ===' as info;
SELECT 'UserRequirements' as table_name, COUNT(*) as count FROM user_requirements
UNION ALL SELECT 'Tasks', COUNT(*) FROM tasks
UNION ALL SELECT 'Itineraries', COUNT(*) FROM itineraries;

SELECT '✅ 业务数据表创建完成！' as status;