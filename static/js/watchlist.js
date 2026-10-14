/**
 * AniVerse AI - Watchlist & Viewing Commitment Manager
 * Features LocalStorage persistence, progress tracking, and Binge Time Calculator.
 */

class WatchlistManager {
  constructor() {
    this.storageKey = 'aniverse_watchlist_v1';
    this.items = this.load();
    this.listeners = [];
  }

  load() {
    try {
      const data = localStorage.getItem(this.storageKey);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      console.warn('Failed to load watchlist from localStorage', e);
      return [];
    }
  }

  save() {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(this.items));
      this.notify();
    } catch (e) {
      console.error('Failed to save watchlist', e);
    }
  }

  subscribe(listener) {
    this.listeners.push(listener);
    listener(this.items);
  }

  notify() {
    this.listeners.forEach(fn => fn(this.items));
  }

  has(animeId) {
    return this.items.some(i => i.id === animeId);
  }

  toggle(anime) {
    const idx = this.items.findIndex(i => i.id === anime.id);
    if (idx >= 0) {
      this.items.splice(idx, 1);
      this.save();
      return false; // removed
    } else {
      this.items.push({
        id: anime.id,
        title: anime.title,
        image_url: anime.image_url,
        score: anime.score,
        episodes: anime.episodes || 12,
        duration_min: anime.duration_min || 24,
        genres: anime.genres || [],
        dna: anime.dna || null,
        status: 'plan_to_watch',
        current_ep: 0,
        added_at: new Date().toISOString()
      });
      this.save();
      return true; // added
    }
  }

  updateStatus(animeId, status, currentEp = 0) {
    const item = this.items.find(i => i.id === animeId);
    if (item) {
      item.status = status;
      if (currentEp !== undefined) item.current_ep = currentEp;
      this.save();
    }
  }

  remove(animeId) {
    this.items = this.items.filter(i => i.id !== animeId);
    this.save();
  }

  /**
   * Binge Commitment Calculator
   * Returns total episodes, hours, and days required at a given daily watch budget.
   */
  calculateBingePlan(dailyHours = 1.0) {
    const activeItems = this.items.filter(i => i.status !== 'completed');
    let totalEpisodes = 0;
    let totalMinutes = 0;

    activeItems.forEach(item => {
      const remainingEps = Math.max(0, item.episodes - (item.current_ep || 0));
      totalEpisodes += remainingEps;
      totalMinutes += remainingEps * (item.duration_min || 24);
    });

    const totalHours = totalMinutes / 60;
    const dailyMinutes = dailyHours * 60;
    const daysToFinish = dailyMinutes > 0 ? Math.ceil(totalMinutes / dailyMinutes) : 0;
    const epsPerDay = (dailyHours * 60) / 24;

    return {
      totalItems: activeItems.length,
      totalEpisodes,
      totalHours: round(totalHours, 1),
      dailyHours,
      daysToFinish,
      epsPerDay: round(epsPerDay, 1)
    };
  }

  /**
   * UNIQUE INNOVATION: Watchlist Taste DNA Fingerprint
   * Computes the aggregated 8D vector of all titles on the user's watchlist
   * and derives their personalized Otaku Persona.
   */
  getWatchlistTasteDNA() {
    const withDna = this.items.filter(i => i.dna);
    if (withDna.length === 0) {
      return {
        hasData: false,
        persona: "Aspiring Watcher",
        dna: null
      };
    }

    const dims = [
      'psychological', 'action_intensity', 'narrative_complexity',
      'emotional_depth', 'pacing', 'darkness', 'world_building', 'philosophical'
    ];

    const avg = {};
    dims.forEach(d => {
      const sum = withDna.reduce((acc, curr) => acc + (curr.dna[d] || 50), 0);
      avg[d] = Math.round(sum / withDna.length);
    });

    // Derive Unique Otaku Persona Title
    let persona = "Eclectic Connoisseur";
    let badgeClass = "badge-connoisseur";
    let description = "Balanced appreciation across diverse anime storytelling traditions.";

    if (avg.psychological >= 78 && avg.narrative_complexity >= 75) {
      persona = "Mastermind Chessmaster";
      description = "Drawn to high-stakes psychological battles, tactical deception, and intricate plot architecture.";
    } else if (avg.action_intensity >= 80 && avg.pacing >= 75) {
      persona = "Sakuga Kinetic Hunter";
      description = "Craves breakneck momentum, explosive fight choreography, and peak visual adrenaline.";
    } else if (avg.emotional_depth >= 82 && avg.philosophical >= 72) {
      persona = "Existential Heartseeker";
      description = "Seeks poignant human vulnerability, philosophical weight, and soul-stirring catharsis.";
    } else if (avg.world_building >= 82) {
      persona = "Mythic Lore Cartographer";
      description = "Immerses in vast fictional universes, deep history, and sprawling world-building.";
    } else if (avg.darkness <= 35 && avg.emotional_depth >= 65) {
      persona = "Wholesome Warmth Purist";
      description = "Favors uplifting character journeys, comedy, and restorative human bonds.";
    }

    return {
      hasData: true,
      totalTracked: withDna.length,
      persona,
      description,
      dna: avg
    };
  }

  /**
   * UNIQUE INNOVATION: Binge Fatigue Detector & Palate Cleanser
   * Detects heavy dark/psychological density and recommends optimal pacing breaks.
   */
  detectFatigueAndRecommendCleanser() {
    const taste = this.getWatchlistTasteDNA();
    if (!taste.hasData) return null;

    const isHighStrain = taste.dna.darkness >= 75 || (taste.dna.psychological >= 82 && taste.dna.narrative_complexity >= 80);

    if (isHighStrain) {
      return {
        risk: "High Cognitive Load",
        message: "Your watchlist is heavily saturated with intense psychological thrillers and grimdark themes.",
        tip: "Schedule a 12-episode comedy or slice-of-life palate cleanser between series to prevent viewing fatigue.",
        recommendedCleanser: "Bocchi the Rock! or Barakamon"
      };
    }
    return null;
  }

  /**
   * UNIQUE INNOVATION: Milestone Calendar Schedule
   * Maps out predicted completion dates for each series based on daily watch budget.
   */
  calculateMilestoneSchedule(dailyHours = 1.5) {
    const active = this.items.filter(i => i.status !== 'completed');
    let cumulativeMinutes = 0;
    const dailyMinutes = dailyHours * 60;

    const milestones = active.map(item => {
      const remainingEps = Math.max(0, item.episodes - (item.current_ep || 0));
      const animeMinutes = remainingEps * (item.duration_min || 24);
      const startDay = Math.floor(cumulativeMinutes / dailyMinutes);
      cumulativeMinutes += animeMinutes;
      const endDay = Math.ceil(cumulativeMinutes / dailyMinutes);

      const startDate = new Date();
      startDate.setDate(startDate.getDate() + startDay);
      const finishDate = new Date();
      finishDate.setDate(finishDate.getDate() + endDay);

      return {
        title: item.title,
        episodes: remainingEps,
        daysNeeded: Math.max(1, endDay - startDay),
        finishDateFormatted: finishDate.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
      };
    });

    return milestones;
  }

  exportJSON() {
    return JSON.stringify(this.items, null, 2);
  }
}

