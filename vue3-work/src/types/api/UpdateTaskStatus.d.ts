// src/types/api/updateTaskStatus.d.ts
// 该接口用于修改日程状态

// 修改日程状态接口请求头的参数类型
export interface UpdateTaskStatusRequestHeaders {
  Authorization?: string;  // 可选的授权令牌
}

// 修改日程状态接口请求体的参数类型
export interface UpdateTaskStatusRequestBody {
  status?: number;         // 日程状态，1表示完成，非必填
  date_id: number;         // 日程ID，必填
}

// 修改日程状态接口的响应类型
export interface UpdateTaskStatusResponse {
  code: 0;                // 返回码，0表示成功
  msg: string;            // 错误说明或操作成功信息
  data: {
    id: number;           // 日程ID
    user_id: number;      // 用户ID
    title?: string;       // 任务标题，非必填
    description?: string; // 任务描述，非必填
    status: number;       // 日程状态，必填
    created_at: string;   // 创建时间
    updated_at: string;   // 更新时间
    deleted_at?: string;  // 删除时间，非必填
    time: string;         // 时间，必填
  };
}
