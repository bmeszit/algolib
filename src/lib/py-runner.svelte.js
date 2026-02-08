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

  function formatBenchmark(res) {
    const sizes = (res.inputSizes ?? []).map((x) => String(x)).join(", ");
    const algoNames = Object.keys(res.timeSec ?? {});

    let s = "";
    s += `input_sizes (chars): [${sizes}]\n`;

    for (const name of algoNames) {
      const ts = (res.timeSec?.[name] ?? []).map((x) => String(x)).join(", ");
      const ms = (res.memoryBytes?.[name] ?? []).map((x) => String(x)).join(", ");
      s += `\n${name}\n`;
      s += `  time_sec: [${ts}]\n`;
      s += `  memory_bytes: [${ms}]\n`;
    }

    const err = String(res.stderr ?? "");
    if (err.trim() !== "") {
      s += `\nerrors:\n\n${err}\n`;
    }

    return s;
  }

  async function run(code, inputText) {
    const debug = false;
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

  async function runAndFormat(code, inputText) {
    const res = await run(code, inputText);
    return format(res);
  }

  async function runBenchmark(algoSources, generatorCode) {
    const debug = false;
    const inst = await load();

    const pyFn = inst.globals.get("run_benchmark_with_metrics");
    if (!pyFn || typeof pyFn.call !== "function") {
      throw new Error("run_benchmark_with_metrics is missing or not callable.");
    }

    let metrics = null;
    let algoSourcesPy = null;

    try {
      algoSourcesPy = inst.toPy(algoSources ?? {});
      metrics = pyFn.call(null, algoSourcesPy, generatorCode ?? "", Boolean(debug));

      const raw = metrics.toJs({ dict_converter: Object.fromEntries });

      const inputSizes = Array.isArray(raw.input_sizes) ? raw.input_sizes.map((x) => Number(x)) : [];
      const timeSec = raw.time_sec ?? {};
      const memoryBytes = raw.memory_bytes ?? {};
      const stderr = String(raw.stderr ?? "");

      lastRun = { inputSizes, timeSec, memoryBytes, stderr };
      return lastRun;
    } finally {
      try { metrics?.destroy?.(); } catch {}
      try { algoSourcesPy?.destroy?.(); } catch {}
      try { pyFn?.destroy?.(); } catch {}
    }
  }

  async function runBenchmarkAndFormat(algoSources, generatorCode) {
    const res = await runBenchmark(algoSources, generatorCode);
    return formatBenchmark(res);
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
    runBenchmark,
    formatBenchmark,
    runBenchmarkAndFormat,
  };
}
