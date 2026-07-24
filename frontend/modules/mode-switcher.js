export function initModeSwitcher() {
  const modeBtns = document.querySelectorAll(".mode-btn");
  const panels = {
    search: document.getElementById("panel-search"),
    add: document.getElementById("panel-add"),
    delete: document.getElementById("panel-delete"),
  };

  modeBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      modeBtns.forEach((button) => {
        button.classList.remove("is-active");
        button.setAttribute("aria-selected", "false");
      });

      btn.classList.add("is-active");
      btn.setAttribute("aria-selected", "true");

      Object.values(panels).forEach((panel) => panel?.classList.remove("is-active"));
      panels[btn.dataset.mode]?.classList.add("is-active");
    });
  });
}
