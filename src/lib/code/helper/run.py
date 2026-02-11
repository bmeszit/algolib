import sys, io, traceback, time, tracemalloc

_measure_time_start = None
_measure_time_end = None
_measure_mem_peak = None

def _reset_measurement():
  global _measure_time_start, _measure_time_end, _measure_mem_peak
  _measure_time_start = None
  _measure_time_end = None
  _measure_mem_peak = None

def _measure_start_hook():
  global _measure_time_start
  _measure_time_start = time.perf_counter()
  tracemalloc.stop()
  tracemalloc.start()

def _measure_stop_hook():
  global _measure_time_end, _measure_mem_peak
  memory_current, memory_peak = tracemalloc.get_traced_memory()
  _measure_time_end = time.perf_counter()
  _measure_mem_peak = memory_peak

def run_user_code_with_metrics(code: str, stdin_text: str | None, debug: bool = False, *, label: str = "<user_code>"):
  _reset_measurement()
  code_obj = compile(code or "", label, "exec")

  old_stdin, old_stdout, old_stderr = sys.stdin, sys.stdout, sys.stderr
  sys.stdin = io.StringIO(stdin_text or "")
  out = io.StringIO()
  err = io.StringIO()
  sys.stdout = out
  sys.stderr = err

  if debug:
    err.write(f"[dbg] code_len={len(code or '')} stdin_len={len(stdin_text or '')}\n")

  env = {
    "__name__": "__main__",
    "MEASURE_START": _measure_start_hook,
    "MEASURE_STOP": _measure_stop_hook,
    "MERES_KEZD": _measure_start_hook,
    "MERES_VEG": _measure_stop_hook,
  }

  tracemalloc.start()
  time_start = time.perf_counter()
  try:
      exec(code_obj, env, env)
  except Exception:
      traceback.print_exc()
  time_end = time.perf_counter()
  memory_current, memory_peak = tracemalloc.get_traced_memory()
  tracemalloc.stop()

  sys.stdin, sys.stdout, sys.stderr = old_stdin, old_stdout, old_stderr

  actual_time = (_measure_time_end or time_end) - (_measure_time_start or time_start)
  actual_memory = _measure_mem_peak or memory_peak
  
  return {
    "stdout": out.getvalue(),
    "stderr": err.getvalue(),
    "time_sec": actual_time,
    "memory_bytes": actual_memory,
  }

_inputs = []

def _reset_inputs():
  _inputs.clear()

def _inputs_hook(input: str):
  global _inputs_storage
  _inputs.append(input)

def load_generator_inputs(generator_src: str):
  _reset_inputs()
  code_obj = compile(generator_src or "", "<generator>", "exec")
  
  env = {
    "__name__": "__main__",
    "INPUT": _inputs_hook,
    "BEMENET": _inputs_hook,
  }

  exec(code_obj, env, env)

  if len(_inputs) == 0:
    raise RuntimeError("Generator must call INPUT() or BEMENET() for every input str.")

  return _inputs

def run_benchmark_with_metrics(algo_sources: dict, generator_src: str, debug: bool = False):
  inputs = load_generator_inputs(generator_src or "")
  input_sizes = [len(s) for s in inputs]

  time_sec = {}
  memory_bytes = {}
  err_chunks = []

  for name, src in (algo_sources or {}).items():
    if not isinstance(name, str) or not isinstance(src, str):
        raise TypeError("algo_sources must be {str: str}.")

    ts = []
    ms = []

    for i, inp in enumerate(inputs):
      m = run_user_code_with_metrics(src, inp, bool(debug), label=f"<{name}>")
      ts.append(float(m["time_sec"]))
      ms.append(int(m["memory_bytes"]))

      e = m["stderr"] or ""
      if e.strip() != "":
        err_chunks.append(f"[{name}][{i}]\n{e}\n")

    time_sec[name] = ts
    memory_bytes[name] = ms

  return {
    "input_sizes": input_sizes,
    "time_sec": time_sec,
    "memory_bytes": memory_bytes,
    "stderr": "".join(err_chunks),
  }