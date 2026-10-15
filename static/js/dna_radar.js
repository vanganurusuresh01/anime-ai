/**
 * AniVerse AI - 8-Axis Anime DNA Radar / Spider Chart Engine
 * High-performance HTML5 Canvas Visualizer with Neon Glow Styling
 */

class DNARadarChart {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');

    this.dimensions = [
      { key: 'psychological', label: 'Psychology' },
      { key: 'action_intensity', label: 'Action' },
      { key: 'narrative_complexity', label: 'Complexity' },
      { key: 'emotional_depth', label: 'Emotion' },
      { key: 'pacing', label: 'Pacing' },
      { key: 'darkness', label: 'Darkness' },
      { key: 'world_building', label: 'World' },
      { key: 'philosophical', label: 'Philosophy' }
    ];

    this.currentValues = [50, 50, 50, 50, 50, 50, 50, 50];
    this.targetValues = [50, 50, 50, 50, 50, 50, 50, 50];
    this.animating = false;

    this.setupCanvas();
    window.addEventListener('resize', () => {
      this.setupCanvas();
      this.draw(this.currentValues);
    });
  }

  setupCanvas() {
    if (!this.canvas) return;
    const rect = this.canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    this.canvas.width = rect.width * dpr;
    this.canvas.height = rect.height * dpr;
    this.ctx.scale(dpr, dpr);
    this.width = rect.width;
    this.height = rect.height;
    this.centerX = this.width / 2;
    this.centerY = this.height / 2;
    this.radius = Math.min(this.centerX, this.centerY) * 0.72;
  }

  update(values, animate = true) {
    if (!this.canvas || !values) return;

    let arr = values;
    if (!Array.isArray(values) && typeof values === 'object') {
      arr = this.dimensions.map(d => typeof values[d.key] === 'number' ? values[d.key] : 50);
    }

    this.targetValues = Array.isArray(arr) ? [...arr] : [50, 50, 50, 50, 50, 50, 50, 50];
    if (!animate) {
      this.currentValues = [...this.targetValues];
      this.draw(this.currentValues);
      return;
    }

    if (!this.animating) {
      this.animating = true;
      this.animateStep();
    }
  }

  animateStep() {
    let diffSum = 0;
    for (let i = 0; i < 8; i++) {
      const diff = this.targetValues[i] - this.currentValues[i];
      this.currentValues[i] += diff * 0.2;
      diffSum += Math.abs(diff);
    }

    this.draw(this.currentValues);

    if (diffSum > 0.5) {
      requestAnimationFrame(() => this.animateStep());
    } else {
      this.currentValues = [...this.targetValues];
      this.draw(this.currentValues);
      this.animating = false;
    }
  }

  draw(values) {
    const ctx = this.ctx;
    const cx = this.centerX;
    const cy = this.centerY;
    const r = this.radius;
    const total = this.dimensions.length;

    ctx.clearRect(0, 0, this.width, this.height);

    // 1. Draw Web Grids (Concentric Polygons)
    const levels = [0.25, 0.5, 0.75, 1.0];
    ctx.lineWidth = 1;

    levels.forEach((lvl, idx) => {
      ctx.beginPath();
      for (let i = 0; i < total; i++) {
        const angle = (Math.PI * 2 / total) * i - Math.PI / 2;
        const x = cx + Math.cos(angle) * (r * lvl);
        const y = cy + Math.sin(angle) * (r * lvl);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.strokeStyle = idx === levels.length - 1 ? 'rgba(0, 242, 254, 0.3)' : 'rgba(255, 255, 255, 0.08)';
      ctx.stroke();

      if (idx === 1 || idx === 3) {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.015)';
        ctx.fill();
      }
    });

    // 2. Draw Spokes and Axis Labels
    for (let i = 0; i < total; i++) {
      const angle = (Math.PI * 2 / total) * i - Math.PI / 2;
      const x = cx + Math.cos(angle) * r;
      const y = cy + Math.sin(angle) * r;

      // Spoke
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(x, y);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
      ctx.stroke();

      // Axis Label
      const labelDistance = r + 22;
      const lx = cx + Math.cos(angle) * labelDistance;
      const ly = cy + Math.sin(angle) * labelDistance;

      ctx.font = '600 11px Outfit, sans-serif';
      ctx.fillStyle = '#94a3b8';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(this.dimensions[i].label, lx, ly);
    }

    // 3. Draw The DNA Polygon (Glowing Fill & Stroke)
    ctx.beginPath();
    for (let i = 0; i < total; i++) {
      const angle = (Math.PI * 2 / total) * i - Math.PI / 2;
      const valRatio = Math.max(0.1, Math.min(1.0, (values[i] || 50) / 100));
      const x = cx + Math.cos(angle) * (r * valRatio);
      const y = cy + Math.sin(angle) * (r * valRatio);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.closePath();

    // Gradient Fill
    const grad = ctx.createRadialGradient(cx, cy, 10, cx, cy, r);
    grad.addColorStop(0, 'rgba(0, 242, 254, 0.45)');
    grad.addColorStop(0.6, 'rgba(121, 40, 202, 0.35)');
    grad.addColorStop(1, 'rgba(255, 0, 128, 0.2)');
    ctx.fillStyle = grad;
    ctx.fill();

    // Glowing Outline
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = '#00f2fe';
    ctx.shadowColor = '#00f2fe';
    ctx.shadowBlur = 12;
    ctx.stroke();
    ctx.shadowBlur = 0; // reset shadow

    // 4. Draw Vertex Nodes
    for (let i = 0; i < total; i++) {
      const angle = (Math.PI * 2 / total) * i - Math.PI / 2;
      const valRatio = Math.max(0.1, Math.min(1.0, (values[i] || 50) / 100));
      const x = cx + Math.cos(angle) * (r * valRatio);
      const y = cy + Math.sin(angle) * (r * valRatio);

      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fillStyle = '#ffffff';
      ctx.fill();
      ctx.lineWidth = 1.5;
      ctx.strokeStyle = '#7928ca';
      ctx.stroke();
    }
  }

  drawComparison(v1, v2, label1 = "Anime A", label2 = "Anime B") {
    const ctx = this.ctx;
    const cx = this.centerX;
    const cy = this.centerY;
    const r = this.radius;
    const total = this.dimensions.length;

    ctx.clearRect(0, 0, this.width, this.height);

    // 1. Web Grids
    const levels = [0.25, 0.5, 0.75, 1.0];
    ctx.lineWidth = 1;
    levels.forEach((lvl, idx) => {
      ctx.beginPath();
      for (let i = 0; i < total; i++) {
        const angle = (Math.PI * 2 / total) * i - Math.PI / 2;
        const x = cx + Math.cos(angle) * (r * lvl);
        const y = cy + Math.sin(angle) * (r * lvl);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.strokeStyle = idx === levels.length - 1 ? 'rgba(0, 242, 254, 0.3)' : 'rgba(255, 255, 255, 0.08)';
      ctx.stroke();
    });

    // 2. Spokes & Labels
    for (let i = 0; i < total; i++) {
      const angle = (Math.PI * 2 / total) * i - Math.PI / 2;
      const x = cx + Math.cos(angle) * r;
      const y = cy + Math.sin(angle) * r;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(x, y);
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
      ctx.stroke();

      const labelDistance = r + 20;
      const lx = cx + Math.cos(angle) * labelDistance;
      const ly = cy + Math.sin(angle) * labelDistance;
      ctx.font = '600 11px Outfit, sans-serif';
      ctx.fillStyle = '#94a3b8';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(this.dimensions[i].label, lx, ly);
    }

    // Helper to draw single polygon
    const drawPolygon = (vals, strokeCol, fillCol, glowCol) => {
      ctx.beginPath();
      for (let i = 0; i < total; i++) {
        const angle = (Math.PI * 2 / total) * i - Math.PI / 2;
        const valRatio = Math.max(0.1, Math.min(1.0, (vals[i] || 50) / 100));
        const x = cx + Math.cos(angle) * (r * valRatio);
        const y = cy + Math.sin(angle) * (r * valRatio);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.fillStyle = fillCol;
      ctx.fill();

      ctx.lineWidth = 2.5;
      ctx.strokeStyle = strokeCol;
      ctx.shadowColor = glowCol;
      ctx.shadowBlur = 10;
      ctx.stroke();
      ctx.shadowBlur = 0;

      // Dots
      for (let i = 0; i < total; i++) {
        const angle = (Math.PI * 2 / total) * i - Math.PI / 2;
        const valRatio = Math.max(0.1, Math.min(1.0, (vals[i] || 50) / 100));
        const x = cx + Math.cos(angle) * (r * valRatio);
        const y = cy + Math.sin(angle) * (r * valRatio);
        ctx.beginPath();
        ctx.arc(x, y, 3.5, 0, Math.PI * 2);
        ctx.fillStyle = strokeCol;
        ctx.fill();
      }
    };

    // Draw Anime 1 (Cyan)
    drawPolygon(v1, '#00f2fe', 'rgba(0, 242, 254, 0.25)', '#00f2fe');

    // Draw Anime 2 (Pink)
    drawPolygon(v2, '#ff0080', 'rgba(255, 0, 128, 0.25)', '#ff0080');

    // Legend
    ctx.font = '700 12px Outfit, sans-serif';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';

    // Label 1
    ctx.fillStyle = '#00f2fe';
    ctx.fillRect(15, 15, 10, 10);
    ctx.fillStyle = '#f8fafc';
    ctx.fillText(label1.substring(0, 18), 32, 14);

    // Label 2
    ctx.fillStyle = '#ff0080';
    ctx.fillRect(15, 33, 10, 10);
    ctx.fillStyle = '#f8fafc';
    ctx.fillText(label2.substring(0, 18), 32, 32);
  }
}

window.DNARadarChart = DNARadarChart;
