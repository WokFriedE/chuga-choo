<script>
  import Crank from "./components/Crank.svelte";
  import Lever from "./components/Lever.svelte";
</script>

<div>
  <Crank />
</div>
<div>
  <Lever />
</div>

<style>
  div {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50vh;
  }
</style>
