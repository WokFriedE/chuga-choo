<script>
  import { spring } from "svelte/motion";
  let { size } = $props();
  //make the lever draggable to rotate the lever
  let lever;
  let SpringStore = spring(0, {
    stiffness: 0.02,
    damping: 0.05,
  });
  function makeDraggable() {
    lever.style.position = "absolute";
    let pos3 = 0,
      pos4 = 0;
    lever.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
      e = e || window.event;
      e.preventDefault();
      pos3 = e.clientX;
      pos4 = e.clientY;
      document.onmouseup = closeDragElement;
      document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
      e = e || window.event;
      e.preventDefault();
      let x =
        e.clientX - lever.getBoundingClientRect().left - lever.offsetWidth / 2;
      let y =
        e.clientY - lever.getBoundingClientRect().top - lever.offsetHeight;
      let r = Math.atan2(y, x);
      let deg = r * (180 / Math.PI) + 90;
      console.log(deg);
      SpringStore.set(Math.min(Math.max(deg, 0), 180));
    }

    function closeDragElement() {
      document.onmouseup = null;
      document.onmousemove = null;
      close();
    }
  }
  function close() {
    if ($SpringStore > 0) {
      SpringStore.update((val) => Math.max(val - 4, 0));

      setTimeout(close, 10);
    }
  }
</script>

<img
  style:width={`${size}px`}
  src="/lever.png"
  alt="lever"
  style:transform={`rotate(${$SpringStore}deg)`}
  bind:this={lever}
  on:load={makeDraggable}
/>

<style>
  img {
    transform-origin: 50% 100%;
    transition: transform 0.1s;
  }
</style>
