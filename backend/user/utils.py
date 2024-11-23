from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken

# 生成JWT token的函数
def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)

    # 获取access token，并设置有效期为12小时
    access_token = AccessToken.for_user(user)

    # 设置 token 的有效期为12小时
    access_token.set_exp(lifetime=timedelta(hours=12))

    return str(access_token)  # 返回生成的 access_token

# 验证token（涉及到需要用户个人服务都需要验证token）
def verify_and_refresh_token(request):
    token = request.headers.get('Authorization')  # 从请求头中获取Authorization字段

    if not token:
        raise AuthenticationFailed('Authorization header missing')

    # 去除 "Bearer " 前缀
    token = token.replace('Bearer ', '')

    try:
        # 验证 token
        access_token = AccessToken(token)

        # 刷新 token（设置新的过期时间为12小时）
        access_token.set_exp(lifetime=timedelta(hours=12))  # 12小时有效期

        # 返回新的 token
        return str(access_token)

    except Exception as e:
        raise AuthenticationFailed(f'Token is invalid or expired: {str(e)}')