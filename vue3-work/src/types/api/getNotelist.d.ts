//该接口用于笔记列表

// 定义笔记的数据结构
export interface Note {
    id: number;           // 笔记 ID
    user_id: number;      // 用户 ID
    title: string;        // 笔记标题
    content: string;      // 笔记内容
    folder_id: number;    // 文件夹 ID
    tag: string;          // 标签，例如“近代史”
    created_at: string;   // 创建时间，格式为 "YYYY-MM-DD HH:mm:ss"
    updated_at: string;   // 更新时间，格式为 "YYYY-MM-DD HH:mm:ss"
    deleted_at: string | null; // 删除时间，可能为 null
  }

export interface Notelist {
    id: number;           // 笔记 ID
    user_id: number;      // 用户 ID
    title: string;        // 笔记标题
    folder_id: number;    // 文件夹 ID
    tag: string;          // 标签，例如“近代史”
    created_at: string;   // 创建时间，格式为 "YYYY-MM-DD HH:mm:ss"
 }
  
  // 定义获取笔记列表返回的结果结构
  export interface GetNotesResponse {
    code: number;         // 状态码，0 表示成功，其他值表示失败
    msg: string;          // 状态信息或错误信息
    data: Note[];         // 笔记数据数组
  }
  
  // 定义获取单个笔记详情返回的结果结构
  export interface GetNoteDetailResponse {
    code: number;         // 状态码，0 表示成功，其他值表示失败
    msg: string;          // 状态信息或错误信息
    data: Note;           // 单个笔记的详细数据
  }
  