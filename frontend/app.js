import { initModeSwitcher } from "./modules/mode-switcher.js";
import { initSearch } from "./modules/search.js";
import { initActions } from "./modules/actions.js";

document.addEventListener("DOMContentLoaded", () => {
  initModeSwitcher();
  initSearch();
  initActions();
});