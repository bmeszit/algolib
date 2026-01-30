import RUN_PY from "$lib/code/hepler/run.py?raw";

type PyRunResult = {
  result: string;
  stdout: string;
  stderr: string;
  timeMs: number;
  peakBytes: number;
};

export function createPyRunner() {
  const indexURL = "https://cdn.jsdelivr.net/pyodide/v0.26.1/full/";

  let pyodide = $state<any>(null);
  let isLoading = $state(false);
  let loadError = $state<string | null>(null);
  let last = $state<PyRunResult | null>(null);

  let loadingPromise: Promise<any> | null = null;

  async function ensurePyodide(): Promise<any> {
    if (pyodide) return pyodide;
    if (loadingPromise) return await loadingPromise;

    isLoading = true;
    loadError = null;

    loadingPromise = (async () => {
      try {
        let loadPyodideFn: any = null;

        try {
          const mod: any = await import("pyodide");
          loadPyodideFn = mod?.loadPyodide ?? null;
        } catch {
          // ignore
        }

        if (!loadPyodideFn) {
          const g: any = globalThis as any;
          loadPyodideFn = g?.loadPyodide ?? null;
        }

        if (!loadPyodideFn) {
          throw new Error("Pyodide loader not found. Install `pyodide` or include a script that defines globalThis.loadPyodide.");
        }

        const inst = await loadPyodideFn({ indexURL });
        inst.runPython(RUN_PY);

        pyodide = inst;
        return inst;
      } catch (e: any) {
        loadError = String(e?.message ?? e);
        throw e;
      } finally {
        isLoading = false;
      }
    })();

    return await loadingPromise;
  }

  async function run(code: string, inputText?: string): Promise<PyRunResult> {
    const inst = await ensurePyodide();

    const fn = inst.globals.get("run_user_code_with_metrics");
    const metrics = fn(code, inputText ?? null);

    const stdout = String(metrics.get("stdout") ?? "");
    const stderr = String(metrics.get("stderr") ?? "");
    const timeMs = Number(metrics.get("time_ms") ?? NaN);
    const peakBytes = Number(metrics.get("peak_bytes") ?? NaN);

    try {
      metrics.destroy?.();
    } catch {
      // ignore
    }

    const result = stdout.length > 0 ? stdout : stderr;

    last = { result, stdout, stderr, timeMs, peakBytes };
    return last;
  }

  return {
    get pyodide() { return pyodide; },
    get isLoading() { return isLoading; },
    get loadError() { return loadError; },
    get last() { return last; },
    ensurePyodide,
    run,
  };
}
