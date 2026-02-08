<script>
  import { t } from "svelte-i18n";
  import { CodeEditorTabs } from "$lib";
  import { getContext } from "svelte";
  import { createPyRunner } from "$lib/py-runner.svelte.js";

  const codeRepo = getContext("codeRepo");
  const pyRunner = createPyRunner();

  let activeFile = $state("");
  let outputText = $state("");
  let isRunning = $state(false);

  let activeSource = $derived(activeFile ? codeRepo.get("sort", activeFile) : "");

  let debugOn = $state(true);

  async function runActive() {
    if (!activeSource) return;

    isRunning = true;
    outputText = "";

    try {
      const res = await pyRunner.run(activeSource, null, debugOn);
      outputText =
        `stdout:\n${res.stdout || "(empty)"}\n\n` +
        `stderr:\n${res.stderr || "(empty)"}\n\n` +
        `timeMs: ${res.timeMs}\n` +
        `peakBytes: ${res.peakBytes}\n`;
    } catch (e) {
      outputText = String(e?.message ?? e);
    } finally {
      isRunning = false;
    }
  }
</script>

<article>
  <header class="page-header">
    <h1>{$t("algos.sort.title")}</h1>
  </header>

  <p>{$t("algos.sort.desc")}</p>

  <div class="editor-section">
    <CodeEditorTabs pageId="sort" repo={codeRepo} bind:activeCode={activeFile} />
  </div>

  <div class="run">
    <button
      type="button"
      onclick={runActive}
      disabled={!activeFile || isRunning || pyRunner.isLoading}
      title={activeFile ? `Run ${activeFile}` : "Select a file to run"}
    >
      {pyRunner.isLoading ? "Loading Python…" : isRunning ? "Running…" : "Run"}
    </button>

    {#if pyRunner.loadError}
      <div class="err">{pyRunner.loadError}</div>
    {/if}

    <div class="out">{outputText}</div>
  </div>
</article>

<style lang="scss">
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
