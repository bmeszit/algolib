const VERSION_KEY = "code-version";

function key(lang, pageId, type) {
  return `lang-${lang}-page-${pageId}-type-${type}`;
}

export function createCodeRepo(defaults, getLang) {
  const storedVersion = Number.parseInt(localStorage.getItem(VERSION_KEY) ?? "0", 10) || 0;

  let pages = $state({ hu: {}, en: {} });

  for (const lang of ["hu", "en"]) {
    for (const pageId in defaults.pages[lang]) {
      pages[lang][pageId] = {};
      for (const type in defaults.pages[lang][pageId]) {
        const raw = localStorage.getItem(key(lang, pageId, type));

        pages[lang][pageId][type] = {
          ...defaults.pages[lang][pageId][type],
          ...(storedVersion >= defaults.version && raw ? JSON.parse(raw) : {}),
        };
      }
    }
  }

  const version = Math.max(storedVersion, defaults.version);
  localStorage.setItem(VERSION_KEY, String(version));

  function save(pageId, type) {
    const lang = getLang();
    localStorage.setItem(key(lang, pageId, type), JSON.stringify(pages[lang][pageId][type]));
  }

  function list(pageId, type) {
    const lang = getLang();
    return Object.keys(pages[lang][pageId][type] ?? {});
  }

  function get(pageId, type, filename) {
    const lang = getLang();
    const bucket = (pages[lang][pageId][type] ??= {});
    if (!bucket[filename]) {
      bucket[filename] = { content: "" };
      save(pageId, type);
    }
    return bucket[filename].content;
  }

  function set(pageId, type, filename, content) {
    const lang = getLang();
    const bucket = (pages[lang][pageId][type] ??= {});
    bucket[filename] = { content };
    save(pageId, type);
  }

  function del(pageId, type, filename) {
    const lang = getLang();
    const bucket = pages[lang][pageId][type];
    if (!bucket) return;
    delete bucket[filename];
    save(pageId, type);
  }

  function rename(pageId, type, from, to) {
    const lang = getLang();
    if (from === to) return true;
    const bucket = pages[lang][pageId][type];
    if (!bucket || !bucket[from] || bucket[to]) return false;
    bucket[to] = bucket[from];
    delete bucket[from];
    save(pageId, type);
    return true;
  }

  function reset(pageId, type) {
    const lang = getLang();
    pages[lang][pageId][type] = { ...defaults.pages[lang][pageId][type] };
    save(pageId, type);
  }

  return { pages, list, get, set, del, rename, reset };
}
