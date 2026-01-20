<script lang="ts">
  import { t, locale } from 'svelte-i18n';
  import CodeEditor from '$lib/CodeEditor.svelte';
  
  // Vite "raw" import: This reads the .py file and gives us the text
  import pythonCode from './binary-search.py?raw';
</script>

<article class="algo-page">
  <header>
    <h1>{$t('algos.binary-search.title')}</h1>
    <p class="desc">{$t('algos.binary-search.desc')}</p>
  </header>

  <div class="code-section">
    <div class="code-header">
      <span>binary_search.py</span>
      <button 
        class="copy-btn" 
        onclick={() => navigator.clipboard.writeText(pythonCode)}
      >
        {$locale === 'en' ? 'Copy' : 'Másolás'}
      </button>
    </div>
    
    <!-- Pass the imported string to your component -->
    <CodeEditor code={pythonCode} />
  </div>

  <footer>
    <!-- Back to home, preserving the ?lang=en parameter -->
    <a href="../{$locale === 'en' ? '?lang=en' : ''}">
      ← {$t('common.back')}
    </a>
  </footer>
</article>

<style>
  .algo-page {
    max-width: 850px;
    margin: 0 auto;
    padding: 2rem;
  }

  header {
    margin-bottom: 2rem;
  }

  h1 {
    font-size: 2.5rem;
    margin: 0 0 0.5rem 0;
  }

  .desc {
    color: #586069;
    font-size: 1.1rem;
  }

  .code-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #f6f8fa;
    padding: 0.5rem 1rem;
    border: 1px solid #e1e4e8;
    border-bottom: none;
    border-radius: 8px 8px 0 0;
    font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
    font-size: 0.85rem;
  }

  .copy-btn {
    background: white;
    border: 1px solid #d1d5da;
    padding: 3px 10px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.75rem;
    transition: background 0.2s;
  }

  .copy-btn:hover {
    background: #f3f4f6;
  }

  footer {
    margin-top: 3rem;
  }

  footer a {
    color: #0366d6;
    text-decoration: none;
    font-weight: 500;
  }

  footer a:hover {
    text-decoration: underline;
  }
</style>