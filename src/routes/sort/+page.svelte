<script>
  import { t } from 'svelte-i18n';
  import { CodeEditorTabs } from '$lib';
  import { getContext } from "svelte";

  const codeRepo = getContext("codeRepo");
</script>

<article>
  <header class="page-header">
    <h1>{$t('algos.sort.title')}</h1>
  </header>
  <p>{$t('algos.sort.desc')}</p>
  
  <div class="editor-section">
    <CodeEditorTabs pageId="sort" repo={codeRepo} />
  </div>
</article>

<style lang="scss">
  .editor-section {
    margin-bottom: 20px;
  }

  .controls {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    align-items: center;

    .input-group {
      display: flex;
      align-items: center;
      gap: 8px;
      input {
        width: 80px;
        padding: 4px;
        border: 1px solid #ccc;
        border-radius: 4px;
      }
    }

    .button-group {
      display: flex;
      gap: 8px;
      button {
        padding: 6px 12px;
        background: #eee;
        border: 1px solid #ccc;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.9rem;
        &:hover { background: #e0e0e0; }
      }
    }

    .preview {
      font-size: 0.85rem;
      color: #666;
      font-style: italic;
    }
  }
</style>