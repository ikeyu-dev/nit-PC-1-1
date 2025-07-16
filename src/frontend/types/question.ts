export interface Question {
    id: number;
    question: string;
    detail: string;
    tag: string;
    created_at: string;
}

// Questionの配列として定義
export type Questions = Question[];
