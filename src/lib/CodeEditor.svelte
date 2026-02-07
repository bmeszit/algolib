<script>
  import { onMount, onDestroy } from "svelte";
  import { EditorView, keymap, lineNumbers, highlightActiveLine, drawSelection } from "@codemirror/view";
  import { EditorState } from "@codemirror/state";
  import { defaultKeymap, history, historyKeymap, indentWithTab } from "@codemirror/commands";
  import { bracketMatching } from "@codemirror/language";
  import { python } from "@codemirror/lang-python";
  import { defaultHighlightStyle, syntaxHighlighting } from "@codemirror/language";

  const { value, onchange = () => {} } = $props();

  let host = null;
  let view = null;

  function makeState(doc) {
    return EditorState.create({
      doc,
      extensions: [
        lineNumbers(),
        highlightActiveLine(),
        syntaxHighlighting(defaultHighlightStyle),
        drawSelection(),
        history(),
        bracketMatching(),
        python(),
        keymap.of([indentWithTab, ...defaultKeymap, ...historyKeymap]),
        EditorView.updateListener.of((u) => {
          if (!u.docChanged) return;
          const next = u.state.doc.toString();
          if (next !== value) onchange(next);
        })
      ]
    });
  }

  onMount(() => {
    if (!host) return;
    view = new EditorView({ state: makeState(value ?? ""), parent: host });
  });

  onDestroy(() => {
    view?.destroy();
    view = null;
  });

  $effect(() => {
    if (!view) return;
    const next = value ?? "";
    const cur = view.state.doc.toString();
    if (next === cur) return;
    view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: next } });
  });
</script>

<div class="host" bind:this={host}></div>

<style lang="scss">
  .host { width: 100%; height: 100%; }
  :global(.cm-editor) { height: 100%; }
  :global(.cm-scroller) {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
      "Liberation Mono", "Courier New", monospace;
    font-size: 14px;
    -webkit-overflow-scrolling: touch;
  }
  :global(.cm-content) { padding: 10px 8px; }
</style>