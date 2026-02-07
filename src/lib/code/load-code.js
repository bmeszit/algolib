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
  const res = {};
  for (const lang of ["hu", "en"]) {
    res[lang] = {
      search: {
        "linsrc.py": { content: file(lang, "search/linsrc.py"), version: 1 },
        "binsrc.py": { content: file(lang, "search/binsrc.py"), version: 1 },
      },
      sort: {
        "bubble.py": { content: file(lang, "sort/bubble.py"), version: 1 },
        "insertion.py": { content: file(lang, "sort/insertion.py"), version: 1 },
        "merge.py": { content: file(lang, "sort/merge.py"), version: 1 },
        "quick.py": { content: file(lang, "sort/quick.py"), version: 1 },
        "selection.py": { content: file(lang, "sort/selection.py"), version: 1 },
      },
    };
  }
  return res;
}

export const defaultCode = loadDefaultCode();