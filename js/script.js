const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');
menuButton?.addEventListener('click', () => nav.classList.toggle('is-open'));
nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => nav.classList.remove('is-open')));

const API_BASE_URL = window.location.port === '63342'
  ? 'http://127.0.0.1:8000'
  : '';
const API_URL = `${API_BASE_URL}/api/news?limit=3&page=1`;
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

const truncateText = (value, maxLength = 150) => {
  const text = String(value || '').replace(/\s+/g, ' ').trim();
  if (text.length <= maxLength) return text;
  const lastSpace = text.lastIndexOf(' ', maxLength);
  const cutAt = lastSpace > 0 ? lastSpace : maxLength;
  return `${text.slice(0, cutAt).trimEnd()}...`;
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
    const excerpt = truncateText(item.text);
    return `<article class="news-card ${index === 0 ? 'featured' : ''}" data-url="${escapeHtml(item.source_url)}" tabindex="0" role="link" aria-label="Открыть новость: ${escapeHtml(item.title)}">
      <div class="news-image image-${['blue', 'yellow', 'green'][index % 3]}">${image}</div>
      <div class="news-content"><div class="news-meta"><p class="tag">Новости</p><time class="news-date">${formatDate(item.published_at)}</time></div><h3>${escapeHtml(item.title)}</h3><p>${escapeHtml(excerpt)}</p><a class="arrow" href="${escapeHtml(item.source_url)}" aria-label="Открыть новость">→</a></div>
    </article>`;
  }).join('');

  newsList.querySelectorAll('.news-card').forEach((card) => {
    const openNews = () => { window.location.href = card.dataset.url; };
    card.addEventListener('click', openNews);
    card.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        openNews();
      }
    });
  });
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
