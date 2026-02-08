const VERSION_KEY = "code-version";

function key(lang, pageId) {
  return `lang-${lang}-page-${pageId}`;
}

export function createCodeRepo(defaults, getLang) {
  const storedVersion = Number.parseInt(localStorage.getItem(VERSION_KEY) ?? "0", 10) || 0;

  let pages = $state({ hu: {}, en: {} });

  for (const lang of ["hu", "en"]) {
    for (const pageId in defaults.pages[lang]) {
      const raw = localStorage.getItem(key(lang, pageId));

      pages[lang][pageId] = {
        ...defaults.pages[lang][pageId],
        ...(storedVersion >= defaults.version && raw ? JSON.parse(raw) : {})
      };
    }
  }

  const version = Math.max(storedVersion, defaults.version);
  localStorage.setItem(VERSION_KEY, String(version));

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
      page[filename] = { content: "" };
      save(pageId);
    }
    return page[filename].content;
  }

  function set(pageId, filename, content) {
    const lang = getLang();
    const page = pages[lang][pageId];
    page[filename] = { content };
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
    pages[lang][pageId] = { ...defaults.pages[lang][pageId] };
    save(pageId);
  }

  return { pages, list, get, set, del, rename, reset };
}