function round(val, dec = 1) {
  const m = Math.pow(10, dec);
  return Math.round(val * m) / m;
}

/* ═══════════════════════════════════════════════════════════════════════════
 * PREMIUM FEATURE — CollaborationManager
 * Lets Premium subscribers create shared "Watch Rooms", invite friends via
 * a link, merge watchlists, vote on the next series to watch together, and
 * export the unified list.
 * ─────────────────────────────────────────────────────────────────────────
 * In a full production build this would talk to a real-time backend (e.g.
 * WebSockets / Firebase). Here we model the complete state machine locally
 * so the feature is fully demonstrable during the hackathon.
 * ═══════════════════════════════════════════════════════════════════════════ */
class CollaborationManager {
  constructor(watchlistManager) {
    this._wl = watchlistManager;
    this._storageKey = 'aniverse_collab_v1';
    this._state = this._load();
  }

  // ── Persistence ────────────────────────────────────────────────────────

  _load() {
    try {
      const raw = localStorage.getItem(this._storageKey);
      return raw ? JSON.parse(raw) : this._defaultState();
    } catch {
      return this._defaultState();
    }
  }

  _save() {
    try {
      localStorage.setItem(this._storageKey, JSON.stringify(this._state));
    } catch (e) {
      console.error('[Collab] Failed to persist state', e);
    }
  }

  _defaultState() {
    return {
      isPremium: false,
      room: null,          // { id, name, ownerId, members[], sharedList[], votes{} }
      localUserId: this._generateId('usr'),
      localUserName: 'You'
    };
  }

  // ── Premium gate ───────────────────────────────────────────────────────

  get isPremium() { return this._state.isPremium; }

  /** Demo helper — toggle premium status (simulates subscription purchase). */
  activatePremium(username = 'You') {
    this._state.isPremium = true;
    this._state.localUserName = username;
    this._save();
    return true;
  }

  // ── Room lifecycle ─────────────────────────────────────────────────────

  /**
   * Create a new collaboration room.
   * @param {string} roomName  Display name shown to all members.
   * @returns {{ success, room, inviteLink }}
   */
  createRoom(roomName = 'Watch Party') {
    if (!this.isPremium) return { success: false, error: 'Premium subscription required.' };

    const roomId = this._generateId('room');
    const owner = { id: this._state.localUserId, name: this._state.localUserName, color: this._avatarColor(this._state.localUserId) };

    this._state.room = {
      id: roomId,
      name: roomName,
      createdAt: new Date().toISOString(),
      ownerId: owner.id,
      members: [owner],
      sharedList: this._snapshotMyList(),
      votes: {}
    };
    this._save();

    return {
      success: true,
      room: this._state.room,
      inviteLink: this._buildInviteLink(roomId, roomName)
    };
  }

