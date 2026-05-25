# 🎉 SQLAlchemy 自动同步建表功能 - 完整实现指南

## 📋 目录

1. [功能概述](#功能概述)
2. [快速开始](#快速开始)
3. [核心脚本](#核心脚本)
4. [使用场景](#使用场景)
5. [技术实现](#技术实现)
6. [最佳实践](#最佳实践)
7. [常见问题](#常见问题)
8. [相关文档](#相关文档)

---

## 功能概述

### 🎯 目标

实现类似 **Sequelize**（Node.js ORM）的自动同步建表功能，让 Python 开发者可以：

- ✅ 用代码定义数据库结构（无需编写 SQL）
- ✅ 自动创建/更新数据库表
- ✅ 智能检测表结构差异
- ✅ 支持多种同步模式（普通/强制/增量）

### 💡 核心价值

| 传统方式 | 新方式 |
|---------|--------|
| ❌ 手动编写 SQL 建表语句 | ✅ Python 代码定义即数据库结构 |
| ❌ 需要记忆复杂的 SQL 语法 | ✅ 使用熟悉的 Python 类定义 |
| ❌ 修改表结构需手动执行 ALTER | ✅ 代码修改后一键同步 |
| ❌ 容易出错且难以维护 | ✅ 类型安全、自动验证 |

---

## 快速开始

### ⚡ 三步上手

```bash
# 1. 确保 PostgreSQL 已启动并配置好连接
# 编辑 src/database.py 中的 DATABASE_URL

# 2. 运行同步脚本
python scripts/sync_db.py

# 3. 验证结果
python scripts/sync_examples.py
```

### 📊 输出示例

```
================================================================================
SQLAlchemy 自动同步建表工具
================================================================================
时间: 2026-05-24 20:44:11
模式: 普通同步
================================================================================

当前数据库状态:
  ✓ 已存在的表: 8 个
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

主键: city_id

索引:
  - idx_cities_city_name       (city_name) [NON-UNIQUE]

✅ 数据库同步完成！
```

---

## 核心脚本

### 1. `scripts/sync_db.py` - 基础同步工具

**用途**: 快速同步所有数据库表

**命令**:
```bash
# 普通同步（推荐）
python scripts/sync_db.py

# 强制重建（会丢失数据！）
python scripts/sync_db.py --force
```

**功能**:
- ✅ 自动检测缺失的表
- ✅ 创建所有不存在的表
- ✅ 显示详细的表结构
- ✅ 验证同步结果

**适用场景**:
- 首次初始化数据库
- 新增模型后同步
- 开发环境重置

---

### 2. `scripts/db_migration.py` - 高级迁移工具

**用途**: 交互式管理数据库结构

**命令**:
```bash
python scripts/db_migration.py
```

**菜单选项**:
```
1. 查看所有表状态
2. 检查表结构差异
3. 创建单个表
4. 删除单个表
5. 添加列
6. 删除列
7. 退出
```

**功能**:
- ✅ 实时查看表状态
- ✅ 精确控制单个表/列
- ✅ 差异分析
- ✅ 交互式操作

**适用场景**:
- 精细化的表结构管理
- 调试和测试
- 学习数据库结构

---

### 3. `scripts/sync_examples.py` - 使用示例

**用途**: 演示各种使用场景

**命令**:
```bash
python scripts/sync_examples.py
```

**示例内容**:
1. 基础同步
2. 检查表是否存在
3. 查询数据验证
4. 高级迁移工具
5. 创建单个表

**适用场景**:
- 学习如何使用
- 集成到项目中
- 验证功能正常

---

## 使用场景

### 场景 1: 首次初始化数据库

```bash
# 第一次运行项目时
python scripts/sync_db.py
```

**说明**: 自动创建所有 8 个表（5个基础数据表 + 3个业务数据表）

---

### 场景 2: 新增模型后同步

**步骤**:

1. 在 `src/models/db_models.py` 中添加新模型：

```python
class Review(Base):
    """评论表"""
    __tablename__ = "reviews"
    
    review_id = Column(String(50), primary_key=True)
    user_id = Column(String(50), nullable=False)
    content = Column(Text)
    rating = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
```

2. 运行同步：

```bash
python scripts/sync_db.py
```

**结果**: 自动创建 `reviews` 表

---

### 场景 3: 开发环境重置

```bash
# 清空所有数据并重新创建
python scripts/sync_db.py --force
```

⚠️ **警告**: 此操作会删除所有数据，仅用于开发环境！

---

### 场景 4: 检查数据库状态

```bash
python scripts/db_migration.py
```

选择选项 `2` 查看数据库与代码定义的差异。

**输出示例**:
```
================================================================================
数据库结构差异分析
================================================================================

✅ 所有代码定义的表都已存在于数据库中

✅ 数据库中没有额外的表

✅ 数据库与代码定义完全同步！
```

---

### 场景 5: 代码集成

#### 应用启动时自动同步

```python
# src/index.py
from fastapi import FastAPI
from src.database import engine, Base

app = FastAPI()

@app.on_event("startup")
def init_database():
    """应用启动时初始化数据库"""
    print("正在检查数据库表...")
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表已就绪")
```

#### 测试环境中使用

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

---

## 技术实现

### 核心技术栈

- **SQLAlchemy**: Python ORM 框架
- **PostgreSQL**: 关系型数据库
- **inspect**: 数据库结构检查工具
- **argparse**: 命令行参数解析

### 关键 API

#### 1. 创建所有表

```python
from src.database import engine, Base

Base.metadata.create_all(bind=engine)
```

**原理**: 
- 检查每个表是否存在
- 只创建不存在的表
- 幂等操作，可安全多次调用

#### 2. 删除所有表

```python
Base.metadata.drop_all(bind=engine)
```

**注意**: 会删除所有数据！

#### 3. 检查表是否存在

```python
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()

if 'cities' in tables:
    print("表存在")
```

#### 4. 创建单个表

```python
from src.models.db_models import City

City.__table__.create(bind=engine)
```

#### 5. 添加列

```python
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text(
        "ALTER TABLE cities ADD COLUMN population INTEGER"
    ))
    conn.commit()
```

---

### 架构设计

```
┌─────────────────────────────────────┐
│       用户界面层                      │
│  ┌──────────┐  ┌─────────────────┐ │
│  │ sync_db  │  │ db_migration    │ │
│  │ .py      │  │ .py             │ │
│  └──────────┘  └─────────────────┘ │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│       业务逻辑层                      │
│  ┌──────────────────────────────┐   │
│  │  sync_tables()               │   │
│  │  check_tables_exist()        │   │
│  │  print_table_structure()     │   │
│  └──────────────────────────────┘   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│       数据访问层                      │
│  ┌──────────────────────────────┐   │
│  │  Base.metadata.create_all()  │   │
│  │  Base.metadata.drop_all()    │   │
│  │  inspector.get_table_names() │   │
│  └──────────────────────────────┘   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│       数据库层                        │
│  ┌──────────────────────────────┐   │
│  │  PostgreSQL                  │   │
│  │  - cities                    │   │
│  │  - attractions               │   │
│  │  - ...                       │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

---

## 最佳实践

### ✅ 推荐做法

#### 1. 开发环境

```bash
# 每次修改模型后
python scripts/sync_db.py --force

# 或使用热重载
watchmedo auto-restart --pattern="*.py" -- python scripts/sync_db.py
```

#### 2. 测试环境

```python
# 使用 fixture 自动管理
@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
```

#### 3. 生产环境

⚠️ **重要**: 使用 **Alembic** 进行版本化迁移

```bash
# 安装 Alembic
pip install alembic

# 初始化
alembic init alembic

# 生成迁移脚本
alembic revision --autogenerate -m "add new table"

# 执行迁移
alembic upgrade head
```

#### 4. 备份策略

```bash
# 定期备份
pg_dump -U postgres -d postgres > backup_$(date +%Y%m%d).sql

# 恢复数据
psql -U postgres -d postgres < backup_20260524.sql
```

---

### ❌ 避免做法

1. **生产环境使用 `--force`**
   ```bash
   # ❌ 错误
   python scripts/sync_db.py --force
   
   # ✅ 正确：使用 Alembic
   alembic upgrade head
   ```

2. **不备份就重建表**
   ```bash
   # ❌ 错误：直接重建
   python scripts/sync_db.py --force
   
   # ✅ 正确：先备份
   pg_dump -U postgres -d postgres > backup.sql
   python scripts/sync_db.py --force
   ```

3. **忽略表结构差异**
   ```bash
   # ❌ 错误：不检查差异
   python scripts/sync_db.py
   
   # ✅ 正确：定期检查
   python scripts/db_migration.py
   # 选择选项 2
   ```

4. **直接修改数据库结构**
   ```sql
   -- ❌ 错误：直接在数据库中修改
   ALTER TABLE cities ADD COLUMN population INTEGER;
   
   -- ✅ 正确：通过代码定义
   # 在 db_models.py 中添加字段，然后同步
   ```

---

## 常见问题

### Q1: 为什么表没有创建？

**原因**: 可能未导入模型文件

**解决**: 确保在 `sync_db.py` 中导入了所有模型：

```python
from src.models.db_models import (
    City, Attraction, Location, Hotel, Restaurant,
    UserRequirement, Task, Itinerary
)
```

---

### Q2: 如何只创建某个特定的表？

**方法 1**: 使用高级迁移工具

```bash
python scripts/db_migration.py
# 选择选项 3，输入表名
```

**方法 2**: 在代码中

```python
from scripts.db_migration import DatabaseMigration

migration = DatabaseMigration()
migration.create_single_table("cities")
```

**方法 3**: 直接使用 SQLAlchemy

```python
from src.models.db_models import City
from src.database import engine

City.__table__.create(bind=engine)
```

---

### Q3: 强制重建后数据丢失怎么办？

**重要**: `--force` 参数会删除所有数据，仅用于开发环境！

**恢复方法**:

1. 从备份恢复：
   ```bash
   psql -U postgres -d postgres < backup.sql
   ```

2. 重新导入初始数据：
   ```bash
   python scripts/init_db.py
   ```

---

### Q4: 生产环境怎么用？

**推荐方案**: 使用 **Alembic** 进行版本化迁移

```bash
# 1. 安装 Alembic
pip install alembic

# 2. 初始化
alembic init alembic

# 3. 配置 alembic.ini
# 修改 sqlalchemy.url = postgresql://user:pass@localhost/dbname

# 4. 生成迁移脚本
alembic revision --autogenerate -m "add new table"

# 5. 检查生成的脚本
# 编辑 alembic/versions/xxx_xxx.py

# 6. 执行迁移
alembic upgrade head

# 7. 回滚（如果需要）
alembic downgrade -1
```

---

### Q5: 如何查看执行的 SQL 语句？

**方法 1**: 启用引擎日志

```python
# src/database.py
engine = create_engine(
    DATABASE_URL,
    echo=True,  # 设置为 True 可查看 SQL
)
```

**方法 2**: 使用事件监听

```python
from sqlalchemy import event

@event.listens_for(engine, "before_cursor_execute")
def log_sql(conn, cursor, statement, parameters, context, executemany):
    print(f"SQL: {statement}")
    print(f"Parameters: {parameters}")
```

---

### Q6: 支持哪些数据库？

**当前支持**:
- ✅ PostgreSQL（主要使用）
- ✅ MySQL（理论上支持，需测试）
- ✅ SQLite（开发/测试用）

**切换数据库**:

```python
# PostgreSQL
DATABASE_URL = "postgresql://user:pass@localhost/dbname"

# MySQL
DATABASE_URL = "mysql+pymysql://user:pass@localhost/dbname"

# SQLite
DATABASE_URL = "sqlite:///./test.db"
```

---

## 相关文档

### 📖 详细文档

- [SQLAlchemy 自动同步建表说明](./SQLAlchemy自动同步建表说明.md) - 完整使用说明
- [实现总结](./SQLAlchemy自动同步建表-实现总结.md) - 技术实现细节
- [快速参考](./SQLAlchemy快速参考.md) - 常用命令速查
- [与 Sequelize 对比](./SQLAlchemy与Sequelize对比.md) - 功能对比

### 🔗 外部资源

- [SQLAlchemy 官方文档](https://docs.sqlalchemy.org/)
- [Alembic 迁移工具](https://alembic.sqlalchemy.org/)
- [PostgreSQL 官方文档](https://www.postgresql.org/docs/)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)

### 📂 项目文件

- [数据库模型定义](../src/models/db_models.py)
- [数据库配置](../src/database.py)
- [同步脚本](../scripts/sync_db.py)
- [迁移工具](../scripts/db_migration.py)
- [使用示例](../scripts/sync_examples.py)

---

## 🎓 学习路线

### 初级（1-2天）

1. ✅ 阅读 [快速参考](./SQLAlchemy快速参考.md)
2. ✅ 运行 `python scripts/sync_db.py`
3. ✅ 运行 `python scripts/sync_examples.py`
4. ✅ 理解基本概念

### 中级（3-5天）

1. ✅ 阅读 [详细说明](./SQLAlchemy自动同步建表说明.md)
2. ✅ 使用 `db_migration.py` 管理表结构
3. ✅ 在代码中集合同步功能
4. ✅ 理解 SQLAlchemy 核心 API

### 高级（1-2周）

1. ✅ 阅读 [实现总结](./SQLAlchemy自动同步建表-实现总结.md)
2. ✅ 学习 Alembic 迁移工具
3. ✅ 自定义同步逻辑
4. ✅ 优化性能和安全性

---

## 🤝 贡献指南

如需扩展此功能，可以考虑：

### 短期目标
- [ ] 集成 **Alembic** 实现版本化迁移
- [ ] 添加 **数据种子** 功能（自动填充测试数据）
- [ ] 支持 **回滚** 操作
- [ ] 生成 **迁移历史记录**

### 长期目标
- [ ] 图形化管理界面（Web UI）
- [ ] 多数据库支持优化
- [ ] 性能监控和优化
- [ ] 自动化测试覆盖

---

## 📞 支持与反馈

如有问题或建议：

1. 📖 查阅相关文档
2. 🐛 提交 Issue
3. 💬 团队群组讨论
4. 📧 联系维护者

---

**最后更新**: 2026-05-24  
**版本**: v1.0.0  
**维护者**: Project Team  
**许可证**: MIT
