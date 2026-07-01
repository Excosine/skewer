import request from './request'

export function login(data) {
  return request.post('/auth/login', data)
}

export function getUserInfo() {
  return request.get('/auth/me')
}

// 获取验证码 key
export function getCaptcha() {
  return request.get('/auth/captcha')
}

// 获取验证码图片 URL（直接使用相对路径，Vite 代理会转发）
export function getCaptchaImageUrl(captchaKey) {
  // 使用相对路径，浏览器会请求前端服务器，然后 Vite 代理转发到后端
  return `/api/auth/captcha/image/${captchaKey}`
}
