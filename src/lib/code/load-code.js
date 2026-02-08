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

function loadHu() {
  return {
    search: {
      "algo": {
        "linker.py": { content: file("hu", "search/algo/linker.py") },
        "binker.py": { content: file("hu", "search/algo/binker.py") },
      },
      "generator": {
        "eleje.py": { content: file("hu", "search/generator/eleje.py") },
        "vege.py": { content: file("hu", "search/generator/vege.py") },
        "veletlen.py": { content: file("hu", "search/generator/veletlen.py") }
      }
    },
    sort: {
      "algo": {
        "buborek.py": { content: file("hu", "sort/algo/buborek.py") },
        "beszurasos.py": { content: file("hu", "sort/algo/beszurasos.py") },
        "osszefesuleses.py": { content: file("hu", "sort/algo/osszefesuleses.py") },
        "gyors.py": { content: file("hu", "sort/algo/gyors.py") },
        "kivalasztasos.py": { content: file("hu", "sort/algo/kivalasztasos.py") },
      },
      "generator": {
        "novekvo.py": { content: file("hu", "sort/generator/novekvo.py") },
        "csokkeno.py": { content: file("hu", "sort/generator/csokkeno.py") },
        "veletlen.py": { content: file("hu", "sort/generator/veletlen.py") }
      }
    }
  };
}

function loadEn() {
  return {
    search: {
      "algo": {
        "linsrc.py": { content: file("en", "search/algo/linsrc.py") },
        "binsrc.py": { content: file("en", "search/algo/binsrc.py") },
      },
      "generator": {
        "begin.py": { content: file("hu", "search/generator/eleje.py") },
        "end.py": { content: file("hu", "search/generator/vege.py") },
        "random.py": { content: file("hu", "search/generator/veletlen.py") }
      }
    },
    sort: {
      "algo": {
        "bubble.py": { content: file("en", "sort/algo/bubble.py") },
        "insertion.py": { content: file("en", "sort/algo/insertion.py") },
        "merge.py": { content: file("en", "sort/algo/merge.py") },
        "quick.py": { content: file("en", "sort/algo/quick.py") },
        "selection.py": { content: file("en", "sort/algo/selection.py") },
      },
      "generator": {
        "increasing.py": { content: file("en", "sort/generator/increasing.py") },
        "decreasing.py": { content: file("hu", "sort/generator/csokkeno.py") },
        "random.py": { content: file("hu", "sort/generator/veletlen.py") }
      }
    }
  };
}

export function loadDefaultCode() {
  return { version: 2, pages: { hu: loadHu(), en: loadEn() } };
}

export const defaultCode = loadDefaultCode();
