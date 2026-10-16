<!DOCTYPE html>
<html lang="kk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GameZone — Ойын әлемі</title>

  <style>
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      font-family: Arial, sans-serif;
      color: white;
      background:
        radial-gradient(ellipse at top, #302052, transparent 55%),
        #0d0b18;
    }

    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px 7%;
      border-bottom: 1px solid #302644;
    }

    .logo {
      color: #b99aff;
      font-size: 27px;
      font-weight: bold;
    }

    header a {
      color: #ddd2ff;
      text-decoration: none;
    }

    main {
      width: min(900px, 92%);
      margin: 45px auto;
      text-align: center;
    }

    h1 {
      font-size: clamp(32px, 6vw, 52px);
      margin-bottom: 10px;
    }

    .accent {
      color: #b99aff;
    }

    .subtitle {
      color: #aaa3c1;
      margin-bottom: 30px;
    }

    .game-card {
      background: #171326;
      border: 1px solid #3a2c55;
      border-radius: 20px;
      padding: 20px;
      box-shadow: 0 15px 60px #0005;
    }

    .stats {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 15px;
      color: #ded3ff;
    }

    .stat {
      background: #241c38;
      border-radius: 10px;
      padding: 12px;
      flex: 1;
    }

    .stat strong {
      color: #b99aff;
    }

    canvas {
      display: block;
      width: 100%;
      max-width: 600px;
      margin: auto;
      background: #0a1019;
      border: 1px solid #44345f;
      border-radius: 10px;
      image-rendering: pixelated;
    }

    #message {
      min-height: 24px;
      color: #d8c9ff;
      margin: 15px 0;
    }

    button {
      border: 0;
      border-radius: 10px;
      padding: 12px 19px;
      font-size: 15px;
      font-weight: bold;
      cursor: pointer;
      transition: .2s;
    }

    button:hover {
      transform: translateY(-2px);
      filter: brightness(1.12);
    }

    .primary {
      background: #a77bff;
      color: #130c24;
    }

    .secondary {
      background: #302541;
      color: white;
    }

    .controls {
      display: flex;
      justify-content: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    .arrows {
      display: grid;
      grid-template-columns: repeat(3, 55px);
      grid-template-rows: repeat(2, 45px);
      gap: 6px;
      justify-content: center;
      margin: 20px auto 0;
    }

    .arrows button {
      padding: 5px;
      font-size: 21px;
      touch-action: manipulation;
    }

    .up { grid-column: 2; grid-row: 1; }
    .left { grid-column: 1; grid-row: 2; }
    .down { grid-column: 2; grid-row: 2; }
    .right { grid-column: 3; grid-row: 2; }

    .instructions {
      color: #aaa3c1;
      font-size: 14px;
      line-height: 1.8;
      margin-top: 25px;
    }

    footer {
      text-align: center;
      padding: 25px;
      color: #777087;
      border-top: 1px solid #302644;
    }

    @media (max-width: 500px) {
      header { padding: 17px 5%; }
      .logo { font-size: 22px; }
      main { margin: 30px auto; }
      .game-card { padding: 12px; }
      button { padding: 12px; }
    }
  </style>
</head>

<body>
  <header>
    <div class="logo">🎮 GameZone</div>
    <a href="#game">Ойнау ↓</a>
  </header>

  <main>
    <h1>Ойын <span class="accent">әлемі</span></h1>
    <p class="subtitle">
      Ойна, ұпай жина және өз рекордыңды жаңарт!
    </p>

    <section class="game-card" id="game">
      <div class="stats">
        <div class="stat">
          Ұпай: <strong id="score">0</strong>
        </div>
        <div class="stat">
          Рекорд: <strong id="best">0</strong>
        </div>
      </div>

      <canvas id="board" width="600" height="400"></canvas>

      <p id="message">«Бастау» батырмасын бас!</p>

      <div class="controls">
        <button class="primary" id="start">▶ Бастау</button>
        <button class="secondary" id="pause">⏸ Пауза</button>
        <button class="secondary" id="restart">↻ Қайта бастау</button>
      </div>

      <div class="arrows">
        <button class="secondary up" data-dir="up">⬆️</button>
        <button class="secondary left" data-dir="left">⬅️</button>
        <button class="secondary down" data-dir="down">⬇️</button>
        <button class="secondary right" data-dir="right">➡️</button>
      </div>

      <p class="instructions">
        Компьютерде: ← ↑ → ↓ пернелерімен басқар.<br>
        Телефонда: экрандағы бағыттау батырмаларын қолдан.<br>
        Жасыл нүктелерді же, қабырғаға және өзіңе соғылма!
      </p>
    </section>
  </main>

  <footer>© 2026 GameZone | Менің алғашқы ойын сайтым</footer>

  <script>
    const canvas = document.getElementById("board");
    const ctx = canvas.getContext("2d");
    const scoreText = document.getElementById("score");
    const bestText = document.getElementById("best");
    const message = document.getElementById("message");

    const CELL = 20;
    const COLS = canvas.width / CELL;
    const ROWS = canvas.height / CELL;

    let snake, food, direction, nextDirection;
    let score = 0;
    let best = 0;
    let timer = null;
    let running = false;
    let over = false;

    try {
      best = Number(localStorage.getItem("gamezoneBest")) || 0;
    } catch (e) {
      best = 0;
    }

    bestText.textContent = best;

    function randomFood() {
      let p;
      do {
        p = {
          x: Math.floor(Math.random() * COLS),
          y: Math.floor(Math.random() * ROWS)
        };
      } while (snake.some(s => s.x === p.x && s.y === p.y));

      return p;
    }

    function reset() {
      clearInterval(timer);
      timer = null;
      running = false;
      over = false;
      score = 0;

      snake = [
        { x: 8, y: 10 },
        { x: 7, y: 10 },
        { x: 6, y: 10 }
      ];

      direction = { x: 1, y: 0 };
      nextDirection = { x: 1, y: 0 };
      food = randomFood();

      scoreText.textContent = score;
      message.textContent = "«Бастау» батырмасын бас!";
      draw();
    }

    function draw() {
      ctx.fillStyle = "#0a1019";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Тор
      ctx.strokeStyle = "#141e2b";
      ctx.lineWidth = 1;

      for (let x = 0; x <= canvas.width; x += CELL) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
      }

      for (let y = 0; y <= canvas.height; y += CELL) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
      }

      // Тамақ
      ctx.fillStyle = "#ff5c85";
      ctx.beginPath();
      ctx.arc(
        food.x * CELL + CELL / 2,
        food.y * CELL + CELL / 2,
        CELL * 0.38, 0, Math.PI * 2
      );
      ctx.fill();

      // Жылан
      snake.forEach((part, i) => {
        ctx.fillStyle = i === 0 ? "#c1ff72" : "#68d391";
        ctx.beginPath();
        ctx.roundRect(
          part.x * CELL + 1,
          part.y * CELL + 1,
          CELL - 2,
          CELL - 2,
          5
        );
        ctx.fill();
      });

      if (!running && !over) {
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 22px Arial";
        ctx.textAlign = "center";
        ctx.fillText(
          "GAMEZONE",
          canvas.width / 2,
          canvas.height / 2 - 8
        );
        ctx.font = "14px Arial";
        ctx.fillStyle = "#c4b5fd";
        ctx.fillText(
          "Ойынды бастауға дайынсың ба?",
          canvas.width / 2,
          canvas.height / 2 + 20
        );
      }

      if (over) {
        ctx.fillStyle = "rgba(5, 5, 15, 0.78)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#ff8aa8";
        ctx.font = "bold 30px Arial";
        ctx.textAlign = "center";
        ctx.fillText(
          "ОЙЫН АЯҚТАЛДЫ!",
          canvas.width / 2,
          canvas.height / 2 - 10
        );
        ctx.fillStyle = "white";
        ctx.font = "18px Arial";
        ctx.fillText(
          "Ұпайың: " + score,
          canvas.width / 2,
          canvas.height / 2 + 25
        );
      }
    }

    function step() {
      direction = nextDirection;

      const head = {
        x: snake[0].x + direction.x,
        y: snake[0].y + direction.y
      };

      const eating = head.x === food.x && head.y === food.y;

      // Тамақ жемесек, құйрық бір қадамда қозғалады.
      const body = eating ? snake : snake.slice(0, -1);

      if (
        head.x < 0 || head.x >= COLS ||
        head.y < 0 || head.y >= ROWS ||
        body.some(p => p.x === head.x && p.y === head.y)
      ) {
        endGame();
        return;
      }

      snake.unshift(head);

      if (eating) {
        score++;
        scoreText.textContent = score;

        if (score > best) {
          best = score;
          bestText.textContent = best;
          try {
            localStorage.setItem("gamezoneBest", best);
          } catch (e) {}
        }

        food = randomFood();
      } else {
        snake.pop();
      }

      draw();
    }

    function start() {
      if (running) return;

      if (over) reset();

      running = true;
      message.textContent = "Сәттілік! 🍀";
      clearInterval(timer);
      timer = setInterval(step, Math.max(65, 140 - score * 3));
      draw();
    }

    function endGame() {
      running = false;
      over = true;
      clearInterval(timer);
      timer = null;
      message.textContent = "Қайта ойнау үшін «Қайта бастау» батырмасын бас!";
      draw();
    }

    function changeDirection(name) {
      const dirs = {
        up: { x: 0, y: -1 },
        down: { x: 0, y: 1 },
        left: { x: -1, y: 0 },
        right: { x: 1, y: 0 }
      };

      const d = dirs[name];
      if (!d) return;

      if (d.x === -direction.x && d.y === -direction.y) return;

      nextDirection = d;

      if (!running && !over) {
        start();
      }
    }

    document.addEventListener("keydown", e => {
      const keys = {
        ArrowUp: "up",
        ArrowDown: "down",
        ArrowLeft: "left",
        ArrowRight: "right",
        w: "up", W: "up",
        s: "down", S: "down",
        a: "left", A: "left",
        d: "right", D: "right"
      };

      if (keys[e.key]) {
        e.preventDefault();
        changeDirection(keys[e.key]);
      }

      if (e.code === "Space") {
        e.preventDefault();
        if (running) {
          running = false;
          clearInterval(timer);
          timer = null;
          message.textContent = "Пауза. Жалғастыру үшін «Бастау» бас.";
          draw();
        } else {
          start();
        }
      }
    });

    document.querySelectorAll("[data-dir]").forEach(btn => {
      btn.addEventListener("click", () => {
        changeDirection(btn.dataset.dir);
      });
    });

    document.getElementById("start").addEventListener("click", start);

    document.getElementById("pause").addEventListener("click", () => {
      if (!running) return;
      running = false;
      clearInterval(timer);
      timer = null;
      message.textContent = "Ойын тоқтатылды.";
      draw();
    });

    document.getElementById("restart").addEventListener("click", reset);

    // Телефонда сырғыту арқылы басқару
    let touchX = 0;
    let touchY = 0;

    canvas.addEventListener("touchstart", e => {
      const t = e.changedTouches[0];
      touchX = t.clientX;
      touchY = t.clientY;
    }, { passive: true });

    canvas.addEventListener("touchend", e => {
      const t = e.changedTouches[0];
      const dx = t.clientX - touchX;
      const dy = t.clientY - touchY;

      if (Math.max(Math.abs(dx), Math.abs(dy)) < 20) return;

      if (Math.abs(dx) > Math.abs(dy)) {
        changeDirection(dx > 0 ? "right" : "left");
      } else {
        changeDirection(dy > 0 ? "down" : "up");
      }
    }, { passive: true });

    reset();
  </script>
</body>
</html>
