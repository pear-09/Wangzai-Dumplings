### 项目依赖
见目录下requirements.txt文件

### 后端自动化单测
```bash
cd backend
make test # 运行所有模块测试
make test-($service) # service为user、note、date服务

# 例如 make test-user 
# 测试用户模块相关函数
```

### 后端服务启动

进入`backend`目录下
```bash
cd backend
pwd # /Wangzai-Dumplings/backend
```

使用pip包管理器安装项目依赖
```bash
pip install pipreqs # 按照pipreqs工具
pipreqs . --force # 重新生成并覆盖依赖(requirement.txt)
pip intsall -r requirement.txt
```

进行数据库迁移
```bash
python manage.py makemigrations # 生成迁移文件,migration目录
python manage.py migrate # 根据model生成表
```

启动服务

```bash
python manage.py runserver
```