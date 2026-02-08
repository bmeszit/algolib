import RUN_PY from "$lib/code/helper/run.py?raw";

export function createPyRunner() {
  const indexURL = "https://cdn.jsdelivr.net/pyodide/v0.29.1/full/";

  let pyodide = $state(null);
  let isLoading = $state(false);
  let loadError = $state(null);
  let lastRun = $state(null);

  let loading = null;

  async function load() {
    if (pyodide) return pyodide;
    if (loading) return await loading;

    isLoading = true;
    loadError = null;

    loading = (async () => {
      try {
        const mod = await import("pyodide").catch(() => null);
        const loadPyodide = mod?.loadPyodide ?? globalThis?.loadPyodide ?? null;
        if (!loadPyodide) throw new Error("Missing Pyodide loader.");

        const inst = await loadPyodide({ indexURL });
        inst.runPython(RUN_PY);
        pyodide = inst;
        return inst;
      } catch (e) {
        loadError = String(e?.message ?? e);
        throw e;
      } finally {
        isLoading = false;
      }
    })();

    return await loading;
  }

  function format(res) {
    return (
      `stdout:\n${res.stdout || "(empty)"}\n\n` +
      `stderr:\n${res.stderr || "(empty)"}\n\n` +
      `time: ${res.timeSec} sec\n` +
      `memory: ${res.memoryBytes} bytes\n`
    );
  }

  async function run(code, inputText, debug = false) {
    const inst = await load();

    const pyFn = inst.globals.get("run_user_code_with_metrics");
    if (!pyFn || typeof pyFn.call !== "function") {
      throw new Error("run_user_code_with_metrics is missing or not callable.");
    }

    let metrics = null;
    try {
      metrics = pyFn.call(null, code ?? "", inputText ?? null, Boolean(debug));

      const stdout = String(metrics.get("stdout") ?? "");
      const stderr = String(metrics.get("stderr") ?? "");
      const timeSec = Number(metrics.get("time_sec") ?? NaN);
      const memoryBytes = Number(metrics.get("memory_bytes") ?? NaN);

      const result = stdout || stderr || "(no output)";
      lastRun = { result, stdout, stderr, timeSec, memoryBytes };
      return lastRun;
    } finally {
      try { metrics?.destroy?.(); } catch {}
      try { pyFn?.destroy?.(); } catch {}
    }
  }

  async function runAndFormat(code, inputText, debug = false) {
    const res = await run(code, inputText, debug);
    return format(res);
  }

  return {
    get pyodide() { return pyodide; },
    get isLoading() { return isLoading; },
    get loadError() { return loadError; },
    get lastRun() { return lastRun; },
    ensurePyodide: load,
    run,
    format,
    runAndFormat,
  };
}