  /** Simulate a friend joining via an invite link (adds a mock member). */
  joinRoom(roomId, friendName) {
    if (!this.isPremium) return { success: false, error: 'Premium subscription required.' };
    if (!this._state.room || this._state.room.id !== roomId) {
      return { success: false, error: 'Room not found. Ask the host to reshare the invite link.' };
    }

    const alreadyMember = this._state.room.members.some(m => m.id === friendName);
    if (alreadyMember) return { success: false, error: 'Already in this room.' };

    const friendId = this._generateId('usr');
    const friend = { id: friendId, name: friendName, color: this._avatarColor(friendId) };
    this._state.room.members.push(friend);

    // Merge the friend's mock watchlist into shared list
    const mockFriendList = this._generateMockFriendList(friendName);
    this._mergeIntoShared(mockFriendList, friend);
    this._save();

    return { success: true, member: friend, room: this._state.room };
  }

  /** Leave / dissolve the current room. */
  leaveRoom() {
    this._state.room = null;
    this._save();
  }

  // ── Shared watchlist & voting ──────────────────────────────────────────

  /** Push your latest local watchlist into the shared room list. */
  syncMyList() {
    if (!this._state.room) return;
    const snapshot = this._snapshotMyList();
    this._mergeIntoShared(snapshot, { id: this._state.localUserId, name: this._state.localUserName });
    this._save();
  }

  /**
   * Vote for the next anime to watch together.
   * @param {string} animeId
   */
  vote(animeId) {
    if (!this._state.room) return;
    const votes = this._state.room.votes;
    votes[animeId] = (votes[animeId] || 0) + 1;
    this._save();
    return votes;
  }

  /** Returns sharedList sorted by vote count (desc). */
  getRankedSharedList() {
    if (!this._state.room) return [];
    const votes = this._state.room.votes;
    return [...this._state.room.sharedList].sort((a, b) =>
      (votes[b.id] || 0) - (votes[a.id] || 0)
    );
  }

  /** Export the entire shared room watchlist as JSON. */
  exportSharedJSON() {
    if (!this._state.room) return '[]';
    return JSON.stringify(this.getRankedSharedList(), null, 2);
  }

  // ── Accessors ──────────────────────────────────────────────────────────

  get room() { return this._state.room; }
  get members() { return this._state.room ? this._state.room.members : []; }
  get localUserName() { return this._state.localUserName; }

  // ── Internal helpers ───────────────────────────────────────────────────

  _generateId(prefix = 'id') {
    return `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 7)}`;
  }

  _buildInviteLink(roomId, roomName) {
    const encoded = encodeURIComponent(roomName);
    return `${window.location.origin}?join=${roomId}&room=${encoded}`;
  }

  _snapshotMyList() {
    return this._wl.items.map(i => ({
      ...i,
      addedBy: this._state.localUserId,
      addedByName: this._state.localUserName
    }));
  }

  _mergeIntoShared(incomingItems, member) {
    const existing = new Set(this._state.room.sharedList.map(i => i.id));
    incomingItems.forEach(item => {
      if (!existing.has(item.id)) {
        this._state.room.sharedList.push({ ...item, addedBy: member.id, addedByName: member.name });
        existing.add(item.id);
      }
    });
  }

  _avatarColor(id) {
    const palette = ['#00f2fe', '#c084fc', '#ff0080', '#fbbf24', '#34d399', '#f97316'];
    let hash = 0;
    for (const ch of id) hash = (hash * 31 + ch.charCodeAt(0)) & 0xffffffff;
    return palette[Math.abs(hash) % palette.length];
  }

  /** Generates a realistic-looking mock list for a simulated friend join. */
  _generateMockFriendList(friendName) {
    const pool = [
      { id: 'fma_brotherhood', title: 'Fullmetal Alchemist: Brotherhood', score: 9.1, episodes: 64, image_url: 'https://cdn.myanimelist.net/images/anime/1223/96541.jpg' },
      { id: 'attack_on_titan', title: 'Attack on Titan', score: 9.0, episodes: 25, image_url: 'https://cdn.myanimelist.net/images/anime/10/47347.jpg' },
      { id: 'hunter_x_hunter', title: 'Hunter × Hunter (2011)', score: 9.1, episodes: 148, image_url: 'https://cdn.myanimelist.net/images/anime/1337/99013.jpg' }
    ];
    return pool.map(a => ({ ...a, status: 'plan_to_watch', current_ep: 0, addedBy: friendName, addedByName: friendName, duration_min: 24, genres: [] }));
  }
}

window.WatchlistManager = WatchlistManager;
window.CollaborationManager = CollaborationManager;
