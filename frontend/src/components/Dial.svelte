<script>
  let { number = $bindable(), max, size } = $props();
  let pin, dial;
  let angle = $state(0);
  $effect(() => {
    angle = (number / max) * 360;
  });
  let tickmarks = size > 100 ? 100 : 50;
  let dial_marks = new Array(tickmarks).fill(0).map((_, i) => i);
</script>

<div
  class="dial"
  bind:this={dial}
  style={`width: ${size}px; height: ${size}px;`}
>
  {#each dial_marks as mark}
    <div
      style={`transform: rotate(${mark * (360 / tickmarks)}deg);`}
      class="mark"
    ></div>
  {/each}
  <p style={`font-size: ${size / 10}px;`}>{Math.floor(number)}</p>
  <div
    class="pin"
    bind:this={pin}
    style={`transform: rotate(${180 - angle + 90}deg);`}
  ></div>
</div>

<style>
  .dial {
    position: relative;
    width: 10em;
    height: 10em;
    border-radius: 50%;
    background: radial-gradient(
      circle,
      #e18f5d 0%,
      #a45c30 25%,
      #a45c30 39%,
      #e4d1c0 40%,
      #e4d1c0 100%
    );
    box-sizing: border-box;
    box-shadow:
      inset 0 0 0.5em #000,
      0 0 0 0.2em #a67f4a;
  }

  /* make the pin a line */
  .pin {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0.1em;
    height: 50%;
    background: #000;
    transform-origin: 50% 0%;
    box-shadow: -1px -1px 1px #00000070;
    transition: all 0.1s;
  }

  .dial::after {
    /* add a ring with tickmarks */
    content: "";
    position: absolute;
    top: -0.2em;
    left: -0.2em;
    width: 100%;
    height: 100%;
    border: 0.2em dashed #000;
    border-radius: 50%;
  }
  p {
    position: absolute;
    top: 28%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 1.5em;
    color: #fff;
  }
  .mark {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0.05em;
    height: 50%;
    background: linear-gradient(10deg, #000, #000) 95% 95% / 1em 1em no-repeat;
    transform-origin: 50% 0%;
  }
</style>
