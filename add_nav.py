#!/usr/bin/env python3
"""Add responsive navigation to all visualization HTML files."""
import re
from pathlib import Path

NAV_STYLES_AND_HTML = '''
<style>
/* Navigation Styles - Matches parent site */
.viz-nav {
  background: var(--bg-card, var(--color-background-secondary, #f5f5f5));
  border-bottom: 1px solid var(--border, var(--color-border-tertiary, rgba(0,0,0,0.1)));
  padding: 1rem 2rem;
  position: sticky;
  top: 0;
  z-index: 100;
  margin-bottom: 2rem;
}
.viz-nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}
.viz-nav-back {
  color: var(--purple-interactive, var(--color-text-info, #2563eb));
  text-decoration: none;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: opacity 0.2s;
}
.viz-nav-back:hover { opacity: 0.7; }
.viz-nav-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}
.viz-nav-links a {
  color: var(--text-muted, var(--color-text-secondary, #666));
  text-decoration: none;
  font-size: 0.875rem;
  transition: color 0.2s;
}
.viz-nav-links a:hover {
  color: var(--purple-decorative, var(--color-text-info, #2563eb));
}
@media (max-width: 768px) {
  .viz-nav { padding: 0.75rem 1rem; }
  .viz-nav-links { gap: 0.75rem; font-size: 0.8125rem; }
  .viz-nav-back { font-size: 0.9375rem; }
}
</style>
<nav class="viz-nav">
  <div class="viz-nav-inner">
    <a href="INDEX_PATH" class="viz-nav-back">
      <span style="font-size: 1.25rem;">←</span> <span>Visualizations</span>
    </a>
    <div class="viz-nav-links">
      <a href="https://continuity-bridge.github.io/">Home</a>
      <a href="https://github.com/continuity-bridge/visualizers">GitHub</a>
    </div>
  </div>
</nav>
'''

def add_nav(filepath, is_subdir=False):
    content = filepath.read_text()
    if 'viz-nav' in content:
        print(f"  ⏭️  {filepath.name}")
        return
    index = "../index.html" if is_subdir else "index.html"
    nav = NAV_STYLES_AND_HTML.replace('INDEX_PATH', index)
    styles = re.search(r'(<style>.*?</style>)', nav, re.DOTALL).group(1)
    nav_html = re.search(r'(<nav class="viz-nav">.*?</nav>)', nav, re.DOTALL).group(1)
    content = content.replace('</head>', f'{styles}\n</head>')
    content = re.sub(r'(<body[^>]*>)', r'\1\n' + nav_html, content, count=1)
    filepath.write_text(content)
    print(f"  ✓ {filepath.name}")

base = Path('.')
print("### Root ###")
for f in base.glob('*.html'):
    if f.name != 'index.html': add_nav(f, False)

for d in ['50-first-dates', 'altered-carbon', 'adhd-journaling', 'operational']:
    if Path(d).exists():
        print(f"\n### {d}/ ###")
        for f in Path(d).glob('*.html'):
            add_nav(f, True)
print("\n✓ Done")
