export interface FileItem {
  file_id: string;
  filename: string;
  url: string;
  uploaded_at: string;
}

export interface QueryReply {
  query: string;
  response: string;
  timestamp?: string;
}