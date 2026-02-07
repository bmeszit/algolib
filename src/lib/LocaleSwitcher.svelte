<script>
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { locale } from 'svelte-i18n';

  function updateLocale(event) {
    const target = event.target;
    const newLang = target.value;

    const newUrl = new URL($page.url);
    if (newLang === 'en') {
      newUrl.searchParams.set('lang', 'en');
    } else {
      newUrl.searchParams.delete('lang');
    }
    goto(newUrl.pathname + newUrl.search, { keepFocus: true, noScroll: true });
  }
</script>

<select 
  class="lang" value={$locale} onchange={updateLocale}>
  <option value="hu">🇭🇺 Magyar</option>
  <option value="en">🇬🇧 English</option>
</select>

<style lang='scss'>
.lang {
  border: 1px solid #ddd;
  background-color: transparent;
  padding: 6px 32px 6px 10px;
  border-radius: 10px;
  cursor: pointer;
  font: inherit;
  color: inherit;
  appearance: none;
  background-image:
    url("data:image/svg+xml;utf8,\
<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 10 6'>\
<path d='M1 1l4 4 4-4' fill='none' stroke='%23666' stroke-width='1.5'/>\
</svg>");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 10px 6px;
}

</style>