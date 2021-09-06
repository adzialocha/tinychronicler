import request from './api.js';

async function initialize() {
  const result = await request(['chronicles']);
  console.log(result);
}

document.addEventListener("DOMContentLoaded", () => {
  initialize();
});
