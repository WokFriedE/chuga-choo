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
  let left = $state(window.innerWidth * Math.random()); // Adjust this to your actual image width
  let imageHeight = 100; // Adjust this to your actual image height
  let top = $state(window.innerHeight * Math.random()); // Adjust this to your actual image height

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
        if (!actPanelOpen) {
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
    border: 2px solid rgb(255, 255, 255);
    background-color: #ffffffac;
    z-index: 3;
  }
</style>
