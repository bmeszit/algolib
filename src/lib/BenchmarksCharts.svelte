<script>
  import { browser } from "$app/environment";

  let { bench } = $props();

  let Scatter = $state(null);
  let ready = $state(false);

  let timeCmp = $state(null);
  let memCmp = $state(null);

  let dpr = $state(1);
  let redrawKey = $state(0);

  $effect(() => {
    if (!browser || ready) return;

    (async () => {
      const chartjs = await import("chart.js");
      const svelteChart = await import("svelte5-chartjs");

      const {
        Chart: ChartJS,
        LinearScale,
        PointElement,
        LineElement,
        Tooltip,
        Legend,
        Title,
      } = chartjs;

      ChartJS.register(LinearScale, PointElement, LineElement, Tooltip, Legend, Title);

      Scatter = svelteChart.Scatter;
      ready = true;
      dpr = window.devicePixelRatio || 1;
    })();
  });

  $effect(() => {
    if (!browser || !ready) return;

    let raf = 0;

    const sync = () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        dpr = window.devicePixelRatio || 1;

        timeCmp?.chart?.resize?.();
        timeCmp?.chart?.update?.("none");

        memCmp?.chart?.resize?.();
        memCmp?.chart?.update?.("none");

        redrawKey += 1;
      });
    };

    const vv = window.visualViewport;

    window.addEventListener("resize", sync, { passive: true });
    vv?.addEventListener("resize", sync, { passive: true });

    return () => {
      window.removeEventListener("resize", sync);
      vv?.removeEventListener("resize", sync);
      cancelAnimationFrame(raf);
    };
  });

  function colorForIndex(i) {
    return `hsl(${(i * 53) % 360} 70% 45%)`;
  }

  let inputSizes = $derived.by(() => bench?.inputSizes ?? []);
  let algoNames = $derived.by(() => Object.keys(bench?.timeSec ?? {}).sort());

  let timeData = $derived.by(() => ({
    datasets: algoNames.map((name, i) => ({
      label: name,
      data: inputSizes.map((x, j) => ({ x, y: Number(bench?.timeSec?.[name]?.[j] ?? NaN) })),
      backgroundColor: colorForIndex(i),
      borderColor: colorForIndex(i),
      showLine: false,
      pointRadius: 3,
    })),
  }));

  let memData = $derived.by(() => ({
    datasets: algoNames.map((name, i) => ({
      label: name,
      data: inputSizes.map((x, j) => ({ x, y: Number(bench?.memoryBytes?.[name]?.[j] ?? NaN) })),
      backgroundColor: colorForIndex(i),
      borderColor: colorForIndex(i),
      showLine: false,
      pointRadius: 3,
    })),
  }));

  let baseOptions = $derived.by(() => ({
    responsive: true,
    maintainAspectRatio: false,
    devicePixelRatio: dpr,
    plugins: { legend: { position: "bottom" } },
    scales: {
      x: { type: "linear", title: { display: true, text: "input size (chars)" } },
    },
  }));

  let timeOptions = $derived.by(() => ({
    ...baseOptions,
    plugins: { ...baseOptions.plugins, title: { display: true, text: "time (sec)" } },
    scales: { ...baseOptions.scales, y: { title: { display: true, text: "time (sec)" } } },
  }));

  let memOptions = $derived.by(() => ({
    ...baseOptions,
    plugins: { ...baseOptions.plugins, title: { display: true, text: "memory (bytes)" } },
    scales: { ...baseOptions.scales, y: { title: { display: true, text: "memory (bytes)" } } },
  }));
</script>

{#if ready && bench && Scatter}
  {#key redrawKey}
    <div class="charts">
      <div class="chartBox">
        <Scatter bind:this={timeCmp} data={timeData} options={timeOptions} />
      </div>

      <div class="chartBox">
        <Scatter bind:this={memCmp} data={memData} options={memOptions} />
      </div>
    </div>
  {/key}

  {#if (bench?.stderr ?? "").trim() !== ""}
    <pre class="err">{bench.stderr}</pre>
  {/if}
{/if}

<style>
  .charts {
    display: grid;
    gap: 16px;
  }

  .chartBox {
    position: relative;
    height: 360px;
    border: 1px solid #ddd;
    border-radius: 12px;
    padding: 10px;
    background: #fff;
  }

  .err {
    margin-top: 12px;
    white-space: pre-wrap;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    font-size: 0.95rem;
    border: 1px solid #ddd;
    border-radius: 12px;
    padding: 10px;
    min-height: 44px;
  }
</style>
