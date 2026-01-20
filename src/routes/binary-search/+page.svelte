<script lang="ts">
  import CodeEditor from '$lib/CodeEditor.svelte';
  import { createEditorManager } from '$lib';
  
  import binarySearchCode from './binary-search.py?raw';
  import linearSearchCode from './linear-search.py?raw';

  const editor = createEditorManager("search-algorithms", {
    "binary-search.py": binarySearchCode,
    "linear-search.py": linearSearchCode
  });
</script>

<article>
  <header class="page-header">
    <h1>Search</h1>
    <button class="reset-btn" onclick={() => editor.reset()}>Reset to Default</button>
  </header>
  
  <div class="editor-section">
    <CodeEditor bind:openNames={editor.openNames} bind:activeName={editor.activeName} />
  </div>
</article>