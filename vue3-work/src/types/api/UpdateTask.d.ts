//src/types/api/UpdateTask.d.ts
export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  date_id?: number;
}

export interface TaskData {
  id: number;
  user_id: number;
  title?: string;
  description?: string;
  status: number;
  created_at: string;
  updated_at: string;
  deleted_at?: string;
  time: string;
}

export interface UpdateTaskResponse {
  code: 0;
  msg: string;
  data: TaskData;
}
