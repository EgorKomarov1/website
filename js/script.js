const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');
menuButton?.addEventListener('click', () => nav.classList.toggle('is-open'));
nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => nav.classList.remove('is-open')));

const API_BASE_URL = window.location.port === '63342'
  ? 'http://127.0.0.1:8000'
  : '';
const newsList = document.querySelector('#news-list');
const isNewsArchive = newsList?.dataset.archive === 'true';
const newsPageSize = isNewsArchive ? 12 : 3;
const newsMoreButton = document.querySelector('#news-more');
const newsFeedback = document.querySelector('#news-feedback');
let nextNewsPage = 1;
let loadedNewsCount = 0;
let newsLoading = false;
let newsHasMore = true;
let newsObserver = null;

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
    : date.toLocaleDateString('ru-RU', {
      day: '2-digit', month: 'long', ...(isNewsArchive ? { year: 'numeric' } : {}),
    });
};

const truncateText = (value, maxLength = 150) => {
  const text = String(value || '').replace(/\s+/g, ' ').trim();
  if (text.length <= maxLength) return text;
  const lastSpace = text.lastIndexOf(' ', maxLength);
  const cutAt = lastSpace > 0 ? lastSpace : maxLength;
  return `${text.slice(0, cutAt).trimEnd()}...`;
};

const renderNews = (items, append = false) => {
  if (!items.length) {
    if (!append) newsList.innerHTML = '<p class="news-status">Новостей пока нет.</p>';
    return;
  }

  const markup = items.map((item, index) => {
    const image = Array.isArray(item.images) && item.images[0]
      ? `<img src="${escapeHtml(item.images[0])}" alt="" loading="lazy" />`
      : '';
    const excerpt = truncateText(item.text);
    const newsUrl = `${API_BASE_URL}/news/${encodeURIComponent(item.code)}`;
    return `<a class="news-card ${!isNewsArchive && index === 0 ? 'featured' : ''}" href="${escapeHtml(newsUrl)}" aria-label="Открыть новость: ${escapeHtml(item.title)}">
      <div class="news-image image-${['blue', 'yellow', 'green'][index % 3]}">${image}</div>
      <div class="news-content"><div class="news-meta"><p class="tag">Новости</p><time class="news-date">${formatDate(item.published_at)}</time></div><h3>${escapeHtml(item.title)}</h3><p>${escapeHtml(excerpt)}</p><span class="arrow" aria-hidden="true">→</span></div>
    </a>`;
  }).join('');
  if (append) {
    newsList.insertAdjacentHTML('beforeend', markup);
  } else {
    newsList.innerHTML = markup;
  }
};

const loadNews = async (focusNewCard = false) => {
  if (!newsList || newsLoading || !newsHasMore) return;
  newsLoading = true;
  newsObserver?.disconnect();
  let loadSucceeded = false;
  newsList.setAttribute('aria-busy', 'true');
  if (!loadedNewsCount) newsList.innerHTML = '<p class="news-status">Загружаем новости…</p>';
  if (newsMoreButton) {
    newsMoreButton.disabled = true;
    newsMoreButton.textContent = 'Загружаем…';
  }
  if (newsFeedback) newsFeedback.textContent = '';
  try {
    const response = await fetch(`${API_BASE_URL}/api/news?limit=${newsPageSize}&page=${nextNewsPage}`, {
      headers: { Accept: 'application/json' },
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    if (!Array.isArray(data)) throw new Error('Invalid news response');
    const firstNewCardIndex = newsList.querySelectorAll('.news-card').length;
    renderNews(data, loadedNewsCount > 0);
    if (focusNewCard && loadedNewsCount && data.length) {
      newsList.querySelectorAll('.news-card')[firstNewCardIndex]?.focus({ preventScroll: true });
    }
    loadedNewsCount += data.length;
    nextNewsPage += 1;
    newsHasMore = data.length === newsPageSize;
    loadSucceeded = true;
    if (newsMoreButton) {
      newsMoreButton.hidden = !newsHasMore;
      newsMoreButton.textContent = 'Показать ещё';
    }
    if (newsFeedback && loadedNewsCount) {
      newsFeedback.textContent = data.length < newsPageSize
        ? `Все новости загружены · ${loadedNewsCount}`
        : `Загружено новостей: ${loadedNewsCount}`;
    }
  } catch (error) {
    console.error('Не удалось загрузить новости:', error);
    if (!loadedNewsCount) newsList.innerHTML = '<p class="news-status">Новости временно недоступны.</p>';
    if (newsFeedback) newsFeedback.textContent = 'Не удалось загрузить новости. Попробуйте ещё раз.';
    if (newsMoreButton) {
      newsMoreButton.hidden = false;
      newsMoreButton.textContent = 'Попробовать ещё раз';
    }
  } finally {
    newsLoading = false;
    newsList.setAttribute('aria-busy', 'false');
    if (newsMoreButton) newsMoreButton.disabled = false;
    if (loadSucceeded && newsHasMore && newsMoreButton) newsObserver?.observe(newsMoreButton);
  }
};

newsMoreButton?.addEventListener('click', () => loadNews(true));
if (isNewsArchive && newsMoreButton && 'IntersectionObserver' in window) {
  newsObserver = new IntersectionObserver((entries) => {
    if (entries.some(entry => entry.isIntersecting) && !newsMoreButton.hidden) loadNews();
  });
}
loadNews();
