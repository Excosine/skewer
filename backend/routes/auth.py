"""Auth routes — login / me / captcha."""

import io
import random
import string
import time
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont

from db import get_session
from db.queries import get_user_by_username, get_user_by_id
from services.auth import create_token, verify_password
from routes._deps import current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

# 验证码存储（内存缓存，实际生产环境应使用 Redis）
captcha_store: Dict[str, dict] = {}


class LoginBody(BaseModel):
    username: str
    password: str
    captcha_key: str  # 验证码唯一标识
    captcha_code: str  # 用户输入的验证码


class LoginResponse(BaseModel):
    token: str
    username: str
    role: str
    real_name: str


class CaptchaResponse(BaseModel):
    captcha_key: str


def generate_captcha_image(code: str, width: int = 120, height: int = 40) -> bytes:
    """生成验证码图片"""
    # 创建图片
    image = Image.new('RGB', (width, height), color=(45, 40, 35))  # 深棕底色
    draw = ImageDraw.Draw(image)
    
    # 尝试使用系统字体，如果没有则使用默认字体
    try:
        # Windows 系统常用字体路径
        font_paths = [
            r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\Arial.ttf",
            r"C:\Windows\Fonts\simhei.ttf",
            r"C:\Windows\Fonts\SimHei.ttf",
        ]
        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, 24)
                break
            except:
                continue
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # 绘制干扰线 - 暗红/暖橙配色
    for _ in range(3):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        color = random.choice([
            (139, 35, 25),    # 暗红
            (180, 80, 50),    # 暖橙
            (230, 184, 125),  # 鎏金
        ])
        draw.line([(x1, y1), (x2, y2)], fill=color, width=1)
    
    # 绘制干扰点
    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        color = random.choice([
            (139, 35, 25),
            (180, 80, 50),
            (230, 184, 125),
            (248, 245, 242),
        ])
        draw.point((x, y), fill=color)
    
    # 绘制验证码字符 - 复古火锅配色
    for i, char in enumerate(code):
        # 每个字符随机颜色
        char_color = random.choice([
            (220, 150, 100),  # 暖焦糖橙
            (230, 184, 125),  # 鎏金
            (200, 120, 80),   # 复古红
            (248, 245, 242),  # 暖白
        ])
        # 每个字符随机位置微调
        x = 15 + i * 25 + random.randint(-3, 3)
        y = 5 + random.randint(0, 10)
        draw.text((x, y), char, font=font, fill=char_color)
    
    # 转为 PNG bytes
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    return buffer.getvalue()


@router.get("/captcha", response_model=CaptchaResponse)
def get_captcha():
    """获取验证码"""
    # 生成随机验证码（4位数字+字母）
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    # 生成唯一 key
    captcha_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    
    # 存储验证码（5分钟有效期）
    captcha_store[captcha_key] = {
        'code': code,
        'expire_time': time.time() + 300  # 5分钟
    }
    
    return CaptchaResponse(captcha_key=captcha_key)


@router.get("/captcha/image/{captcha_key}")
def get_captcha_image(captcha_key: str):
    """获取验证码图片"""
    # 检查验证码是否存在
    if captcha_key not in captcha_store:
        raise HTTPException(status_code=404, detail="验证码不存在")
    
    captcha_data = captcha_store[captcha_key]
    
    # 检查是否过期
    if time.time() > captcha_data['expire_time']:
        del captcha_store[captcha_key]
        raise HTTPException(status_code=410, detail="验证码已过期")
    
    # 生成验证码图片
    image_bytes = generate_captcha_image(captcha_data['code'])
    
    # 返回图片流
    return StreamingResponse(
        io.BytesIO(image_bytes),
        media_type="image/png",
        headers={"Cache-Control": "no-cache"}
    )


@router.post("/login", response_model=LoginResponse)
def login(body: LoginBody):
    # 验证验证码
    if body.captcha_key not in captcha_store:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码不存在，请重新获取"
        )
    
    captcha_data = captcha_store[body.captcha_key]
    
    # 检查是否过期
    if time.time() > captcha_data['expire_time']:
        del captcha_store[body.captcha_key]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码已过期，请重新获取"
        )
    
    # 验证码不区分大小写
    if body.captcha_code.upper() != captcha_data['code'].upper():
        # 验证失败后删除验证码
        del captcha_store[body.captcha_key]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码错误"
        )
    
    # 验证成功后删除验证码（一次性使用）
    del captcha_store[body.captcha_key]
    
    # 验证用户名密码
    db = get_session()
    user = get_user_by_username(db, body.username)
    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

    token = create_token(user.id, user.username, user.role_id)
    return LoginResponse(
        token=token,
        username=user.username,
        role="admin" if user.role_id == 1 else "waiter",
        real_name=user.real_name,
    )


@router.get("/me")
def me(user=Depends(current_user)):
    db = get_session()
    u = get_user_by_id(db, int(user["sub"]))
    return {
        "id": u.id,
        "username": u.username,
        "real_name": u.real_name,
        "role": "admin" if u.role_id == 1 else "waiter",
    }