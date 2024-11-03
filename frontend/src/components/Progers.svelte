<script>
  let { percent = $bindable() } = $props();
  percent = (percent / 9000000) * 100;
</script>

<div class="trainwrap">
  <img
    src="/train.gif"
    alt="train"
    style="left: {percent > 100 ? 100 : percent}%;"
  />
  <progress value={percent} max="100"></progress>
</div>

<style>
  .trainwrap {
    position: relative;
    width: 100%;
    min-width: 20em;
  }
  img {
    position: absolute;
    bottom: 10px;
    width: 100px;
    z-index: -1;
    transform: translateX(-50%);
    box-shadow: 0 0 10px 5px rgba(255, 255, 255, 0.25) inset;
  }
  progress {
    position: absolute;
    bottom: 0;
    width: 20em;
  }
</style>
