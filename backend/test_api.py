"""
测试婴儿图像生成 API
用法: python test_api.py <图片路径> [图片路径2] [性别]
示例: 
  python test_api.py parent1.jpg              # 单人照片，随机性别
  python test_api.py mom.jpg dad.jpg male     # 双人照片，男婴
"""
import sys
import httpx
import os

API_URL = "http://localhost:8000/api/v1/generate-baby"

def test_generate(photo_paths: list, gender: str = "random"):
    print(f"正在生成婴儿图像...")
    print(f"  照片: {photo_paths}")
    print(f"  性别: {gender}")
    print(f"  API: {API_URL}")
    
    # 先测试连接
    try:
        print("  测试连接...")
        with httpx.Client(timeout=5.0, proxy=None, trust_env=False) as client:
            health = client.get("http://localhost:8000/health")
            print(f"  健康检查: {health.status_code} - {health.text}")
    except Exception as e:
        print(f"  连接失败: {e}")
        return
    
    files = []
    for path in photo_paths:
        if not os.path.exists(path):
            print(f"错误: 文件不存在 - {path}")
            return
        f = open(path, "rb")
        files.append(("photos", (os.path.basename(path), f, "image/jpeg")))
    
    data = {"gender": gender}
    
    try:
        print("  发送生成请求...")
        with httpx.Client(timeout=120.0, proxy=None, trust_env=False) as client:
            response = client.post(API_URL, data=data, files=files)
            print(f"  状态码: {response.status_code}")
        
        if response.status_code != 200:
            print(f"\n❌ HTTP错误: {response.text}")
            return
            
        result = response.json()
        
        if result.get("success"):
            print(f"\n✅ 生成成功!")
            print(f"  图片URL: {result['data']['image_url']}")
        else:
            print(f"\n❌ 生成失败: {result}")
    except httpx.TimeoutException:
        print(f"\n❌ 请求超时 (120秒)")
    except Exception as e:
        print(f"\n❌ 请求错误: {type(e).__name__}: {e}")
    finally:
        for _, f in files:
            f[1].close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    photos = []
    gender = "random"
    
    for arg in sys.argv[1:]:
        if arg in ["male", "female", "random"]:
            gender = arg
        else:
            photos.append(arg)
    
    test_generate(photos, gender)
