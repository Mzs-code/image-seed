/* 在「Prompt 正文」标题文字后面追加一个复制按钮,一键拷走紧随其后的代码块全文。
   隐藏该代码块默认的右上角复制按钮,避免重复。
   用 Material 的 document$(每次即时导航后都会触发)保证 navigation.instant 下仍生效。 */
(function () {
  function mount() {
    var heads = document.querySelectorAll(".md-typeset .prompt-head");
    heads.forEach(function (h) {
      if (h.dataset.promptCopy === "1") return;

      // 找紧随标题的代码块
      var block = h.nextElementSibling;
      while (block && !block.classList.contains("highlight")) {
        block = block.nextElementSibling;
      }
      var code = block && block.querySelector("code");
      if (!code) return;

      h.dataset.promptCopy = "1";

      // 隐藏 Material 默认右上角按钮,避免和自定义按钮重复
      var def = block.querySelector(".md-clipboard");
      if (def) def.style.display = "none";

      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "prompt-copy";
      btn.setAttribute("aria-label", "复制 Prompt 正文");
      btn.innerHTML =
        '<svg viewBox="0 0 24 24" width="13" height="13" aria-hidden="true">' +
        '<path fill="currentColor" d="M19 21H8V7h11m0-2H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2m-3-4H4a2 2 0 0 0-2 2v14h2V3h12V1Z"/>' +
        '</svg><span class="prompt-copy__label">复制</span>';

      btn.addEventListener("click", function () {
        var text = code.innerText;
        var done = function () {
          btn.classList.add("prompt-copy--done");
          btn.querySelector(".prompt-copy__label").textContent = "已复制";
          setTimeout(function () {
            btn.classList.remove("prompt-copy--done");
            btn.querySelector(".prompt-copy__label").textContent = "复制";
          }, 1600);
        };
        function fallback() {
          var ta = document.createElement("textarea");
          ta.value = text;
          ta.style.position = "fixed";
          ta.style.opacity = "0";
          document.body.appendChild(ta);
          ta.select();
          try { document.execCommand("copy"); done(); } catch (e) {}
          document.body.removeChild(ta);
        }
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done).catch(fallback);
        } else {
          fallback();
        }
      });

      h.appendChild(btn);
    });
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(mount);
  } else {
    document.addEventListener("DOMContentLoaded", mount);
  }
})();
