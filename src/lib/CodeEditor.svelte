<script lang="ts">
  import { EditorView, basicSetup } from "codemirror";
  import { python } from "@codemirror/lang-python";

  // PROPS: openNames (milyen tabok vannak nyitva), activeName (melyik látszik)
  let { 
    openNames = $bindable([]), 
    activeName = $bindable("") 
  } = $props<{ openNames: string[], activeName: string }>();

  // Globális tárhely betöltése
  let allFiles = $state<Record<string, string>>(
    JSON.parse(localStorage.getItem("global_files_db") || "{}")
  );

  let view: EditorView | null = null;

  // Az éppen szerkesztett fájl tartalma a globális tárból
  let activeContent = $derived(activeName ? allFiles[activeName] ?? "" : "");

  // Mentés a globális tárba, ha bármi változik
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

  // Tartalom frissítése tab váltáskor
  $effect(() => {
    if (view && activeName && view.state.doc.toString() !== activeContent) {
      view.dispatch({
        changes: { from: 0, to: view.state.doc.length, insert: activeContent },
      });
    }
  });

  function add() {
    const newName = `uj_file_${openNames.length + 1}.py`;
    allFiles[newName] = ""; // Beírjuk a globálisba
    openNames.push(newName); // Hozzáadjuk a látható tabokhoz
    activeName = newName;
  }

  function remove(name: string, e: MouseEvent) {
    e.stopPropagation();
    openNames = openNames.filter(n => n !== name); // Csak a listából vesszük ki
    if (activeName === name) activeName = openNames[0] || "";
  }

  function rename(oldName: string, e: Event) {
    const newName = (e.target as HTMLInputElement).value;
    if (newName === oldName || !newName) return;
    
    // Áthelyezzük az adatot a globális tárban
    allFiles[newName] = allFiles[oldName];
    delete allFiles[oldName];

    // Frissítjük a látható listát
    const idx = openNames.indexOf(oldName);
    openNames[idx] = newName;
    if (activeName === oldName) activeName = newName;
  }
</script>

<div class="container">
  <nav class="tabs">
    {#each openNames as name (name)}
      <div class="tab" class:active={activeName === name} onclick={() => activeName = name}>
        <input value={name} onchange={(e) => rename(name, e)} onclick={e => e.stopPropagation()} />
        <button onclick={(e) => remove(name, e)}>×</button>
      </div>
    {/each}
    <button class="add" onclick={add}>+</button>
  </nav>

  <div class="editor">
    {#if activeName}
      {#key activeName}
        <div use:setupEditor></div>
      {/key}  <!-- Itt volt a hiba: a perjel (/) hiányzott -->
    {:else}
      <div class="empty">Nincs megnyitott fájl</div>
    {/if}
  </div>
</div>

<style lang="scss">
  .container {
    display: flex; flex-direction: column; height: 450px; border: 1px solid #333;
    .tabs {
      display: flex; gap: 2px; padding: 4px; background: #222;
      .tab {
        display: flex; align-items: center; padding: 4px 8px; background: #444; color: #ccc; cursor: pointer;
        &.active { background: #fff; color: #000; input { color: #000; } }
        input { border: none; background: transparent; width: 100px; font-size: 12px; color: inherit; outline: none; }
        button { border: none; background: transparent; color: inherit; cursor: pointer; margin-left: 5px; }
      }
      .add { background: #3776ab; color: #fff; border: none; padding: 0 10px; cursor: pointer; }
    }
    .editor { flex: 1; overflow: hidden; :global(.cm-editor) { height: 100%; } .empty { padding: 20px; color: #888; } }
  }
</style>