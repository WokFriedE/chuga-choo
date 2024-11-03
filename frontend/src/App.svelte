<script>
  import Coal from "./components/Coal.svelte";
  import Crank from "./components/Crank.svelte";
  import Dial from "./components/Dial.svelte";
  import BigBurny from "./components/BigBurny.svelte";
  import Lever from "./components/Lever.svelte";
  import Light from "./components/Light.svelte";
  import PullCord from "./components/PullCord.svelte";
  import Tv from "./components/TV.svelte";
  // setInterval(() => {
  // dialNumber++;
  // if (dialNumber > 100) {
  // dialNumber = 0;
  // }
  // }, 100);
  let coalArr = $state([
    { x: 0, y: 0 },
    { x: 0, y: 0 },
    { x: 0, y: 0 },
    { x: 0, y: 0 },
    { x: 0, y: 0 },
  ]);
  let coalVals_height = $state(0);
  let coalVals_width = $state(0);
  let coalVals_x = $state(0);
  let coalVals_y = $state(0);
  let holdingCoal = $state(false);
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

<Dial size={200} bind:number={dialNumber} max={100} />
<div class="lvr">
  <Lever size="350" />
</div>
<div class="cord">
  <PullCord size="200" />
</div>
<div class="crnk1">
  <Crank size={"1.5"} bind:val={CrankVal} />
</div>
<div class="crnk2">
  <Crank size={"1.5"} bind:val={CrankVal} />
</div>
<!-- <Coal bind:x={} /> -->
{#each coalArr as coalpc}
  <Coal
    onmouseup={() => {
      for (let i = 0; i < coalArr.length; i++) {
        //check if the coal is in the hole
        //check for overlap
        //if overlap, remove the coal from the array
        //and add to the fire
        let coal = coalArr[i];
        // let hole = holeElm.getBoundingClientRect();
        let tolerance = 10;
        if (
          coal.x > coalVals_x - tolerance &&
          coal.x < coalVals_x + coalVals_width + tolerance &&
          coal.y > coalVals_y - tolerance &&
          coal.y < coalVals_y + coalVals_height + tolerance
        ) {
          coalArr.splice(i, 1);
          // holeElm.appendChild(coal);
        }
      }
    }}
    bind:x={coalpc.x}
    bind:y={coalpc.y}
  />
{/each}
<BigBurny
  bind:width={coalVals_width}
  bind:height={coalVals_height}
  bind:x={coalVals_x}
  bind:y={coalVals_y}
/>
<div class="light1">
  <Light />
</div>
<div class="tv">
  <Tv />
</div>

<style>
  /* div {  
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50vh;
  } */
  .crnk1 {
    margin: 3em;
  }
  .crnk2 {
    position: absolute;
    left: 80em;
    top: 20em;
  }
  .cord {
    position: absolute;
    top: -13em;
    left: 85em;
  }
  .lvr {
    position: absolute;
    top: 10em;
    left: 53em;
  }
  .tv {
    position: absolute;
    top: 35em;
    left: 70em;
    z-index: -1;
  }
  .light1 {
    position: absolute;
    top: 0em;
    left: 40em;
    transform: rotate(180deg);
  }
  :global(body) {
    background-image: url("/bg.png");
    background-attachment: fixed;
    background-size: cover;
    background-repeat: no-repeat;
    animation: verticalshake 2s infinite;
  }
  @keyframes verticalshake {
    0% {
      background-position: 0px 0px;
      transform: translate(0px, 0px);
    }
    50% {
      background-position: 0px 2px;
      transform: translate(0px, 2px);
    }
    100% {
      background-position: 0px 0px;
      transform: translate(0px, 0px);
    }
  }
</style>
