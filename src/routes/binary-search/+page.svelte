<script lang="ts">
  import { onMount } from 'svelte';
  import CodeEditor from '$lib/CodeEditor.svelte';
  import pythonCode from './binary-search.py?raw';

  const PAGE_ID = "binary-search";
  const DEFAULT_FILE = "binary-search.py";

  // 1. Az oldalhoz tartozó nyitott tabok listája
  let openFiles = $state<string[]>(
    JSON.parse(localStorage.getItem(`tabs_${PAGE_ID}`) || "[]")
  );
  
  let activeFile = $state<string>("");

  // 2. Mentés: ha az oldal tabjai változnak, elmentjük
  $effect(() => {
    localStorage.setItem(`tabs_${PAGE_ID}`, JSON.stringify(openFiles));
  });

  onMount(() => {
    // Globális fájltár ellenőrzése
    const db = JSON.parse(localStorage.getItem("global_files_db") || "{}");
    
    // Ha a binary-search.py még soha nem volt bent a globális tárban, betöltjük a nyers kódot
    if (!db[DEFAULT_FILE]) {
      db[DEFAULT_FILE] = pythonCode;
      localStorage.setItem("global_files_db", JSON.stringify(db));
    }

    // Ha még nincsenek elmentett tabok ehhez az oldalhoz, alapértelmezett beállítása
    if (openFiles.length === 0) {
      openFiles = [DEFAULT_FILE];
    }
    activeFile = openFiles[0];
  });
</script>

<article>
  <h1>Binary Search</h1>
  
  <div class="editor-section">
    <!-- Kétirányú bindelés: az editor módosíthatja a listát (pl. törlés/átnevezés) -->
    <CodeEditor bind:openNames={openFiles} bind:activeName={activeFile} />
  </div>
</article>