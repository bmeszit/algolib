// src/lib/py-worker.js
import RUN_PY from "./code/helper/run.py?raw";

const indexURL = "https://cdn.jsdelivr.net/pyodide/v0.29.1/full/";

let pyodide = null;
let loading = null;

async function ensurePyodide() {
  if (pyodide) return pyodide;
  if (loading) return await loading;

  loading = (async () => {
    const mod = await import("pyodide");
    const inst = await mod.loadPyodide({ indexURL });
    inst.runPython(RUN_PY);
    pyodide = inst;
    return inst;
  })();

  return await loading;
}

self.onmessage = async (ev) => {
  const { id, kind, payload } = ev.data || {};

  try {
    const inst = await ensurePyodide();

    if (kind === "ensure") {
      self.postMessage({ id, ok: true, result: true });
      return;
    }

    if (kind === "run") {
      const pyFn = inst.globals.get("run_user_code_with_metrics");
      const m = pyFn.call(null, payload.code ?? "", payload.inputText ?? null, false);

      const res = {
        stdout: String(m.get("stdout") ?? ""),
        stderr: String(m.get("stderr") ?? ""),
        timeSec: Number(m.get("time_sec") ?? NaN),
        memoryBytes: Number(m.get("memory_bytes") ?? NaN),
      };

      try { m?.destroy?.(); } catch {}
      try { pyFn?.destroy?.(); } catch {}

      self.postMessage({ id, ok: true, result: res });
      return;
    }

    if (kind === "benchmark") {
      const pyFn = inst.globals.get("run_benchmark_with_metrics");
      const algoSourcesPy = inst.toPy(payload.algoSources ?? {});
      const m = pyFn.call(null, algoSourcesPy, payload.generatorCode ?? "", false);

      const raw = m.toJs({ dict_converter: Object.fromEntries });

      const res = {
        inputSizes: Array.isArray(raw.input_sizes) ? raw.input_sizes.map((x) => Number(x)) : [],
        timeSec: raw.time_sec ?? {},
        memoryBytes: raw.memory_bytes ?? {},
        stderr: String(raw.stderr ?? ""),
      };

      try { m?.destroy?.(); } catch {}
      try { algoSourcesPy?.destroy?.(); } catch {}
      try { pyFn?.destroy?.(); } catch {}

      self.postMessage({ id, ok: true, result: res });
      return;
    }

    throw new Error(`Unknown kind: ${String(kind)}`);
  } catch (e) {
    self.postMessage({ id, ok: false, error: String(e?.message ?? e) });
  }
};
