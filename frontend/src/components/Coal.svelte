<script>
  let moving = false;
  let {
    holdingCoal = $bindable(),
    furnace_pos,
    addCoal,
    actPanelOpen = $bindable(),
  } = $props();
  let hidden = $state(false);
  // Set the initial position at the bottom left, adjusted up by half the image height
  let left = $state(0 + 100 * Math.random()); // Adjust this to your actual image width
  let imageHeight = 100; // Adjust this to your actual image height
  let top = $state(window.innerHeight - 150 - 150 * Math.random()); // Adjust this to your actual image height

  function onMouseDown() {
    moving = true;
    holdingCoal = true;
  }

  function onMouseMove(e) {
    if (moving) {
      left += e.movementX;
      top += e.movementY;
    }
  }

  function onMouseUp(e) {
    moving = false;
    holdingCoal = false;
    if (furnace_pos) {
      if (
        left > furnace_pos?.x &&
        left < furnace_pos?.x + furnace_pos?.width &&
        top > furnace_pos?.y &&
        top < furnace_pos?.y + furnace_pos?.height
      ) {
        if (!actPanelOpen && !hidden) {
          addCoal();
          // remove the coal from the screen
          hidden = true;
        }
      }
    }
  }
</script>

<svelte:window on:mousemove={onMouseMove} on:mouseup={onMouseUp} />
{#if !hidden}
  <img
    src="/Coal.png"
    alt="Coal"
    style="top: {top}px; left: {left}px;"
    draggable="false"
    class="draggable"
    on:mousedown={onMouseDown}
  />
{/if}

<style>
  img {
    position: absolute;
    user-select: none;
    object-fit: contain;
    border-radius: 50%;
    border: 2px solid rgb(236, 217, 45);
    background-color: #ffffff8d;
    z-index: 3;
  }
  img:hover {
    cursor: pointer;
    border: 2px solid green;
  }
</style>
