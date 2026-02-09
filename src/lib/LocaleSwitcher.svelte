<script>
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { locale } from 'svelte-i18n';

  const options = [
    { value: 'hu', label: 'Magyar', flag: '🇭🇺' },
    { value: 'en', label: 'English', flag: '🇬🇧' }
  ];

  let open = $state(false);

  const currentValue = $derived($locale);
  const current = $derived(options.find((o) => o.value === currentValue) ?? options[0]);

  function setLang(newLang) {
    const newUrl = new URL($page.url);
    if (newLang === 'en') {
      newUrl.searchParams.set('lang', 'en');
    } else {
      newUrl.searchParams.delete('lang');
    }
    open = false;
    goto(newUrl.pathname + newUrl.search, { keepFocus: true, noScroll: true });
  }

  function toggle() {
    open = !open;
  }

  $effect(() => {
    if (!open) return;
    const onDoc = (e) => {
      const t = e.target;
      if (!(t instanceof Node)) return;
      const root = document.getElementById('lang-dd');
      if (root && !root.contains(t)) {
        open = false;
      }
    };
    const onKey = (e) => {
      if (e.key === 'Escape') open = false;
    };
    document.addEventListener('pointerdown', onDoc, true);
    document.addEventListener('keydown', onKey, true);
    return () => {
      document.removeEventListener('pointerdown', onDoc, true);
      document.removeEventListener('keydown', onKey, true);
    };
  });
</script>

<div id="lang-dd" class="dd">
  <button
    type="button"
    class="trigger"
    aria-haspopup="listbox"
    aria-expanded={open}
    onclick={toggle}
  >
    <span class="flag">{current.flag}</span>
    <span class="text">{current.label}</span>
    <span class="chev" aria-hidden="true"></span>
  </button>

  {#if open}
    <div class="menu" role="listbox" aria-label="Language">
      {#each options as opt (opt.value)}
        <button
          type="button"
          class="item"
          role="option"
          aria-selected={opt.value === currentValue}
          onclick={() => setLang(opt.value)}
        >
          <span class="flag">{opt.flag}</span>
          <span class="text">{opt.label}</span>
          {#if opt.value === currentValue}
            <span class="check" aria-hidden="true">✓</span>
          {/if}
        </button>
      {/each}
    </div>
  {/if}
</div>

<style lang="scss">
  .dd {
    position: relative;
    display: inline-block;
  }

  .trigger {
    border: 1px solid #ddd;
    background: transparent;
    padding: 6px 32px 6px 10px;
    border-radius: 10px;
    cursor: pointer;
    font: inherit;
    color: inherit;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    user-select: none;
  }

  .flag {
    width: 1.25em;
    display: inline-flex;
    justify-content: center;
  }

  .chev {
    position: absolute;
    right: 10px;
    width: 10px;
    height: 6px;
    background-image:
      url("data:image/svg+xml;utf8,\
<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 10 6'>\
<path d='M1 1l4 4 4-4' fill='none' stroke='%23666' stroke-width='1.5'/>\
</svg>");
    background-repeat: no-repeat;
    background-size: 10px 6px;
    background-position: center;
  }

  .menu {
    position: absolute;
    top: calc(100% + 6px);
    left: 0;
    min-width: 100%;
    border: 1px solid #ddd;
    border-radius: 10px;
    background: canvas;
    color: canvastext;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
    padding: 6px;
    z-index: 50;
  }

  .item {
    width: 100%;
    border: 0;
    background: transparent;
    font: inherit;
    color: inherit;
    padding: 8px 10px;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .item:hover,
  .item[aria-selected="true"] {
    background: rgba(0, 0, 0, 0.06);
  }

  .check {
    margin-left: auto;
    opacity: 0.8;
  }
</style>
