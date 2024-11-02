<script>
  let handle, wrap, cog2;
  let { val = $bindable() } = $props();
  function handleMousemove(event) {
    //rotate the wrap element based on the mouse position
    const rect = wrap.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    const angle = Math.atan2(event.clientY - centerY, event.clientX - centerX);
    let deg = angle * (180 / Math.PI);
    val = deg;
    wrap.style.transform = `rotate(${deg + 90}deg)`;
    //rotate the cog2 element in the opposite direction
    cog2.style.transform = `rotate(${-deg}deg)`;
  }
  function handleMouseup() {
    window.removeEventListener("mousemove", handleMousemove);
    window.removeEventListener("mouseup", handleMouseup);
  }
  function handleMousedown() {
    window.addEventListener("mousemove", handleMousemove);
    window.addEventListener("mouseup", handleMouseup);
  }
  function handleLoaded() {
    handle.addEventListener("mousedown", handleMousedown);
  }
</script>

<div class="aslo_wrap">
  <div class="wrap" bind:this={wrap}>
    <img src="/cog.png" alt="cog" class="cog" draggable="false" />
    <img
      draggable="false"
      src="/handle.png"
      alt="handle"
      class="handle"
      bind:this={handle}
      on:load={handleLoaded}
    />
  </div>
  <img
    src="/cog.png"
    alt="cog"
    class="cog2"
    draggable="false"
    bind:this={cog2}
  />
</div>

<style>
  .wrap {
    position: relative;
    width: 5em;
    height: 5em;
  }

  img {
    position: absolute;
    user-select: none;
    object-fit: contain;
  }

  .cog {
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
  .aslo_wrap {
    position: relative;
    width: 7em;
    height: 7em;
  }
  .cog2 {
    position: absolute;
    top: 40%;
    left: 30%;
    width: 7em;
    z-index: -1;
  }
  .handle {
    top: -2.5em;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
  }
</style>
