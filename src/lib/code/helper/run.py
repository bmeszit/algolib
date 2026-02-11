import sys, io, traceback, time, tracemalloc

# Global state for measurement hooks
_measure_active = False
_measure_time_start = None
_measure_time_end = None
_measure_mem_peak = None

def _reset_measurement():
    global _measure_active, _measure_time_start, _measure_time_end, _measure_mem_peak
    _measure_active = False
    _measure_time_start = None
    _measure_time_end = None
    _measure_mem_peak = None

def _measure_start_hook():
    global _measure_active, _measure_time_start
    if not _measure_active:
        _measure_active = True
        _measure_time_start = time.perf_counter()
        
        # RESET peak tracking by stopping and restarting tracemalloc!
        tracemalloc.stop()
        tracemalloc.start()

def _measure_stop_hook():
    global _measure_time_end, _measure_mem_peak
    if _measure_active:
        _measure_time_end = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        _measure_mem_peak = peak  # This is the peak since MEASURE_START

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

    # Inject hook functions into global namespace
    glb = {
        "__name__": "__main__",
        # English hooks
        "MEASURE_START": _measure_start_hook,
        "MEASURE_STOP": _measure_stop_hook,
        # Hungarian hooks (same functions, different names)
        "MERES_KEZD": _measure_start_hook,
        "MERES_VEG": _measure_stop_hook,
    }
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

    # Determine actual measurement times and memory
    if _measure_active and _measure_time_start is not None:
        # Hooks were used - measure only the section between hooks
        actual_time = (_measure_time_end or t1) - _measure_time_start
        
        # Memory: We reset tracemalloc at MEASURE_START(), so the peak
        # at MEASURE_STOP() is the peak since the reset = algorithm's peak!
        actual_memory = _measure_mem_peak if _measure_mem_peak is not None else 0
    else:
        # No hooks used, measure everything
        actual_time = t1 - t0
        actual_memory = peak

    return {
        "stdout": out.getvalue(),
        "stderr": err.getvalue(),
        "time_sec": actual_time,
        "memory_bytes": int(max(0, actual_memory)),
    }

def load_generator_inputs(generator_src: str):
    _inputs_storage = []
    
    # Hook function to capture INPUTS
    def _inputs_hook(inputs_list):
        if not isinstance(inputs_list, list):
            raise TypeError("INPUTS() must be called with a list[str].")
        if any(not isinstance(x, str) for x in inputs_list):
            raise TypeError("INPUTS() must be called with a list[str].")
        if len(inputs_list) == 0:
            raise RuntimeError("INPUTS() called with empty list.")
        _inputs_storage.clear()
        _inputs_storage.extend(inputs_list)
    
    env = {
        "__name__": "__main__",
        "INPUTS": _inputs_hook,  # English hook
        "BEMENETEK": _inputs_hook,  # Hungarian hook
    }
    
    exec(compile(generator_src or "", "<generator>", "exec"), env, env)

    if len(_inputs_storage) == 0:
        raise RuntimeError("Generator must call INPUTS() or BEMENETEK() with a non-empty list.")

    return _inputs_storage

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