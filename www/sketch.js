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

  update(close) {
    this._current = this._target;
    this._target = new Range(this._current.close, close);
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

for (let i = 0; i < STICKS; i++) {
  sticks.push(new Stick());
  bars.push(new Bar());
}

export function newClose(close, sell) {
  sticks[STICKS - 1].update(close);
  bars[STICKS - 1].update(sell);

  for (let i = STICKS - 2; i >= 0; i--) {
    sticks[i].update(sticks[i + 1].current.close);
    bars[i].update(bars[i + 1].current);
  }
}

new p5(sketch => {
  const barchart = 200;
  const candlestick = sketch.windowHeight - barchart;
  const mid = candlestick / 2;
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
        // if (i > 20 && i < 30) sketch.fill("#ffed4a");
        sketch.rect(
          sector * (i + 0.5) * 2,
          mid - range.open * 0.5 * (candlestick - 50),
          sector,
          (range.open - range.close) * 0.5 * (candlestick - 50),
          5
        );
      } else {
        sketch.fill("#38c172");
        // if (i > 20 && i < 30) sketch.fill("#ffed4a");
        sketch.rect(
          sector * (i + 0.5) * 2,
          mid - range.close * 0.5 * (candlestick - 50),
          sector,
          (range.close - range.open) * 0.5 * (candlestick - 50),
          5
        );
      }
    }

    sketch.fill("#12283a");
    sketch.rect(0, candlestick, sketch.windowWidth, barchart);

    for (let i = 0; i < STICKS; i++) {
      const bar = bars[i];
      bar.draw();

      const height = bar.current * barchart - 25;

      sketch.fill("#ffed4a");
      sketch.rect(sector * (i + 0.5) * 2, candlestick + (barchart - height), sector, barchart, 5);
    }
  };
}, document.getElementById("sketch"));
