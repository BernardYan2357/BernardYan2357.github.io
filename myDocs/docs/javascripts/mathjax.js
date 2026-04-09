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
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise();
    }
  });
}

if (typeof component$ !== "undefined") {
  component$.subscribe(({ ref }) => {
    if (
      window.MathJax &&
      window.MathJax.typesetPromise &&
      ref &&
      ref.classList &&
      ref.classList.contains("md-annotation")
    ) {
      window.MathJax.typesetPromise([ref]);
    }
  });
}
