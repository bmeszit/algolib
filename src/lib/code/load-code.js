const rawFiles = import.meta.glob("./{hu,en}/**/*.py", {
  as: "raw",
  eager: true,
});

function file(lang, path) {
  const key = `./${lang}/${path}`;
  const v = rawFiles[key];
  if (v === undefined) {
    throw new Error(`Missing file: ${key}`);
  }
  return v;
}

export function loadDefaultCode() {
  const res = { version: 1, pages: { hu: {}, en: {} } };

  for (const lang of ["hu", "en"]) {
    res.pages[lang] = {
      search: {
        "linsrc.py": { content: file(lang, "search/linsrc.py") },
        "binsrc.py": { content: file(lang, "search/binsrc.py") },
      },
      sort: {
        "bubble.py": { content: file(lang, "sort/bubble.py") },
        "insertion.py": { content: file(lang, "sort/insertion.py") },
        "merge.py": { content: file(lang, "sort/merge.py") },
        "quick.py": { content: file(lang, "sort/quick.py") },
        "selection.py": { content: file(lang, "sort/selection.py") },
      },
    };
  }

  return res;
}

export const defaultCode = loadDefaultCode();