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
  };

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
    if (!meetingCard || !config.nextMeeting) return;

    const nm = config.nextMeeting;
    const hasImage = Boolean(nm.image);

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
   * Renders the Timeline News Feed (Matching website_reference tile lines)
   */
  function renderNewsFeed(newsList) {
    const container = document.getElementById('news-timeline');
    if (!container) return;

    if (!newsList || newsList.length === 0) {
      container.innerHTML = '<p class="empty-feed">Brak aktualności do wyświetlenia.</p>';
      return;
    }

    let html = '';

    newsList.forEach((item, index) => {
      // Category divider tags along the timeline line (like in website_reference)
      if (index === 0) {
        html += `
          <div class="timeline-category" aria-hidden="true">
            <span class="category-pill">Najnowsze Wydarzenia</span>
          </div>
        `;
      } else if (index === 2) {
        html += `
          <div class="timeline-category" aria-hidden="true">
            <span class="category-pill">Komunikaty i Dokumenty</span>
          </div>
        `;
      } else if (index === 5) {
        html += `
          <div class="timeline-category" aria-hidden="true">
            <span class="category-pill">Z Życia Parafii Kozanów</span>
          </div>
        `;
      }

      const formattedDate = formatDatePl(item.date);
      const hasAttachments = item.attachments && item.attachments.length > 0;
      const mediaSrc = item.featuredImage || 'assets/images/header/wspolnota_rodzin_header.png';

      html += `
        <article class="news-tile" data-article-id="${item.id}" tabindex="0" role="button" aria-label="Czytaj artykuł: ${item.title}">
          <div class="tile-media-wrap">
            <img src="${mediaSrc}" alt="${item.title}" loading="lazy" class="tile-img" />
            <!-- The vertical line continuing inside the tile -->
            <div class="tile-inner-line" aria-hidden="true"></div>
            <!-- The circular node on the vertical line -->
            <div class="tile-node-dot" aria-hidden="true"></div>
            <!-- Floating white badge cutout overlay -->
            <div class="tile-badge-box">
              <div class="tile-meta-row">
                <span class="tile-date-pill">${formattedDate}</span>
                ${hasAttachments ? '<span class="tile-pdf-pill">📄 2 dokumenty PDF</span>' : ''}
              </div>
              <h3 class="tile-title">${item.title}</h3>
              <div class="tile-action-row">
                <span class="tile-action-link">
                  Czytaj całość
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </span>
              </div>
            </div>
          </div>
        </article>
      `;
    });

    container.innerHTML = html;

    // Attach click and keyboard listeners to tiles
    container.querySelectorAll('.news-tile').forEach(tile => {
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

    // Check if the article's body HTML already contains an image to prevent duplication
    const bodyHasImage = Boolean(article.contentHtml && /<img[^>]+src=/i.test(article.contentHtml));
    const showFeaturedFigure = Boolean(article.featuredImage && !bodyHasImage);

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
