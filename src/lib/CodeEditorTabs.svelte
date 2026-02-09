<script>
  import { tick } from "svelte";
  import { t } from "svelte-i18n";
  import CodeEditor from "./CodeEditor.svelte";

  let { pageId, type, repo, activeCode = $bindable("") } = $props();

  let active = $state("");

  let renaming = $state("");
  let renameValue = $state("");
  let renameEl = $state(null);

  let tabs = $derived(repo.list(pageId, type));
  let content = $derived(active ? repo.get(pageId, type, active) : "");

  $effect(() => {
    if (tabs.length === 0) {
      active = "";
      renaming = "";
      return;
    }
    if (active === "" || !tabs.includes(active)) active = tabs[0];
    if (renaming && !tabs.includes(renaming)) renaming = "";
  });

  $effect(() => { activeCode = active; });

  function nextNewName() {
    let i = 1;
    for (;;) {
      const name = `new${i}.py`;
      if (!tabs.includes(name)) return name;
      i += 1;
    }
  }

  function addFile() {
    const name = nextNewName();
    repo.set(pageId, type, name, "");
    active = name;
  }

  function closeFile(name) {
    repo.del(pageId, type, name);
    if (active === name) active = "";
    if (renaming === name) renaming = "";
  }

  function resetPage() {
    repo.reset?.(pageId, type);
    renaming = "";
  }

  function onEdit(next) {
    if (!active) return;
    repo.set(pageId, type, active, next);
  }

  async function beginRename(name) {
    renaming = name;
    renameValue = name;
    await tick();

    const el = renameEl;
    if (!el) return;

    el.focus();

    const text = el.textContent ?? "";
    const pos = text.endsWith(".py") ? text.length - 3 : text.length;

    const sel = window.getSelection();
    if (!sel || !el.firstChild) return;

    const range = document.createRange();
    range.setStart(el.firstChild, pos);
    range.collapse(true);
    sel.removeAllRanges();
    sel.addRange(range);
  }

  function cancelRename() {
    renaming = "";
    renameValue = "";
  }

  function commitRename(next) {
    if (!renaming) return;
    const from = renaming;
    const to = (next ?? renameValue).trim();
    if (to === "" || to === from) {
      cancelRename();
      return;
    }
    const ok = repo.rename?.(pageId, type, from, to);
    if (!ok) return;
    if (active === from) active = to;
    renaming = "";
    renameValue = "";
  }

  function onRenameMenu(e, name) {
    e.preventDefault();
    beginRename(name);
  }
</script>

<div class="wrap">
  <div class="bar">
    <div class="tabs">
      {#each tabs as t (t)}
        <div class="tab" data-active={t === active}>
          {#if renaming === t}
            <span
              class="rename"
              bind:this={renameEl}
              contenteditable
              role="textbox"
              aria-label="Rename file"
              aria-multiline="false"
              tabindex="0"
              spellcheck="false"
              onkeydown={(e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  commitRename(e.currentTarget.textContent ?? "");
                }
                if (e.key === "Escape") {
                  e.preventDefault();
                  cancelRename();
                }
              }}
              onblur={(e) => {
                commitRename(e.currentTarget.textContent ?? "");
              }}
            >
              {renameValue}
            </span>
          {:else}
            <button
              class="tabbtn"
              type="button"
              onclick={() => (active = t)}
              ondblclick={() => beginRename(t)}
              oncontextmenu={(e) => onRenameMenu(e, t)}
            >
              {t}
            </button>
          {/if}
          <button class="close" type="button" aria-label="Close" onclick={() => closeFile(t)}>×</button>
        </div>
      {/each}
      <button class="new" type="button" onclick={addFile}>+ {$t("common.new")}</button>
    </div>
    <button class="reset" type="button" onclick={resetPage} disabled={!repo.reset}>{$t("common.reset")}</button>
  </div>

  <div class="editor">
    {#if active}
      <CodeEditor value={content} onchange={onEdit} />
    {:else}
      <div class="empty">{$t("common.no_file_selected")}</div>
    {/if}
  </div>
</div>

<style lang="scss">
  .wrap {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 8px;
    height: 100%;
    min-height: 0;
  }

  .bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
  }

  @media (max-width: 800px) {
    .bar {
      flex-direction: column;
      align-items: flex-start;
    }

    .reset {
      align-self: flex-start;
    }
  }

  .tabs {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
    min-width: 0;
  }

  .tab {
    display: flex;
    align-items: stretch;
    border: 1px solid #ddd;
    border-radius: 10px;
    overflow: hidden;
  }

  .tab[data-active="true"] { font-size: 18px; font-weight: 700; }

  .tabbtn {
    border: 0;
    background: transparent;
    padding: 6px 10px;
    cursor: pointer;
    max-width: 240px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font: inherit;
    color: inherit;
  }

  .rename {
    border: 0;
    background: transparent;
    padding: 6px 10px;
    cursor: text;
    max-width: 240px;
    outline: none;
    font: inherit;
    color: inherit;
  }

  .close {
    border: 0;
    background: transparent;
    padding: 6px 10px;
    cursor: pointer;
  }

  .new, .reset {
    border: 1px solid #ddd;
    background: transparent;
    padding: 6px 10px;
    border-radius: 10px;
    cursor: pointer;
  }

  .editor {
    flex: 1;
    min-height: 0;
    border: 1px solid #ddd;
    border-radius: 12px;
    overflow: hidden;
  }

  .empty { padding: 12px; opacity: 0.7; }
</style>
