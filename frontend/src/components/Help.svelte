<script>
  let helpImgs = [
    "coalbox.png",
    "dumpcoal.png",
    "engine intake.png",
    "furnace intake.png",
    "gauges.png",
    "gearbox.png",
  ];
  let curImg = $state(0);
</script>

<button popovertarget="mypopover">
  <img src="/helpbook.png" alt="Help" />
</button>
<div id="mypopover" popover={"auto"}>
  <div style="display: flex; flex-direction: row;">
    {#each helpImgs as img, i}
      {#if i === curImg}
        <img src={img} alt="image" />
      {/if}
    {/each}
  </div>
  <button
    class="next"
    on:click={() => (curImg = (curImg + 1) % helpImgs.length)}
  >
  </button>
</div>

<style>
  .next {
    position: absolute;
    width: 100%;
    bottom: 0;
    left: 0;
    border: none;
    cursor: pointer;
    height: 100%;
  }
  button {
    background-color: transparent;
    border: none;
    cursor: pointer;
    transition: 0.3s;
  }
  button img {
    width: 50px;
    height: 50px;
  }
  div img {
    width: 400px;
    height: 400px;
  }
  button:hover img {
    width: 60px;
    height: 60px;
  }
</style>
