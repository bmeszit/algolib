import type { PageId, Filename, Pages } from "$lib";

function key(pageId: PageId): string { return `pageCode:${pageId}`; }

export function createCodeRepo(defaults: Pages) {
  let pages = $state<Pages>({});
  for (const pageId in defaults) {

    const raw = localStorage.getItem(key(pageId as PageId));
    const stored = raw ? JSON.parse(raw) : {};

    pages[pageId as PageId] = stored
      ? { ...defaults[pageId as PageId], ...stored }
      : { ...defaults[pageId as PageId] };

    for (const fname in stored) {
      const def = defaults[pageId]?.[fname];
      const cur = stored[fname];
      if (def && def.version > cur.version) {
        pages[pageId][fname] = def;
      }
    }
  }

  function save(pageId: PageId): void {
    localStorage.setItem(key(pageId), JSON.stringify(pages[pageId]));
  }

  function list(pageId: PageId): Filename[] {
    return Object.keys(pages[pageId]) as Filename[];
  }

  function get(pageId: PageId, filename: Filename): string {
    const page = pages[pageId];
    if (!page[filename]) {
      page[filename] = { content: "", version: 0 };
      save(pageId);
    }
    return page[filename].content;
  }

  function set(pageId: PageId, filename: Filename, content: string): void {
    const page = pages[pageId];
    const version = page[filename]?.version ?? 0;
    page[filename] = { content, version };
    save(pageId);
  }

  function del(pageId: PageId, filename: Filename): void {
    delete pages[pageId][filename];
    save(pageId);
  }

  function rename(pageId: PageId, from: Filename, to: Filename): boolean {
    if (from === to) return true;
    const page = pages[pageId];
    if (!page[from] || page[to]) return false;

    page[to] = page[from];
    delete page[from];
    save(pageId);
    return true;
  }

  function reset(pageId: PageId): void {
    pages[pageId] = { ...defaults[pageId] };
    save(pageId);
  }

  return { pages, list, get, set, del, rename, reset };
}
