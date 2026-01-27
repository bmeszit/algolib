<!-- CodeEditorTabs.svelte (Svelte 5) -->
<script lang="ts">
  import CodeEditor from "./CodeEditor.svelte"

  type PageId = string;
  type Filename = string;

  type Repo = {
    list: (pageId: PageId) => Filename[]
    get: (pageId: PageId, filename: Filename) => string
    set: (pageId: PageId, filename: Filename, content: string) => void
    del: (pageId: PageId, filename: Filename) => void
    reset?: (pageId: PageId) => void
  };

  type Props = {
    pageId: PageId
    repo: Repo
    showReset?: boolean
  };

  const { pageId, repo, showReset = true } = $props() as Props;

  let tabs = $state<Filename[]>([]);
  let active = $state<Filename>("");
  let nextId = $state<number>(1);
  let menuOpen = $state<boolean>(false);

  $effect(() => {
    tabs = repo.list(pageId);
    if (tabs.length === 0) {
      active = "";
      menuOpen = false;
      return;
    }
    if (active === "" || !tabs.includes(active)) active = tabs[0];
  })

  let content = $derived(active ? repo.get(pageId, active) : "");

  function addTab(): void {
    let name: Filename
    for (;;) {
      name = `new${nextId}.py`
      nextId += 1
      if (!tabs.includes(name)) break;
    }
    repo.get(pageId, name);
    active = name;
    menuOpen = false;
  }

  function closeTab(filename: Filename): void {
    repo.del(pageId, filename);
    if (active === filename) active = "";
  }

  function pick(filename: Filename): void {
    active = filename;
    menuOpen = false;
  }

  function onEdit(next: string): void {
    if (!active) return;
    repo.set(pageId, active, next);
  }

  function resetPage(): void {
    if (!repo.reset) return;
    repo.reset(pageId);
    menuOpen = false;
  }
</script>

<div class="wrap">
  <div class="bar">
    <div class="mobile">
      <div class="title" title={active || ""}>{active || "No file"}</div>
      <button
        class="hamb"
        type="button"
        aria-label="Menu"
        aria-expanded={menuOpen}
        on:click={() => (menuOpen = !menuOpen)}
      >
        ☰
      </button>
    </div>

    <div class="tabs">
      {#each tabs as t (t)}
        <div class="tab" data-active={t === active}>
          <button class="tabbtn" type="button" on:click={() => (active = t)}>
            {t}
          </button>
          <button class="close" type="button" aria-label="Close" on:click={() => closeTab(t)}>
            ×
          </button>
        </div>
      {/each}
      <button class="new" type="button" on:click={addTab}>+ New</button>
    </div>

    {#if showReset && repo.reset}
      <button class="reset" type="button" on:click={resetPage}>Reset</button>
    {/if}
  </div>

  {#if menuOpen}
    <div class="menu" role="dialog" aria-label="Files">
      <div class="menuHead">
        <div class="menuTitle">Files</div>
        <button class="x" type="button" aria-label="Close" on:click={() => (menuOpen = false)}>×</button>
      </div>

      <div class="menuList">
        {#each tabs as t (t)}
          <div class="row" data-active={t === active}>
            <button class="pick" type="button" on:click={() => pick(t)}>
              {t}
            </button>
            <button class="close" type="button" aria-label="Close" on:click={() => closeTab(t)}>
              ×
            </button>
          </div>
        {/each}
      </div>

      <div class="menuActions">
        <button class="new" type="button" on:click={addTab}>+ New</button>
        {#if showReset && repo.reset}
          <button class="reset" type="button" on:click={resetPage}>Reset</button>
        {/if}
      </div>
    </div>
    <button class="backdrop" type="button" aria-label="Close" on:click={() => (menuOpen = false)}></button>
  {/if}

  <div class="editor">
    {#if active}
      <CodeEditor value={content} onChange={onEdit} />
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

  .hamb {
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

  .tab[data-active="true"] {
    background: #eee;
  }

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
    background: rgba(0,0,0,0.2);
    border: 0;
  }

  .editor {
    flex: 1;
    min-height: 0;
    border: 1px solid #ddd;
    border-radius: 12px;
    overflow: hidden;
  }

  .empty {
    padding: 12px;
    opacity: 0.7;
  }

  @media (max-width: 640px) {
    .tabs { display: none; }
    .mobile { display: flex; }
    .bar { position: relative; }
  }
</style>
