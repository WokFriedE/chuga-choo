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
  import Label from "./components/Label.svelte";
  import Help from "./components/Help.svelte";
  // setInterval(() => {
  // dialNumber++;
  // if (dialNumber > 100) {
  // dialNumber = 0;
  // }
  // }, 100);

  let coalArr = $state(new Array(10));
  //add a random chance of coal appearing every 10 seconds
  setInterval(() => {
    if (Math.random() > 0.15 && coalArr.length < 10) {
      coalArr.push("");
    }
  }, 5000);

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
  let actGear = $state(5);
  let actEngineIntake = $state(0);
  let actFurnaceIntake = $state(0);

  let session_id = $state();
  async function StartGame() {
    let startRes = await (
      await fetch("https://api.chuggachugga-choochoo.tech/start")
    ).json();
    console.log(startRes);
    session_id = startRes["id"];

    setInterval(() => {
      ActObserve();
    }, 1000);
  }
  $effect(() => {
    if (simTemp > 700) {
      // reset the game
      simTemp = 20;
      simCoal = 0;
      simP1 = 0;
      simP2 = 0;
      simP3 = 0;
      simSpeed = 0;
      actAddCoal = 0;
      actDumpCoal = false;
      actPanelOpen = false;
      actExhaustOpen = 0;
      actGear = 0;
      actEngineIntake = 0;
      actFurnaceIntake = 0;
      // get a new session id
      StartGame().then(() => {
        window.location.href = "/fail.gif";
      });
    }
  });
  async function ActObserve() {
    var postHeaders = new Headers();
    postHeaders.append("Content-Type", "application/json");
    let actRes = await fetch(
      `https://api.chuggachugga-choochoo.tech/actions?id=${session_id}`,
      {
        method: "POST",
        headers: postHeaders,
        body: JSON.stringify({
          panel_open: actPanelOpen,
          add_coal: actAddCoal,
          dump_coal: actDumpCoal,
          add_water: 0,
          drain_water: 0,
          exhaut_openness: actExhaustOpen,
          gear: actGear,
          engine_intake: actEngineIntake,
          furnace_intake: actFurnaceIntake,
        }),
        redirect: "follow",
      }
    );

    let statusUpdate = await (
      await fetch(
        `https://api.chuggachugga-choochoo.tech/status?id=${session_id}`
      )
    ).json();
    simTemp = statusUpdate["engine_temperature"];
    simCoal = statusUpdate["fuel_weight"];
    simP1 = statusUpdate["cond_boiler_pressure"];
    simP2 = statusUpdate["boiler_engine_pressure"];
    simP3 = statusUpdate["engine_cond_pressure"];
    simSpeed = statusUpdate["speed"];

    actAddCoal = 0;
    actDumpCoal = false;
  }

  StartGame();
  // set a css variable globally
  $effect(() => {
    document.documentElement.style.setProperty("--shake-speed", simSpeed);
  });
  $effect(() => {
    console.log(simCoal);
  });
</script>

<svelte:window
  on:click|once={() => {
    let audio = new Audio("/bgsnd.mp3");
    audio.play();
    audio.volume = 0.4;
    audio.loop = true;
    // random chance every 100 seconds
    setInterval(() => {
      if (Math.random() > 0.25) {
        let audio2 = new Audio("/honkhonk.mp3");
        audio2.play();
        audio2.volume = 0.7;
      }
    }, 30000);
  }}
/>
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
  <div class="poslable_1">
    <Label label="Emergency Dump" />
  </div>
</div>
<div class="cord">
  <PullCord size="200" bind:val={actExhaustOpen} />
</div>
<div class="crnk1">
  <Crank size={"1.5"} bind:val={actEngineIntake} />
  <br />
  <br />
  <br />
  <Label label="Engine Intake" />
</div>
<div class="crnk2">
  <Crank size={"1.5"} bind:val={actFurnaceIntake} />
  <br />
  <br />
  <br />
  <Label label="Furnace Intake" />
</div>
<div style="position: absolute; left:1300px; top:470px">
  <Gearbox size="100" bind:val={actGear}></Gearbox>
</div>
<!-- <Coal bind:x={} /> -->

{#each coalArr as coalpc}
  <Coal
    addCoal={() => {
      actAddCoal += 10;
      console.log(actAddCoal);
    }}
    bind:actPanelOpen
    furnace_pos={{
      x: coalVals_x,
      y: coalVals_y,
      width: coalVals_width,
      height: coalVals_height,
    }}
  />
{/each}
<BigBurny
  bind:width={coalVals_width}
  bind:height={coalVals_height}
  bind:x={coalVals_x}
  bind:y={coalVals_y}
  bind:hasGlass={actPanelOpen}
  bind:CoalIndicator={simCoal}
/>
<div style="position: absolute; left: 250px; top: 800px">
  <Label label="Furnace" />
</div>
<div class="help">
  <Help />
</div>

<!-- <div class="light1">
  <Light />
</div> -->
<!-- <div class="tv">
  <Tv />
</div> -->

<style>
  .poslable_1 {
    position: absolute;
    top: 8em;
    left: -5em;
  }
  .help {
    position: absolute;
    top: 1em;
    right: 1em;
  }
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
    /* animation: verticalshake calc(var(--shake-speed) / 100s) infinite; */
    animation: verticalshake 1s infinite linear;
  }
  @keyframes verticalshake {
    0% {
      background-position: 0px 0px;
      transform: translate(0px, 0px);
    }
    50% {
      background-position: 0px 2px;
      transform: translate(0px, calc(var(--shake-speed) * 2px));
    }
    100% {
      background-position: 0px 0px;
      transform: translate(0px, 0px);
    }
  }
</style>
