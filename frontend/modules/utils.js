export function setStatus(el, message, kind) {
  if (!el) return;

  el.textContent = message;
  el.className = `status-msg ${kind}`;
}

export function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
