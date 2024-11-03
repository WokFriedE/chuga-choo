<script>
  let hasGlass = $state(false);
  let {
    width = $bindable(),
    height = $bindable(),
    x = $bindable(),
    y = $bindable(),
  } = $props();
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
    <div class="glass">
      <div class="hole">
        <div class="fire"></div>
      </div>
    </div>
  {:else}
    <div class="hole">
      <div class="fire"></div>
    </div>
  {/if}
</button>

<style>
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
  .fire {
    width: 8em;
    height: 8em;
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
  .square {
    background: url("/plate.jpg");
    width: 15em;
    height: 15em;
    display: flex;
    justify-content: center;
    align-items: center;
    border: none;
  }
  .hole {
    background-color: #000;
    border-radius: 50%;
  }
</style>
