<script>
  let handle, wrap, cog2;
  let { val = $bindable(), size } = $props();

  function handleMousemove(event) {
    // Get the position of the wrap element and calculate the rotation angle
    const rect = wrap.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    const angle = Math.atan2(event.clientY - centerY, event.clientX - centerX);
    let deg = angle * (180 / Math.PI);

    // Constrain the angle between -90 and +90 degrees
    deg = Math.max(-90, Math.min(90, deg));

    // Normalize the angle to a range from 0 (right) to 1 (left)
    val = (90 - deg) / 180;

    // Rotate the wrap element based on the angle
    wrap.style.transform = `rotate(${deg + 90}deg)`;

    // Rotate the cog2 element in the opposite direction
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

<div class="aslo_wrap" style:--size={size}>
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
    width: calc(var(--size) * 5em);
    height: calc(var(--size) * 5em);
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
    width: calc(var(--size) * 7em);
    height: calc(var(--size) * 7em);
  }
  .cog2 {
    position: absolute;
    top: 40%;
    left: 30%;
    width: calc(var(--size) * 7em);
    z-index: -1;
  }
  .handle {
    top: calc(var(--size) * -2.5em);
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
  }
</style>
