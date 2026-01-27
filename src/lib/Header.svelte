<script lang="ts">
  import { resolve } from '$app/paths';
  import { t, locale } from 'svelte-i18n';
  import LocaleSwitcher from './LocaleSwitcher.svelte';
</script>

<header>
  <nav>
    <a href={resolve('/') + ($locale === 'en' ? '?lang=en' : '')} class="logo">{$t('common.title')}</a>
    <LocaleSwitcher />
  </nav>
</header>

<style>
  nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 3rem 0rem;
    border-bottom: 1px solid #eee;
  }

  .logo {
    font-size: 3.5rem;
    font-weight: bold;
    text-decoration: none;
    color: black;
  }

  @media (max-width: 768px) {
    nav {
      flex-direction: column;
      gap: 1.5rem;
      padding: 2rem 0rem;
    }

    .logo {
      font-size: 2.5rem;
      text-align: center;
    }
  }
</style>