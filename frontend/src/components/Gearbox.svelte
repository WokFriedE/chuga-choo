<script>
  import { spring } from "svelte/motion";
  import { writable } from "svelte/store";

  let { size, val = $bindable(5) } = $props();
  let lever;
  let activeTick = writable(0); // Use writable store for reactive state

  // Define tick values for positions: 5, 4, 3, 2, 1, BRAKE, REVERSE
  const box_height = (571 / 171) * size;
  const tickLabels = ["5", "4", "3", "2", "1", "BRAKE", "REVERSE"];
  const ticks = [
    0,
    (1 / 6) * box_height,
    (2 / 6) * box_height,
    (3 / 6) * box_height,
    (4 / 6) * box_height,
    (5 / 6) * box_height,
    box_height,
  ];

  let verticalSpring = spring(0, {
    stiffness: 0.1,
    damping: 0.3,
  });

  function makeDraggable() {
    lever.style.position = "absolute";
    let initialY = 0;
    let currentY = 0;

    lever.onmousedown = (e) => {
      e.preventDefault();
      initialY = e.clientY - currentY;

      document.onmousemove = (event) => {
        // Calculate new position based on displacement from initial click
        currentY = Math.max(
          0,
          Math.min(event.clientY - initialY, ticks[ticks.length - 1])
        );
        verticalSpring.set(currentY);

        // Determine the closest tick dynamically during movement
        let closestTick = ticks.reduce((prev, curr) => {
          return Math.abs(curr - currentY) < Math.abs(prev - currentY)
            ? curr
            : prev;
        }, ticks[0]);

        // Update activeTick dynamically
        activeTick.set(ticks.indexOf(closestTick));
      };

      document.onmouseup = () => {
        // let audio = new Audio("/choochoo.mp3");
        // audio.play();

        document.onmousemove = null;
        document.onmouseup = null;

        // Snap to the nearest tick on mouse release
        let closestTick = ticks.reduce((prev, curr) => {
          return Math.abs(curr - currentY) < Math.abs(prev - currentY)
            ? curr
            : prev;
        }, ticks[0]);

        // Update spring and active tick to the snapped position
        verticalSpring.set(closestTick);
        currentY = closestTick; // Maintain the snapped position
        activeTick.set(ticks.indexOf(closestTick));

        let activeLabel = tickLabels[ticks.indexOf(closestTick)];
        if (activeLabel === "BRAKE") {
          val = 0;
        } else if (activeLabel === "REVERSE") {
          val = -1;
        } else {
          val = parseInt(activeLabel);
        }
      };
    };
  }
</script>

<div class="lever-container" style="position: relative; width: ${size}px;">
  <img
    draggable="false"
    src="/gearbox_handle.png"
    alt="lever"
    width={`${size}px`}
    bind:this={lever}
    on:load={makeDraggable}
    style:transform={`translateY(${$verticalSpring}px)`}
  />

  <!-- Tick labels and markers on the right side -->
  <div
    class="ticks-container"
    style="position: absolute; top: 0; right: -100px; height: {(box_height *
      7) /
      6}px; width: 100px; background-color:#404040"
  >
    {#each tickLabels as label, index}
      <div
        class="tick-label"
        style="position: absolute; top: {ticks[
          index
        ]}px; display: flex; align-items: center;"
      >
        <div
          class="tick-mark"
          style="width: 10px; height: 2px; background: black; margin-right: 5px;"
        ></div>
        <span
          style="font-weight: {index === $activeTick
            ? 'bold'
            : 'normal'}; color: {index === $activeTick ? 'red' : 'white'};"
        >
          {label}
        </span>
      </div>
    {/each}
  </div>
</div>
<img
  src="/gearbox_base.png"
  height={`${(box_height * 7) / 6}px`}
  draggable="false"
/>

<style>
  img {
    transform-origin: 50% 100%;
    transition: transform 0.1s;
  }
  .ticks-container {
    width: 50px;
  }
  .tick-label {
    font-size: 1em;
  }
  .tick-mark {
    background-color: black;
  }
</style>
