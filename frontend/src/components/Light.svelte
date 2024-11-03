<script>
  let light = $state(false);
  function toggleLight() {
    light = !light;
  }
</script>

<button onclick={toggleLight}>
  <img
    src="/bulb.png"
    alt="light"
    style={`
    ${light ? "" : "filter:grayscale(100%);"}
    `}
  />
</button>

<style>
  img {
    width: 300px;
    height: 300px;
  }
  button {
    background: none;
    border: none;
  }
</style>
