function key(lang, pageId) {
  return `lang-${lang}-page-${pageId}`;
}

export function createCodeRepo(defaults, getLang) {
  let pages = $state({ hu: {}, en: {} });

  for (const lang of ["hu", "en"]) {
    for (const pageId in defaults[lang]) {
      const raw = localStorage.getItem(key(lang, pageId));
      const stored = (raw ? JSON.parse(raw) : {});

      pages[lang][pageId] = {
        ...defaults[lang][pageId],
        ...stored,
      };

      for (const fname in stored) {
        const def = defaults[lang][pageId]?.[fname];
        const cur = stored[fname];
        const curVersion = typeof cur?.version === "number" ? cur.version : 0;
        if (def && def.version > curVersion) {
          pages[lang][pageId][fname] = def;
        }
      }
    }
  }

  function save(pageId) {
    const lang = getLang();
    localStorage.setItem(key(lang, pageId), JSON.stringify(pages[lang][pageId]));
  }

  function list(pageId) {
    const lang = getLang();
    return Object.keys(pages[lang][pageId]);
  }

  function get(pageId, filename) {
    const lang = getLang();
    const page = pages[lang][pageId];
    if (!page[filename]) {
      page[filename] = { content: "", version: 0 };
      save(pageId);
    }
    return page[filename].content;
  }

  function set(pageId, filename, content) {
    const lang = getLang();
    const page = pages[lang][pageId];
    const version = page[filename]?.version ?? 0;
    page[filename] = { content, version };
    save(pageId);
  }

  function del(pageId, filename) {
    const lang = getLang();
    delete pages[lang][pageId][filename];
    save(pageId);
  }

  function rename(pageId, from, to) {
    const lang = getLang();
    if (from === to) return true;
    const page = pages[lang][pageId];
    if (!page[from] || page[to]) return false;
    page[to] = page[from];
    delete page[from];
    save(pageId);
    return true;
  }

  function reset(pageId) {
    const lang = getLang();
    pages[lang][pageId] = { ...defaults[lang][pageId] };
    save(pageId);
  }

  return { pages, list, get, set, del, rename, reset };
}