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
        "beszurasos_binker.py": { content: file("hu", "sort/algo/beszurasos_binker.py") },
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
        "dfs_ellista.py": { content: file("hu", "dfs/algo/dfs_ellista.py") },
        "dfs_szmat.py": { content: file("hu", "dfs/algo/dfs_szmat.py") },
        "dfs_rekurziv_ellista.py": { content: file("hu", "dfs/algo/dfs_rekurziv_ellista.py") },
        "dfs_rekurziv_szmat.py": { content: file("hu", "dfs/algo/dfs_rekurziv_szmat.py") },
      },
      "generator": {
        "erdos_renyi_0.2.py": { content: file("hu", "dfs/generator/erdos_renyi_0.2.py") },
        "erdos_renyi_0.8.py": { content: file("hu", "dfs/generator/erdos_renyi_0.8.py") },
      },
      "input": {
        "input.txt": { content: file("hu", "dfs/input.txt") },
      }
    },
    dfs_ec: {
      "algo": {
        "dfs_elosztaly.py": { content: file("hu", "dfs_ec/algo/dfs_elosztaly.py") },
      },
      "generator": {
        "erdos_renyi_0.2.py": { content: file("hu", "dfs/generator/erdos_renyi_0.2.py") },
        "erdos_renyi_0.8.py": { content: file("hu", "dfs/generator/erdos_renyi_0.8.py") },
      },
      "input": {
        "input.txt": { content: file("hu", "dfs_ec/input.txt") },
      }
    },
    dfs_topo: {
      "algo": {
        "dfs_topo.py": { content: file("hu", "dfs_topo/algo/dfs_topo.py") },
      },
      "generator": {
        "erdos_renyi_0.2.py": { content: file("hu", "dfs_topo/generator/erdos_renyi_0.2.py") },
        "erdos_renyi_0.8.py": { content: file("hu", "dfs_topo/generator/erdos_renyi_0.8.py") },
      },
      "input": {
        "input.txt": { content: file("hu", "dfs_topo/input.txt") },
      }
    },
    dijkstra: {
      "algo": {
        "dijkstra_ellista.py": { content: file("hu", "dijkstra/algo/dijkstra_ellista.py") },
        "dijkstra_szmat.py": { content: file("hu", "dijkstra/algo/dijkstra_szmat.py") },
      },
      "generator": {
        "erdos_renyi_0.2.py": { content: file("hu", "dijkstra/generator/erdos_renyi_0.2.py") },
        "erdos_renyi_0.8.py": { content: file("hu", "dijkstra/generator/erdos_renyi_0.8.py") },
      },
      "input": {
        "input.txt": { content: file("hu", "dijkstra/input.txt") },
      }
    },
    bf: {
      "algo": {
        "bellman_ford_ellista.py": { content: file("hu", "bf/algo/bellman_ford_ellista.py") },
        "bellman_ford_szmat.py": { content: file("hu", "bf/algo/bellman_ford_szmat.py") },
      },
      "generator": {
        "erdos_renyi_0.2.py": { content: file("hu", "bf/generator/erdos_renyi_0.2.py") },
        "erdos_renyi_0.8.py": { content: file("hu", "bf/generator/erdos_renyi_0.8.py") },
      },
      "input": {
        "input.txt": { content: file("hu", "bf/input.txt") },
      }
    },
    mindist: {
      "algo": {
        "dfs_topo_ellista.py": { content: file("hu", "mindist/algo/dfs_topo_ellista.py") },
        "dfs_topo_szmat.py": { content: file("hu", "mindist/algo/dfs_topo_szmat.py") },
        "dijkstra_ellista.py": { content: file("hu", "dijkstra/algo/dijkstra_ellista.py") },
        "dijkstra_szmat.py": { content: file("hu", "dijkstra/algo/dijkstra_szmat.py") },
        "bellman_ford_ellista.py": { content: file("hu", "bf/algo/bellman_ford_ellista.py") },
        "bellman_ford_szmat.py": { content: file("hu", "bf/algo/bellman_ford_szmat.py") },
      },
      "generator": {
        "erdos_renyi_0.2.py": { content: file("hu", "mindist/generator/erdos_renyi_0.2.py") },
        "erdos_renyi_0.8.py": { content: file("hu", "mindist/generator/erdos_renyi_0.8.py") },
      },
      "input": {
        "input.txt": { content: file("hu", "mindist/input.txt") },
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
        "insertion_binsrc.py": { content: file("en", "sort/algo/insertion_binsrc.py") },
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
        "dfs_elist.py": { content: file("en", "dfs/algo/dfs_elist.py") },
        "dfs_amat.py": { content: file("en", "dfs/algo/dfs_amat.py") },
        "dfs_recursive_elist.py": { content: file("en", "dfs/algo/dfs_recursive_elist.py") },
        "dfs_recursive_amat.py": { content: file("en", "dfs/algo/dfs_recursive_amat.py") },
      },
      "generator": {
        "erdos_renyi_0.2.py": { content: file("en", "dfs/generator/erdos_renyi_0.2.py") },
        "erdos_renyi_0.8.py": { content: file("en", "dfs/generator/erdos_renyi_0.8.py") },
      },
      "input": {
        "input.txt": { content: file("en", "dfs/input.txt") },
      }
    },
    dfs_ec: {
      "algo": {
        "dfs_edgeclass.py": { content: file("en", "dfs_ec/algo/dfs_edgeclass.py") },
      },
      "generator": {
        "erdos_renyi_0.2.py": { content: file("en", "dfs/generator/erdos_renyi_0.2.py") },
        "erdos_renyi_0.8.py": { content: file("en", "dfs/generator/erdos_renyi_0.8.py") },
      },
      "input": {
        "input.txt": { content: file("en", "dfs_ec/input.txt") },
      }
    },
    dfs_topo: {
      "algo": {
        "dfs_topo.py": { content: file("en", "dfs_topo/algo/dfs_topo.py") },
      },
      "generator": {
        "erdos_renyi_0.2.py": { content: file("en", "dfs_topo/generator/erdos_renyi_0.2.py") },
        "erdos_renyi_0.8.py": { content: file("en", "dfs_topo/generator/erdos_renyi_0.8.py") },
      },
      "input": {
        "input.txt": { content: file("en", "dfs_topo/input.txt") },
      }
    },
    dijkstra: {
      "algo": {
        "dijkstra_elist.py": { content: file("en", "dijkstra/algo/dijkstra_elist.py") },
        "dijkstra_amat.py": { content: file("en", "dijkstra/algo/dijkstra_amat.py") },
      },
      "generator": {
        "erdos_renyi_0.2.py": { content: file("en", "dijkstra/generator/erdos_renyi_0.2.py") },
        "erdos_renyi_0.8.py": { content: file("en", "dijkstra/generator/erdos_renyi_0.8.py") },
      },
      "input": {
        "input.txt": { content: file("en", "dijkstra/input.txt") },
      }
    },
    bf: {
      "algo": {
        "bellman_ford_elist.py": { content: file("en", "bf/algo/bellman_ford_elist.py") },
        "bellman_ford_amat.py": { content: file("en", "bf/algo/bellman_ford_amat.py") },
      },
      "generator": {
        "erdos_renyi_0.2.py": { content: file("en", "bf/generator/erdos_renyi_0.2.py") },
        "erdos_renyi_0.8.py": { content: file("en", "bf/generator/erdos_renyi_0.8.py") },
      },
      "input": {
        "input.txt": { content: file("en", "bf/input.txt") },
      }
    },
    mindist: {
      "algo": {
        "dfs_topo_elist.py": { content: file("en", "mindist/algo/dfs_topo_elist.py") },
        "dfs_topo_amat.py": { content: file("en", "mindist/algo/dfs_topo_amat.py") },
        "dijkstra_elist.py": { content: file("en", "dijkstra/algo/dijkstra_elist.py") },
        "dijkstra_amat.py": { content: file("en", "dijkstra/algo/dijkstra_amat.py") },
        "bellman_ford_elist.py": { content: file("en", "bf/algo/bellman_ford_elist.py") },
        "bellman_ford_amat.py": { content: file("en", "bf/algo/bellman_ford_amat.py") },
      },
      "generator": {
        "erdos_renyi_0.2.py": { content: file("en", "mindist/generator/erdos_renyi_0.2.py") },
        "erdos_renyi_0.8.py": { content: file("en", "mindist/generator/erdos_renyi_0.8.py") },
      },
      "input": {
        "input.txt": { content: file("en", "mindist/input.txt") },
      }
    }
  };
}

export function loadDefaultCode() {
  return { version: 36, pages: { hu: loadHu(), en: loadEn() } };
}

export const defaultCode = loadDefaultCode();
