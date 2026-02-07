<script>
  import { t } from 'svelte-i18n';
  import { CodeEditorTabs } from '$lib';
  import { getContext } from 'svelte';
  import { createPyRunner } from '$lib';
  import searchIn from '$lib/code/tests/search.in?raw';

  const pageId = 'search';
  const codeRepo = getContext('codeRepo');

  let activeCode = $state(null);
  let inputText = $state(searchIn);

  const runner = createPyRunner();

  const output = $derived(runner.last?.result ?? '');
  const meta = $derived(
    runner.last
      ? `time=${runner.last.timeMs.toFixed(2)}ms, peak=${runner.last.peakBytes} bytes`
      : '',
  );

  async function onRun() {
    let code = codeRepo.get(pageId, activeCode);
    await runner.run(code, inputText);
  }
</script>