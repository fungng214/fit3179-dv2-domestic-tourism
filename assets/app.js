/* Hover details and a chart action menu on all figures; Figure 6 has a filter. */
(() => {
  'use strict';
  if (!window.vegaEmbed || !window.TOURISM_SPECS) return;
  const frames = [...document.querySelectorAll('[data-chart]')];
  const views = new Map();
  const widthFor = frame => Math.max(240, Math.floor(frame.clientWidth));
  async function mount(frame) {
    if (frame.dataset.mounted) return;
    frame.dataset.mounted = 'pending';
    const spec = JSON.parse(JSON.stringify(window.TOURISM_SPECS[frame.dataset.chart]));
    spec.width = widthFor(frame);
    const target = document.createElement('div');
    target.className = 'hover-chart';
    // Keep the static figure visible until its hover-enabled chart is ready.
    target.style.position = 'absolute';
    target.style.visibility = 'hidden';
    frame.append(target);
    try {
      const {view} = await vegaEmbed(target, spec, {
        renderer:'svg',
        actions:{export:{svg:true,png:true},source:true,compiled:true,editor:true},
        tooltip:{theme:'light'},
        defaultStyle:true,
        downloadFileName:frame.dataset.chart
      });
      // Native Vega charts already use Vega source, so expose that same JSON
      // under View Compiled Vega to keep the five menu options consistent.
      const menu = target.querySelector('.vega-actions');
      if (menu && !spec.$schema.includes('vega-lite')) {
        const compiled = document.createElement('a');
        compiled.textContent = 'View Compiled Vega';
        compiled.href = `chart-specs/${frame.dataset.chart}.json`;
        compiled.target = '_blank';
        compiled.rel = 'noopener';
        menu.insertBefore(compiled, menu.lastElementChild);
      }
      const details = target.querySelector('details');
      const summary = details?.querySelector('summary');
      if (summary) summary.setAttribute('aria-label', `Chart options: ${frame.getAttribute('aria-label')}`);
      details?.addEventListener('keydown', event => {
        if (event.key === 'Escape') {
          details.open = false;
          summary?.focus();
        }
      });
      frame.querySelector('img')?.remove();
      target.style.position = '';
      target.style.visibility = '';
      frame.dataset.mounted = 'ready';
      views.set(frame, {view, width:spec.width});
    } catch (error) {
      target.remove();
      frame.dataset.mounted = 'fallback';
      const note = document.createElement('p');
      note.className = 'fallback-note';
      note.textContent = frame.dataset.filterChart
        ? 'Hover details and the trip-type filter are unavailable. The static graph shows overnight trips.'
        : 'Hover details are unavailable. The chart is shown as a static figure.';
      frame.append(note);
      console.error('Chart could not initialise:', frame.dataset.chart, error.message);
    }
  }
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.filter(entry => entry.isIntersecting).forEach(entry => {
        mount(entry.target);
        observer.unobserve(entry.target);
      });
    }, {rootMargin:'450px'});
    frames.forEach(frame => observer.observe(frame));
  } else frames.forEach(mount);
  if ('ResizeObserver' in window) {
    const observer = new ResizeObserver(entries => {
      entries.forEach(({target}) => {
        const item = views.get(target), width = widthFor(target);
        if (item && Math.abs(item.width - width) > 2) {
          item.width = width;
          item.view.width(width).resize().runAsync();
        }
      });
    });
    frames.forEach(frame => observer.observe(frame));
  }
})();
