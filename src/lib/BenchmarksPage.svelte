<script>
  import { t } from "svelte-i18n";
  import { CodeEditorTabs } from "$lib";
  import { getContext } from "svelte";
  import { goto } from "$app/navigation";
  import { base } from "$app/paths";
  import { page as appPage } from "$app/state";
  import { getPyRunner } from "$lib/py-runner.svelte.js";
  import BenchmarksCharts from "$lib/BenchmarksCharts.svelte";
  import { getBenchState, setBenchState } from "$lib/bench-cache.js";

  let { page } = $props();
  const pageId = $derived.by(() => page);
  const codeRepo = getContext("codeRepo");
  const pyRunner = getPyRunner();

  // Get initial values from cache based on pageId
  const cachedState = $derived.by(() => getBenchState(pageId));
  let activeGenerator = $state(cachedState?.activeGenerator ?? "");
  let bench = $state(cachedState?.bench ?? null);
  let isRunning = $state(false);

  // Restore from cache when pageId changes
  $effect(() => {
    const init = getBenchState(pageId);
    if (init) {
      activeGenerator = init.activeGenerator ?? "";
      bench = init.bench ?? null;
    }
  });

  // Save to cache when state changes
  $effect(() => {
    setBenchState(pageId, { activeGenerator, bench });
  });

  let generatorSource = $derived.by(() =>
    activeGenerator ? codeRepo.get(pageId, "generator", activeGenerator) : "",
  );
  let algoFiles = $derived.by(() => codeRepo.list(pageId, "algo"));
  let algoSources = $derived.by(() => {
    const res = {};
    for (const f of algoFiles) {
      res[f] = codeRepo.get(pageId, "algo", f);
    }
    return res;
  });

  function goBack() {
    goto(`${base}/${pageId}${appPage.url.search}`);
  }

  async function runBenchmark() {
    if (!generatorSource) return;
    isRunning = true;
    bench = null;
    try {
      bench = await pyRunner.runBenchmark(
        algoSources,
        activeGenerator,
        generatorSource,
      );
    } catch (e) {
      bench = {
        generatorName: "",
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
      <h1>{$t("common.benchmarks")}: {$t(`algos.${pageId}.title`)}</h1>
      <button type="button" class="backBtn" onclick={goBack}>
        {$t("common.back")}
      </button>
    </div>
  </header>
  <p>{$t(`algos.${pageId}.desc`)}</p>
  <div class="editor-section">
    <CodeEditorTabs
      {pageId}
      type="generator"
      repo={codeRepo}
      bind:activeCode={activeGenerator}
    />
  </div>
  <div class="run">
    <button
      type="button"
      onclick={runBenchmark}
      disabled={!activeGenerator ||
        algoFiles.length === 0 ||
        isRunning ||
        pyRunner.isLoading}
      title={activeGenerator
        ? `${$t("common.run")} ${activeGenerator}`
        : $t("common.select_a_file_to_run")}
    >
      {pyRunner.isLoading
        ? $t("common.loading_python")
        : isRunning
          ? $t("common.running")
          : $t("common.run")}
    </button>
    {#if pyRunner.loadError}
      <div class="err">{pyRunner.loadError}</div>
    {/if}
    <BenchmarksCharts {bench} />
  </div>
</article>

<style lang="scss">
  .headRow {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }
  .headRow h1 {
    min-width: 0;
    flex: 1 1 auto;
    overflow-wrap: anywhere;
    hyphens: auto;
  }
  @media (max-width: 800px) {
    .headRow {
      flex-direction: column;
      align-items: flex-start;
    }
    .backBtn {
      align-self: flex-start;
    }
  }
  .backBtn {
    flex: 0 0 auto;
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
