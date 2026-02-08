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
  let inputText = $state("");

  async function runActive() {
    if (!activeSource) return;
    isRunning = true;
    outputText = "";
    try {
      outputText = await pyRunner.runAndFormat(activeSource, inputText, debugOn);
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
    <label class="inLabel">
      <span>{$t("common.input")}</span>
      <textarea
        class="inBox"
        rows="3"
        value={inputText}
        oninput={(e) => (inputText = e.currentTarget.value)}
        spellcheck="false"
      ></textarea>
    </label>

    <button
      type="button"
      onclick={runActive}
      disabled={!activeFile || isRunning || pyRunner.isLoading}
      title={activeFile ? `$t("common.run") ${activeFile}` : $t("common.select_a_file_to_run")}
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
