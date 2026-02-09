<script>
  import "../lib/i18n";
  import { page } from "$app/state";
  import favicon from "$lib/assets/favicon.svg";
  import Header from "$lib/Header.svelte";
  import Footer from "$lib/Footer.svelte";
  import "../app.scss";

  import { createCodeRepo } from "$lib";
  import { defaultCode } from "$lib";
  import { setContext } from "svelte";

  const lang = $derived(page.url.searchParams.get("lang") ?? "hu");
  const codeRepo = createCodeRepo(defaultCode, () => lang);
  setContext("codeRepo", codeRepo);

  let { children } = $props();
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

<Header />

<main>
  {@render children()}
</main>

<Footer />
