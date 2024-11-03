<div>
  <img src="/tv.png" alt="TV" />
  <img src="/view.gif" alt="view" class="view" />
</div>

<style>
  div {
    position: relative;
    width: 500px;
    height: 300px;
    overflow: hidden;
  }
  div img {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
  }
  .view {
    z-index: -1;
    margin: 1em;
    height: 80%;
    width: 80%;
  }
</style>
