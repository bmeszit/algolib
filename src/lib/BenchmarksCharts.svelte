<script>
  import { browser } from "$app/environment";
  import { t } from "svelte-i18n";

  let { bench } = $props();

  let Bar = $state(null);
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
        CategoryScale,
        LinearScale,
        BarElement,
        Tooltip,
        Legend,
        Title
      } = chartjs;

      ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend, Title);

      Bar = svelteChart.Bar;
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
    labels: inputSizes.map(x => String(x)),
    datasets: algoNames.map((name, i) => ({
      label: name,
      data: inputSizes.map((x, j) => Number(bench?.timeSec?.[name]?.[j] ?? NaN)),
      backgroundColor: colorForIndex(i),
      borderColor: colorForIndex(i)
    }))
  }));

  let memData = $derived.by(() => ({
    labels: inputSizes.map(x => String(x)),
    datasets: algoNames.map((name, i) => ({
      label: name,
      data: inputSizes.map((x, j) => Number(bench?.memoryBytes?.[name]?.[j] ?? NaN)),
      backgroundColor: colorForIndex(i),
      borderColor: colorForIndex(i)
    }))
  }));

  let baseOptions = $derived.by(() => ({
    responsive: true,
    maintainAspectRatio: false,
    devicePixelRatio: dpr,
    plugins: { 
      legend: { 
        position: "bottom",
        labels: {
          font: { size: 18 }
        }
      }
    },
    scales: {
      x: { 
        title: { 
          display: true, 
          text: $t("benchmarks.axes.x_input_size_chars"),
          font: { size: 18 }
        },
        ticks: {
          font: { size: 16 }
        }
      }
    }
  }));

  let timeOptions = $derived.by(() => ({
    ...baseOptions,
    plugins: { 
      ...baseOptions.plugins, 
      title: { 
        display: true, 
        text: $t("benchmarks.charts.time_title") + ": " + bench.generatorName,
        font: { size: 20 }
      } 
    },
    scales: {
      ...baseOptions.scales,
      y: { 
        title: { 
          display: true, 
          text: $t("benchmarks.axes.y_time_sec"),
          font: { size: 18 }
        },
        ticks: {
          font: { size: 16 }
        }
      } 
    }
  }));

  let memOptions = $derived.by(() => ({
    ...baseOptions,
    plugins: { 
      ...baseOptions.plugins, 
      title: { 
        display: true, 
        text: $t("benchmarks.charts.memory_title") + ": " + bench.generatorName,
        font: { size: 20 }
      } 
    },
    scales: {
      ...baseOptions.scales,
      y: { 
        title: { 
          display: true, 
          text: $t("benchmarks.axes.y_memory_bytes"),
          font: { size: 18 }
        },
        ticks: {
          font: { size: 16 }
        }
      }
    }
  }));

  let stderrText = $derived.by(() => String(bench?.stderr ?? "").trim());
</script>

{#if ready && bench && Bar}
  {#if stderrText !== ""}
    <pre class="err">{$t("benchmarks.errors.stderr_title")}:<br><br>{stderrText}</pre>
  {/if}

  {#key redrawKey}
    <div class="charts">
      <div class="chartBox">
        <Bar bind:this={timeCmp} data={timeData} options={timeOptions} />
      </div>

      <div class="chartBox">
        <Bar bind:this={memCmp} data={memData} options={memOptions} />
      </div>
    </div>
  {/key}
{/if}

<style>
  .charts {
    display: grid;
    gap: 16px;
  }

  .chartBox {
    position: relative;
    height: 520px;
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
