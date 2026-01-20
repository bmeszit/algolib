<script lang="ts">
  import { t } from 'svelte-i18n';
  import AlgorithmGrid from '$lib/AlgorithmGrid.svelte';
  import AlgorithmCard from '$lib/AlgorithmCard.svelte';

  // We only keep the ID and Slug here
  const algorithms = [
    { id: 'binary-search', slug: 'binary-search' },
    { id: 'dijkstra', slug: 'dijkstra' },
    { id: 'quick-sort', slug: 'quick-sort' }
  ];
</script>

<section style="padding: 2rem;">
  <h1>{$t('common.title')}</h1>

  <AlgorithmGrid gap="2rem">
    {#each algorithms as algo}
      <AlgorithmCard
        title={$t(`algos.${algo.id}.title`)}
        description={$t(`algos.${algo.id}.desc`)}
        href="/{algo.slug}"
      />
    {/each}
  </AlgorithmGrid>
</section>