<script lang="ts">
  import { onMount } from 'svelte';
  import { EditorView, basicSetup } from 'codemirror';
  import { python } from '@codemirror/lang-python';

  let { code } = $props();
  let editorElement: HTMLDivElement;

  onMount(() => {
    const view = new EditorView({
      doc: code,
      extensions: [
        basicSetup,
        python(),
        EditorView.editable.of(false), 
        EditorView.lineWrapping,
        EditorView.theme({
          "&": { height: "auto", maxHeight: "600px" },
          ".cm-scroller": { overflow: "auto" },
          // Optional: Force a specific font if you want
          ".cm-content": { fontFamily: "ui-monospace, monospace" }
        })
      ],
      parent: editorElement
    });

    return () => view.destroy();
  });
</script>

<div class="editor-wrapper" bind:this={editorElement}></div>

<style>
  .editor-wrapper {
    border-radius: 8px;
    overflow: hidden;
    font-size: 14px;
    border: 1px solid #ddd; /* Light border for the code box */
    background-color: #fff;
    margin-top: 1rem;
  }

  /* Basic styling for the gutter (line numbers) to make it look clean */
  :global(.cm-gutters) {
    background-color: #f7f7f7 !important;
    border-right: 1px solid #ddd !important;
    color: #999 !important;
  }
</style>