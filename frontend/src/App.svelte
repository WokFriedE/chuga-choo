<script>
  import Crank from "./components/Crank.svelte";
  import Dial from "./components/Dial.svelte";
  import Lever from "./components/Lever.svelte";
  // setInterval(() => {
  // dialNumber++;
  // if (dialNumber > 100) {
  // dialNumber = 0;
  // }
  // }, 100);
  let CrankVal = $state(0);
  let dialNumber = $state(0);
  $effect(() => {
    dialNumber = CrankVal;
  });
  async function StartGame() {
    let uuid = await fetch("https://chuggachugga-choochoo.tech/api/start");
  }
</script>

<!-- <button>start</button> -->

<Dial size={100} bind:number={dialNumber} max={100} />
<div class="lvr">
  <Lever />
</div>
<div class="crnk">
  <Crank bind:val={CrankVal} />
</div>

<style>
  /* div {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50vh;
  } */
  .crnk {
    margin: 3em;
  }
  .lvr {
    position: absolute;
    top: 16em;
    left: 16em;
  }
  :global(body) {
    background-image: url("/bg.jpg");
  }
</style>
