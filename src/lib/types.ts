export type PageId = string;
export type Filename = string;
export type CodeFile = {content: string; version: number;};
export type Pages = Record<PageId, Record<Filename, CodeFile>>;
