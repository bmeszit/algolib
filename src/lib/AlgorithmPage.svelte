<script>
  import { t } from "svelte-i18n";
  import { CodeEditorTabs } from "$lib";
  import { getContext } from "svelte";
  import { goto } from "$app/navigation";
  import { base } from "$app/paths";
  import { page as appPage } from "$app/state";
  import { getPyRunner } from "$lib/py-runner.svelte.js";
  import { getAlgoRunState, setAlgoRunState } from "$lib/algo-cache.js";

  let { page } = $props();
  const pageId = $derived.by(() => page);
  const codeRepo = getContext("codeRepo");
  const pyRunner = getPyRunner();

  const cachedState = $derived.by(() => getAlgoRunState(pageId));

  let activeFile = $state(cachedState?.activeFile ?? "");
  let inputText = $state(cachedState?.inputText ?? "");
  let outputText = $state(cachedState?.outputText ?? "");
  let isRunning = $state(false);
  let isHydrating = $state(false);

  const defaultInput = $derived.by(() => codeRepo.get(pageId, "input", "input.txt") ?? "");
  const activeSource = $derived.by(() => (activeFile ? codeRepo.get(pageId, "algo", activeFile) : ""));

  $effect(() => {
    isHydrating = true;

    const init = getAlgoRunState(pageId);
    if (init) {
      activeFile = init.activeFile ?? "";
      inputText = init.inputText ?? "";
      outputText = init.outputText ?? "";
    } else {
      //activeFile = "";
      inputText = defaultInput;
      outputText = "";
    }

    isHydrating = false;
  });

  $effect(() => {
    if (isHydrating) return;
    setAlgoRunState(pageId, { activeFile, inputText, outputText });
  });

  function goBenchmarks() {
    goto(`${base}/${pageId}/benchmarks${appPage.url.search}`);
  }

  function restoreInput() {
    codeRepo.reset?.(pageId, "input");
    inputText = defaultInput;
    outputText = "";
  }

  function formatRun(res) {
    const stdout = String(res?.stdout ?? "");
    const stderr = String(res?.stderr ?? "");
    const timeSec = Number(res?.timeSec ?? NaN);
    const memoryBytes = Number(res?.memoryBytes ?? NaN);

    let s = "";

    const output = stdout.trim() === "" ? $t("benchmarks.runner.empty") : stdout;
    s += `${$t("benchmarks.runner.stdout_label")}:\n\n${output}\n\n`;

    if (stderr.trim() !== "") {
      s += `${$t("benchmarks.runner.stderr_label")}:\n\n${stderr}\n\n`;
    }

    s += `${$t("benchmarks.runner.time_label")}:\n${timeSec} ${$t("benchmarks.runner.time_unit_sec")}\n\n`;
    s += `${$t("benchmarks.runner.memory_label")}:\n${memoryBytes} ${$t("benchmarks.runner.memory_unit_bytes")}\n`;

    return s;
  }

  async function runActive() {
    if (!activeSource) return;
    isRunning = true;
    outputText = "";
    try {
      const res = await pyRunner.run(activeSource, inputText);
      outputText = formatRun(res);
    } catch (e) {
      outputText = String(e?.message ?? e);
    } finally {
      isRunning = false;
    }
  }
</script>

<article>
  <header class="page-header">
    <div class="headRow">
      <h1>{$t(`algos.${pageId}.title`)}</h1>
      <button type="button" class="benchBtn" onclick={goBenchmarks}>
        {$t("common.benchmarks")}
      </button>
    </div>
  </header>

  <p>{$t(`algos.${pageId}.desc`)}</p>

  <div class="editor-section">
    <CodeEditorTabs {pageId} type="algo" repo={codeRepo} bind:activeCode={activeFile} />
  </div>

  <div class="run">
    <div class="inHead">
      <span>{$t("common.input")}</span>
      <button type="button" class="resetBtn" onclick={restoreInput} disabled={defaultInput.trim() === ""}>
        {$t("common.reset")}
      </button>
    </div>

    <label class="inLabel">
      <textarea
        class="inBox"
        rows="3"
        value={inputText}
        oninput={(e) => {
          inputText = e.currentTarget.value;
        }}
        spellcheck="false"
      ></textarea>
    </label>

    <button
      type="button"
      onclick={runActive}
      disabled={!activeFile || isRunning || pyRunner.isLoading}
      title={activeFile ? `${$t("common.run")} ${activeFile}` : $t("common.select_a_file_to_run")}
    >
      {pyRunner.isLoading ? $t("common.loading_python") : isRunning ? $t("common.running") : $t("common.run")}
    </button>

    {#if pyRunner.loadError}
      <div class="err">{pyRunner.loadError}</div>
    {/if}

    <span>{$t("common.result")}</span>
    <div class="out">{outputText}</div>
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

    .benchBtn {
      align-self: flex-start;
    }
  }

  .benchBtn {
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

  .inHead {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }

  @media (max-width: 800px) {
    .inHead {
      flex-direction: column;
      align-items: flex-start;
    }

    .resetBtn {
      align-self: flex-start;
    }
  }

  .resetBtn {
    border: 1px solid #ddd;
    background: transparent;
    padding: 4px 8px;
    border-radius: 10px;
    cursor: pointer;

    &:disabled {
      cursor: default;
      opacity: 0.6;
    }
  }

  .inLabel {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .inBox {
    background: #eee;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 10px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    font-size: 1rem;
    resize: vertical;
  }

  .err {
    font-size: 0.9rem;
    opacity: 0.9;
  }

  .out {
    white-space: pre-wrap;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    font-size: 0.95rem;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 10px;
    min-height: 44px;
  }
</style>
