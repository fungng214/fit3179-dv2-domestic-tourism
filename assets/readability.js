/* Natural line wrapping, with a maximum of twelve words per prose line.
 * The generated HTML also has conservative breaks for the no-JavaScript case.
 * This only adjusts layout: it adds no controls or chart interactions.
 */
(() => {
  'use strict';
  let pending;
  function fitProse() {
    document.querySelectorAll('br.prose-break').forEach(br => br.remove());
    for (const block of document.querySelectorAll('p,h1,h2,h3,h4,li')) {
      block.normalize();
      const walker = document.createTreeWalker(block, NodeFilter.SHOW_TEXT);
      const words = [];
      let node;
      while ((node = walker.nextNode())) {
        for (const match of node.textContent.matchAll(/\S+/g)) {
          const range = document.createRange();
          range.setStart(node, match.index);
          range.setEnd(node, match.index + match[0].length);
          words.push(range);
        }
      }
      let previousBottom = -Infinity, count = 0;
      for (const word of words) {
        const bounds = [...word.getClientRects()].find(rect => rect.width > 0);
        if (!bounds || !bounds.width) continue;
        if (Math.abs(bounds.bottom - previousBottom) > 4) count = 0;
        if (count === 12) {
          const start = word.cloneRange();
          start.collapse(true);
          const br = document.createElement('br');
          br.className = 'prose-break';
          start.insertNode(br);
          count = 0;
        }
        previousBottom = [...word.getClientRects()].find(rect => rect.width > 0)?.bottom ?? bounds.bottom;
        count++;
      }
    }
  }
  const schedule = () => {
    clearTimeout(pending);
    pending = setTimeout(fitProse, 100);
  };
  document.fonts.ready.then(fitProse);
  window.addEventListener('resize', schedule, {passive:true});
})();
