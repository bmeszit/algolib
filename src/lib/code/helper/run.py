import sys, io, traceback, time, tracemalloc;

def __run_user_code_with_metrics__(code: str, stdin_text: str | None, debug: bool = False):
  old_stdin, old_stdout, old_stderr = sys.stdin, sys.stdout, sys.stderr;
  sys.stdin = io.StringIO(stdin_text or "");
  out = io.StringIO();
  err = io.StringIO();
  sys.stdout = out;
  sys.stderr = err;

  if debug:
    err.write(f"[dbg] code_len={len(code or '')} stdin_len={len(stdin_text or '')}\n");

  glb = {"__name__": "__main__"};
  loc = glb;

  tracemalloc.start();
  t0 = time.perf_counter();
  try:
    exec(compile(code, "<user_code>", "exec"), glb, loc);
  except Exception:
    traceback.print_exc();
  t1 = time.perf_counter();
  current, peak = tracemalloc.get_traced_memory();
  tracemalloc.stop();

  sys.stdin, sys.stdout, sys.stderr = old_stdin, old_stdout, old_stderr;

  return {
    "stdout": out.getvalue(),
    "stderr": err.getvalue(),
    "time_ms": (t1 - t0) * 1000.0,
    "peak_bytes": int(peak),
  };

run_user_code_with_metrics = __run_user_code_with_metrics__;
