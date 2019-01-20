const STICKS = 100;
const SPEED = 0.1;

class Range {
  constructor(open, close) {
    this._open = open;
    this._close = close;
  }

  get open() {
    return this._open;
  }

  get close() {
    return this._close;
  }
}

class Stick {
  constructor() {
    this._current = new Range(0, 0);
    this._target = new Range(0, 0);
  }

  get current() {
    return this._current;
  }

  get target() {
    return this._target;
  }

  update(open, close) {
    this._current = this._target;
    this._target = new Range(open, close);
  }

  draw() {
    this._current = new Range(
      this._current.open + (this._target.open - this._current.open) * SPEED,
      this._current.close + (this._target.close - this._current.close) * SPEED
    );
  }
}

class Bar {
  constructor() {
    this._current = 0;
    this._target = 0;
  }

  get current() {
    return this._current;
  }

  update(sell) {
    this._current = this._target;
    this._target = sell;
  }

  draw() {
    this._current += (this._target - this._current) * SPEED;
  }
}

const sticks = [];
const bars = [];

let pastCloses = [];
let pastSells = [];

for (let i = 0; i < STICKS; i++) {
  sticks.push(new Stick());
  bars.push(new Bar());

  pastCloses.push(0);
  pastSells.push(0);
}

pastCloses.push(0);

export function addCloses(closes) {
  pastCloses = closes;

  const max = Math.max(...closes);
  const min = Math.min(...closes);

  const range = max - min;
  const normalised = closes.map(close => (close - min) / range);

  sticks[0].update(0, normalised[0]);

  for (let i = 0; i < STICKS; i++) {
    sticks[i].update(normalised[i], normalised[i + 1]);
  }
}

export function addSells(sells) {
  pastSells = sells;

  const max = Math.max(...sells);
  const normalised = sells.map(sell => sell / max);

  for (let i = 0; i < STICKS; i++) {
    bars[i].update(normalised[i]);
  }
}

export function newEntry(close, sell) {
  pastCloses.push(close);
  pastCloses.shift();

  pastSells.push(sell);
  pastSells.shift();

  addCloses(pastCloses);
  addSells(pastSells);
}

new p5(sketch => {
  const barchart = 0.3 * sketch.windowHeight;
  const candlestick = sketch.windowHeight - barchart;
  const sector = sketch.windowWidth / (STICKS * 2);

  sketch.setup = function() {
    sketch.createCanvas(sketch.windowWidth, sketch.windowHeight);

    sketch.noStroke();
  };

  sketch.draw = function() {
    sketch.background("#1c3d5a");

    for (let i = 0; i < STICKS; i++) {
      const stick = sticks[i];
      stick.draw();

      const range = stick.current;

      if (range.open > range.close) {
        sketch.fill("#e3342f");
        sketch.rect(
          sector * (i + 0.25) * 2,
          (1 - range.open) * (candlestick - 50) + 25,
          sector,
          (range.open - range.close) * (candlestick - 50),
          5
        );
      } else {
        sketch.fill("#38c172");
        sketch.rect(
          sector * (i + 0.25) * 2,
          (1 - range.close) * (candlestick - 50) + 25,
          sector,
          (range.close - range.open) * (candlestick - 50),
          5
        );
      }
    }

    sketch.fill("rgba(0, 0, 0, 0.5)");
    sketch.rect(0, candlestick, sketch.windowWidth, barchart);

    for (let i = 0; i < STICKS; i++) {
      const bar = bars[i];
      bar.draw();

      const height = bar.current * barchart - 25;

      sketch.fill("#ffed4a");
      sketch.rect(sector * (i + 0.25) * 2, candlestick + (barchart - height), sector, barchart, 5);
    }
  };
}, document.getElementById("sketch"));
