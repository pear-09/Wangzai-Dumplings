//该接口用于新建笔记文件夹

// 定义单个文件夹的结构
export interface Notefiles {
    id: number;          // 文件夹 ID
    user_id: number;     // 用户 ID
    name: string;        // 文件夹名称
    created_at: string;  // 创建时间，格式为 "YYYY-MM-DD HH:mm:ss"
  }
  
  // 定义获取单个文件夹详细信息的接口返回结构
  export interface GetNotefilesResponse {
    code: number;         // 状态码，0 表示成功，其他值表示失败
    msg: string;          // 状态信息或错误信息
    data: Notefiles;      // 返回的单个文件夹信息
  }

