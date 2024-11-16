// src/types/api/response.ts

export interface ApiResponse<T> {
    code: number;   // 返回的状态码
    msg: string;    // 错误或成功信息
    data: T;        // 响应数据
  }
  