// src/types/api/makeTask.d.ts
export interface MakeTaskRequest {
  user_id?: number;
  title?: string;
  description?: string;
  time?: string;
}

export interface MakeTaskResponse {
  code: 0;
  msg: string;
}
