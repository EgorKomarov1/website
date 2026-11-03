const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');
menuButton?.addEventListener('click', () => nav.classList.toggle('is-open'));
nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => nav.classList.remove('is-open')));
