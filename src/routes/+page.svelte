<script lang="ts">
  import { t, locale } from 'svelte-i18n';
  import { base } from '$app/paths';
  import AlgorithmGrid from '$lib/AlgorithmGrid.svelte';
  import AlgorithmCard from '$lib/AlgorithmCard.svelte';

  const algorithms = [
    { id: 'search', slug: 'search' },
    { id: 'sort', slug: 'sort' },
  ];
</script>

<section>
  
  <AlgorithmGrid gap="2rem">
    {#each algorithms as algo}
      <AlgorithmCard
        title={$t(`algos.${algo.id}.title`)}
        description={$t(`algos.${algo.id}.desc`)}
        href="{algo.slug}{$locale === 'en' ? '?lang=en' : ''}"
      />
    {/each}
  </AlgorithmGrid>
</section>