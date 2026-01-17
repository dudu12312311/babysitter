#!/usr/bin/env python3
"""
准备硬核育儿模拟器代码文件，用于上传到GitHub
"""

import os
import shutil
from pathlib import Path

def create_github_structure():
    """创建适合GitHub的项目结构"""
    
    # 创建目标目录
    target_dir = Path("babysitter_github")
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir()
    
    # 核心文件列表
    core_files = [
        "hardcore_parenting_game.py",
        "game_demo.py", 
        "README.md",
        "user_test_report.md"
    ]
    
    # 复制核心文件
    for file in core_files:
        if Path(file).exists():
            shutil.copy2(file, target_dir / file)
            print(f"✅ 复制: {file}")
        else:
            print(f"❌ 文件不存在: {file}")
    
    # 创建项目结构目录
    (target_dir / "docs").mkdir()
    (target_dir / "tests").mkdir()
    (target_dir / "examples").mkdir()
    
    # 复制规格文档
    spec_dir = Path(".kiro/specs/hardcore-parenting-simulator")
    if spec_dir.exists():
        target_spec_dir = target_dir / "docs" / "specs"
        target_spec_dir.mkdir(parents=True)
        
        spec_files = ["requirements.md", "design.md", "tasks.md"]
        for spec_file in spec_files:
            source = spec_dir / spec_file
            if source.exists():
                shutil.copy2(source, target_spec_dir / spec_file)
                print(f"✅ 复制规格文档: {spec_file}")
    
    # 创建.gitignore文件
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
"""
    
    with open(target_dir / ".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    print("✅ 创建: .gitignore")
    
    # 创建requirements.txt
    requirements_content = """# 硬核育儿模拟器依赖
# 使用Python标准库，无需额外依赖

# 可选依赖（用于扩展功能）
# asyncio  # Python 3.7+ 内置
# dataclasses  # Python 3.7+ 内置
# enum  # Python 3.4+ 内置
# typing  # Python 3.5+ 内置
# datetime  # Python 标准库
# random  # Python 标准库
# json  # Python 标准库
# time  # Python 标准库
"""
    
    with open(target_dir / "requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements_content)
    print("✅ 创建: requirements.txt")
    
    # 创建setup.py
    setup_content = '''#!/usr/bin/env python3
"""
硬核育儿模拟器安装脚本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hardcore-parenting-simulator",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="硬核育儿模拟器：岗前特训",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dudu12312311/babysitter",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Simulation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        # 使用Python标准库，无需额外依赖
    ],
    entry_points={
        "console_scripts": [
            "hardcore-parenting=hardcore_parenting_game:main",
        ],
    },
)
'''
    
    with open(target_dir / "setup.py", "w", encoding="utf-8") as f:
        f.write(setup_content)
    print("✅ 创建: setup.py")
    
    # 创建LICENSE文件
    license_content = """MIT License

Copyright (c) 2026 Hardcore Parenting Simulator

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    with open(target_dir / "LICENSE", "w", encoding="utf-8") as f:
        f.write(license_content)
    print("✅ 创建: LICENSE")
    
    # 创建GitHub Actions工作流
    github_dir = target_dir / ".github" / "workflows"
    github_dir.mkdir(parents=True)
    
    workflow_content = """name: Python Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run demo
      run: |
        python game_demo.py
    
    - name: Test import
      run: |
        python -c "from hardcore_parenting_game import HardcoreParentingGame; print('Import successful')"
"""
    
    with open(github_dir / "python-tests.yml", "w", encoding="utf-8") as f:
        f.write(workflow_content)
    print("✅ 创建: GitHub Actions 工作流")
    
    print(f"\n🎉 项目结构创建完成！")
    print(f"📁 目标目录: {target_dir.absolute()}")
    print(f"\n📋 项目结构:")
    
    # 显示目录结构
    def show_tree(directory, prefix="", max_depth=3, current_depth=0):
        if current_depth >= max_depth:
            return
        
        items = sorted(directory.iterdir())
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            print(f"{prefix}{current_prefix}{item.name}")
            
            if item.is_dir() and current_depth < max_depth - 1:
                next_prefix = prefix + ("    " if is_last else "│   ")
                show_tree(item, next_prefix, max_depth, current_depth + 1)
    
    show_tree(target_dir)
    
    return target_dir

if __name__ == "__main__":
    create_github_structure()