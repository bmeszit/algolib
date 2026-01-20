<script lang="ts">
  import { EditorView, basicSetup } from "codemirror";
  import { python } from "@codemirror/lang-python";
  import { tick } from "svelte";

  let { 
    openNames = $bindable([]), 
    activeName = $bindable("") 
  } = $props<{ openNames: string[], activeName: string }>();

  let allFiles = $state<Record<string, string>>(
    JSON.parse(localStorage.getItem("global_files_db") || "{}")
  );

  let view: EditorView | null = null;
  let editingName = $state<string | null>(null); // Tárolja, melyik tabot szerkesztjük éppen

  const activeContent = $derived(activeName ? allFiles[activeName] ?? "" : "");

  $effect(() => {
    localStorage.setItem("global_files_db", JSON.stringify(allFiles));
  });

  function setupEditor(node: HTMLElement) {
    view = new EditorView({
      parent: node,
      doc: activeContent,
      extensions: [
        basicSetup,
        python(),
        EditorView.updateListener.of((u) => {
          if (u.docChanged && activeName) {
            allFiles[activeName] = u.state.doc.toString();
          }
        }),
      ],
    });
    return { destroy: () => view?.destroy() };
  }

  $effect(() => {
    if (view && activeName && view.state.doc.toString() !== activeContent) {
      view.dispatch({
        changes: { from: 0, to: view.state.doc.length, insert: activeContent },
      });
    }
  });

  function add() {
    const newName = `uj_file_${openNames.length + 1}.py`;
    allFiles[newName] = "";
    openNames.push(newName);
    activeName = newName;
  }

  function remove(name: string, e: MouseEvent) {
    e.stopPropagation();
    openNames = openNames.filter(n => n !== name);
    if (activeName === name) activeName = openNames[0] || "";
  }

  async function startEditing(name: string) {
    editingName = name;
    await tick();
    const input = document.querySelector('.tab-input-active') as HTMLInputElement;
    input?.focus();
    input?.select();
  }

  function finishRename(oldName: string, e: Event) {
    const newName = (e.target as HTMLInputElement).value.trim();
    editingName = null;
    
    if (!newName || newName === oldName) return;
    
    allFiles[newName] = allFiles[oldName];
    delete allFiles[oldName];

    const idx = openNames.indexOf(oldName);
    openNames[idx] = newName;
    if (activeName === oldName) activeName = newName;
  }
</script>

<div class="container">
  <nav class="tabs-bar">
    {#each openNames as name (name)}
      <div
        class="tab"
        class:active={activeName === name}
        onclick={() => activeName = name}
        ondblclick={() => startEditing(name)}
        onkeydown={(e) => e.key === 'Enter' && (activeName = name)}
        role="button"
        tabindex="0"
      >
        {#if editingName === name}
          <input 
            class="tab-input-active"
            value={name} 
            onblur={(e) => finishRename(name, e)}
            onkeydown={(e) => e.key === 'Enter' && finishRename(name, e)}
            onclick={e => e.stopPropagation()} 
          />
        {:else}
          <span class="tab-label">{name}</span>
        {/if}
        <button class="close-btn" onclick={(e) => remove(name, e)}>×</button>
      </div>
    {/each}
    <button class="add-btn" onclick={add} title="Új fájl">+</button>
  </nav>

  <div class="editor-body">
    {#if activeName}
      {#key activeName}
        <div class="cm-wrapper" use:setupEditor></div>
      {/key}
    {:else}
      <div class="empty">Nincs megnyitott fájl. Kattints a + gombra.</div>
    {/if}
  </div>
</div>

<style lang="scss">
  .container {
    display: flex;
    flex-direction: column;
    height: 500px;
    border: 1px solid #ddd;
    background: #fff;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    font-family: Roboto, sans-serif;

    .tabs-bar {
      display: flex;
      align-items: center;
      background: #f5f5f5; // Szürkébb háttér a tab sávnak
      border-bottom: 1px solid #ddd;

      .tab {
        display: flex;
        align-items: center;
        padding: 6px 12px;
        background: #fff;
        border: 1px solid #ddd;
        border-bottom: none;
        cursor: pointer;
        min-width: 100px;
        height: 28px;
        max-width: 180px;
        box-shadow: 0 -1px 2px rgba(0,0,0,0.03);

        &.active {
          background: #fff;
          border-bottom: 2px solid #3776ab; // Python-kék jelzés
          .tab-label { font-weight: 600; color: #000; }
        }

        .tab-label {
          font-size: 13px;
          color: #666;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          user-select: none;
        }

        input {
          border: 1px solid #3776ab;
          background: #fff;
          width: 100%;
          font-size: 13px;
          outline: none;
          padding: 0 2px;
        }

        .close-btn {
          border: none;
          background: transparent;
          color: #999;
          font-size: 16px;
          margin-left: 8px;
          cursor: pointer;
          &:hover { color: #d00; }
        }
      }

      .add-btn {
        background: #fff;
        border: 1px solid #ddd;
        color: #3776ab;
        border-radius: 4px;
        width: 28px;
        height: 28px;
        margin-left: 4px;
        cursor: pointer;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;

        &:hover { background: #f0f0f0; border-color: #ccc; }
      }
    }

    .editor-body {
      flex: 1;
      overflow: hidden;
      background: #fff;

      .empty {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        color: #999;
        font-size: 14px;
      }
    }
  }
</style>