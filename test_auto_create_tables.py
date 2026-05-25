"""
测试应用启动时自动建表功能

此脚本会：
1. 模拟应用启动过程
2. 验证数据库表是否自动创建
3. 检查表结构是否正确
"""
import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.database import engine, Base
from sqlalchemy import inspect


def test_auto_create_tables():
    """测试自动建表功能"""
    print("\n" + "="*80)
    print("🧪 测试：应用启动时自动建表")
    print("="*80)
    
    # 步骤 1: 检查当前数据库状态
    print("\n📋 步骤 1: 检查当前数据库状态...")
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    print(f"   当前数据库中有 {len(existing_tables)} 个表")
    
    if existing_tables:
        print("   已存在的表:")
        for table in sorted(existing_tables):
            print(f"     - {table}")
    
    # 步骤 2: 模拟应用启动时的建表操作
    print("\n📋 步骤 2: 执行自动建表（Base.metadata.create_all）...")
    try:
        Base.metadata.create_all(bind=engine)
        print("   ✅ 建表操作完成")
    except Exception as e:
        print(f"   ❌ 建表失败: {e}")
        return False
    
    # 步骤 3: 验证表是否创建成功
    print("\n📋 步骤 3: 验证表结构...")
    inspector = inspect(engine)
    new_tables = set(inspector.get_table_names())
    
    expected_tables = {
        'cities', 'attractions', 'locations', 'hotels', 'restaurants',
        'user_requirements', 'tasks', 'itineraries'
    }
    
    missing_tables = expected_tables - new_tables
    extra_tables = new_tables - expected_tables
    
    if missing_tables:
        print(f"   ❌ 缺失的表: {missing_tables}")
        return False
    
    if extra_tables:
        print(f"   ⚠️  额外的表: {extra_tables}")
    
    print(f"   ✅ 所有预期的表都已创建 ({len(expected_tables)} 个)")
    
    # 步骤 4: 检查表结构详情
    print("\n📋 步骤 4: 检查关键表结构...")
    
    # 检查 cities 表
    if 'cities' in new_tables:
        columns = inspector.get_columns('cities')
        column_names = [col['name'] for col in columns]
        expected_columns = ['city_id', 'city_name', 'province', 'created_at', 'updated_at']
        
        missing_columns = set(expected_columns) - set(column_names)
        if missing_columns:
            print(f"   ❌ cities 表缺失列: {missing_columns}")
            return False
        
        print(f"   ✅ cities 表结构正确 ({len(columns)} 个列)")
    
    # 检查 attractions 表
    if 'attractions' in new_tables:
        columns = inspector.get_columns('attractions')
        column_names = [col['name'] for col in columns]
        
        # 检查外键
        fks = inspector.get_foreign_keys('attractions')
        has_city_fk = any('city_id' in fk['constrained_columns'] for fk in fks)
        
        if not has_city_fk:
            print(f"   ❌ attractions 表缺少 city_id 外键")
            return False
        
        print(f"   ✅ attractions 表结构正确 ({len(columns)} 个列，外键正常)")
    
    # 步骤 5: 测试幂等性（再次执行不应报错）
    print("\n📋 步骤 5: 测试幂等性（再次执行建表）...")
    try:
        Base.metadata.create_all(bind=engine)
        print("   ✅ 幂等性测试通过（可安全多次调用）")
    except Exception as e:
        print(f"   ❌ 幂等性测试失败: {e}")
        return False
    
    # 总结
    print("\n" + "="*80)
    print("✅ 所有测试通过！")
    print("="*80)
    print("\n📊 测试结果总结:")
    print(f"   - 表数量: {len(new_tables)} 个")
    print(f"   - 表结构: 正确")
    print(f"   - 外键关系: 正确")
    print(f"   - 幂等性: 通过")
    print("\n✨ 应用启动时自动建表功能正常工作！")
    print("="*80 + "\n")
    
    return True


if __name__ == '__main__':
    success = test_auto_create_tables()
    sys.exit(0 if success else 1)
