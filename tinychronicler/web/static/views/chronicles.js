import request from '../utils/api.js';

async function initialize() {
  const result = await request(['chronicles']);
  const html = result.items.map((chronicle) => {
    return `<li><strong>${chronicle.title}:</strong> (${chronicle.created_at}) ${chronicle.description}</li>`;
  }).join('');
  document.getElementById('chronicles').innerHTML = html;
}

document.addEventListener("DOMContentLoaded", () => {
  initialize();
});
