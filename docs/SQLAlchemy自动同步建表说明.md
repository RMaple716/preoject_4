# SQLAlchemy 自动同步建表功能说明

## 📖 概述

本项目实现了类似 **Sequelize** 的自动同步建表功能，使用 SQLAlchemy 的 `metadata.create_all()` 方法实现数据库表的自动创建和管理。

## 🎯 核心特性

- ✅ **幂等性**: 多次执行不会重复创建已存在的表
- ✅ **自动检测**: 智能识别缺失的表和多余的表
- ✅ **强制重建**: 支持删除所有表后重新创建（用于开发环境）
- ✅ **详细日志**: 完整的执行过程和表结构输出
- ✅ **增量更新**: 支持单个表的创建/删除操作
- ✅ **交互式管理**: 提供图形化菜单进行数据库管理

## 🚀 快速开始

### 1. 基础用法 - 自动同步所有表

```bash
# 普通同步（只创建不存在的表，保留现有数据）
python scripts/sync_db.py

# 强制重建（删除所有表后重新创建，会丢失数据！）
python scripts/sync_db.py --force
```

### 2. 高级用法 - 交互式迁移管理

```bash
# 启动交互式管理工具
python scripts/db_migration.py
```

交互式菜单提供以下功能：
- 查看所有表状态
- 检查表结构差异
- 创建/删除单个表
- 添加/删除列

## 📋 使用场景

### 场景 1: 首次初始化数据库

```bash
# 第一次运行项目时，创建所有表
python scripts/sync_db.py
```

**输出示例:**
```
================================================================================
SQLAlchemy 自动同步建表工具
================================================================================
时间: 2026-05-24 20:30:00
模式: 普通同步
================================================================================

当前数据库状态:
  ✓ 已存在的表: 0 个
  ⚠ 缺失的表: 8 个
    - attractions
    - cities
    - hotels
    - itineraries
    - locations
    - restaurants
    - tasks
    - user_requirements

📝 正在创建表...
✅ 表创建完成

🔍 验证表结构...
✅ 所有表已成功创建

============================================================
表: cities
============================================================

列 (8个):
  - city_id                   VARCHAR(50)          NOT NULL
  - city_name                 VARCHAR(100)         NOT NULL
  - province                  VARCHAR(100)         NULL
  ...

✅ 数据库同步完成！
```

### 场景 2: 新增模型后同步

当你添加了新的数据库模型类后：

```python
# src/models/db_models.py
class NewModel(Base):
    __tablename__ = "new_models"
    id = Column(String(50), primary_key=True)
    name = Column(String(100))
```

然后运行：
```bash
python scripts/sync_db.py
```

系统会自动检测并创建 `new_models` 表。

### 场景 3: 开发环境重置数据库

```bash
# 清空所有数据并重新创建表结构
python scripts/sync_db.py --force
```

⚠️ **警告**: 此操作会删除所有数据，仅用于开发环境！

### 场景 4: 检查数据库状态

```bash
python scripts/db_migration.py
```

选择选项 `2` 查看数据库与代码定义的差异。

## 🔧 代码集成

### 在应用启动时自动同步

如果你希望在应用启动时自动同步数据库，可以在 `src/index.py` 中添加：

```python
from src.database import engine, Base
from src.models import db_models  # 导入所有模型

def init_database():
    """初始化数据库"""
    print("正在检查数据库表...")
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表已就绪")

# 在应用启动时调用
init_database()
```

### 在测试环境中使用

```python
# tests/conftest.py
import pytest
from src.database import engine, Base

@pytest.fixture(scope="session")
def test_db():
    """创建测试数据库"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
```

## 📊 支持的表列表

当前项目包含以下表：

### 基础数据表
- `cities` - 城市信息
- `attractions` - 景点信息
- `locations` - 地点信息（交通枢纽等）
- `hotels` - 酒店信息
- `restaurants` - 餐厅信息

### 业务数据表
- `user_requirements` - 用户需求
- `tasks` - 任务分解结果
- `itineraries` - 行程方案

## ⚙️ 配置说明

### 数据库连接配置

编辑 `src/database.py`:

```python
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:123456@localhost:5432/postgres"
)
```

或通过环境变量设置：

```bash
export DATABASE_URL="postgresql://user:password@host:port/dbname"
```

### 调试模式

在 `src/database.py` 中启用 SQL 日志：

```python
engine = create_engine(
    DATABASE_URL,
    echo=True,  # 设置为 True 可查看执行的 SQL 语句
)
```

## 🛠️ 常见问题

### Q1: 为什么表没有创建？

**原因**: 可能未导入模型文件

**解决**: 确保在 `sync_db.py` 中导入了所有模型：

```python
from src.models.db_models import (
    City, Attraction, Location, Hotel, Restaurant,
    UserRequirement, Task, Itinerary
)
```

### Q2: 如何只创建某个特定的表？

使用高级迁移工具：

```bash
python scripts/db_migration.py
# 选择选项 3，输入表名
```

或在代码中：

```python
from scripts.db_migration import DatabaseMigration

migration = DatabaseMigration()
migration.create_single_table("cities")
```

### Q3: 强制重建后数据丢失怎么办？

**重要**: `--force` 参数会删除所有数据，仅用于开发环境！

生产环境应使用数据库迁移工具（如 Alembic）进行结构变更。

### Q4: 如何备份数据后再重建？

```bash
# 1. 导出数据
pg_dump -U postgres -d postgres > backup.sql

# 2. 重建表
python scripts/sync_db.py --force

# 3. 恢复数据（如果需要）
psql -U postgres -d postgres < backup.sql
```

## 📚 进阶阅读

- [SQLAlchemy 官方文档](https://docs.sqlalchemy.org/)
- [Alembic 数据库迁移工具](https://alembic.sqlalchemy.org/)
- [PostgreSQL 官方文档](https://www.postgresql.org/docs/)

## 🤝 贡献指南

如需扩展此功能，可以考虑：

1. 集成 **Alembic** 实现版本化迁移
2. 添加 **数据种子** 功能（自动填充测试数据）
3. 支持 **回滚** 操作
4. 生成 **迁移历史记录**

---

**最后更新**: 2026-05-24  
**维护者**: Project Team
