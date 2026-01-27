<!-- CodeEditor.svelte (Svelte 5 + CodeMirror 6, runes mode) -->
<script lang="ts">
  import { onMount, onDestroy } from "svelte"

  import { EditorView, keymap, lineNumbers, highlightActiveLine, drawSelection } from "@codemirror/view"
  import { EditorState, Compartment } from "@codemirror/state"
  import { defaultKeymap, history, historyKeymap, indentWithTab } from "@codemirror/commands"
  import { bracketMatching } from "@codemirror/language"
  import { python } from "@codemirror/lang-python"

  type Props = {
    value: string
    onChange?: (next: string) => void
    readOnly?: boolean
    extraExtensions?: any[]
  }

  const {
    value,
    onChange = () => {},
    readOnly = false,
    extraExtensions = []
  } = $props() as Props

  let host: HTMLDivElement | null = null
  let view: EditorView | null = null

  const ro = new Compartment()
  const extras = new Compartment()

  function roExt(v: boolean) {
    return EditorState.readOnly.of(v)
  }

  function makeState(doc: string) {
    return EditorState.create({
      doc,
      extensions: [
        lineNumbers(),
        highlightActiveLine(),
        drawSelection(),
        history(),
        bracketMatching(),
        python(),
        keymap.of([indentWithTab, ...defaultKeymap, ...historyKeymap]),
        EditorView.updateListener.of((u) => {
          if (!u.docChanged) return
          const next = u.state.doc.toString()
          if (next !== value) onChange(next)
        }),
        ro.of(roExt(readOnly)),
        extras.of(extraExtensions)
      ]
    })
  }

  onMount(() => {
    if (!host) return
    view = new EditorView({
      state: makeState(value ?? ""),
      parent: host
    })
  })

  onDestroy(() => {
    view?.destroy()
    view = null
  })

  // parent -> editor sync (tab switch / external update)
  $effect(() => {
    if (!view) return
    const next = value ?? ""
    const cur = view.state.doc.toString()
    if (next === cur) return
    view.dispatch({
      changes: { from: 0, to: view.state.doc.length, insert: next }
    })
  })

  // readOnly sync
  $effect(() => {
    if (!view) return
    view.dispatch({ effects: ro.reconfigure(roExt(readOnly)) })
  })

  // extraExtensions sync
  $effect(() => {
    if (!view) return
    view.dispatch({ effects: extras.reconfigure(extraExtensions) })
  })
</script>

<div class="host" bind:this={host}></div>

<style>
  .host { width: 100%; height: 100%; }
  :global(.cm-editor) { height: 100%; }
  :global(.cm-scroller) {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
      "Liberation Mono", "Courier New", monospace;
  }
</style>
