<script>
  let {
    CoalIndicator = $bindable(),
    hasGlass = $bindable(),
    width = $bindable(),
    height = $bindable(),
    x = $bindable(),
    y = $bindable(),
  } = $props();
  hasGlass = false;
  let elmrect = $state({});
  $effect(() => {
    width = elmrect?.getBoundingClientRect().width;
    height = elmrect?.getBoundingClientRect().height;
    x = elmrect?.getBoundingClientRect().x;
    y = elmrect?.getBoundingClientRect().y;
  });
</script>

<button
  class="square"
  onclick={() => (hasGlass = !hasGlass)}
  bind:this={elmrect}
>
  {#if hasGlass}
    <div class="glass dim">
      <div class="hole dim">
        <div class="fire dim"></div>
      </div>
    </div>
  {:else}
    <div class="hole">
      <div class="fire"></div>
    </div>
  {/if}
  <p class="coal_left">
    {CoalIndicator}
  </p>
</button>

<style>
  .coal_left {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-size: 2em;
  }
  .square {
    background: url("/black-cast-iron-background.png");
    width: 40em;
    height: 20em;
    position: absolute;
    left: 100px;
    top: 600px;
    display: flex;
    justify-content: center;
    align-items: center;
    border: none;
  }
  .glass {
    width: 10em;
    height: 10em;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(2px);
    border: 3px solid #a45c30;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .hole {
    width: 8em;
    height: 8em;
    border-radius: 50%;
    background-color: #000;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .fire {
    width: 6em;
    height: 6em;
    border-radius: 50%;
    filter: blur(1em);
    background: radial-gradient(
      circle,
      #ff9100 0%,
      #ff0000 25%,
      #d9bd30 39%,
      #eb5611 40%,
      #ff0000 100%
    );
    animation: fireFlicker 2s infinite;
  }
  @keyframes fireFlicker {
    0% {
      opacity: 0.8;
      scale: 1.1;
    }
    50% {
      opacity: 0.9;
      scale: 1.05;
    }
    100% {
      opacity: 0.8;
      scale: 1.1;
    }
  }
  .fire.dim {
    width: 4em;
    height: 4em;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    z-index: -1;
  }
  .glass.dim {
    position: relative;
  }
  .glass.dim::before {
    content: "";
    width: 10em;
    height: 10em;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(2px);
    border: 3px solid #a45c30;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    z-index: -1;
  }
  .hole.dim {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    z-index: -1;
    background-color: #333;
  }
</style>
