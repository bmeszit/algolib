<!-- CodeEditorTabs.svelte (Svelte 5) -->
<script lang="ts">
  import CodeEditor from "./CodeEditor.svelte"

  export type PageId = string
  export type Filename = string

  export type Repo = {
    list: (pageId: PageId) => Filename[]
    get: (pageId: PageId, filename: Filename) => string // create-if-missing
    set: (pageId: PageId, filename: Filename, content: string) => void
    del: (pageId: PageId, filename: Filename) => void
    reset?: (pageId: PageId) => void
  }

  type Props = {
    pageId: PageId
    repo: Repo
    showReset?: boolean
  }

  const { pageId, repo, showReset = true } = $props() as Props

  let tabs = $state<Filename[]>([])
  let active = $state<Filename>("")
  let nextId = $state<number>(1)

  $effect(() => {
    tabs = repo.list(pageId)
    if (tabs.length === 0) {
      active = ""
      return
    }
    if (active === "" || !tabs.includes(active)) active = tabs[0]
  })

  let content = $derived(active ? repo.get(pageId, active) : "")

  function addTab(): void {
    let name: Filename
    for (;;) {
      name = `new${nextId}.py`
      nextId += 1
      if (!tabs.includes(name)) break
    }
    repo.get(pageId, name) // create-if-missing
    active = name
  }

  function closeTab(filename: Filename): void {
    repo.del(pageId, filename)
    if (active === filename) active = ""
  }

  function onEdit(next: string): void {
    if (!active) return
    repo.set(pageId, active, next)
  }

  function resetPage(): void {
    if (!repo.reset) return
    repo.reset(pageId)
  }
</script>

<div class="wrap">
  <div class="bar">
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
</style>
