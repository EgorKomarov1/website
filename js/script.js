const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');
menuButton?.addEventListener('click', () => nav.classList.toggle('is-open'));
nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => nav.classList.remove('is-open')));

const API_URL = '/api/news?limit=3&page=1';
const newsList = document.querySelector('#news-list');

const escapeHtml = (value = '') => String(value)
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&#039;');

const formatDate = (value) => {
  if (!value) return '';
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? escapeHtml(value)
    : date.toLocaleDateString('ru-RU', { day: '2-digit', month: 'long' });
};

const renderNews = (items) => {
  if (!items.length) {
    newsList.innerHTML = '<p class="news-status">Новостей пока нет.</p>';
    return;
  }

  newsList.innerHTML = items.map((item, index) => {
    const image = Array.isArray(item.images) && item.images[0]
      ? `<img src="${escapeHtml(item.images[0])}" alt="" loading="lazy" />`
      : '';
    const excerpt = (item.text || '').replace(/\s+/g, ' ').trim().slice(0, 150);
    return `<article class="news-card ${index === 0 ? 'featured' : ''}">
      <div class="news-image image-${['blue', 'yellow', 'green'][index % 3]}">${image}<span>${formatDate(item.published_at)}</span></div>
      <div class="news-content"><p class="tag">Новости</p><h3>${escapeHtml(item.title)}</h3><p>${escapeHtml(excerpt)}</p><a class="arrow" href="${escapeHtml(item.source_url)}" target="_blank" rel="noopener" aria-label="Открыть новость">→</a></div>
    </article>`;
  }).join('');
};

const loadNews = async () => {
  if (!newsList) return;
  newsList.innerHTML = '<p class="news-status">Загружаем новости…</p>';
  try {
    const response = await fetch(API_URL, { headers: { Accept: 'application/json' } });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    renderNews(Array.isArray(data) ? data : []);
  } catch (error) {
    console.error('Не удалось загрузить новости:', error);
    newsList.innerHTML = '<p class="news-status">Новости временно недоступны.</p>';
  }
};

loadNews();
