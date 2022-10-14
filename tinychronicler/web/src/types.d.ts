export type Chronicle = {
  created_at: string;
  language: string;
  description: string;
  id: number;
  title: string;
};

export type File = {
  created_at: string;
  id: number;
  mime: string;
  name: string;
  thumb_name: string;
  thumb_url: string;
  url: string;
};

export type Composition = {
  created_at: string;
  data?: {
    notes: [number, number][];
    parameters: {
      parameters: string[];
      module: [number, number];
    }[];
  };
  score?: string;
  id: number;
  is_ready: boolean;
  title: string;
  version: number;
};
