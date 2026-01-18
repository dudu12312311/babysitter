#!/usr/bin/env python3
"""
宝宝面部融合 API
支持上传父母照片，生成宝宝照片
"""

import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from baby_face_fusion import BabyFaceFusion

# 创建 Blueprint
baby_fusion_bp = Blueprint('baby_fusion', __name__, url_prefix='/api/baby-fusion')

# 配置上传文件夹
UPLOAD_FOLDER = 'uploads/parents'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# 确保上传文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 创建面部融合生成器
fusion_generator = BabyFaceFusion()


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@baby_fusion_bp.route('/upload-and-generate', methods=['POST'])
def upload_and_generate():
    """
    上传父母照片并生成宝宝照片
    
    表单数据:
        - parent1: 父母1的照片文件
        - parent2: 父母2的照片文件（可选）
        - baby_age: 宝宝年龄 (newborn, 6months, 1year, 2years)
        - num_variations: 生成变体数量 (1-4)
    """
    try:
        # 检查是否有文件
        if 'parent1' not in request.files:
            return jsonify({
                'success': False,
                'error': '缺少父母1的照片'
            }), 400
        
        parent1_file = request.files['parent1']
        parent2_file = request.files.get('parent2')
        
        # 检查文件名
        if parent1_file.filename == '':
            return jsonify({
                'success': False,
                'error': '未选择文件'
            }), 400
        
        # 检查文件类型
        if not allowed_file(parent1_file.filename):
            return jsonify({
                'success': False,
                'error': f'不支持的文件类型，仅支持: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # 保存父母1的照片
        filename1 = secure_filename(parent1_file.filename)
        parent1_path = os.path.join(UPLOAD_FOLDER, f"parent1_{filename1}")
        parent1_file.save(parent1_path)
        
        # 保存父母2的照片（如果有）
        parent2_path = None
        if parent2_file and parent2_file.filename != '':
            if not allowed_file(parent2_file.filename):
                return jsonify({
                    'success': False,
                    'error': f'父母2照片类型不支持'
                }), 400
            
            filename2 = secure_filename(parent2_file.filename)
            parent2_path = os.path.join(UPLOAD_FOLDER, f"parent2_{filename2}")
            parent2_file.save(parent2_path)
        
        # 获取参数
        baby_age = request.form.get('baby_age', 'newborn')
        num_variations = int(request.form.get('num_variations', 4))
        
        # 验证参数
        valid_ages = ['newborn', '6months', '1year', '2years']
        if baby_age not in valid_ages:
            return jsonify({
                'success': False,
                'error': f'无效的年龄，必须是: {", ".join(valid_ages)}'
            }), 400
        
        if not 1 <= num_variations <= 4:
            return jsonify({
                'success': False,
                'error': '变体数量必须在 1-4 之间'
            }), 400
        
        # 生成宝宝照片
        result = fusion_generator.generate_baby_from_parents_fal(
            parent1_image=parent1_path,
            parent2_image=parent2_path,
            baby_age=baby_age,
            num_variations=num_variations
        )
        
        # 清理上传的文件（可选）
        # os.remove(parent1_path)
        # if parent2_path:
        #     os.remove(parent2_path)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@baby_fusion_bp.route('/generate-from-urls', methods=['POST'])
def generate_from_urls():
    """
    从 URL 生成宝宝照片
    
    请求体:
    {
        "parent1_url": "https://...",
        "parent2_url": "https://...",  // 可选
        "baby_age": "newborn",
        "num_variations": 4
    }
    """
    try:
        data = request.get_json() or {}
        
        parent1_url = data.get('parent1_url')
        if not parent1_url:
            return jsonify({
                'success': False,
                'error': '缺少 parent1_url'
            }), 400
        
        parent2_url = data.get('parent2_url')
        baby_age = data.get('baby_age', 'newborn')
        num_variations = int(data.get('num_variations', 4))
        
        # 生成宝宝照片
        result = fusion_generator.generate_baby_from_parents_fal(
            parent1_image=parent1_url,
            parent2_image=parent2_url,
            baby_age=baby_age,
            num_variations=num_variations
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@baby_fusion_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    from baby_face_fusion import FAL_AVAILABLE, REPLICATE_AVAILABLE
    
    return jsonify({
        'status': 'healthy',
        'fal_available': FAL_AVAILABLE,
        'replicate_available': REPLICATE_AVAILABLE,
        'fal_key_configured': bool(os.environ.get('FAL_KEY')),
        'replicate_key_configured': bool(os.environ.get('REPLICATE_API_TOKEN'))
    })


@baby_fusion_bp.route('/test-upload', methods=['GET'])
def test_upload_form():
    """测试上传表单"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>宝宝面部融合 - 测试上传</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input[type="file"], select { width: 100%; padding: 8px; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; }
            button:hover { background: #0056b3; }
            .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; }
            .image-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 10px; }
            .image-grid img { width: 100%; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>🍼 宝宝面部融合生成器</h1>
        <p>上传父母照片，AI 生成预测的宝宝照片</p>
        
        <form id="uploadForm" enctype="multipart/form-data">
            <div class="form-group">
                <label>父母1照片 *</label>
                <input type="file" name="parent1" accept="image/*" required>
            </div>
            
            <div class="form-group">
                <label>父母2照片（可选）</label>
                <input type="file" name="parent2" accept="image/*">
            </div>
            
            <div class="form-group">
                <label>宝宝年龄</label>
                <select name="baby_age">
                    <option value="newborn">新生儿 (0-3个月)</option>
                    <option value="6months">6个月</option>
                    <option value="1year">1岁</option>
                    <option value="2years">2岁</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>生成数量</label>
                <select name="num_variations">
                    <option value="1">1张</option>
                    <option value="2">2张</option>
                    <option value="4" selected>4张</option>
                </select>
            </div>
            
            <button type="submit">🎨 生成宝宝照片</button>
        </form>
        
        <div id="result" class="result" style="display:none;">
            <h3>生成结果</h3>
            <div id="resultContent"></div>
        </div>
        
        <script>
            document.getElementById('uploadForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const formData = new FormData(e.target);
                const resultDiv = document.getElementById('result');
                const resultContent = document.getElementById('resultContent');
                
                resultDiv.style.display = 'block';
                resultContent.innerHTML = '<p>⏳ 正在生成宝宝照片，请稍候...</p>';
                
                try {
                    const response = await fetch('/api/baby-fusion/upload-and-generate', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        let html = '<p>✅ 生成成功！</p>';
                        html += '<div class="image-grid">';
                        data.images.forEach((url, i) => {
                            html += `<img src="${url}" alt="宝宝照片 ${i+1}">`;
                        });
                        html += '</div>';
                        resultContent.innerHTML = html;
                    } else {
                        resultContent.innerHTML = `<p>❌ 生成失败: ${data.error || data.message}</p>`;
                    }
                } catch (error) {
                    resultContent.innerHTML = `<p>❌ 请求失败: ${error.message}</p>`;
                }
            });
        </script>
    </body>
    </html>
    '''
