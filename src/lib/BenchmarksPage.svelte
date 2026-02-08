<script>
  import { t } from "svelte-i18n";
  import { CodeEditorTabs } from "$lib";
  import { getContext } from "svelte";
  import { goto } from "$app/navigation";
  import { createPyRunner } from "$lib/py-runner.svelte.js";
  import BenchmarksCharts from "$lib/BenchmarksCharts.svelte";

  let { page } = $props();

  const codeRepo = getContext("codeRepo");
  const pyRunner = createPyRunner();

  let activeGenerator = $state("");
  let isRunning = $state(false);

  let bench = $state(null);

  let generatorSource = $derived.by(() => (activeGenerator ? codeRepo.get(page, "generator", activeGenerator) : ""));
  let algoFiles = $derived.by(() => codeRepo.list(page, "algo"));

  let algoSources = $derived.by(() => {
    const res = {};
    for (const f of algoFiles) {
      res[f] = codeRepo.get(page, "algo", f);
    }
    return res;
  });

  function goBack() {
    goto(`/${page}`);
  }

  async function runBenchmark() {
    if (!generatorSource) return;
    isRunning = true;
    bench = null;

    try {
      bench = await pyRunner.runBenchmark(algoSources, generatorSource);
    } catch (e) {
      bench = {
        inputSizes: [],
        timeSec: {},
        memoryBytes: {},
        stderr: String(e?.message ?? e),
      };
    } finally {
      isRunning = false;
    }
  }
</script>

<article>
  <header class="page-header">
    <div class="headRow">
      <h1>{$t("common.benchmarks")}: {$t(`algos.${page}.title`)}</h1>
      <button type="button" class="backBtn" onclick={goBack}>
        {$t("common.back")}
      </button>
    </div>
  </header>

  <p>{$t(`algos.${page}.desc`)}</p>

  <div class="editor-section">
    <CodeEditorTabs pageId={page} type="generator" repo={codeRepo} bind:activeCode={activeGenerator} />
  </div>

  <div class="run">
    <button
      type="button"
      onclick={runBenchmark}
      disabled={!activeGenerator || algoFiles.length === 0 || isRunning || pyRunner.isLoading}
      title={activeGenerator ? `${$t("common.run")} ${activeGenerator}` : $t("common.select_a_file_to_run")}
    >
      {pyRunner.isLoading ? $t("common.loading_python") : isRunning ? $t("common.running") : $t("common.run")}
    </button>

    {#if pyRunner.loadError}
      <div class="err">{pyRunner.loadError}</div>
    {/if}

    <BenchmarksCharts bench={bench} />
  </div>
</article>

<style lang="scss">
  .headRow {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }

  .backBtn {
    border: 1px solid #ddd;
    background: transparent;
    padding: 6px 10px;
    border-radius: 10px;
    cursor: pointer;
  }

  .editor-section {
    margin-bottom: 20px;
  }

  .run {
    display: flex;
    flex-direction: column;
    gap: 10px;

    button {
      align-self: flex-start;
      padding: 6px 12px;
      background: #eee;
      border: 1px solid #ccc;
      border-radius: 8px;
      cursor: pointer;

      &:disabled {
        cursor: default;
        opacity: 0.6;
      }
    }
  }

  .err {
    font-size: 0.9rem;
    opacity: 0.9;
  }
</style>
