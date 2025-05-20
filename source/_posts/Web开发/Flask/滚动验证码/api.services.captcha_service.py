import os
import random
import io
import time
import json
import logging
from PIL import Image, ImageDraw, ImageFont
from extensions.ext_redis import redis_client



CAPTCHA_EXPIRE_TIME = 100  # 验证码有效期（秒）
VALIDATOR_WAIT_TIME = 300  # 验证码失败时间
VALIDATOR_MAX_FAIL_COUNT = 3  # 最大失败次数

class CaptchaService:
    # 定義圖片目錄
    IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'images')
    
    @staticmethod
    def get_random_image():
        """從圖片目錄隨機選擇一張圖片"""
        image_files = [f for f in os.listdir(CaptchaService.IMAGE_DIR) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not image_files:
            raise Exception("No images found in the images directory")
        
        random_image = random.choice(image_files)
        image_path = os.path.join(CaptchaService.IMAGE_DIR, random_image)
        return Image.open(image_path)


    @staticmethod
    def _get_redis_key(user_ip, key_type='captcha'):
        """生成 Redis 键名
        Args:
            user_ip: 用户IP
            key_type: 键类型 ('captcha' 或 'attempts')
        """
        return f"captcha:{key_type}:{user_ip}"

    @staticmethod
    def _get_captcha_data(user_ip):
        """从 Redis 获取验证码数据"""
        key = CaptchaService._get_redis_key(user_ip, 'captcha')
        data = redis_client.get(key)
        return json.loads(data) if data else None
    
    @staticmethod
    def _get_attempts_data(user_ip):
        """从 Redis 获取失败尝试数据"""
        key = CaptchaService._get_redis_key(user_ip, 'attempts')
        data = redis_client.get(key)
        return json.loads(data) if data else None
    
    @staticmethod
    def _save_captcha_data(user_ip, data):
        """保存验证码数据到 Redis"""
        key = CaptchaService._get_redis_key(user_ip, 'captcha')
        redis_client.setex(key, CAPTCHA_EXPIRE_TIME, json.dumps(data))
    
    @staticmethod
    def _save_attempts_data(user_ip, data):
        """保存失败尝试数据到 Redis"""
        key = CaptchaService._get_redis_key(user_ip, 'attempts')
        redis_client.setex(key, VALIDATOR_WAIT_TIME * 2, json.dumps(data))

    @staticmethod
    def check_failed_attempts(user_ip):
        """检查失败次数"""
        data = CaptchaService._get_captcha_data(user_ip)
        if not data:
            return True, 0

        failed_attempts = data.get('failed_attempts', 0)
        last_failed_time = data.get('last_failed_time', 0)

        if failed_attempts >= VALIDATOR_MAX_FAIL_COUNT:
            if time.time() - last_failed_time < VALIDATOR_WAIT_TIME:
                return False, VALIDATOR_WAIT_TIME - (time.time() - last_failed_time)
            else:
                # 重置失败次数
                data['failed_attempts'] = 0
                CaptchaService._save_attempts_data(user_ip, data)
        
        return True, 0
    
    @staticmethod
    def log_failed_attempt(user_ip):
        """记录失败尝试"""
        data = CaptchaService._get_captcha_data(user_ip) or {
            'failed_attempts': 0,
            'last_failed_time': 0
        }
        data['failed_attempts'] = data.get('failed_attempts', 0) + 1
        data['last_failed_time'] = time.time()
        CaptchaService._save_attempts_data(user_ip, data)

    @staticmethod
    def generate_slide_captcha():
        """生成滑块验证码图片

        Returns:
            tuple: 包含三个元素：
                - background_byte_arr: 背景图片的字节流
                - slider_byte_arr: 滑块图片的字节流
                - hole_position: 滑块位置的坐标元组 (x, y)
        """
        # 从预设的图片目录中随机获取一张背景图片
        original_image = CaptchaService.get_random_image()

        # 获取原图的宽度和高度
        width, height = original_image.size

        # 确保图片是 RGB 模式，如果不是则进行转换
        if original_image.mode != 'RGB':
            original_image = original_image.convert('RGB')
        
        # 计算滑块的大小，设置为图片宽度的 8%
        slider_size = int(width * 0.08)
        # 设置滑块最小尺寸为 40 像素，确保滑块不会太小
        slider_size = max(slider_size, 40)

        # 随机生成滑块的水平位置
        # 将图片横向分为四等份，滑块位置在中间两份之间
        # 这样可以避免滑块太靠近图片边缘
        hole_position_x = random.randint(
            width // 4,  # 最小水平位置：图片宽度的 1/4
            width * 3 // 4 - slider_size  # 最大水平位置：图片宽度的 3/4 减去滑块宽度
        )

        # 生成滑塊的垂直位置（在圖片中間區域）
        hole_position_y = random.randint(
            height // 4,  # 避免太靠上
            height * 3 // 4 - slider_size  # 避免太靠下
        )

        # 創建滑塊圖片（使用 RGBA 模式支持透明度）
        slider_image = Image.new('RGBA', (slider_size, slider_size), (0, 0, 0, 0))
        
        # 从原图中裁剪出滑块大小的区域
        # crop 方法接收一个元组 (left, top, right, bottom)
        slider_region = original_image.crop((
            hole_position_x, 
            hole_position_y,
            hole_position_x + slider_size,
            hole_position_y + slider_size
        ))
        # 将裁剪出的区域粘贴到透明滑块图片上
        slider_image.paste(slider_region, (0, 0))
        
        # 在背景图片上绘制一个半透明的白色方块，表示滑块的凹槽
        background_draw = ImageDraw.Draw(original_image)
        background_draw.rectangle(
            [
                hole_position_x, 
                hole_position_y,
                hole_position_x + slider_size,
                hole_position_y + slider_size
            ],
            fill=(255, 255, 255, 128)  # 半透明白色
        )
        
        # 在凹槽周围绘制一个灰色边框
        background_draw.rectangle(
            [
                hole_position_x - 1,
                hole_position_y - 1,
                hole_position_x + slider_size + 1,
                hole_position_y + slider_size + 1
            ],
            outline=(100, 100, 100), width=1  # 灰色邊框
        )

        # 创建两个字节流对象，用于存储图片数据
        background_byte_arr = io.BytesIO()
        slider_byte_arr = io.BytesIO()
        
        # 将图片保存为 PNG 格式到字节流中
        original_image.save(background_byte_arr, format='PNG')
        slider_image.save(slider_byte_arr, format='PNG')
        
        # 将字节流的指针移到开始位置，准备读取
        background_byte_arr.seek(0)
        slider_byte_arr.seek(0)

        hole_position = (hole_position_x, hole_position_y)

        return background_byte_arr, slider_byte_arr, hole_position
    

    @staticmethod
    def validate_slide_captcha(user_ip, user_position):
        """验证滑动位置"""
        data = CaptchaService._get_captcha_data(user_ip)
        if not data:
            return False, "验证码无效"

        # 检查是否过期
        if time.time() - data.get('created_at', 0) > CAPTCHA_EXPIRE_TIME:
            CaptchaService.reset_captcha(user_ip)
            return False, "验证码已过期"

        correct_position = data.get('hole_position_x')
        slider_size = data.get('slider_size', 30)  # 獲取保存的滑塊尺寸，默認值為30
        
        # 使用實際的滑塊尺寸計算允許的誤差範圍
        error_range = slider_size * 0.3  # 允許 30% 的誤差範圍
        
        if abs(user_position - correct_position) <= error_range:
            CaptchaService.reset_captcha(user_ip)
            return True, "验证成功"
        else:
            CaptchaService.log_failed_attempt(user_ip)
            return False, "验证失败"

    @staticmethod
    def reset_captcha(user_ip):
        """重置验证码"""
        key = CaptchaService._get_redis_key(user_ip, 'captcha')
        redis_client.delete(key)

    @staticmethod
    def generate(user_ip):
        """生成验证码"""
        valid, wait_time = CaptchaService.check_failed_attempts(user_ip)
        if not valid:
            return {
                "status": "error",
                "message": f"验证失败次数过多，请等待 {int(wait_time)} 秒后再试"
            }, 403

        try:
            background_image, slider_image, hole_position = CaptchaService.generate_slide_captcha()
        except Exception as e:
            logging.error(f"Generate captcha error: {str(e)}")
            return {
                "status": "error",
                "message": "生成驗證碼失敗"
            }, 500
        
        # 保存验证码数据到 Redis
        data = {
            'type': 'slide',
            'hole_position_x': hole_position[0],
            'hole_position_y': hole_position[1],
            'failed_attempts': 0,
            'last_failed_time': 0,
            'created_at': time.time()
        }
        CaptchaService._save_captcha_data(user_ip, data)

        # 转换图片为 base64
        import base64
        background_image.seek(0)
        slider_image.seek(0)

        background_base64 = base64.b64encode(background_image.getvalue()).decode('utf-8')
        slider_base64 = base64.b64encode(slider_image.getvalue()).decode('utf-8')
        
        return {
            "status": "success",
            "background_image": background_base64,
            "slider_image": slider_base64,
            "hole_position_y": hole_position[1],
            "user_ip": user_ip
        }