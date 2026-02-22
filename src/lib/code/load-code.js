const rawFiles = import.meta.glob("./{hu,en}/**/*.{py,txt}", {
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
        "veletlen.py": { content: file("hu", "search/generator/veletlen.py") },
        "vege.py": { content: file("hu", "search/generator/vege.py") },
        "eleje.py": { content: file("hu", "search/generator/eleje.py") },
      },
      "input": {
        "input.txt": { content: file("hu", "search/input.txt") },
      }
    },
    sort: {
      "algo": {
        "buborek.py": { content: file("hu", "sort/algo/buborek.py") },
        "beszurasos.py": { content: file("hu", "sort/algo/beszurasos.py") },
        "kivalasztasos.py": { content: file("hu", "sort/algo/kivalasztasos.py") },
        "osszefesuleses.py": { content: file("hu", "sort/algo/osszefesuleses.py") },
        "gyors.py": { content: file("hu", "sort/algo/gyors.py") },
        "gyors_nemhelyben.py": { content: file("hu", "sort/algo/gyors_nemhelyben.py") },
        "beepitett.py": { content: file("hu", "sort/algo/beepitett.py") },
      },
      "generator": {
        "veletlen.py": { content: file("hu", "sort/generator/veletlen.py") },
        "novekvo.py": { content: file("hu", "sort/generator/novekvo.py") },
        "csokkeno.py": { content: file("hu", "sort/generator/csokkeno.py") },
      },
      "input": {
        "input.txt": { content: file("hu", "sort/input.txt") },
      }
    },
    dfs: {
      "algo": {
        "dfs_verem_szmat.py": { content: file("hu", "dfs/algo/dfs_verem_szmat.py") },
        "dfs_bsz2_szmat.py": { content: file("hu", "dfs/algo/dfs_bsz2_szmat.py") },
        "dfs_rekurziv_szmat.py": { content: file("hu", "dfs/algo/dfs_rekurziv_szmat.py") },
        "dfs_verem_ellista.py": { content: file("hu", "dfs/algo/dfs_verem_ellista.py") },
        "dfs_bsz2_ellista.py": { content: file("hu", "dfs/algo/dfs_bsz2_ellista.py") },
        "dfs_rekurziv_ellista.py": { content: file("hu", "dfs/algo/dfs_rekurziv_ellista.py") },
      },
      "generator": {
        "erdos_renyi_0.2.py": { content: file("hu", "dfs/generator/erdos_renyi_0.2.py") },
        "erdos_renyi_0.8.py": { content: file("hu", "dfs/generator/erdos_renyi_0.8.py") },
      },
      "input": {
        "input.txt": { content: file("hu", "dfs/input.txt") },
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
        "random.py": { content: file("en", "search/generator/random.py") },
        "last.py": { content: file("en", "search/generator/last.py") },
        "first.py": { content: file("en", "search/generator/first.py") },
      },
      "input": {
        "input.txt": { content: file("en", "search/input.txt") },
      }
    },
    sort: {
      "algo": {
        "bubble.py": { content: file("en", "sort/algo/bubble.py") },
        "insertion.py": { content: file("en", "sort/algo/insertion.py") },
        "selection.py": { content: file("en", "sort/algo/selection.py") },
        "merge.py": { content: file("en", "sort/algo/merge.py") },
        "quick.py": { content: file("en", "sort/algo/quick.py") },
        "quick_notinplace.py": { content: file("en", "sort/algo/quick_notinplace.py") },
        "builtin.py": { content: file("en", "sort/algo/builtin.py") },
      },
      "generator": {
        "random.py": { content: file("en", "sort/generator/random.py") },
        "increasing.py": { content: file("en", "sort/generator/increasing.py") },
        "decreasing.py": { content: file("en", "sort/generator/decreasing.py") },
      },
      "input": {
        "input.txt": { content: file("en", "sort/input.txt") },
      }
    },
    dfs: {
      "algo": {
        "dfs_stack_amat.py": { content: file("hu", "dfs/algo/dfs_verem_szmat.py") },
        "dfs_itc2_amat.py":  { content: file("hu", "dfs/algo/dfs_bsz2_szmat.py") },
        "dfs_recursive_amat.py": { content: file("hu", "dfs/algo/dfs_rekurziv_szmat.py") },
        "dfs_verem_elist.py": { content: file("hu", "dfs/algo/dfs_verem_ellista.py") },
        "dfs_bsz2_elist.py": { content: file("hu", "dfs/algo/dfs_bsz2_ellista.py") },
        "dfs_rekurziv_elist.py": { content: file("hu", "dfs/algo/dfs_rekurziv_ellista.py") },
      },
      "generator": {
        "erdos_renyi_0.2.py": { content: file("hu", "dfs/generator/erdos_renyi_0.2.py") },
        "erdos_renyi_0.8.py": { content: file("hu", "dfs/generator/erdos_renyi_0.8.py") },
      },
      "input": {
        "input.txt": { content: file("hu", "dfs/input.txt") },
      }
    }
  };
}

export function loadDefaultCode() {
  return { version: 12, pages: { hu: loadHu(), en: loadEn() } };
}

export const defaultCode = loadDefaultCode();
