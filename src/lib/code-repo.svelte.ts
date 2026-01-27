export type PageId = string
export type Filename = string
export type Pages = Record<PageId, Record<Filename, string>>

function key(pageId: PageId): string { return `pageCode:${pageId}`; }

export function createCodeRepo(defaults: Pages) {
  let pages = $state<Pages>({});

  function ensure(pageId: PageId): void {
    if (pages[pageId] !== undefined) return;

    const raw = localStorage.getItem(key(pageId));
    pages[pageId] = raw ? JSON.parse(raw) : { ...(defaults[pageId] ?? {}) };
  }

  function save(pageId: PageId): void {
    localStorage.setItem(key(pageId), JSON.stringify(pages[pageId]));
  }

  function list(pageId: PageId): Filename[] {
    ensure(pageId);
    return Object.keys(pages[pageId]);
  }

  function get(pageId: PageId, filename: Filename): string {
    ensure(pageId);
    if (pages[pageId][filename] === undefined) {
      pages[pageId][filename] = defaults[pageId]?.[filename] ?? "";
      save(pageId);
    }
    return pages[pageId][filename];
  }

  function set(pageId: PageId, filename: Filename, content: string): void {
    ensure(pageId);
    pages[pageId][filename] = content;
    save(pageId);
  }

  function del(pageId: PageId, filename: Filename): void {
    ensure(pageId);
    delete pages[pageId][filename];
    save(pageId);
  }

  function reset(pageId: PageId): void {
    pages[pageId] = { ...defaults[pageId] };
    save(pageId);
  }

  return { pages, list, get, set, del, reset };
}
