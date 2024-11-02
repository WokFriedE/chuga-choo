<script>
  import Crank from "./components/Crank.svelte";
  import Dial from "./components/Dial.svelte";
  import Lever from "./components/Lever.svelte";
  let dialNumber = $state(0);
  setInterval(() => {
    dialNumber++;
    if (dialNumber > 100) {
      dialNumber = 0;
    }
  }, 100);
</script>

<div>
  <!-- <Crank /> -->
</div>

<!-- <div> -->
<!-- <Lever /> -->
<!-- </div> -->

<!-- <Dial size={350} bind:number={dialNumber} max={100} /> -->

<style>
  div {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50vh;
  }
  :global(body) {
    background-image: url("/bg.jpg");
  }
</style>
