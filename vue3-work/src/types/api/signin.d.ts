// signin.d.ts

// 定义用户注册请求的接口
export interface UserRegistrationRequest {
    username: string;  // 用户名
    password: string;  // 密码
}

// 定义用户注册响应的接口
export interface UserRegistrationResponse {
    code: number;         // 状态码，0 表示成功，其他值表示失败
    msg: string;          // 状态信息或错误信息          
}