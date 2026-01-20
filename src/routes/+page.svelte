<!-- src/routes/+page.svelte -->
<script lang="ts">
  import AlgorithmGrid from '$lib/AlgorithmGrid.svelte';
  import AlgorithmCard from '$lib/AlgorithmCard.svelte';

  const algos = [
    {
      title: 'Binary Search',
      description: 'Efficient search in sorted arrays.',
      slug: 'binary-search'
    },
    {
      title: 'Dijkstra',
      description: 'Shortest path algorithm.',
      slug: 'dijkstra'
    },
    {
      title: 'Quick Sort',
      description: 'Divide-and-conquer sorting algorithm.',
      slug: 'quick-sort'
    }
  ];
</script>

<AlgorithmGrid gap="2rem">
  {#each algos as algo}
    <AlgorithmCard
      title={algo.title}
      description={algo.description}
      href="/{algo.slug}" 
    />
  {/each}
</AlgorithmGrid>