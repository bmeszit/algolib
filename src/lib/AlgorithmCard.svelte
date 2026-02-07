<script>
  export let title;
  export let description;
  export let href;
</script>

<a {href} class="card">
  <h3>{title}</h3>
  <p>{description}</p>
  <slot />
</a>

<style lang="scss">
  .card {
    display: block;
    text-decoration: none;
    color: inherit;
    background: white;
    border-radius: 12px;
    padding: 1.25rem;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
    flex: 1 1 260px;
    max-width: 320px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
  }

  .card:hover {
    transform: translateY(-4px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    border: 1px solid #3b82f6;
  }

  h3 {
    margin: 0 0 0.5rem;
    font-size: 1.1rem;
    color: #111;
  }

  p {
    margin: 0;
    color: #555;
    line-height: 1.4;
  }
</style>