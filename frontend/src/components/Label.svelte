<script>
  let { label } = $props();
</script>

<span class="labelwrap">
  <img src="/plate.png" alt="Plate" class="label" />
  <p class="labeltxt">{label}</p>
</span>

<style>
  img {
    width: 250px;
    height: 90px;
  }
  .labelwrap {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  p {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    margin: 0;
    color: #221b04;
    font-weight: bold;
    font-size: 1.5em;
    text-align: center;
  }
</style>
