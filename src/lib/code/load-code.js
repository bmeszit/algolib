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
  const res = { version: 2, pages: { hu: {}, en: {} } };

  for (const lang of ["hu", "en"]) {
    res.pages[lang] = {
      search: {
        "algo": {
          "linsrc.py": { content: file(lang, "search/algo/linsrc.py") },
          "binsrc.py": { content: file(lang, "search/algo/binsrc.py") },
        }
      },
      sort: {
        "algo": {
          "bubble.py": { content: file(lang, "sort/algo/bubble.py") },
          "insertion.py": { content: file(lang, "sort/algo/insertion.py") },
          "merge.py": { content: file(lang, "sort/algo/merge.py") },
          "quick.py": { content: file(lang, "sort/algo/quick.py") },
          "selection.py": { content: file(lang, "sort/algo/selection.py") },
        },
        "generator": {
          "increasing.py": { content: file(lang, "sort/generator/increasing.py") }
        }
      }
    };
  }

  return res;
}

export const defaultCode = loadDefaultCode();