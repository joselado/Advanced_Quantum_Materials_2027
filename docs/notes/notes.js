// Shared script of the notes pages. Phase 1 leaves only the hooks.
// The build writes the fenced divs of the Markdown as <div class="quiz">, <div class="tryit"> and
// <div class="widget">. Phase 4 turns the quiz divs into questions with a hidden answer, and phase 6 turns
// the widget divs into plots with their sliders. Until then the divs show their text as it is.
(function () {
  'use strict';
  document.documentElement.classList.add('js');
})();
