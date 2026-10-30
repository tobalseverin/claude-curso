/* Shared motion for the catalog and static courses, with the timing of the
   Claude landing page. The page lists what to animate in data-reveal on <body>
   and marks commands inside a .terminal-body with .command. Content rendered
   later is picked up automatically. */
(function () {
  "use strict";

  var reduced = false;
  try {
    reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  } catch (e) {}

  document.documentElement.classList.add("js");
  var selector = document.body.getAttribute("data-reveal");
  var liftSelector = document.body.getAttribute("data-lift");

  var observer =
    "IntersectionObserver" in window && !reduced
      ? new IntersectionObserver(
          function (entries) {
            entries.forEach(function (entry) {
              if (entry.isIntersecting) {
                entry.target.classList.add("in");
                observer.unobserve(entry.target);
              }
            });
          },
          { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
        )
      : null;

  function scanReveal() {
    if (!selector || !observer) return;
    document.querySelectorAll(selector).forEach(function (el) {
      if (el.classList.contains("reveal")) return;
      var index = Array.prototype.indexOf.call(el.parentElement.children, el);
      el.style.setProperty("--d", Math.min(index, 4) * 0.08 + "s");
      el.classList.add("reveal");
      observer.observe(el);
    });
  }

  function scanLift() {
    if (!liftSelector) return;
    document.querySelectorAll(liftSelector).forEach(function (el) {
      el.classList.add("curso-lift");
    });
  }

  function runTerminal(body) {
    if (body.dataset.typing || reduced) return;
    body.dataset.typing = "on";

    var lines = Array.prototype.filter
      .call(body.children, function (el) {
        return el.tagName === "DIV";
      })
      .map(function (line, index) {
        var cmd = line.classList.contains("command") || index === 0;
        return { line: line, cmd: cmd, text: line.textContent };
      });
    var last = lines[lines.length - 1].line;
    last.textContent = "$ ";

    function play() {
      if (!body.isConnected) return;
      lines.forEach(function (item) {
        item.line.style.visibility = "hidden";
        item.line.classList.remove("curso-caret");
      });
      var t = 350;
      lines.forEach(function (item) {
        if (item.line === last) return;
        if (item.cmd) {
          for (var i = 0; i <= item.text.length; i++) {
            setTimeout(
              function (it, count) {
                it.line.style.visibility = "visible";
                it.line.textContent = it.text.slice(0, count);
                it.line.classList.add("curso-caret");
              },
              t + i * 38,
              item,
              i
            );
          }
          t += item.text.length * 38 + 420;
          setTimeout(
            function (it) {
              it.line.classList.remove("curso-caret");
            },
            t - 380,
            item
          );
        } else {
          setTimeout(
            function (it) {
              it.line.style.visibility = "visible";
            },
            t,
            item
          );
          t += 260;
        }
      });
      setTimeout(function () {
        last.style.visibility = "visible";
        last.classList.add("curso-caret");
      }, t);
      setTimeout(play, t + 6500);
    }

    play();
  }

  function scan() {
    scanReveal();
    scanLift();
    document.querySelectorAll(".terminal-body").forEach(runTerminal);
  }

  scan();
  var root = document.querySelector("main");
  if (root) new MutationObserver(scan).observe(root, { childList: true });
})();
