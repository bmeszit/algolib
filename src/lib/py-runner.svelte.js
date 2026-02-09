// src/lib/py-runner.svelte.js
export function createPyRunner() {
  let pyodide = $state(null);
  let isLoading = $state(false);
  let loadError = $state(null);
  let lastRun = $state(null);

  let worker = null;
  let nextId = 1;
  const pending = new Map();

  function failAll(err) {
    const msg = String(err?.message ?? err ?? "Worker error.");
    loadError = msg;

    for (const [, p] of pending) {
      try { p.reject(new Error(msg)); } catch {}
    }
    pending.clear();

    isLoading = false;
    pyodide = null;
  }

  function ensureWorker() {
    if (worker) return worker;

    worker = new Worker(new URL("./py-worker.js", import.meta.url), { type: "module" });

    worker.onmessage = (ev) => {
      const { id, ok, result, error } = ev.data || {};
      const p = pending.get(id);
      if (!p) return;
      pending.delete(id);

      if (ok) p.resolve(result);
      else p.reject(new Error(String(error ?? "Worker error.")));
    };

    worker.onerror = (e) => {
      failAll(e?.message ?? e);
    };

    worker.onmessageerror = (e) => {
      failAll(e?.message ?? e);
    };

    return worker;
  }

  function call(kind, payload) {
    const w = ensureWorker();
    const id = nextId++;
    return new Promise((resolve, reject) => {
      pending.set(id, { resolve, reject });
      w.postMessage({ id, kind, payload });
    });
  }

  async function load() {
    if (pyodide) return pyodide;

    isLoading = true;
    loadError = null;

    try {
      await call("ensure", {});
      pyodide = { kind: "worker" };
      return pyodide;
    } catch (e) {
      failAll(e);
      throw e;
    } finally {
      isLoading = false;
    }
  }

  async function run(code, inputText) {
    await load();
    const m = await call("run", { code: code ?? "", inputText: inputText ?? null });

    const stdout = String(m.stdout ?? "");
    const stderr = String(m.stderr ?? "");
    const timeSec = Number(m.timeSec ?? NaN);
    const memoryBytes = Number(m.memoryBytes ?? NaN);

    const result = stdout || stderr || "";
    lastRun = { result, stdout, stderr, timeSec, memoryBytes };
    return lastRun;
  }

  async function runBenchmark(algoSources, generatorCode) {
    await load();
    const m = await call("benchmark", {
      algoSources: algoSources ?? {},
      generatorCode: generatorCode ?? ""
    });

    const inputSizes = Array.isArray(m.inputSizes) ? m.inputSizes.map((x) => Number(x)) : [];
    const timeSec = m.timeSec ?? {};
    const memoryBytes = m.memoryBytes ?? {};
    const stderr = String(m.stderr ?? "");

    lastRun = { inputSizes, timeSec, memoryBytes, stderr };
    return lastRun;
  }

  return {
    get pyodide() { return pyodide; },
    get isLoading() { return isLoading; },
    get loadError() { return loadError; },
    get lastRun() { return lastRun; },
    ensurePyodide: load,
    run,
    runBenchmark
  };
}
