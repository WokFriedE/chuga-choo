<script>
  import { store_val } from "./lib/datastore.js";
  import RoundLever from "./components/RoundLever.svelte";
</script>

<h1>
  {$store_val["gesture"]}
</h1>
<div>
  <RoundLever />
</div>

<style>
  div {
    width: 50%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  h1 {
    position: absolute;
    top: 50%;
    left: 50%;
    z-index: 10;
    transform: translate(-50%, -50%);
  }
</style>
