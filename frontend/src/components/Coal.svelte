<script>
  let moving = false;
  let {
    holdingCoal = $bindable(),
    x = $bindable(),
    y = $bindable(),
    onmouseup,
  } = $props();
  
  // Set the initial position at the bottom left, adjusted up by half the image height
  let left = $state(0);
  let imageHeight = 100; // Adjust this to your actual image height
  let top = $state(window.innerHeight - 3*imageHeight); // Move up by half the height

  function onMouseDown() {
    moving = true;
    holdingCoal = true;
  }

  function onMouseMove(e) {
    if (moving) {
      left += e.movementX;
      top += e.movementY;
      x = e.target.getBoundingClientRect().left;
      y = e.target.getBoundingClientRect().top;
    }
  }

  function onMouseUp() {
    onmouseup();
    moving = false;
    holdingCoal = false;
  }
</script>

<svelte:window on:mousemove={onMouseMove} on:mouseup={onMouseUp} />
<img
  src="/Coal.png"
  alt="Coal"
  style="top: {top}px; left: {left}px;"
  draggable="false"
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
    z-index: 3;
  }
</style>
