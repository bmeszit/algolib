<script>
  import { t } from "svelte-i18n";
</script>

<footer>
  <div class="inner">
    <div class="line">
      <span>{$t("footer.about")}</span>
      <span class="sep">·</span>
      <a href="https://cs.bme.hu/~vkitti/" target="_blank" rel="noreferrer">{$t("footer.creator_vkitti")}</a>
      <span class="sep">·</span>
      <a href="https://cs.bme.hu/~nemkin/" target="_blank" rel="noreferrer">{$t("footer.creator_nemkin")}</a>
    </div>

    <div class="line">
      <a href="https://github.com/bmeszit/algolib" target="_blank" rel="noreferrer">
        {$t("footer.issues_feature_requests")}
      </a>
    </div>
  </div>
</footer>

<style lang="scss">
  footer {
    border-top: 1px solid #eee;
    margin-top: 3rem;
    padding: 2rem 0rem;
  }

  .inner {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    font-size: 0.95rem;
  }

  .line {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    align-items: center;
  }

  .sep {
    opacity: 0.6;
  }

  a {
    color: inherit;
    text-decoration: none;
    border-bottom: 1px solid transparent;
  }

  a:hover {
    border-bottom-color: currentColor;
  }
</style>
