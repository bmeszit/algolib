<script>
  import { browser } from "$app/environment";

  let { bench } = $props();

  let Scatter = $state(null);
  let ready = $state(false);

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
    })();
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

  const baseOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: "bottom" } },
    scales: {
      x: { type: "linear", title: { display: true, text: "input size (chars)" } },
    },
  };

  const timeOptions = {
    ...baseOptions,
    plugins: { ...baseOptions.plugins, title: { display: true, text: "time (sec)" } },
    scales: { ...baseOptions.scales, y: { title: { display: true, text: "time (sec)" } } },
  };

  const memOptions = {
    ...baseOptions,
    plugins: { ...baseOptions.plugins, title: { display: true, text: "memory (bytes)" } },
    scales: { ...baseOptions.scales, y: { title: { display: true, text: "memory (bytes)" } } },
  };
</script>

{#if ready && bench && Scatter}
  <div class="charts">
    <div class="chartBox">
      <Scatter data={timeData} options={timeOptions} />
    </div>

    <div class="chartBox">
      <Scatter data={memData} options={memOptions} />
    </div>
  </div>

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
