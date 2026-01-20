// src/lib/editor-manager.svelte.ts
export function createEditorManager(pageId: string, defaultFiles: Record<string, string>) {
    // 1. Állapotok inicializálása
    let openNames = $state<string[]>(
        JSON.parse(localStorage.getItem(`tabs_${pageId}`) || "[]")
    );
    
    let activeName = $state<string>(
        localStorage.getItem(`active_tab_${pageId}`) || ""
    );

    // 2. Automatikus mentés, ha változik a tabok listája vagy az aktív tab
    $effect(() => {
        localStorage.setItem(`tabs_${pageId}`, JSON.stringify(openNames));
    });

    $effect(() => {
        localStorage.setItem(`active_tab_${pageId}`, activeName);
    });

    // 3. Inicializálás (onMount-szerű logika, de univerzálisan)
    function init() {
        const db = JSON.parse(localStorage.getItem("global_files_db") || "{}");
        let changed = false;

        // Ha nincs elmentett tab, betöltjük az alapértelmezetteket
        if (openNames.length === 0) {
            openNames = Object.keys(defaultFiles);
            activeName = openNames[0] || "";
            
            for (const [name, content] of Object.entries(defaultFiles)) {
                if (!db[name]) {
                    db[name] = content;
                    changed = true;
                }
            }
        }

        if (changed) {
            localStorage.setItem("global_files_db", JSON.stringify(db));
        }
        
        if (!activeName && openNames.length > 0) {
            activeName = openNames[0];
        }
    }

    // 4. Reset funkció
    function reset() {
        const db = JSON.parse(localStorage.getItem("global_files_db") || "{}");

        // Régi fájlok takarítása (opcionális, de ajánlott)
        openNames.forEach(name => delete db[name]);

        // Alapértelmezettek visszaállítása
        for (const [name, content] of Object.entries(defaultFiles)) {
            db[name] = content;
        }

        localStorage.setItem("global_files_db", JSON.stringify(db));
        
        // Tabok visszaállítása
        openNames = Object.keys(defaultFiles);
        activeName = openNames[0] || "";

        // Mivel a CodeEditor belső állapota a localStorage-ra épül, 
        // egy reload a legbiztosabb a teljes szinkronhoz
        window.location.reload();
    }

    // Inicializálunk az indításkor
    init();

    // Visszaadjuk az állapotokat és a reset függvényt
    // Getter/setter-t használunk, hogy a bind: továbbra is működjön a komponensekkel
    return {
        get openNames() { return openNames; },
        set openNames(val) { openNames = val; },
        get activeName() { return activeName; },
        set activeName(val) { activeName = val; },
        reset
    };
}