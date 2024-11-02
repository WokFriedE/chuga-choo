<script>
  import { store_val } from "../lib/datastore.js";
  let coords = $store_val["landmarks"];
  let gesture = $store_val["gesture"];
  let rect = $state(null);
  let leverDegs = $state(0);
  let center = $state({
    x: 0,
    y: 0,
    z: 0,
  });
  let delta = $state(0);
  store_val.subscribe((value) => {
    function getAvg(val) {
      let pt1 = val[0];
      let pt2 = val[17];
      let pt3 = val[5];
      if (pt1 == undefined || pt2 == undefined || pt3 == undefined) {
        console.log("Undefined");
        return;
      }
      let xavg = (pt1.x + pt2.x + pt3.x) / 3;
      let yavg = (pt1.y + pt2.y + pt3.y) / 3;
      let zavg = (pt1.z + pt2.z + pt3.z) / 3;
      if ($store_val["gesture"] == "Closed_Fist") {
        return {
          x: xavg * window.innerWidth,
          y: yavg * window.innerHeight,
          z: zavg,
        };
      }
    }

    if (value["landmarks"] && value["landmarks"].length > 0) {
      delta = Math.sqrt(
        Math.pow(
          window.innerWidth -
            center?.x -
            (rect?.getBoundingClientRect()?.width / 2 +
              rect?.getBoundingClientRect()?.x),
          2
        ) +
          Math.pow(
            center?.y -
              (rect?.getBoundingClientRect()?.height / 2 +
                rect?.getBoundingClientRect()?.top),
            2
          )
      );
      console.log(delta);
      center = getAvg(value["landmarks"]);
      if (delta < 500) {
        //set a max distance for the lever to move of the height of the lever, and a min distance of 0
        // if (
        //   center?.y > rect?.getBoundingClientRect()?.y &&
        //   center?.y <
        //     rect?.getBoundingClientRect()?.y +
        //       rect?.getBoundingClientRect()?.height &&
        //   center?.x > rect?.getBoundingClientRect()?.x &&
        //   center?.x <
        //     rect?.getBoundingClientRect()?.x +
        //       rect?.getBoundingClientRect()?.width
        // ) {
        // leverDegs =
        //find the angle from the bottom of the lever to the center of the hand
        let angle = Math.atan2(
          rect?.getBoundingClientRect()?.height -
            rect?.getBoundingClientRect()?.y,
          center?.x - rect?.getBoundingClientRect()?.x
        );
        angle = angle ** 2;
        //convert the angle to degrees
        leverDegs = (angle * 180) / Math.PI;
        console.log(leverDegs + "test");
      }
      // }
      // if (
      //   center?.x + 100 >
      //     rect?.getBoundingClientRect()?.width / 2 +
      //       rect?.getBoundingClientRect()?.x &&
      //   center?.x - 100 <
      //     rect?.getBoundingClientRect()?.width / 2 +
      //       rect?.getBoundingClientRect()?.x &&
      //   center?.y + 100 >
      //     rect?.getBoundingClientRect()?.height / 2 + rect.top &&
      //   center?.y - 100 <
      //     rect?.getBoundingClientRect()?.height / 2 +
      //       rect?.getBoundingClientRect()?.top
      // ) {
      //   console.log("In the center");
      // }
      //get the distance between the center of the screen and the center of the lever
    }
  });
</script>

<div class="lever" style="transform: rotate({leverDegs}deg)" bind:this={rect}>
  <div class="lever__handle"></div>
  {leverDegs}
  <div class="lever__base"></div>
</div>

<style>
  .lever {
    background-color: rgb(117, 83, 10);
    width: 70px;
    height: 400px;
    transform-origin: 50% 100%;
    transition: all 0.1s;
  }
  .lever__handle {
    width: 200%;
    background-color: red;
    height: 1.5em;
    transform: translate(-25%, 0);
  }
</style>
