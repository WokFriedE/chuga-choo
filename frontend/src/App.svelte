<script>
  import Coal from "./components/Coal.svelte";
  import Crank from "./components/Crank.svelte";
  import Dial from "./components/Dial.svelte";
  import BigBurny from "./components/BigBurny.svelte";
  import Lever from "./components/Lever.svelte";
  import Light from "./components/Light.svelte";
  import PullCord from "./components/PullCord.svelte";
  import Tv from "./components/TV.svelte";
  import LogDial from "./components/LogDial.svelte";
  import Gearbox from "./components/Gearbox.svelte";
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

  let simTemp = $state(20);
  // Cond-Boiler Pressure
  let simP1 = $state(0);
  // Boiler-Engine Pressure
  let simP2 = $state(0);
  // Engine-Cond Pressure
  let simP3 = $state(0);
  let simSpeed = $state(0);
  let simCoal = $state(0);

  let actAddCoal = $state(0);
  let actDumpCoal = $state(false);
  let actPanelOpen = $state(false);
  let actExhaustOpen = $state(0);
  let actGear = $state(0);
  let actEngineIntake = $state(0);
  let actFurnaceIntake = $state(0);


  let session_id = $state()
  async function StartGame() {
    session_id = (await fetch("https://api.chuggachugga-choochoo.tech/start"))['id'];

    setInterval(() => {
      ActObserve();
    }, 1000);
  }
  async function ActObserve() {
    var postHeaders = new Headers();
    postHeaders.append("Content-Type", "application/json");
    let actRes = await fetch(
      `https://api.chuggachugga-choochoo.tech/actions?id=${session_id}`,
      {
        method: 'POST',
        headers: postHeaders,
        body: JSON.stringify({
          'panel_open':actPanelOpen,
          'add_coal': actAddCoal,
          'dump_coal': actDumpCoal,
          'add_water':0,
          'drain_water':0,
          'exhaut_openness':actExhaustOpen,
          'gear':actGear,
          'engine_intake':actEngineIntake,
          'furnace_intake':actFurnaceIntake
        }),
        redirect: 'follow'
      }
    )
    let statusUpdate = await fetch(`https://api.chuggachugga-choochoo.tech/status?id=${session_id}`)
    simTemp = statusUpdate['engine_temperature']
    simCoal = statusUpdate['fuel_weight']
    simP1 = statusUpdate['cond_boiler_pressure']
    simP2 = statusUpdate['boiler_engine_pressure']
    simP3 = statusUpdate['engine_cond_pressure']
    simSpeed = statusUpdate['speed']

    actAddCoal = 0
    actDumpCoal = false
  }

  StartGame()
</script>

<!-- <button>start</button> -->
<div style="display: flex; flex-direction: column;">
  <div style="display: flex; flex-direction: row; align-items: center;">
    <Dial size={200} bind:number={simSpeed} max={200} label="Speed" />
    <Dial size={150} bind:number={simTemp} max={400} label="Temp." />
  </div>
  <div style="display: flex; flex-direction: row;">
    <LogDial size={75} bind:number={simP1} max={70000000} label="Pressure 1" />
    <LogDial size={75} bind:number={simP2} max={70000000} label="Pressure 2" />
    <LogDial size={75} bind:number={simP3} max={70000000} label="Pressure 3" />
  </div>
</div>
<div class="lvr">
  <Lever
    onleverpulled={() => {
      actDumpCoal = true;
    }}
    size="350"
  />
</div>
<div class="cord">
  <PullCord size="200" bind:val={actExhaustOpen} />
</div>
<div class="crnk1">
  <Crank size={"1.5"} bind:val={actEngineIntake} />
</div>
<div class="crnk2">
  <Crank size={"1.5"} bind:val={actFurnaceIntake} />
</div>
<div style="position: absolute; left:1300px; top:470px">
  <Gearbox size="100" bind:val={actGear}></Gearbox>
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
  bind:hasGlass={actPanelOpen}
/>

<!-- <div class="light1">
  <Light />
</div> -->
<!-- <div class="tv">
  <Tv />
</div> -->

<style>
  /* div {  
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50vh;
  } */
  .crnk1 {
    position: absolute;
    left: 40em;
    top: 23em;
  }
  .crnk2 {
    position: absolute;
    left: 60em;
    top: 33em;
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
