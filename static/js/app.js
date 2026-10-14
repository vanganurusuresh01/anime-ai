/**
 * AniVerse AI - Core Frontend Controller
 */

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Core Subsystems
  const watchlist = new WatchlistManager();
  const collab = new CollaborationManager(watchlist);
  const pitchTour = new PitchModeTour();
  let radarChart = null;

  // Active State
  let currentResults = [];
  let allCatalog = [];
  let userProfile = {
    psychological: 65,
    action_intensity: 60,
    narrative_complexity: 70,
    emotional_depth: 65,
    pacing: 60,
    darkness: 55,
    world_building: 70,
    philosophical: 65
  };

  // Blender State
  let selectedBlends = [];

  // DOM Elements
  const searchInput = document.getElementById('search-input');
  const searchBtn = document.getElementById('search-btn');
  const animeGrid = document.getElementById('anime-grid');
  const intentBanner = document.getElementById('intent-banner');
  const intentText = document.getElementById('intent-text');
  const presetChips = document.getElementById('preset-chips');
  const genreFilter = document.getElementById('genre-filter');
  const episodeFilter = document.getElementById('episode-filter');
  const sortFilter = document.getElementById('sort-filter');
  const watchlistCountBadge = document.getElementById('watchlist-count');

  // Modals
  const detailModal = document.getElementById('detail-modal');
  const detailModalClose = document.getElementById('detail-modal-close');
  const watchlistModal = document.getElementById('watchlist-modal');
  const watchlistModalClose = document.getElementById('watchlist-modal-close');
  const openWatchlistBtn = document.getElementById('open-watchlist-btn');

  // Sliders
  const sliders = {
    complexity: document.getElementById('slider-complexity'),
    emotion: document.getElementById('slider-emotion'),
    pacing: document.getElementById('slider-pacing'),
    darkness: document.getElementById('slider-darkness'),
    action: document.getElementById('slider-action'),
    world: document.getElementById('slider-world')
  };

  // Setup Radar
  try {
    radarChart = new DNARadarChart('dna-radar-canvas');
  } catch (e) {
    console.warn('Canvas radar setup error:', e);
  }

  // 1. Initialize & Fetch Initial Recommendations & Presets
  initApp();

  async function initApp() {
    updateWatchlistBadge();
    loadPresets();
    setupTabNavigation();
    setupEventListeners();
    setupSliderListeners();
    await fetchInitialCatalog();
    executeSearch("Mastermind psychological mind game with battle of wits under 25 episodes");
  }

  async function fetchInitialCatalog() {
    try {
      const res = await fetch('/api/anime');
      if (res.ok) {
        allCatalog = await res.json();
        populateBlenderOptions();
        populateCompareOptions();
      }
    } catch (e) {
      console.error('Failed to load anime catalog', e);
    }
  }

  // Preset Chips
  async function loadPresets() {
    try {
      const res = await fetch('/api/presets');
      if (!res.ok) return;
      const presets = await res.json();
      if (!presetChips) return;

      presetChips.innerHTML = presets.map(p => `
        <button class="chip-btn" data-prompt="${p.prompt}">
          <span>⚡</span> ${p.title}
        </button>
      `).join('');

      presetChips.querySelectorAll('.chip-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const prompt = btn.getAttribute('data-prompt');
          if (searchInput) searchInput.value = prompt;
          executeSearch(prompt);
        });
      });
    } catch (e) {
      console.warn('Could not load presets', e);
    }
  }

  // Search Dispatch
  async function executeSearch(promptOverride) {
    const prompt = promptOverride !== undefined ? promptOverride : (searchInput?.value || '');
    const maxEps = episodeFilter?.value ? parseInt(episodeFilter.value) : null;
    const genre = genreFilter?.value || null;
    const sortBy = sortFilter?.value || 'dna_match';

    showLoading();

    try {
      const payload = {
        prompt: prompt,
        max_episodes: maxEps,
        genre_filter: genre ? [genre] : null,
        sort_by: sortBy,
        limit: 20
      };

      const res = await fetch('/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error('Search failed');
      const data = await res.json();
      currentResults = data.results;

      // Update Intent Banner
      if (intentBanner && intentText) {
        intentBanner.style.display = 'flex';
        intentText.textContent = data.extracted_intent.summary || 'Custom Semantic Synthesis';
      }

      // Update Radar
      if (radarChart && data.target_dna) {
        radarChart.update(data.target_dna);
      }

      renderCards(currentResults);
    } catch (e) {
      console.error('Search error', e);
      showToast('Error performing AI search', 'error');
    }
  }

  function showLoading() {
    if (!animeGrid) return;
    animeGrid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align:center; padding: 4rem 1rem;">
        <div style="display:inline-block; width:48px; height:48px; border:3px solid rgba(0,242,254,0.2); border-top-color:#00f2fe; border-radius:50%; animation:spin 0.8s linear infinite;"></div>
        <p style="margin-top:1rem; color:#94a3b8; font-weight:600;">Analyzing 8D Anime DNA & Semantic Vectors...</p>
      </div>
      <style>@keyframes spin { to { transform: rotate(360deg); } }</style>
    `;
  }

  // Render Result Cards
  function renderCards(results) {
    if (!animeGrid) return;

    if (!results || results.length === 0) {
      animeGrid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align:center; padding: 4rem 1rem; color:#94a3b8;">
          <h3 style="color:#fff; margin-bottom:0.5rem;">No exact match found</h3>
          <p>Try widening your episode filter or exploring a different genre.</p>
        </div>
      `;
      return;
    }

    animeGrid.innerHTML = results.map(item => {
      const anime = item.anime;
      const score = item.compatibility_score;
      const isSaved = watchlist.has(anime.id);
      const epDisplay = anime.episodes > 1 ? `${anime.episodes} Eps` : 'Film';

      return `
        <div class="anime-card" data-id="${anime.id}">
          <div class="card-poster-wrap" onclick="window.AniVerse.openDetail('${anime.id}')">
            <img class="card-poster" src="${anime.image_url}" alt="${anime.title}" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1578632767115-351597cf2477?w=600&auto=format&fit=crop&q=80'" />
            <div class="poster-overlay">
              <div class="poster-top-badges">
                <div class="compatibility-pill">
                  <span>🧬</span> ${score}% DNA Match
                </div>
                <div class="score-badge">
                  <span>★</span> ${anime.score.toFixed(1)}
                </div>
              </div>
            </div>
          </div>
          
          <div class="card-body">
            <div class="card-meta-line">
              <span>${anime.studio}</span> • <span>${anime.year}</span> • <span>${epDisplay}</span>
            </div>
            
            <h3 class="card-title" onclick="window.AniVerse.openDetail('${anime.id}')">${anime.title}</h3>
            
            <div class="card-genres">
              ${anime.genres.slice(0, 3).map(g => `<span class="genre-tag">${g}</span>`).join('')}
            </div>

            <p class="card-synopsis">${anime.synopsis}</p>

            <div class="ai-reasoning-box">
              <div class="ai-reasoning-header">
                <span>🤖</span> AI Compatibility Analysis
              </div>
              <p>${item.ai_explanation}</p>
            </div>

            <div class="card-actions">
              <button class="btn-action-primary" onclick="window.AniVerse.openDetail('${anime.id}')">
                DNA Breakdown
              </button>
              <button class="btn-icon-action ${isSaved ? 'saved' : ''}" title="Save to Watchlist" onclick="window.AniVerse.toggleWatchlist('${anime.id}')">
                ${isSaved ? '🔖' : '➕'}
              </button>
              <button class="btn-icon-action" title="Like / Reinforce DNA" onclick="window.AniVerse.giveFeedback('${anime.id}', 'like')">
                👍
              </button>
              <button class="btn-icon-action" title="Dislike / Penalize DNA" onclick="window.AniVerse.giveFeedback('${anime.id}', 'dislike')">
                👎
              </button>
            </div>
          </div>
        </div>
      `;
    }).join('');
  }

  // Open Details Modal
  async function openDetail(animeId) {
    try {
      const res = await fetch(`/api/anime/${animeId}`);
      if (!res.ok) return;
      const data = await res.json();
      const anime = data.anime;
      const siblings = data.dna_siblings || [];

      const modalTitle = document.getElementById('modal-title');
      const modalBody = document.getElementById('modal-body-content');

      if (modalTitle) modalTitle.textContent = anime.title;
      if (modalBody) {
        modalBody.innerHTML = `
          <div style="display:flex; gap:1.5rem; flex-wrap:wrap; margin-bottom:1.5rem;">
            <img src="${anime.image_url}" style="width:160px; height:240px; object-fit:cover; border-radius:12px; box-shadow:0 10px 25px rgba(0,0,0,0.6);" />
            <div style="flex:1; min-width:260px;">
              <h3 style="font-size:1.4rem; margin-bottom:0.4rem; color:#fff;">${anime.title}</h3>
              <p style="font-size:0.85rem; color:#94a3b8; margin-bottom:0.75rem;">${anime.title_jp} • ${anime.studio} • ${anime.year} • ${anime.episodes} Episodes</p>
              <div style="display:flex; gap:6px; flex-wrap:wrap; margin-bottom:1rem;">
                ${anime.genres.map(g => `<span class="genre-tag" style="background:rgba(0,242,254,0.1); color:#00f2fe; border-color:rgba(0,242,254,0.3);">${g}</span>`).join('')}
                ${(anime.archetypes || []).map(a => `<span class="genre-tag" style="background:rgba(255,0,128,0.1); color:#ff0080; border-color:rgba(255,0,128,0.3);">${a}</span>`).join('')}
              </div>
              <p style="font-size:0.9rem; color:#cbd5e1; line-height:1.6; margin-bottom:1rem;">${anime.synopsis}</p>
              <div style="font-size:0.82rem; color:#fbbf24; background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.25); padding:0.6rem 0.8rem; border-radius:8px;">
                💡 <strong>Why Watch:</strong> ${anime.why_watch}
              </div>
            </div>
          </div>

          <h4 style="margin:1.5rem 0 0.75rem; color:#00f2fe; font-size:1rem; border-bottom:1px solid var(--border-subtle); padding-bottom:0.4rem;">
            🧬 8-Dimensional DNA Fingerprint
          </h4>
          <div class="detail-dna-bars">
            ${renderDNABar('Psychological Mind Games', anime.dna.psychological)}
            ${renderDNABar('Action & Combat Intensity', anime.dna.action_intensity)}
            ${renderDNABar('Narrative Complexity', anime.dna.narrative_complexity)}
            ${renderDNABar('Emotional Depth', anime.dna.emotional_depth)}
            ${renderDNABar('Pacing Momentum', anime.dna.pacing)}
            ${renderDNABar('Grimdark Tone', anime.dna.darkness)}
            ${renderDNABar('World Building & Lore', anime.dna.world_building)}
            ${renderDNABar('Philosophical Questions', anime.dna.philosophical)}
          </div>

          ${anime.dub_tier ? `
          <h4 style="margin:2rem 0 0.75rem; color:#fbbf24; font-size:1rem; border-bottom:1px solid var(--border-subtle); padding-bottom:0.4rem;">
            🎙️ Audio & Premium Metadata
          </h4>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-bottom:1rem;">
            <div style="background:rgba(251,191,36,0.06); border:1px solid rgba(251,191,36,0.2); border-radius:10px; padding:0.85rem;">
              <div style="font-size:0.72rem; color:#94a3b8; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0.3rem;">Dub Tier</div>
              <div style="font-size:1.1rem; font-weight:800; color:${anime.dub_tier.includes('S-Tier') ? '#fbbf24' : anime.dub_tier.includes('A-Tier') ? '#34d399' : '#94a3b8'};">
                ${anime.dub_tier.includes('S-Tier') ? '🏆' : anime.dub_tier.includes('A-Tier') ? '🎖️' : '🔉'} ${anime.dub_tier}
              </div>
            </div>
            <div style="background:rgba(192,132,252,0.06); border:1px solid rgba(192,132,252,0.2); border-radius:10px; padding:0.85rem;">
              <div style="font-size:0.72rem; color:#94a3b8; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0.3rem;">Soundtrack</div>
              <div style="font-size:1.1rem; font-weight:700; color:#c084fc;">🎵 ${anime.soundtrack_genre || 'Cinematic'}</div>
            </div>
          </div>
          ${anime.dub_cast && anime.dub_cast.length > 0 ? `
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-bottom:1rem;">
            <div>
              <div style="font-size:0.72rem; color:#00f2fe; text-transform:uppercase; font-weight:700; margin-bottom:0.4rem;">🇺🇸 English Dub Cast</div>
              ${anime.dub_cast.map(c => `<div style="font-size:0.8rem; color:#cbd5e1; padding:2px 0;">• ${c}</div>`).join('')}
            </div>
            ${anime.sub_cast && anime.sub_cast.length > 0 ? `
            <div>
              <div style="font-size:0.72rem; color:#ff0080; text-transform:uppercase; font-weight:700; margin-bottom:0.4rem;">🇯🇵 Japanese Sub Cast</div>
              ${anime.sub_cast.map(c => `<div style="font-size:0.8rem; color:#cbd5e1; padding:2px 0;">• ${c}</div>`).join('')}
            </div>
            ` : ''}
          </div>
          ` : ''}
          ${anime.iconic_quote ? `
          <div style="background:linear-gradient(135deg, rgba(0,242,254,0.04), rgba(192,132,252,0.04)); border-left:3px solid #c084fc; border-radius:0 8px 8px 0; padding:0.85rem 1rem; margin-bottom:1rem;">
            <div style="font-size:0.72rem; color:#94a3b8; text-transform:uppercase; margin-bottom:0.3rem;">Iconic Quote — ${anime.iconic_quote.speaker}</div>
            <div style="font-size:1rem; font-weight:600; color:#fff; font-style:italic; line-height:1.5;">"${anime.iconic_quote.en}"</div>
            ${anime.iconic_quote.jp ? `<div style="font-size:0.8rem; color:#64748b; margin-top:0.25rem;">${anime.iconic_quote.jp}</div>` : ''}
          </div>
          ` : ''}
          ${anime.streaming && anime.streaming.length > 0 ? `
          <div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-bottom:0.5rem;">
            <span style="font-size:0.72rem; color:#94a3b8; text-transform:uppercase; font-weight:700; align-self:center;">Available on:</span>
            ${anime.streaming.map(s => `<span style="background:rgba(0,242,254,0.08); border:1px solid rgba(0,242,254,0.2); color:#00f2fe; padding:2px 10px; border-radius:20px; font-size:0.75rem; font-weight:600;">${s}</span>`).join('')}
          </div>
          ` : ''}
          ` : ''}

          <h4 style="margin:2rem 0 0.75rem; color:#c084fc; font-size:1rem; border-bottom:1px solid var(--border-subtle); padding-bottom:0.4rem;">
            🔗 Closest DNA Siblings in Vector Space
          </h4>
          <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(180px, 1fr)); gap:1rem;">
            ${siblings.map(s => `
              <div style="background:rgba(255,255,255,0.03); border:1px solid var(--border-subtle); border-radius:10px; padding:0.75rem; text-align:center; cursor:pointer;" onclick="window.AniVerse.openDetail('${s.anime.id}')">
                <img src="${s.anime.image_url}" style="width:100%; height:140px; object-fit:cover; border-radius:6px; margin-bottom:0.5rem;" />
                <h5 style="font-size:0.82rem; color:#fff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${s.anime.title}</h5>
                <span style="font-size:0.75rem; color:#00f2fe; font-weight:700;">${s.similarity}% Similarity</span>
              </div>
            `).join('')}
          </div>
        `;
      }

      if (detailModal) detailModal.classList.add('active');
    } catch (e) {
      console.error('Failed to open detail modal', e);
    }
  }

  function renderDNABar(label, val) {
    return `
      <div class="dna-bar-item">
        <div class="dna-bar-label">
          <span>${label}</span>
          <span style="font-weight:700; color:#fff;">${Math.round(val)}%</span>
        </div>
        <div class="dna-bar-track">
          <div class="dna-bar-fill" style="width: ${val}%;"></div>
        </div>
      </div>
    `;
  }

  // Feedback Adaptation
  async function giveFeedback(animeId, action) {
    try {
      const res = await fetch('/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ anime_id: animeId, action: action })
      });
      if (res.ok) {
        const data = await res.json();
        showToast(`Taste DNA refined: ${action === 'like' ? '+ resonance' : '- resonance'} for ${data.anime_title}`);
        if (data.updated_profile && radarChart) {
          userProfile = data.updated_profile;
          // Refresh current search to reflect updated weights
          executeSearch();
        }
      }
    } catch (e) {
      console.error('Feedback failed', e);
    }
  }

  // Watchlist Toggle
  function toggleWatchlist(animeId) {
    const item = allCatalog.find(a => a.id === animeId) || currentResults.find(r => r.anime.id === animeId)?.anime;
    if (!item) return;

    const added = watchlist.toggle(item);
    updateWatchlistBadge();
    showToast(added ? `Added "${item.title}" to Watchlist` : `Removed "${item.title}" from Watchlist`);

    // Re-render cards to reflect icon change
    renderCards(currentResults);
  }

  function updateWatchlistBadge() {
    if (watchlistCountBadge) {
      watchlistCountBadge.textContent = watchlist.items.length;
    }
  }

  // Watchlist Modal & Binge Calculator Render
  function openWatchlistModal() {
    const body = document.getElementById('watchlist-modal-body');
    if (!body) return;

    const plan = watchlist.calculateBingePlan(1.5);
    const taste = watchlist.getWatchlistTasteDNA();
    const cleanser = watchlist.detectFatigueAndRecommendCleanser();
    const milestones = watchlist.calculateMilestoneSchedule(1.5);

    body.innerHTML = `
      <!-- ══════════════════ PREMIUM COLLABORATION PANEL ══════════════════ -->
      <div class="collab-panel" id="collab-panel-root">
        ${!collab.isPremium ? `
          <!-- LOCKED STATE -->
          <div class="collab-locked-banner">
            <div class="collab-lock-icon">👑</div>
            <div class="collab-lock-text">
              <span class="collab-lock-title">Watch Together — Premium Feature</span>
              <span class="collab-lock-sub">Create shared Watch Rooms, invite friends, merge watchlists & vote on what to watch next.</span>
            </div>
            <button class="btn-premium-unlock" onclick="window.AniVerse.collabActivatePremium()">
              Unlock Premium
            </button>
          </div>
        ` : collab.room ? `
          <!-- ACTIVE ROOM STATE -->
          <div class="collab-room-active">
            <div class="collab-room-header">
              <div>
                <span class="collab-badge-premium">👑 Premium</span>
                <span class="collab-room-name">🎬 ${collab.room.name}</span>
              </div>
              <div style="display:flex;gap:0.5rem;align-items:center;">
                <button class="btn-collab-secondary" onclick="window.AniVerse.collabSyncList()" title="Push your latest watchlist into the room">
                  🔄 Sync My List
                </button>
                <button class="btn-collab-danger" onclick="window.AniVerse.collabLeaveRoom()">Leave Room</button>
              </div>
            </div>

            <!-- Member Avatars -->
            <div class="collab-members-row">
              <span class="collab-section-label">👥 Members</span>
              <div class="collab-avatars">
                ${collab.members.map(m => `
                  <div class="collab-avatar" style="background:${m.color};" title="${m.name}">
                    ${m.name.charAt(0).toUpperCase()}
                  </div>
                `).join('')}
              </div>
            </div>

            <!-- Invite Link -->
            <div class="collab-invite-row">
              <span class="collab-section-label">🔗 Invite Link</span>
              <div class="collab-invite-input-row">
                <input class="collab-invite-input" id="collab-invite-link" readonly
                  value="${collab._buildInviteLink(collab.room.id, collab.room.name)}" />
                <button class="btn-collab-copy" onclick="window.AniVerse.collabCopyLink()">Copy</button>
              </div>
            </div>

            <!-- Simulate friend joining -->
            <div class="collab-invite-row">
              <span class="collab-section-label">➕ Simulate Friend Join</span>
              <div class="collab-invite-input-row">
                <input class="collab-invite-input" id="collab-friend-name" placeholder="Friend's name…" />
                <button class="btn-collab-secondary" onclick="window.AniVerse.collabSimulateJoin()">Add Friend</button>
              </div>
            </div>

            <!-- Shared Watchlist with voting -->
            <div class="collab-shared-list-wrap">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;">
                <span class="collab-section-label">🗳️ Shared Watchlist — Vote for Next</span>
                <button class="btn-collab-secondary" style="font-size:0.72rem;" onclick="window.AniVerse.collabExportShared()">Export JSON</button>
              </div>
              <div id="collab-shared-list" class="collab-shared-list">
                ${collab.getRankedSharedList().length === 0 ? `
                  <p style="color:#64748b;font-size:0.84rem;text-align:center;padding:1rem;">
                    No titles yet. Sync your list or invite a friend to populate the shared room.
                  </p>
                ` : collab.getRankedSharedList().map(item => `
                  <div class="collab-shared-item">
                    <img src="${item.image_url}" class="collab-shared-poster" />
                    <div class="collab-shared-info">
                      <span class="collab-shared-title">${item.title}</span>
                      <span class="collab-shared-meta">Added by <strong style="color:${collab.members.find(m=>m.id===item.addedBy)?.color||'#00f2fe'}">${item.addedByName||'—'}</strong></span>
                    </div>
                    <div class="collab-vote-wrap">
                      <button class="btn-vote" onclick="window.AniVerse.collabVote('${item.id}')">👍</button>
                      <span class="collab-vote-count" id="vote-${item.id}">${collab.room.votes[item.id]||0}</span>
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>
          </div>
        ` : `
          <!-- PREMIUM UNLOCKED — NO ROOM YET -->
          <div class="collab-create-room">
            <div class="collab-create-header">
              <span class="collab-badge-premium">👑 Premium Active</span>
              <span style="color:#94a3b8;font-size:0.82rem;">Hello, <strong style="color:#fff;">${collab.localUserName}</strong> — start a Watch Party with friends!</span>
            </div>
            <div class="collab-invite-input-row" style="margin-top:0.75rem;">
              <input class="collab-invite-input" id="collab-room-name-input" placeholder="Room name (e.g. Friday Night Anime)" />
              <button class="btn-premium-unlock" style="white-space:nowrap;" onclick="window.AniVerse.collabCreateRoom()">Create Room 🚀</button>
            </div>
          </div>
        `}
      </div>
      <!-- ════════════════════════════════════════════════════════════════ -->

      ${taste.hasData ? `
        <div style="background:linear-gradient(135deg, rgba(0,242,254,0.12), rgba(121,40,202,0.12)); border:1px solid rgba(0,242,254,0.3); border-radius:12px; padding:1.25rem; margin-bottom:1.5rem;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
            <span style="font-size:0.75rem; font-weight:800; color:#00f2fe; text-transform:uppercase; letter-spacing:0.5px;">🧬 Your Watchlist DNA Persona</span>
            <span style="background:rgba(0,242,254,0.2); color:#00f2fe; padding:2px 8px; border-radius:4px; font-size:0.75rem; font-weight:700;">${taste.totalTracked} Titles Synthesized</span>
          </div>
          <h4 style="font-size:1.25rem; font-weight:800; color:#fff; margin-bottom:0.25rem;">${taste.persona}</h4>
          <p style="font-size:0.85rem; color:#cbd5e1; line-height:1.4;">${taste.description}</p>
        </div>
      ` : ''}

      ${cleanser ? `
        <div style="background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.3); border-radius:10px; padding:1rem 1.25rem; margin-bottom:1.5rem; display:flex; align-items:flex-start; gap:0.75rem;">
          <span style="font-size:1.3rem;">⚡</span>
          <div>
            <strong style="color:#fbbf24; font-size:0.88rem; display:block; margin-bottom:2px;">Binge Strain Warning: ${cleanser.risk}</strong>
            <p style="font-size:0.8rem; color:#94a3b8; margin-bottom:4px;">${cleanser.message}</p>
            <span style="font-size:0.78rem; color:#00f2fe;">💡 Recommended Palate Cleanser: <strong>${cleanser.recommendedCleanser}</strong></span>
          </div>
        </div>
      ` : ''}

      <div style="background:rgba(0,242,254,0.06); border:1px solid rgba(0,242,254,0.25); border-radius:12px; padding:1.25rem; margin-bottom:1.5rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
          <div>
            <h4 style="color:#00f2fe; margin-bottom:0.25rem; font-size:1.1rem;">⏱️ Smart Binge Commitment Calculator</h4>
            <p style="font-size:0.84rem; color:#94a3b8;">Plan your viewing schedule effortlessly based on your daily free time.</p>
          </div>
          <div style="display:flex; align-items:center; gap:0.5rem;">
            <label style="font-size:0.82rem; color:#cbd5e1;">Daily Watch Time:</label>
            <select id="binge-hours-select" class="filter-select" style="padding:4px 8px;">
              <option value="0.5">30 mins / day</option>
              <option value="1.0">1.0 hr / day</option>
              <option value="1.5" selected>1.5 hrs / day</option>
              <option value="2.0">2.0 hrs / day</option>
              <option value="3.0">3.0 hrs / day</option>
            </select>
          </div>
        </div>
        
        <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:1rem; margin-top:1.25rem; text-align:center;">
          <div style="background:rgba(255,255,255,0.03); padding:0.75rem; border-radius:8px;">
            <span style="font-size:1.4rem; font-weight:800; color:#fff;" id="binge-stat-eps">${plan.totalEpisodes}</span>
            <div style="font-size:0.72rem; color:#94a3b8; text-transform:uppercase;">Remaining Eps</div>
          </div>
          <div style="background:rgba(255,255,255,0.03); padding:0.75rem; border-radius:8px;">
            <span style="font-size:1.4rem; font-weight:800; color:#00f2fe;" id="binge-stat-hrs">${plan.totalHours}h</span>
            <div style="font-size:0.72rem; color:#94a3b8; text-transform:uppercase;">Total Hours</div>
          </div>
          <div style="background:rgba(255,255,255,0.03); padding:0.75rem; border-radius:8px;">
            <span style="font-size:1.4rem; font-weight:800; color:#c084fc;" id="binge-stat-days">${plan.daysToFinish}</span>
            <div style="font-size:0.72rem; color:#94a3b8; text-transform:uppercase;">Days to Finish</div>
          </div>
          <div style="background:rgba(255,255,255,0.03); padding:0.75rem; border-radius:8px;">
            <span style="font-size:1.4rem; font-weight:800; color:#ff0080;" id="binge-stat-daily">${plan.epsPerDay}</span>
            <div style="font-size:0.72rem; color:#94a3b8; text-transform:uppercase;">Target Eps/Day</div>
          </div>
        </div>

        ${milestones.length > 0 ? `
          <div style="margin-top:1.25rem; padding-top:1rem; border-top:1px solid rgba(255,255,255,0.08);">
            <div style="font-size:0.8rem; font-weight:700; color:#cbd5e1; margin-bottom:0.5rem;">📅 Predicted Completion Milestones:</div>
            <div id="milestones-timeline-wrap" style="display:flex; gap:0.5rem; flex-wrap:wrap;">
              ${milestones.map(m => `
                <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border-subtle); border-radius:6px; padding:0.35rem 0.65rem; font-size:0.75rem;">
                  <strong style="color:#fff;">${m.title}</strong>: <span style="color:#00f2fe;">${m.finishDateFormatted}</span> (${m.daysNeeded}d)
                </div>
              `).join('')}
            </div>
          </div>
        ` : ''}
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
        <h4 style="font-size:1rem; color:#fff;">Saved Titles (${watchlist.items.length})</h4>
        <button class="btn-action-primary" style="padding:4px 12px; font-size:0.75rem;" onclick="window.AniVerse.exportWatchlist()">
          Export JSON
        </button>
      </div>

      <div style="display:flex; flex-direction:column; gap:0.75rem;">
        ${watchlist.items.length === 0 ? '<p style="color:#64748b; text-align:center; padding:2rem;">Your watchlist is currently empty. Bookmark titles from recommendations to plan your binge!</p>' : ''}
        ${watchlist.items.map(item => `
          <div style="display:flex; align-items:center; justify-content:space-between; background:rgba(255,255,255,0.03); border:1px solid var(--border-subtle); border-radius:10px; padding:0.75rem 1rem;">
            <div style="display:flex; align-items:center; gap:1rem;">
              <img src="${item.image_url}" style="width:48px; height:68px; object-fit:cover; border-radius:6px;" />
              <div>
                <h5 style="color:#fff; font-size:0.95rem; margin-bottom:0.25rem;">${item.title}</h5>
                <span style="font-size:0.78rem; color:#94a3b8;">${item.episodes} episodes • ★ ${item.score}</span>
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:0.75rem;">
              <select class="filter-select" style="padding:4px 8px; font-size:0.75rem;" onchange="window.AniVerse.updateWatchlistStatus('${item.id}', this.value)">
                <option value="plan_to_watch" ${item.status === 'plan_to_watch' ? 'selected' : ''}>Plan to Watch</option>
                <option value="watching" ${item.status === 'watching' ? 'selected' : ''}>Watching</option>
                <option value="completed" ${item.status === 'completed' ? 'selected' : ''}>Completed</option>
              </select>
              <button class="btn-icon-action" style="color:#ef4444;" onclick="window.AniVerse.removeWatchlist('${item.id}')">
                🗑️
              </button>
            </div>
          </div>
        `).join('')}
      </div>
    `;

    // Hook up Binge Select Change
    const bingeSelect = document.getElementById('binge-hours-select');
    if (bingeSelect) {
      bingeSelect.addEventListener('change', (e) => {
        const hours = parseFloat(e.target.value);
        const p = watchlist.calculateBingePlan(hours);
        document.getElementById('binge-stat-days').textContent = p.daysToFinish;
        document.getElementById('binge-stat-daily').textContent = p.epsPerDay;

        const updatedMilestones = watchlist.calculateMilestoneSchedule(hours);
        const wrap = document.getElementById('milestones-timeline-wrap');
        if (wrap) {
          wrap.innerHTML = updatedMilestones.map(m => `
            <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border-subtle); border-radius:6px; padding:0.35rem 0.65rem; font-size:0.75rem;">
              <strong style="color:#fff;">${m.title}</strong>: <span style="color:#00f2fe;">${m.finishDateFormatted}</span> (${m.daysNeeded}d)
            </div>
          `).join('');
        }
      });
    }

    if (watchlistModal) watchlistModal.classList.add('active');
  }

  // Taste Blender Options
  function populateBlenderOptions() {
    const s1 = document.getElementById('blend-select-1');
    const s2 = document.getElementById('blend-select-2');
    if (!s1 || !s2) return;

    const options = allCatalog.map(a => `<option value="${a.id}">${a.title} (${a.genres.slice(0, 2).join(', ')})</option>`).join('');
    s1.innerHTML = `<option value="">Select First Anchor Anime...</option>` + options;
    s2.innerHTML = `<option value="">Select Second Anchor Anime...</option>` + options;

    // Defaults
    s1.value = 'death-note';
    s2.value = 'cyberpunk-edgerunners';
  }

  // Execute Taste Blend
  async function executeBlend() {
    const s1 = document.getElementById('blend-select-1')?.value;
    const s2 = document.getElementById('blend-select-2')?.value;
    const blendResultsContainer = document.getElementById('blend-results-grid');

    if (!s1 || !s2) {
      showToast('Select 2 anime to blend', 'warn');
      return;
    }

    if (blendResultsContainer) {
      blendResultsContainer.innerHTML = '<div style="grid-column:1/-1; text-align:center; padding:2rem; color:#94a3b8;">Synthesizing DNA centroid in 8D vector space...</div>';
    }

    try {
      const res = await fetch('/api/blend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ anime_ids: [s1, s2], limit: 8 })
      });

      if (!res.ok) throw new Error('Blend failed');
      const data = await res.json();

      if (blendResultsContainer) {
        blendResultsContainer.innerHTML = data.results.map(item => `
          <div class="anime-card" style="background:rgba(20,24,40,0.85);">
            <div class="card-poster-wrap" onclick="window.AniVerse.openDetail('${item.anime.id}')">
              <img class="card-poster" src="${item.anime.image_url}" alt="${item.anime.title}" />
              <div class="poster-overlay">
                <div class="poster-top-badges">
                  <div class="compatibility-pill">🧬 ${item.compatibility_score}% Hybrid Fit</div>
                  <div class="score-badge">★ ${item.anime.score}</div>
                </div>
              </div>
            </div>
            <div class="card-body">
              <h4 class="card-title" onclick="window.AniVerse.openDetail('${item.anime.id}')">${item.anime.title}</h4>
              <p style="font-size:0.75rem; color:#00f2fe; margin-bottom:0.5rem;">${item.ai_explanation}</p>
              <button class="btn-action-primary" style="margin-top:auto;" onclick="window.AniVerse.openDetail('${item.anime.id}')">View Details</button>
            </div>
          </div>
        `).join('');
      }
    } catch (e) {
      console.error('Blend error', e);
      showToast('Failed to blend anime DNA', 'error');
    }
  }

  // Populate Compare Options
  function populateCompareOptions() {
    const s1 = document.getElementById('compare-select-1');
    const s2 = document.getElementById('compare-select-2');
    if (!s1 || !s2) return;

    const options = allCatalog.map(a => `<option value="${a.id}">${a.title} (${a.year})</option>`).join('');
    s1.innerHTML = `<option value="">Select First Title...</option>` + options;
    s2.innerHTML = `<option value="">Select Second Title...</option>` + options;

    s1.value = 'death-note';
    s2.value = 'monster';
  }

  let compareRadarChart = null;

  async function executeCompare() {
    const id1 = document.getElementById('compare-select-1')?.value;
    const id2 = document.getElementById('compare-select-2')?.value;
    const resultBox = document.getElementById('compare-result-container');
    if (!id1 || !id2) {
      showToast('Select 2 anime to compare', 'warn');
      return;
    }
    if (id1 === id2) {
      showToast('Please select two distinct anime titles', 'warn');
      return;
    }

    try {
      const res = await fetch('/api/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ anime_id_1: id1, anime_id_2: id2 })
      });
      if (!res.ok) throw new Error('Comparison failed');
      const data = await res.json();

      if (resultBox) resultBox.style.display = 'block';

      // Setup Compare Radar
      if (!compareRadarChart) {
        compareRadarChart = new DNARadarChart('compare-radar-canvas');
      } else {
        compareRadarChart.setupCanvas();
      }

      const v1 = [
        data.dna_1.psychological,
        data.dna_1.action_intensity,
        data.dna_1.narrative_complexity,
        data.dna_1.emotional_depth,
        data.dna_1.pacing,
        data.dna_1.darkness,
        data.dna_1.world_building,
        data.dna_1.philosophical
      ];
      const v2 = [
        data.dna_2.psychological,
        data.dna_2.action_intensity,
        data.dna_2.narrative_complexity,
        data.dna_2.emotional_depth,
        data.dna_2.pacing,
        data.dna_2.darkness,
        data.dna_2.world_building,
        data.dna_2.philosophical
      ];

      compareRadarChart.drawComparison(v1, v2, data.anime_1.title, data.anime_2.title);

      // Populate text insights
      const overlapPill = document.getElementById('compare-overlap-pill');
      const summaryText = document.getElementById('compare-summary-text');
      const divList = document.getElementById('compare-divergences-list');
      const deltaTable = document.getElementById('compare-deltas-table');

      if (overlapPill) overlapPill.textContent = `${data.overlap_score}% Narrative Overlap`;
      if (summaryText) summaryText.textContent = data.comparison_summary;

      if (divList) {
        divList.innerHTML = data.divergence_highlights.map(h => `
          <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border-subtle); padding:0.5rem 0.75rem; border-radius:6px; font-size:0.8rem; color:#e2e8f0;">
            🔹 ${h}
          </div>
        `).join('') || '<div style="color:#94a3b8; font-size:0.8rem;">Parity across primary dimensions</div>';
      }

      if (deltaTable) {
        deltaTable.innerHTML = Object.entries(data.dimension_deltas).map(([k, diff]) => {
          const col = diff > 0 ? '#00f2fe' : (diff < 0 ? '#ff0080' : '#94a3b8');
          const sign = diff > 0 ? `+${diff}% (${data.anime_1.title.substring(0, 10)})` : (diff < 0 ? `${diff}% (${data.anime_2.title.substring(0, 10)})` : 'Even');
          return `
            <div style="background:rgba(255,255,255,0.02); padding:0.4rem 0.6rem; border-radius:4px; display:flex; justify-content:space-between;">
              <span style="color:#94a3b8;">${k.replace('_', ' ').toUpperCase()}</span>
              <span style="color:${col}; font-weight:700;">${sign}</span>
            </div>
          `;
        }).join('');
      }

    } catch (e) {
      console.error('Comparison error', e);
      showToast('Failed to compare anime', 'error');
    }
  }

  // Quiz Listener
  function setupQuizListener() {
    const form = document.getElementById('quiz-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const mood = form.querySelector('input[name="quiz-mood"]:checked')?.value || 'mind_games';
      const complexity = form.querySelector('input[name="quiz-complexity"]:checked')?.value || 'mind_bending';
      const pacing = form.querySelector('input[name="quiz-pacing"]:checked')?.value || 'breakneck';
      const budget = form.querySelector('input[name="quiz-budget"]:checked')?.value || 'under_26';

      showToast('Synthesizing your personal Anime DNA from quiz results...', 'info');

      try {
        const res = await fetch('/api/quiz', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            mood,
            complexity,
            pacing,
            episode_budget: budget
          })
        });

        if (!res.ok) throw new Error('Quiz synthesis failed');
        const data = await res.json();
        currentResults = data.results;

        // Switch back to discovery
        switchTab('tab-discovery');
        if (intentBanner && intentText) {
          intentBanner.style.display = 'flex';
          intentText.textContent = `🎯 Quiz Result Profile: ${mood.replace('_', ' ').toUpperCase()} | Pacing: ${pacing.toUpperCase()}`;
        }
        if (radarChart && data.target_dna) {
          radarChart.update(data.target_dna);
        }
        renderCards(currentResults);
        showToast('Found tailored anime matches based on your Quiz!', 'info');
      } catch (err) {
        console.error('Quiz error', err);
        showToast('Error synthesizing quiz DNA', 'error');
      }
    });
  }

  // Live Jikan Search
  let searchTimer = null;
  function handleLiveExternalSearch(query) {
    clearTimeout(searchTimer);
    const container = document.getElementById('external-results-grid');
    if (!container) return;

    if (!query || query.length < 2) {
      container.innerHTML = '<p style="color:#64748b; text-align:center; padding:2rem;">Type an anime title above to search the global MyAnimeList universe.</p>';
      return;
    }

    container.innerHTML = '<p style="color:#00f2fe; text-align:center; padding:2rem;">Querying live Jikan API and inferring DNA vectors on the fly...</p>';

    searchTimer = setTimeout(async () => {
      try {
        const res = await fetch(`/api/external/search?q=${encodeURIComponent(query)}`);
        if (!res.ok) throw new Error('Live search failed');
        const data = await res.json();
        
        if (!data.results || data.results.length === 0) {
          container.innerHTML = '<p style="color:#94a3b8; text-align:center; padding:2rem;">No titles found on MyAnimeList for this query.</p>';
          return;
        }

        container.innerHTML = data.results.map(anime => `
          <div class="anime-card" style="background:rgba(20,24,40,0.85);">
            <div class="card-poster-wrap" onclick="window.AniVerse.openDetail('${anime.id}')">
              <img class="card-poster" src="${anime.image_url}" alt="${anime.title}" />
              <div class="poster-overlay">
                <div class="poster-top-badges">
                  <div class="compatibility-pill">🌐 Live MAL</div>
                  <div class="score-badge">★ ${anime.score}</div>
                </div>
              </div>
            </div>
            <div class="card-body">
              <h4 class="card-title" onclick="window.AniVerse.openDetail('${anime.id}')">${anime.title}</h4>
              <p style="font-size:0.75rem; color:#94a3b8; margin-bottom:0.5rem;">${anime.episodes} eps • ${anime.genres.join(', ')}</p>
              <button class="btn-action-primary" style="margin-top:auto;" onclick="window.AniVerse.openDetail('${anime.id}')">View Inferred DNA</button>
            </div>
          </div>
        `).join('');
      } catch (e) {
        container.innerHTML = '<p style="color:#ef4444; text-align:center; padding:2rem;">MyAnimeList live search rate limited or offline. Please retry in a moment.</p>';
      }
    }, 450);
  }

  // Setup Sliders
  function setupSliderListeners() {
    const sliderComplexity = document.getElementById('slider-complexity');
    const sliderEmotion = document.getElementById('slider-emotion');
    const sliderPacing = document.getElementById('slider-pacing');
    const sliderDarkness = document.getElementById('slider-darkness');
    const sliderAction = document.getElementById('slider-action');
    const sliderWorld = document.getElementById('slider-world');

    const updateFromSliders = () => {
      const vComplexity = parseFloat(sliderComplexity?.value || 50);
      const vEmotion = parseFloat(sliderEmotion?.value || 50);
      const vPacing = parseFloat(sliderPacing?.value || 50);
      const vDarkness = parseFloat(sliderDarkness?.value || 50);
      const vAction = parseFloat(sliderAction?.value || 50);
      const vWorld = parseFloat(sliderWorld?.value || 50);

      // Update badge text
      document.getElementById('val-complexity').textContent = vComplexity;
      document.getElementById('val-emotion').textContent = vEmotion;
      document.getElementById('val-pacing').textContent = vPacing;
      document.getElementById('val-darkness').textContent = vDarkness;
      document.getElementById('val-action').textContent = vAction;
      document.getElementById('val-world').textContent = vWorld;

      // Update vector in radar
      if (radarChart) {
        radarChart.update([
          vComplexity * 0.95, // psychological correlation
          vAction,
          vComplexity,
          vEmotion,
          vPacing,
          vDarkness,
          vWorld,
          (vComplexity + vEmotion) * 0.5
        ]);
      }
    };

    [sliderComplexity, sliderEmotion, sliderPacing, sliderDarkness, sliderAction, sliderWorld].forEach(sl => {
      if (sl) sl.addEventListener('input', updateFromSliders);
    });

    const btnCalibrateSearch = document.getElementById('btn-calibrate-search');
    if (btnCalibrateSearch) {
      btnCalibrateSearch.addEventListener('click', () => {
        const vComplexity = parseFloat(sliderComplexity?.value || 50);
        const vEmotion = parseFloat(sliderEmotion?.value || 50);
        const vPacing = parseFloat(sliderPacing?.value || 50);
        const vDarkness = parseFloat(sliderDarkness?.value || 50);
        const vAction = parseFloat(sliderAction?.value || 50);
        const vWorld = parseFloat(sliderWorld?.value || 50);

        const customDNA = {
          psychological: vComplexity * 0.95,
          action_intensity: vAction,
          narrative_complexity: vComplexity,
          emotional_depth: vEmotion,
          pacing: vPacing,
          darkness: vDarkness,
          world_building: vWorld,
          philosophical: (vComplexity + vEmotion) * 0.5
        };

        // Switch to Discovery tab and run query with DNA override
        switchTab('tab-discovery');
        showLoading();

        fetch('/api/recommend', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ dna_override: customDNA, limit: 15 })
        })
        .then(res => res.json())
        .then(data => {
          currentResults = data.results;
          if (intentBanner && intentText) {
            intentBanner.style.display = 'flex';
            intentText.textContent = "Custom DNA Vector Calibration Applied";
          }
          renderCards(currentResults);
        });
      });
    }
  }

  // Setup Tab Navigation
  function setupTabNavigation() {
    const tabBtns = document.querySelectorAll('.nav-tab-btn');
    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const tabTarget = btn.getAttribute('data-tab');
        switchTab(tabTarget);
      });
    });
  }

  function switchTab(tabId) {
    document.querySelectorAll('.nav-tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-view').forEach(v => v.style.display = 'none');

    const activeBtn = document.querySelector(`.nav-tab-btn[data-tab="${tabId}"]`);
    const activeView = document.getElementById(tabId);

    if (activeBtn) activeBtn.classList.add('active');
    if (activeView) activeView.style.display = 'block';

    if (tabId === 'tab-dna-studio' && radarChart) {
      setTimeout(() => radarChart.setupCanvas(), 50);
    }
    if (tabId === 'tab-compare' && compareRadarChart) {
      setTimeout(() => compareRadarChart.setupCanvas(), 50);
    }
  }

  // Event Listeners
  function setupEventListeners() {
    if (searchBtn) {
      searchBtn.addEventListener('click', () => executeSearch());
    }

    if (searchInput) {
      searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') executeSearch();
      });
    }

    if (genreFilter) genreFilter.addEventListener('change', () => executeSearch());
    if (episodeFilter) episodeFilter.addEventListener('change', () => executeSearch());
    if (sortFilter) sortFilter.addEventListener('change', () => executeSearch());

    // Blend Button
    const btnBlend = document.getElementById('btn-execute-blend');
    if (btnBlend) btnBlend.addEventListener('click', executeBlend);

    // Compare Button
    const btnCompare = document.getElementById('btn-execute-compare');
    if (btnCompare) btnCompare.addEventListener('click', executeCompare);

    // Setup Quiz Form Listener
    setupQuizListener();

    // Live MAL Search Input
    const externalInput = document.getElementById('external-search-input');
    if (externalInput) {
      externalInput.addEventListener('input', (e) => handleLiveExternalSearch(e.target.value));
    }

    // Modal Closures
    if (detailModalClose) detailModalClose.addEventListener('click', () => detailModal.classList.remove('active'));
    if (detailModal) {
      detailModal.addEventListener('click', (e) => {
        if (e.target === detailModal) detailModal.classList.remove('active');
      });
    }

    if (openWatchlistBtn) openWatchlistBtn.addEventListener('click', openWatchlistModal);
    if (watchlistModalClose) watchlistModalClose.addEventListener('click', () => watchlistModal.classList.remove('active'));
    if (watchlistModal) {
      watchlistModal.addEventListener('click', (e) => {
        if (e.target === watchlistModal) watchlistModal.classList.remove('active');
      });
    }
  }

  // Toast System
  function showToast(msg, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast';
    const icon = type === 'error' ? '⚠️' : (type === 'warn' ? '⚡' : '✨');
    toast.innerHTML = `<span>${icon}</span> <span>${msg}</span>`;

    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3200);
  }

  // Expose global window API for inline onclick handlers
  window.AniVerse = {
    openDetail,
    toggleWatchlist,
    giveFeedback,
    executeSearch,
    removeWatchlist: (id) => {
      watchlist.remove(id);
      updateWatchlistBadge();
      openWatchlistModal();
    },
    updateWatchlistStatus: (id, status) => {
      watchlist.updateStatus(id, status);
      openWatchlistModal();
    },
    exportWatchlist: () => {
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(watchlist.exportJSON());
      const dlAnchor = document.createElement('a');
      dlAnchor.setAttribute("href", dataStr);
      dlAnchor.setAttribute("download", "aniverse_watchlist.json");
      dlAnchor.click();
      dlAnchor.remove();
      showToast('Watchlist exported as JSON!');
    },

    // ── Premium Collaboration API ──────────────────────────────────────
    collabActivatePremium: () => {
      const name = prompt('Enter your display name for the Watch Room:', 'Anime Fan') || 'Anime Fan';
      collab.activatePremium(name);
      showToast(`👑 Premium activated! Welcome, ${name}!`);
      openWatchlistModal(); // re-render with unlocked state
    },

    collabCreateRoom: () => {
      const input = document.getElementById('collab-room-name-input');
      const roomName = (input && input.value.trim()) || 'Watch Party';
      const result = collab.createRoom(roomName);
      if (result.success) {
        collab.syncMyList();
        showToast(`🚀 Room "${roomName}" created! Share the invite link.`);
        openWatchlistModal();
      } else {
        showToast(result.error, 'error');
      }
    },

    collabSimulateJoin: () => {
      const input = document.getElementById('collab-friend-name');
      const friendName = (input && input.value.trim()) || 'Friend';
      if (!collab.room) { showToast('Create a room first.', 'warn'); return; }
      const result = collab.joinRoom(collab.room.id, friendName);
      if (result.success) {
        showToast(`🎉 ${friendName} joined the Watch Room!`);
        openWatchlistModal();
      } else {
        showToast(result.error, 'error');
      }
    },

    collabSyncList: () => {
      collab.syncMyList();
      showToast('🔄 Your watchlist synced to the room!');
      openWatchlistModal();
    },

    collabVote: (animeId) => {
      const votes = collab.vote(animeId);
      if (votes) {
        const el = document.getElementById(`vote-${animeId}`);
        if (el) el.textContent = votes[animeId] || 0;
        showToast('🗳️ Vote counted!');
      }
    },

    collabCopyLink: () => {
      const input = document.getElementById('collab-invite-link');
      if (input) {
        navigator.clipboard.writeText(input.value)
          .then(() => showToast('🔗 Invite link copied to clipboard!'))
          .catch(() => { input.select(); document.execCommand('copy'); showToast('🔗 Link copied!'); });
      }
    },

    collabExportShared: () => {
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(collab.exportSharedJSON());
      const dlAnchor = document.createElement('a');
      dlAnchor.setAttribute("href", dataStr);
      dlAnchor.setAttribute("download", "aniverse_shared_watchlist.json");
      dlAnchor.click();
      dlAnchor.remove();
      showToast('📦 Shared watchlist exported!');
    },

    collabLeaveRoom: () => {
      if (!confirm('Leave the Watch Room? This will remove the shared room from your device.')) return;
      collab.leaveRoom();
      showToast('👋 Left the Watch Room.');
      openWatchlistModal();
    }
  };
});
