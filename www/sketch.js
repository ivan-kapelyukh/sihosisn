class Box {
  constructor() {
    this.open = 0;
    this.close = 0;
    this.target_open = 0;
    this.target_close = 0;
  }

  update(close) {
    this.open = this.target_open;
    this.close = this.target_close;

    this.target_open = this.close;
    this.target_close = close;
  }

  draw() {
    if (this.open > this.target_open) {
      this.open -= (this.open - this.target_open) * 0.1;
    } else {
      this.open += (this.target_open - this.open) * 0.1;
    }

    if (this.close > this.target_close) {
      this.close -= (this.close - this.target_close) * 0.1;
    } else {
      this.close += (this.target_close - this.close) * 0.1;
    }
  }
}

const n = 100;
const boxes = [];

for (let i = 0; i < n; i++) {
  const box = new Box();
  boxes.push(box);
}

for (let i = 0; i < n; i++) {
  const value = 2 * Math.random() - 1;
  boxes[n - 1].update(value);

  for (let i = n - 2; i >= 0; i--) {
    boxes[i].update(boxes[i + 1].close);
  }
}

setInterval(() => {
  const value = 2 * Math.random() - 1;
  boxes[n - 1].update(value);

  for (let i = n - 2; i >= 0; i--) {
    boxes[i].update(boxes[i + 1].close);
  }

  // console.log(boxes);
}, 5000);

new p5(sketch => {
  const mid = sketch.windowHeight / 2;
  const sector = sketch.windowWidth / (n * 2);

  sketch.setup = function() {
    sketch.createCanvas(sketch.windowWidth, sketch.windowHeight);

    sketch.noStroke();
  };

  sketch.draw = function() {
    sketch.background("#1c3d5a");

    for (let i = 0; i < n; i++) {
      const box = boxes[i];
      box.draw();

      if (box.open > box.close) {
        sketch.fill("#e3342f");
        sketch.rect(
          sector * (i + 0.5) * 2,
          mid - box.open * 0.5 * sketch.windowHeight,
          sector,
          (box.open - box.close) * 0.5 * sketch.windowHeight,
          5
        );
      } else {
        sketch.fill("#38c172");
        sketch.rect(
          sector * (i + 0.5) * 2,
          mid - box.close * 0.5 * sketch.windowHeight,
          sector,
          (box.close - box.open) * 0.5 * sketch.windowHeight,
          5
        );
      }
    }
  };
}, document.getElementById("sketch"));
