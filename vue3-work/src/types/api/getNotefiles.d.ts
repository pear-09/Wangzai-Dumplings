//该接口用于获取笔记文件夹列表

// 定义数据部分的结构
export interface Notefiles {
    id: number;          //文件夹 ID
    user_id: number;     // 用户 ID
    name: string;        // 文件夹名称
    created_at: string;  // 创建时间，格式为 "YYYY-MM-DD HH:mm:ss"
    updated_at: string;  // 更新时间，格式为 "YYYY-MM-DD"
    deleted_at: string | null; // 删除时间，可能为 null（假如课程没有被删除）
  }

// 定义获取笔记文件夹返回的结果结构
export interface GetNotefilesResponse {
    code: number;         // 状态码，0 表示成功，其他值表示失败
    msg: string;          // 状态信息或错误信息
    data: Notefiles[];             
  }

