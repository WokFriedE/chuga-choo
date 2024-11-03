<script>
  let { percent = $bindable() } = $props();
  percent = (percent / 40000) * 100;
</script>

<div class="trainwrap">
  <img
    src="/train.gif"
    alt="train"
    style="left: {percent > 100 ? 100 : percent}%;"
  />
  <div
    style="left: {percent > 100 ? 100 : percent + 5}%;"
    class="imgline"
  ></div>
  <progress value={percent} max="100"></progress>
  <div class="line">
    <p>Progress</p>
  </div>
</div>

<style>
  .line {
    background-image: url("/gearbox_handle.png");
    background-size: 100% 100%;
    background-repeat: no-repeat;
    height: 2em;
  }
  .trainwrap {
    position: relative;
    width: 100%;
    min-width: 20em;
  }
  img {
    position: absolute;
    bottom: 30px;
    width: 100px;
    z-index: -1;
    transform: translateX(-50%);
    box-shadow: 0 0 10px 5px rgba(255, 255, 255, 0.25) inset;
    background-color: #9d753e;
    animation: wobble 2s infinite;
    transition: 1s linear;
  }
  /* make the image line under the train */
  .imgline {
    position: absolute;
    bottom: 0px;
    width: 5px;
    height: 40px;
    background-color: #000000;
    z-index: 10;
    transition: 1s linear;
  }
  progress {
    display: none;
    position: absolute;
    bottom: 0;
    width: 20em;
  }
  p {
    color: white;
    font-size: 1.5em;
    text-align: center;
  }
  @keyframes wobble {
    0% {
      transform: rotate(0deg);
    }
    25% {
      transform: rotate(5deg);
    }
    50% {
      transform: rotate(0deg);
    }
    75% {
      transform: rotate(-5deg);
    }
    100% {
      transform: rotate(0deg);
    }
  }
</style>
