<script>
  import { spring} from "svelte/motion";
  let { size, val = $bindable() } = $props();
  let lever;

  // Initialize spring with parameters for smooth return
  let verticalSpring = spring(0, {
    stiffness: 0.1, // Increased stiffness for a slightly stronger pull-back effect
    damping: 0.3, // Damping to control the bounciness on release
  });

  function makeDraggable() {
    lever.style.position = "absolute";
    let initialY = 0;

    lever.onmousedown = (e) => {
      e.preventDefault();
      initialY = e.clientY;

      // Track mouse movement
      document.onmousemove = (event) => {
        let displacement = event.clientY - initialY;
        verticalSpring.set(Math.min(displacement, 200));
        val = Math.min(Math.max(displacement, 0), 200) / 200
      };

      // Reset when mouse is released
      document.onmouseup = () => {
        let audio = new Audio("/choochoo.mp3");

        audio.play();

        document.onmousemove = null;
        document.onmouseup = null;

        // Reset to zero by setting the spring to 0
        verticalSpring.set(0);
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
