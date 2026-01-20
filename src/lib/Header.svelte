<script lang="ts">
  import LocaleSwitcher from './LocaleSwitcher.svelte';
</script>

<header>
  <nav>
    <a href="/" class="logo">AlgoLib</a>
    <LocaleSwitcher />
  </nav>
</header>

<style>
  nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0rem;
    border-bottom: 1px solid #eee;
  }
  .logo {
    font-size: 3.5rem;
    font-weight: bold;
    text-decoration: none;
    color: black;
  }
</style>