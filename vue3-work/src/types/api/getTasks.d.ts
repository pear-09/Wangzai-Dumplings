// src/types/api/getTasks.d.ts
// 该接口用于获取单天日程

// 定义日程类型
export interface Task {
    id: number;
    title: string;
    description: string;
    time: string;
    status: string;
  }

  // 获取日程列表接口的响应类型
  export interface GetTasksResponse {
    code: number;
    msg: string;
    data: Task[];
  }



