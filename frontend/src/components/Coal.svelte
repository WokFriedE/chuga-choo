<script>
  let moving = false;

  let left = $state(0);
  let top = $state(0);
  function onMouseDown() {
    moving = true;
  }

  function onMouseMove(e) {
    if (moving) {
      left += e.movementX;
      top += e.movementY;
    }
  }

  function onMouseUp() {
    moving = false;
  }
</script>

<svelte:window on:mousemove={onMouseMove} on:mouseup={onMouseUp} />
<img
  src="/Coal.png"
  alt="Coal"
  style:top={top + "px"}
  draggable="false"
  style:left={left + "px"}
  class="draggable"
  on:mousedown={onMouseDown}
/>

<style>
  img {
    position: absolute;
    user-select: none;
    object-fit: contain;
    border-radius: 50%;
    border: 2px solid rgb(255, 255, 255);
    background-color: #ffffffac;
  }
</style>
