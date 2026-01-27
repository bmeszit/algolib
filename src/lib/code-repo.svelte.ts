import type { PageId, Filename, Pages } from "$lib";

function key(pageId: PageId): string { return `pageCode:${pageId}`; }

export function createCodeRepo(defaults: Pages) {
  let pages = $state<Pages>({});
  for (const pageId in defaults) {
    const raw = localStorage.getItem(key(pageId));
    pages[pageId] = raw
      ? { ...defaults[pageId as PageId], ...JSON.parse(raw) }
      : { ...defaults[pageId as PageId]};
  }

  function save(pageId: PageId): void {
    localStorage.setItem(key(pageId), JSON.stringify(pages[pageId]));
  }

  function list(pageId: PageId): Filename[] {
    return Object.keys(pages[pageId]);
  }

  function get(pageId: PageId, filename: Filename): string {
    if (pages[pageId][filename] === undefined) {
      pages[pageId][filename] = defaults[pageId]?.[filename] ?? "";
      save(pageId);
    }
    return pages[pageId][filename];
  }

  function set(pageId: PageId, filename: Filename, content: string): void {
    pages[pageId][filename] = content;
    save(pageId);
  }

  function del(pageId: PageId, filename: Filename): void {
    delete pages[pageId][filename];
    save(pageId);
  }

  function reset(pageId: PageId): void {
    pages[pageId] = { ...defaults[pageId] };
    save(pageId);
  }

  return { pages, list, get, set, del, reset };
}
