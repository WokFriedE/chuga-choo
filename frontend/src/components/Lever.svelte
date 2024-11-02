<script>
  import { spring } from "svelte/motion";

  //make the lever draggable to rotate the lever
  let lever;
  let SpringStore = spring(0, {
    stiffness: 0.05,
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
      // pos1 = pos3 - e.clientX;
      // pos2 = pos4 - e.clientY;
      // pos3 = e.clientX;
      // pos4 = e.clientY;
      // lever.style.top = lever.offsetTop - pos2 + "px";
      // lever.style.left = lever.offsetLeft - pos1 + "px";
      // rotate the lever
      let x =
        e.clientX - lever.getBoundingClientRect().left - lever.offsetWidth / 2;
      let y =
        e.clientY - lever.getBoundingClientRect().top - lever.offsetHeight;
      let r = Math.atan2(y, x);
      let deg = r * (180 / Math.PI) + 90;
      console.log(deg);
      SpringStore.set(deg);
    }

    function closeDragElement() {
      document.onmouseup = null;
      document.onmousemove = null;
      close();
    }
  }
  function close() {
    if ($SpringStore > 0) {
      SpringStore.update((val) => val - 1);
      console.log($SpringStore);

      setTimeout(close, 10);
    }
  }
</script>

<img
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
    width: 100px; 
  }
</style>
