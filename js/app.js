/**
 * Wspólnota Rodzin Kozanów - Client Application
 * Hydrates content, renders website_reference timeline news tiles,
 * provides interactive meeting details modal and full news modal reader without image duplication.
 */

(function () {
  'use strict';

  // Application State
  const state = {
    data: null,
    activeArticleId: null,
    renderedNewsCount: 0,
    feedObserver: null,
  };

  const INITIAL_NEWS_COUNT = 8;
  const NEWS_BATCH_SIZE = 4;

  let savedScrollY = 0;

  /**
   * Freezes background document scroll to prevent scroll bleed/chaining on mobile
   */
  function lockBodyScroll() {
    savedScrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop || 0;
    document.body.style.position = 'fixed';
    document.body.style.top = `-${savedScrollY}px`;
    document.body.style.left = '0';
    document.body.style.right = '0';
    document.body.style.width = '100%';
    document.body.classList.add('modal-open');
  }

  /**
   * Unfreezes background document scroll and restores exact scroll position
   */
  function unlockBodyScroll() {
    const top = document.body.style.top;
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.left = '';
    document.body.style.right = '';
    document.body.style.width = '';
    document.body.classList.remove('modal-open');
    if (top) {
      window.scrollTo(0, savedScrollY);
    }
  }

  /**
   * Loads community data via fetch with fallback to window.COMMUNITY_DATA
   */
  async function loadCommunityData() {
    try {
      const response = await fetch('data/content.json', { cache: 'no-cache' });
      if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
      }
      return await response.json();
    } catch (err) {
      console.warn('Fetch failed or running on file:// protocol, falling back to window.COMMUNITY_DATA:', err);
      if (window.COMMUNITY_DATA) {
        return window.COMMUNITY_DATA;
      }
      throw new Error('No community data available.');
    }
  }

  /**
   * Helper to format ISO date YYYY-MM-DD into Polish locale string
   */
  function formatDatePl(isoDate) {
    if (!isoDate) return '';
    try {
      const parts = isoDate.split('-');
      if (parts.length === 3) {
        const months = [
          'stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca',
          'lipca', 'sierpnia', 'września', 'października', 'listopada', 'grudnia'
        ];
        const day = parseInt(parts[2], 10);
        const month = months[parseInt(parts[1], 10) - 1];
        const year = parts[0];
        return `${day} ${month} ${year}`;
      }
      return isoDate;
    } catch (e) {
      return isoDate;
    }
  }

  /**
   * Renders Next Meeting Notice with Clickable Image Preview
   */
  function renderMeeting(config) {
    const meetingCard = document.getElementById('meeting-card');
    const headlineDateBadge = document.getElementById('headline-meeting-date');
    if (!meetingCard) return;

    if (!config || !config.nextMeeting) {
      meetingCard.style.display = 'none';
      meetingCard.innerHTML = '';
      if (headlineDateBadge) headlineDateBadge.style.display = 'none';
      return;
    }

    meetingCard.style.display = '';
    const nm = config.nextMeeting;
    const hasImage = Boolean(nm.image);

    if (headlineDateBadge) {
      const badgeText = nm.badgeText || (nm.dateText ? (nm.dateText.match(/(\d{1,2}\.\d{2})/) ? nm.dateText.match(/(\d{1,2}\.\d{2})/)[1] : '') : '') || '09.10';
      headlineDateBadge.textContent = badgeText;
      headlineDateBadge.style.display = '';
      headlineDateBadge.setAttribute('aria-label', `Data następnego spotkania: ${badgeText}`);
    }

    meetingCard.innerHTML = `
      <div class="meeting-highlight-badge">Najbliższe Spotkanie Wspólnoty</div>
      <div class="meeting-date-row">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="16" y1="2" x2="16" y2="6"></line>
          <line x1="8" y1="2" x2="8" y2="6"></line>
          <line x1="3" y1="10" x2="21" y2="10"></line>
        </svg>
        <span>${nm.dateText}</span>
      </div>
      <div class="meeting-location-row">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
          <circle cx="12" cy="10" r="3"></circle>
        </svg>
        <span>${nm.locationText}</span>
      </div>
      ${hasImage ? `
        <div class="meeting-image-preview" tabindex="0" role="button" aria-label="Zobacz szczegóły spotkania: ${nm.title}">
          <img src="${nm.image}" alt="${nm.title}" class="meeting-poster-thumb" loading="lazy" />
          <div class="meeting-image-overlay">
            <span class="meeting-overlay-cta">
              Zobacz szczegóły spotkania
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </span>
          </div>
        </div>
      ` : ''}
    `;

    // Attach click listeners to open meeting modal
    const previewEl = meetingCard.querySelector('.meeting-image-preview');
    if (previewEl) {
      previewEl.addEventListener('click', openMeetingModal);
      previewEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openMeetingModal();
        }
      });
    }
  }

  /**
   * Opens Meeting Details Modal
   */
  function openMeetingModal() {
    if (!state.data || !state.data.siteConfig || !state.data.siteConfig.nextMeeting) return;
    const nm = state.data.siteConfig.nextMeeting;

    state.activeArticleId = 'spotkanie';

    const modal = document.getElementById('article-modal');
    const modalBody = document.getElementById('modal-body');
    if (!modal || !modalBody) return;

    modalBody.innerHTML = `
      <header class="modal-article-header">
        <div class="modal-article-meta">
          <span class="modal-date">${nm.dateText}</span>
          <span>&bull; ${nm.locationText}</span>
        </div>
        <h2 class="modal-article-title">${nm.title}</h2>
      </header>

      ${nm.image ? `
        <figure class="modal-featured-figure">
          <img src="${nm.image}" alt="${nm.title}" class="modal-featured-img" />
        </figure>
      ` : ''}

      <div class="modal-article-prose">
        ${nm.contentHtml || `<p>${nm.description}</p>`}
      </div>
    `;

    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');
    lockBodyScroll();
    window.location.hash = 'spotkanie';
  }

  /**
   * Generates single article tile HTML
   */
  function buildTileHtml(item, isIncremental = false) {
    const formattedDate = formatDatePl(item.date);
    const hasAttachments = item.attachments && item.attachments.length > 0;
    const isVideo = Boolean(item.isVideo || (item.contentHtml && /<iframe/i.test(item.contentHtml)));
    const mediaSrc = item.featuredImage || 'assets/images/header/wspolnota_rodzin_header.png';
    const animClass = isIncremental ? ' fade-in' : '';

    return `
      <article class="news-tile${animClass}" data-article-id="${item.id}" tabindex="0" role="button" aria-label="Czytaj artykuł: ${item.title}">
        <div class="tile-media-wrap">
          <img src="${mediaSrc}" alt="${item.title}" loading="lazy" class="tile-img" />
          ${isVideo ? `
            <div class="tile-play-overlay" aria-hidden="true">
              <div class="tile-play-btn" title="Odtwórz wideo">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
                  <polygon points="6 3 20 12 6 21 6 3"></polygon>
                </svg>
              </div>
            </div>
          ` : ''}
          <!-- The vertical line continuing inside the tile -->
          <div class="tile-inner-line" aria-hidden="true"></div>
          <!-- The circular node on the vertical line -->
          <div class="tile-node-dot" aria-hidden="true"></div>
          <!-- Floating white badge cutout overlay -->
          <div class="tile-badge-box">
            <div class="tile-meta-row">
              <span class="tile-date-pill">${formattedDate}</span>
              ${isVideo ? '<span class="tile-video-pill">▶ Wideo</span>' : ''}
              ${hasAttachments ? `<span class="tile-pdf-pill">📄 ${item.attachments.length} ${item.attachments.length === 1 ? 'dokument' : (item.attachments.length < 5 ? 'dokumenty' : 'dokumentów')}</span>` : ''}
            </div>
            <h3 class="tile-title">${item.title}</h3>
            <div class="tile-action-row">
              <span class="tile-action-link">
                ${isVideo ? 'Obejrzyj nagranie' : 'Czytaj całość'}
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true">
                  <polyline points="9 18 15 12 9 6"></polyline>
                </svg>
              </span>
            </div>
          </div>
        </div>
      </article>
    `;
  }

  /**
   * Binds click and keyboard listeners to newly rendered tiles
   */
  function bindTileEvents(scopeElement) {
    scopeElement.querySelectorAll('.news-tile').forEach(tile => {
      if (tile.dataset.eventsBound) return;
      tile.dataset.eventsBound = 'true';

      const open = () => {
        const id = tile.getAttribute('data-article-id');
        openArticleModal(id);
      };

      tile.addEventListener('click', open);
      tile.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          open();
        }
      });
    });
  }

  /**
   * Appends the next batch of news articles to the timeline feed
   */
  function loadMoreNews(count, isIncremental = false) {
    const container = document.getElementById('news-timeline');
    const sentinel = document.getElementById('timeline-sentinel');
    if (!container || !state.data || !state.data.news) return;

    const allNews = state.data.news;
    if (state.renderedNewsCount >= allNews.length) {
      if (sentinel) sentinel.remove();
      if (state.feedObserver) {
        state.feedObserver.disconnect();
        state.feedObserver = null;
      }
      return;
    }

    const nextBatch = allNews.slice(state.renderedNewsCount, state.renderedNewsCount + count);
    if (nextBatch.length === 0) return;

    const tempWrapper = document.createElement('div');
    let batchHtml = '';

    nextBatch.forEach((item, batchIdx) => {
      const globalIndex = state.renderedNewsCount + batchIdx;

      // Category divider tags along the timeline line (like in website_reference)
      if (globalIndex === 0) {
        batchHtml += `
          <div class="timeline-category" aria-hidden="true">
            <span class="category-pill">Najnowsze Wydarzenia</span>
          </div>
        `;
      } else if (item.id === 19366 || item.slug === 'adoracja-najswietszego-sakramentu-w-iii-piatek-18-wrzesnia-2026r') {
        batchHtml += `
          <div class="timeline-category" aria-hidden="true">
            <span class="category-pill">Z Życia Parafii Kozanów</span>
          </div>
        `;
      }

      batchHtml += buildTileHtml(item, isIncremental);
    });

    tempWrapper.innerHTML = batchHtml;

    const fragment = document.createDocumentFragment();
    while (tempWrapper.firstChild) {
      fragment.appendChild(tempWrapper.firstChild);
    }

    bindTileEvents(fragment);

    if (sentinel && sentinel.parentNode === container) {
      container.insertBefore(fragment, sentinel);
    } else {
      container.appendChild(fragment);
    }

    state.renderedNewsCount += nextBatch.length;

    // Remove sentinel & disconnect observer once all items are rendered
    if (state.renderedNewsCount >= allNews.length) {
      if (sentinel) sentinel.remove();
      if (state.feedObserver) {
        state.feedObserver.disconnect();
        state.feedObserver = null;
      }
    }
  }

  /**
   * Initializes the Timeline News Feed with progressive loading (Infinite Scroll)
   */
  function renderNewsFeed(newsList) {
    const container = document.getElementById('news-timeline');
    if (!container) return;

    if (!newsList || newsList.length === 0) {
      container.innerHTML = '<p class="empty-feed">Brak aktualności do wyświetlenia.</p>';
      return;
    }

    // Reset container and counters
    container.innerHTML = '';
    state.renderedNewsCount = 0;

    // Create bottom sentinel with subtle loader
    const sentinel = document.createElement('div');
    sentinel.id = 'timeline-sentinel';
    sentinel.className = 'timeline-sentinel';
    sentinel.setAttribute('aria-hidden', 'true');
    sentinel.innerHTML = `
      <div class="timeline-loader" aria-label="Wczytywanie kolejnych wpisów">
        <span>Wczytywanie</span>
        <span class="timeline-loader-dots">
          <span class="timeline-loader-dot"></span>
          <span class="timeline-loader-dot"></span>
          <span class="timeline-loader-dot"></span>
        </span>
      </div>
    `;
    container.appendChild(sentinel);

    // Initial batch of 8 articles
    loadMoreNews(INITIAL_NEWS_COUNT, false);

    // Setup progressive infinite scroll if more articles remain
    if (state.renderedNewsCount < newsList.length) {
      if ('IntersectionObserver' in window) {
        if (state.feedObserver) state.feedObserver.disconnect();
        state.feedObserver = new IntersectionObserver((entries) => {
          const entry = entries[0];
          if (entry && entry.isIntersecting) {
            loadMoreNews(NEWS_BATCH_SIZE, true);
          }
        }, {
          root: null,
          rootMargin: '300px 0px',
          threshold: 0.01
        });
        state.feedObserver.observe(sentinel);
      } else {
        // Fallback for older environments without IntersectionObserver
        loadMoreNews(newsList.length, false);
      }
    } else {
      sentinel.remove();
    }
  }

  /**
   * Opens the in-page Article Modal Reader
   */
  function openArticleModal(articleId) {
    if (!state.data || !state.data.news) return;
    const article = state.data.news.find(n => String(n.id) === String(articleId));
    if (!article) return;

    state.activeArticleId = article.id;

    const modal = document.getElementById('article-modal');
    const modalBody = document.getElementById('modal-body');
    if (!modal || !modalBody) return;

    const formattedDate = formatDatePl(article.date);
    const hasAttachments = article.attachments && article.attachments.length > 0;

    // Check if the article's body HTML already contains an image or video to prevent duplicate figure
    const bodyHasMedia = Boolean(article.contentHtml && /(<img[^>]+src=|<iframe[^>]+src=)/i.test(article.contentHtml));
    const showFeaturedFigure = Boolean(article.featuredImage && !bodyHasMedia);

    modalBody.innerHTML = `
      <header class="modal-article-header">
        <div class="modal-article-meta">
          <span class="modal-date">${formattedDate}</span>
          ${article.author ? `<span>&bull; Autor: ${article.author}</span>` : ''}
        </div>
        <h2 class="modal-article-title">${article.title}</h2>
      </header>

      ${showFeaturedFigure ? `
        <figure class="modal-featured-figure">
          <img src="${article.featuredImage}" alt="${article.title}" class="modal-featured-img" />
        </figure>
      ` : ''}

      <div class="modal-article-prose">
        ${article.contentHtml || `<p>${article.excerpt}</p>`}
      </div>

      ${hasAttachments ? `
        <section class="modal-attachments-box">
          <h4 class="attachments-heading">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
              <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path>
            </svg>
            Załączone dokumenty do pobrania:
          </h4>
          <ul class="attachments-list">
            ${article.attachments.map(att => `
              <li>
                <a href="${att.path}" class="attachment-download-link" download target="_blank" rel="noopener">
                  <span class="att-icon">PDF</span>
                  <span class="att-name">${att.name}</span>
                  ${att.sizeText ? `<span class="att-size">(${att.sizeText})</span>` : ''}
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="7 10 12 15 17 10"></polyline>
                  </svg>
                </a>
              </li>
            `).join('')}
          </ul>
        </section>
      ` : ''}

      ${article.sourceUrl ? `
        <footer class="modal-source-footer">
          <p>Oryginalny wpis opublikowany na: <a href="${article.sourceUrl}" target="_blank" rel="noopener noreferrer">${article.sourceUrl}</a></p>
        </footer>
      ` : ''}
    `;

    // Show modal & lock background scroll
    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');
    lockBodyScroll();

    // Update URL hash without page reload
    window.location.hash = `artykul-${article.id}`;
  }

  /**
   * Closes the Article/Meeting Modal Reader
   */
  function closeArticleModal() {
    const modal = document.getElementById('article-modal');
    if (!modal) return;

    // Reset iframe to stop audio/video playback when modal is closed
    const iframes = modal.querySelectorAll('iframe');
    iframes.forEach(iframe => {
      iframe.src = iframe.src;
    });

    modal.classList.remove('is-open');
    modal.setAttribute('aria-hidden', 'true');
    unlockBodyScroll();
    state.activeArticleId = null;

    if (window.location.hash.startsWith('#artykul-') || window.location.hash === '#spotkanie') {
      history.replaceState(null, '', window.location.pathname + window.location.search);
    }
  }

  /**
   * Checks hash on page load or hashchange
   */
  function handleHashNavigation() {
    const hash = window.location.hash;
    if (hash === '#spotkanie') {
      openMeetingModal();
    } else if (hash && hash.startsWith('#artykul-')) {
      const articleId = hash.replace('#artykul-', '');
      if (state.data && state.data.news) {
        const targetIdx = state.data.news.findIndex(n => String(n.id) === String(articleId));
        if (targetIdx !== -1 && targetIdx >= state.renderedNewsCount) {
          loadMoreNews((targetIdx - state.renderedNewsCount) + 1, false);
        }
      }
      openArticleModal(articleId);
    } else if (state.activeArticleId) {
      closeArticleModal();
    }
  }

  /**
   * Setup modal event listeners
   */
  function setupModalListeners() {
    const modal = document.getElementById('article-modal');
    const closeBtn = document.getElementById('modal-close-btn');
    const backdrop = document.getElementById('modal-backdrop');

    if (closeBtn) closeBtn.addEventListener('click', closeArticleModal);
    if (backdrop) {
      backdrop.addEventListener('click', closeArticleModal);
      backdrop.addEventListener('touchmove', (e) => e.preventDefault(), { passive: false });
    }
    const topBar = document.querySelector('.modal-top-bar');
    if (topBar) {
      topBar.addEventListener('touchmove', (e) => e.preventDefault(), { passive: false });
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal && modal.classList.contains('is-open')) {
        closeArticleModal();
      }
    });

    window.addEventListener('hashchange', handleHashNavigation);
  }

  /**
   * App Initialization
   */
  async function init() {
    try {
      const data = await loadCommunityData();
      state.data = data;

      renderMeeting(data.siteConfig);
      renderNewsFeed(data.news);
      setupModalListeners();

      // Check initial hash
      handleHashNavigation();

      console.log('Wspólnota Rodzin website hydrated successfully.');
    } catch (err) {
      console.error('Failed to initialize app:', err);
      const container = document.getElementById('news-timeline');
      if (container) {
        container.innerHTML = '<p class="error-msg">Przepraszamy, nie udało się załadować treści. Odśwież stronę.</p>';
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
