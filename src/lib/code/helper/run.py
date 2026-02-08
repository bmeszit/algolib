import sys, io, traceback, time, tracemalloc

def run_user_code_with_metrics(code: str, stdin_text: str | None, debug: bool = False, *, label: str = "<user_code>"):
  code_obj = compile(code or "", label, "exec")

  old_stdin, old_stdout, old_stderr = sys.stdin, sys.stdout, sys.stderr
  sys.stdin = io.StringIO(stdin_text or "")
  out = io.StringIO()
  err = io.StringIO()
  sys.stdout = out
  sys.stderr = err

  if debug:
    err.write(f"[dbg] code_len={len(code or '')} stdin_len={len(stdin_text or '')}\n")

  glb = {"__name__": "__main__"}
  loc = glb

  tracemalloc.start()
  t0 = time.perf_counter()
  try:
    exec(code_obj, glb, loc)
  except Exception:
    traceback.print_exc()
  t1 = time.perf_counter()
  current, peak = tracemalloc.get_traced_memory()
  tracemalloc.stop()

  sys.stdin, sys.stdout, sys.stderr = old_stdin, old_stdout, old_stderr

  return {
    "stdout": out.getvalue(),
    "stderr": err.getvalue(),
    "time_sec": t1 - t0,
    "memory_bytes": int(peak),
  }

def load_generator_inputs(generator_src: str):
  env = {"__name__": "__main__"}
  exec(compile(generator_src or "", "<generator>", "exec"), env, env)

  inputs = env.get("INPUTS", None)
  if not isinstance(inputs, list) or any(not isinstance(x, str) for x in inputs):
    raise TypeError("Generator must define global INPUTS: list[str].")
  if len(inputs) == 0:
    raise RuntimeError("Generator INPUTS is empty.")

  return inputs

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
