(() => {
  const elements = document.querySelectorAll("button, a, [role='button']");
  return Array.from(elements).map(el => ({
    text: el.innerText || el.ariaLabel || "Unnamed",
    tag: el.tagName,
    href: el.href || null,
    type: el.type || null
  }));
})();
