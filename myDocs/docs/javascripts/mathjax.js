window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

if (typeof document$ !== "undefined") {
  document$.subscribe(() => {
    const mathjax = window.MathJax;
    if (!mathjax.typesetPromise) return;
    mathjax.startup.promise = mathjax.startup.promise.then(() => {
      mathjax.startup.output.clearCache();
      mathjax.typesetClear();
      mathjax.texReset();
      return mathjax.typesetPromise();
    }).catch((error) => console.error("MathJax rendering failed", error));
  });
}

if (typeof component$ !== "undefined") {
  component$.subscribe(({ ref }) => {
    const mathjax = window.MathJax;
    if (!mathjax.typesetPromise || !ref?.classList?.contains("md-annotation")) return;
    mathjax.startup.promise = mathjax.startup.promise
      .then(() => mathjax.typesetPromise([ref]))
      .catch((error) => console.error("MathJax rendering failed", error));
  });
}
