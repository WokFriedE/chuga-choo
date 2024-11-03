<script>
  import { spring } from "svelte/motion";
  let { size } = $props();
  let lever;

  // Define tick values for positions: 5, 4, 3, 2, 1, BRAKE, REVERSE
  const ticks = [0, 40, 80, 120, 160, 200, 240]; // Adjust these values based on layout

  let verticalSpring = spring(0, {
    stiffness: 0.1,
    damping: 0.3,
  });

  function makeDraggable() {
    lever.style.position = "absolute";
    let initialY = 0;

    lever.onmousedown = (e) => {
      e.preventDefault();
      initialY = e.clientY;

      document.onmousemove = (event) => {
        let displacement = event.clientY - initialY;
        // Limit displacement within the track bounds
        verticalSpring.set(Math.max(0, Math.min(displacement, ticks[ticks.length - 1])));
      };

      document.onmouseup = () => {
        let audio = new Audio("/choochoo.mp3");
        audio.play();

        document.onmousemove = null;
        document.onmouseup = null;

        // Snap to the nearest tick
        let currentY = verticalSpring.get();
        let closestTick = ticks.reduce((prev, curr) => {
          return Math.abs(curr - currentY) < Math.abs(prev - currentY) ? curr : prev;
        }, ticks[0]);

        // Set spring to the nearest tick
        verticalSpring.set(closestTick);

        // Output position or perform any logic based on position
        let positionIndex = ticks.indexOf(closestTick);
        console.log("Lever position:", ["5", "4", "3", "2", "1", "BRAKE", "REVERSE"][positionIndex]);
      };
    };
  }
</script>

<img
  src="/pull_cord.png"
  alt="lever"
  height={`${size * 3}px`}
  bind:this={lever}
  on:load={makeDraggable}
  style:transform={`translateY(${$verticalSpring}px)`}
/>

<style>
  img {
    transform-origin: 50% 100%;
    transition: transform 0.1s;
  }
</style>
