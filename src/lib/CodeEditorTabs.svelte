<script lang="ts">

  import { tick } from "svelte";
  import CodeEditor from "./CodeEditor.svelte";

  const { pageId, repo } = $props();

  let active = $state<string>("");
  let menuOpen = $state<boolean>(false);

  let renaming = $state<string>("");
  let renameValue = $state<string>("");
  let renameEl = $state<HTMLElement | null>(null);

  let tabs = $derived(repo.list(pageId));
  let content = $derived(active ? repo.get(pageId, active) : "");

  $effect(() => {
    if (tabs.length === 0) {
      active = "";
      menuOpen = false;
      renaming = "";
      return;
    }
    if (active === "" || !tabs.includes(active)) active = tabs[0];
    if (renaming && !tabs.includes(renaming)) renaming = "";
  });

  function nextNewName(): string {
    let i = 1;
    for (;;) {
      const name = `new${i}.py`;
      if (!tabs.includes(name)) return name;
      i += 1;
    }
  }

  function addFile(): void {
    const name = nextNewName();
    repo.get(pageId, name);
    active = name;
    menuOpen = false;
  }

  function closeFile(name: string): void {
    repo.del(pageId, name);
    if (active === name) active = "";
    if (renaming === name) renaming = "";
  }

  function resetPage(): void {
    repo.reset?.(pageId);
    menuOpen = false;
    renaming = "";
  }

  function onEdit(next: string): void {
    if (!active) return;
    repo.set(pageId, active, next);
  }

  async function beginRename(name: string): Promise<void> {
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

  function cancelRename(): void {
    renaming = "";
    renameValue = "";
  }

  function commitRename(next?: string): void {
    if (!renaming) return;
    const from = renaming;
    const to = (next ?? renameValue).trim();
    if (to === "" || to === from) {
      cancelRename();
      return;
    }
    const ok = repo.rename?.(pageId, from, to);
    if (!ok) return;
    if (active === from) active = to;
    renaming = "";
    renameValue = "";
  }

  function onRenameMenu(e: MouseEvent, name: string): void {
    e.preventDefault();
    beginRename(name);
  }
</script>

<div class="wrap">
  <div class="bar">
    <div class="mobile">
      <div class="title" title={active || ""}>{active || "No file"}</div>
      <button class="hamb" type="button" aria-label="Menu" onclick={() => (menuOpen = !menuOpen)}>☰</button>
    </div>

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
              const el = e.currentTarget as HTMLSpanElement;
              if (e.key === "Enter") {
                e.preventDefault();
                commitRename(el.textContent ?? "");
              }
              if (e.key === "Escape") {
                e.preventDefault();
                cancelRename();
              }
            }}
            onblur={(e) => {
              const el = e.currentTarget as HTMLSpanElement;
              commitRename(el.textContent ?? "");
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
      <button class="new" type="button" onclick={addFile}>+ New</button>
    </div>
  </div>

  {#if menuOpen}
    <div class="menu" role="dialog" aria-label="Files">
      <div class="menuHead">
        <div class="menuTitle">Files</div>
        <button class="x" type="button" aria-label="Close" onclick={() => (menuOpen = false)}>×</button>
      </div>

      <div class="menuList">
        {#each tabs as t (t)}
          <div class="row" data-active={t === active}>
            {#if renaming === t}
              <input
                class="rename pick"
                value={renameValue}
                autofocus
                oninput={(e) => (renameValue = (e.currentTarget as HTMLInputElement).value)}
                onkeydown={(e) => {
                  if (e.key === "Enter") commitRename();
                  if (e.key === "Escape") cancelRename();
                }}
                onblur={commitRename}
              />
            {:else}
              <button
                class="pick"
                type="button"
                onclick={() => (active = t, menuOpen = false)}
                ondblclick={() => beginRename(t)}
                oncontextmenu={(e) => onRenameMenu(e, t)}
              >
                {t}
              </button>
            {/if}
            <button class="close" type="button" aria-label="Close" onclick={() => closeFile(t)}>×</button>
          </div>
        {/each}
      </div>

      <div class="menuActions">
        <button class="new" type="button" onclick={addFile}>+ New</button>
        <button class="reset" type="button" onclick={resetPage} disabled={!repo.reset}>Reset</button>
      </div>
    </div>
    <button class="backdrop" type="button" aria-label="Close" onclick={() => (menuOpen = false)}></button>
  {/if}

  <div class="editor">
    {#if active}
      <CodeEditor value={content} onchange={onEdit} />
    {:else}
      <div class="empty">No file selected.</div>
    {/if}
  </div>
</div>

<style>
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

  .mobile {
    display: none;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    min-width: 0;
    flex: 1;
  }

  .title {
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-weight: 600;
  }

  .hamb, .new, .reset {
    border: 1px solid #ddd;
    background: transparent;
    padding: 6px 10px;
    border-radius: 10px;
    cursor: pointer;
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

  .tab[data-active="true"] { background: #eee; }

  .tabbtn {
    border: 0;
    background: transparent;
    padding: 6px 10px;
    cursor: pointer;
    max-width: 240px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
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

  .menu {
    position: absolute;
    top: 10px;
    left: 10px;
    right: 10px;
    z-index: 20;
    border: 1px solid #ddd;
    background: white;
    border-radius: 12px;
    overflow: hidden;
  }

  .menuHead {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 12px;
    border-bottom: 1px solid #eee;
  }

  .menuTitle { font-weight: 600; }

  .x {
    border: 0;
    background: transparent;
    padding: 6px 10px;
    cursor: pointer;
  }

  .menuList {
    max-height: 55vh;
    overflow: auto;
    -webkit-overflow-scrolling: touch;
  }

  .row {
    display: flex;
    align-items: stretch;
    border-top: 1px solid #eee;
  }

  .row[data-active="true"] { background: #eee; }

  .pick {
    border: 0;
    background: transparent;
    padding: 10px 12px;
    cursor: pointer;
    flex: 1;
    text-align: left;
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .menuActions {
    display: flex;
    gap: 8px;
    padding: 10px 12px;
    border-top: 1px solid #eee;
  }

  .backdrop {
    position: fixed;
    inset: 0;
    z-index: 10;
    background: rgba(0, 0, 0, 0.2);
    border: 0;
  }

  .editor {
    flex: 1;
    min-height: 0;
    border: 1px solid #ddd;
    border-radius: 12px;
    overflow: hidden;
  }

  .empty { padding: 12px; opacity: 0.7; }

  @media (max-width: 640px) {
    .tabs { display: none; }
    .mobile { display: flex; }
  }
</style>
