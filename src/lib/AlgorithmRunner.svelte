<script>
  import { usePyodide } from './pyodide.svelte';

  // Props:
  // - openNames: a nyitott tabok nevei (hogy tudjuk mit kell futtatni)
  // - allFiles: az összes fájl tartalma (a kódok eléréséhez)
  // - inputData: a generált adat (ezt bindoljuk, hogy a textarea szerkeszthesse)
  // - pythonCall: a hívás sablon
  // - children: generáló gombok

  let { 
    openNames, 
    allFiles, 
    inputData = $bindable(), 
    pythonCall, 
    children 
  } = $props();

  const py = usePyodide();
  
  // Eredmények tárolása: { "file.py": 1.234 }
  let results = $state({});
  let isExecuting = $state(false);

  // Textarea kezelése: szinkronizáljuk az inputData-val
  let textRepresentation = $state("");

  // Ha kívülről (generátorral) változik az adat, frissítjük a szöveget
  $effect(() => {
    if (typeof inputData === 'object' && inputData !== null) {
      // Ha a Search-féle objektumunk van {list, target}
      const list = inputData.list || inputData; 
      textRepresentation = Array.isArray(list) ? list.join(', ') : JSON.stringify(inputData);
    } else {
      textRepresentation = String(inputData);
    }
  });

  // Ha a textarea-ban szerkesztjük, megpróbáljuk visszatölteni az adatba
  function handleTextChange(e) {
    const val = e.target.value;
    const parsed = val.split(',').map(n => Number(n.trim())).filter(n => !isNaN(n));
    
    if (inputData && typeof inputData === 'object' && inputData.list) {
      inputData.list = parsed;
    } else {
      inputData = parsed;
    }
  }

  async function runAll() {
    isExecuting = true;
    results = {}; // Reset
    
    try {
      const instance = await py.init();
      
      for (const fileName of openNames) {
        const code = allFiles[fileName];
        if (!code) continue;

        // Adat átadása
        instance.globals.set('raw_data', inputData);
        
        const t0 = performance.now();
        try {
          await instance.runPythonAsync(`${code}\n${pythonCall}`);
          const t1 = performance.now();
          results[fileName] = (t1 - t0).toFixed(4);
        } catch (err) {
          results[fileName] = "Hiba";
          console.error(`Hiba a(z) ${fileName} futtatásakor:`, err);
        }
      }
    } catch (e) {
      alert("Pyodide hiba: " + e.message);
    } finally {
      isExecuting = false;
    }
  }
</script>

<div class="runner-container">
  <div class="top-row">
    <div class="generator-slot">
      {@render children()}
    </div>
    <button class="run-btn" onclick={runAll} disabled={isExecuting || openNames.length === 0}>
      {isExecuting ? 'Futás...' : 'Összes futtatása'}
    </button>
  </div>

  <div class="data-section">
    <label for="data-input">Bemeneti adatok (szerkeszthető, vesszővel elválasztva):</label>
    <textarea 
      id="data-input"
      value={textRepresentation} 
      oninput={handleTextChange}
      placeholder="1, 2, 3..."
    ></textarea>
  </div>

  {#if Object.keys(results).length > 0}
    <div class="results-grid">
      {#each openNames as name}
        <div class="result-card" class:has-error={results[name] === 'Hiba'}>
          <span class="file-name">{name}</span>
          <span class="time">{results[name] ? `${results[name]} ms` : '...'}</span>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style lang="scss">
  .runner-container {
    margin-top: 1rem;
    padding: 1.5rem;
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;

    .top-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }

    .data-section {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      
      label {
        font-size: 0.85rem;
        font-weight: bold;
        color: #555;
      }

      textarea {
        width: 100%;
        height: 80px;
        padding: 10px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 13px;
        border: 1px solid #ccc;
        border-radius: 4px;
        resize: vertical;
        background: #fff;
      }
    }

    .run-btn {
      background: #3776ab;
      color: white;
      border: none;
      padding: 10px 24px;
      border-radius: 6px;
      cursor: pointer;
      font-weight: bold;
      font-size: 1rem;
      &:hover:not(:disabled) { background: #2b5b87; }
      &:disabled { background: #adb5bd; cursor: not-allowed; }
    }

    .results-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
      gap: 10px;

      .result-card {
        background: #fff;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 6px;
        display: flex;
        flex-direction: column;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);

        &.has-error {
          border-color: #ffc107;
          background: #fff8e1;
          .time { color: #d32f2f; }
        }

        .file-name {
          font-size: 0.75rem;
          color: #666;
          margin-bottom: 4px;
          text-overflow: ellipsis;
          overflow: hidden;
          white-space: nowrap;
          width: 100%;
          text-align: center;
        }

        .time {
          font-weight: bold;
          font-family: monospace;
          font-size: 1rem;
          color: #2e7d32;
        }
      }
    }
  }
</style>