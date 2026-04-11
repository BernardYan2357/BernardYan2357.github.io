if (typeof mermaid !== "undefined") {
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "loose"
  });
}

function renderMermaid() {
  if (typeof mermaid === "undefined") return;
  const blocks = document.querySelectorAll("pre.mermaid");
  if (!blocks.length) return;

  blocks.forEach((block) => {
    const source = block.textContent || "";
    const container = document.createElement("div");
    container.className = "mermaid";
    container.textContent = source;
    block.replaceWith(container);
  });

  mermaid.run({ querySelector: ".mermaid" });
}

if (typeof document$ !== "undefined") {
  document$.subscribe(() => {
    renderMermaid();
  });
} else {
  document.addEventListener("DOMContentLoaded", () => {
    renderMermaid();
  });
}
