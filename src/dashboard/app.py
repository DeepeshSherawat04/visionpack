# dashboard/app.py
import streamlit as st
import requests
import pandas as pd
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io
import time

# ═══════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════
API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="VisionPack AI | Industrial CV Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"Get help": None, "Report a bug": None, "About": None},
)

# ═══════════════════════════════════════════════
# THEME
# ═══════════════════════════════════════════════
current_theme = "dark"
is_dark = True

# ═══════════════════════════════════════════════
# ICON SYSTEM  (Lucide-style inline SVGs)
# ═══════════════════════════════════════════════
ICONS = {
    "logo": """<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8V5a2 2 0 0 1 2-2h3"/><path d="M16 3h3a2 2 0 0 1 2 2v3"/><path d="M21 16v3a2 2 0 0 1-2 2h-3"/><path d="M8 21H5a2 2 0 0 1-2-2v-3"/><circle cx="12" cy="12" r="3.5"/><circle cx="12" cy="12" r="1.3" fill="#0ea5e9" stroke="none"/></svg>""",
    "predict": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>""",
    "analytics": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>""",
    "system": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>""",
    "upload": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>""",
    "metrics": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>""",
    "target": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>""",
    "list": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" x2="21" y1="6" y2="6"/><line x1="8" x2="21" y1="12" y2="12"/><line x1="8" x2="21" y1="18" y2="18"/><line x1="3" x2="3.01" y1="6" y2="6"/><line x1="3" x2="3.01" y1="12" y2="12"/><line x1="3" x2="3.01" y1="18" y2="18"/></svg>""",
    "lab": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 2v7.31"/><path d="M14 2v7.31"/><path d="M8.5 2h7"/><path d="M14 9.3a6.5 6.5 0 1 1-4 0"/></svg>""",
    "rocket": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>""",
    "brain": """<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/></svg>""",
    "clock": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>""",
    "memory": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 19v2"/><path d="M12 19v2"/><path d="M18 19v2"/><path d="M6 4v2a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4"/><path d="M8 11v3"/><path d="M16 11v3"/><path d="M12 11v3"/><path d="M4 8h16v10a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8Z"/></svg>""",
    "info": """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>""",
    "image": """<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>""",
    "zap": """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>""",
    "refresh": """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/></svg>""",
    "check": """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>""",
    "alert": """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/></svg>""",
    "x": """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>""",
    "box": """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>""",
    "sun": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>""",
    "moon": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>""",
}

# ═══════════════════════════════════════════════
# DESIGN SYSTEM CSS — DUAL THEME SUPPORT
# ═══════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── CSS Variables: Dark (default) ── */
:root {{
  --vp-bg: #0b1120;
  --vp-surface: #111827;
  --vp-elevated: #1a2332;
  --vp-border: rgba(148, 163, 184, 0.08);
  --vp-border-hover: rgba(14, 165, 233, 0.25);
  --vp-accent: #0ea5e9;
  --vp-accent-soft: rgba(14, 165, 233, 0.1);
  --vp-accent-glow: rgba(14, 165, 233, 0.15);
  --vp-text: #f1f5f9;
  --vp-text-secondary: #94a3b8;
  --vp-text-muted: #64748b;
  --vp-status-good: #22c55e;
  --vp-status-warn: #f59e0b;
  --vp-status-bad: #ef4444;
  --vp-shadow: rgba(0, 0, 0, 0.3);
  --vp-chart-grid: rgba(148, 163, 184, 0.06);
}}

/* ── CSS Variables: Light ── */
[data-theme="light"] {{
  --vp-bg: #f8fafc;
  --vp-surface: #ffffff;
  --vp-elevated: #f1f5f9;
  --vp-border: rgba(148, 163, 184, 0.18);
  --vp-border-hover: rgba(14, 165, 233, 0.35);
  --vp-accent: #0284c7;
  --vp-accent-soft: rgba(2, 132, 199, 0.08);
  --vp-accent-glow: rgba(2, 132, 199, 0.12);
  --vp-text: #0f172a;
  --vp-text-secondary: #475569;
  --vp-text-muted: #64748b;
  --vp-status-good: #16a34a;
  --vp-status-warn: #d97706;
  --vp-status-bad: #dc2626;
  --vp-shadow: rgba(0, 0, 0, 0.06);
  --vp-chart-grid: rgba(148, 163, 184, 0.12);
}}

/* ── Smooth Theme Transitions ── */
.stApp,
.vp-card,
.vp-detection-card,
[data-testid="stFileUploaderDropzone"],
.stTabs [data-baseweb="tab-list"],
.stJson, .stDataFrame,
.streamlit-expanderHeader,
.stButton > button,
.vp-section-icon {{
  transition: background-color 0.45s cubic-bezier(0.4, 0, 0.2, 1),
              color 0.45s cubic-bezier(0.4, 0, 0.2, 1),
              border-color 0.45s cubic-bezier(0.4, 0, 0.2, 1),
              box-shadow 0.45s cubic-bezier(0.4, 0, 0.2, 1) !important;
}}

/* ── Hide Streamlit Dev Chrome ── */
.stAppHeader, .stToolbar, .stDeployButton, .stAppDeployButton,
[data-testid="stHeader"], .stActionButton, #MainMenu,
[data-testid="stManageAppButton"], [data-testid="stStatusWidget"],
[data-testid="stDecoration"], [data-testid="stAppViewContainer"] > header {{
  display: none !important;
}}

/* ── Base ── */
.stApp {{
  background: var(--vp-bg);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}}

.block-container {{
  padding-top: 1.5rem !important;
  padding-bottom: 2rem !important;
  max-width: 1200px;
}}

/* ── Typography ── */
h1, h2, h3, h4, h5, h6, p, div, span, label, button, input, textarea, select {{
  font-family: 'Inter', sans-serif !important;
  letter-spacing: -0.01em;
}}

/* ── Tab Pills ── */
.stTabs [data-baseweb="tab-list"] {{
  background: var(--vp-surface);
  border: 1px solid var(--vp-border);
  border-radius: 12px;
  padding: 5px;
  gap: 4px;
}}

.stTabs [data-baseweb="tab"] {{
  background: transparent;
  border-radius: 8px;
  padding: 10px 24px;
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--vp-text-secondary);
  border: none;
  transition: all 0.2s ease;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}

.stTabs [data-baseweb="tab"]:hover {{
  color: var(--vp-text);
  background: rgba(128,128,128,0.04);
}}

.stTabs [aria-selected="true"] {{
  background: var(--vp-elevated) !important;
  color: var(--vp-accent) !important;
  box-shadow: 0 1px 2px var(--vp-shadow);
}}

.stTabs [data-baseweb="tab-highlight"] {{
  background: transparent !important;
}}

/* ── Upload Zone ── */
[data-testid="stFileUploaderDropzone"] {{
  background: var(--vp-surface) !important;
  border: 2px dashed var(--vp-border) !important;
  border-radius: 12px !important;
  transition: all 0.2s ease;
}}

[data-testid="stFileUploaderDropzone"]:hover {{
  border-color: var(--vp-accent) !important;
  background: var(--vp-elevated) !important;
}}

[data-testid="stFileUploaderDropzone"] > div > small,
[data-testid="stFileUploaderDropzone"] > div > span {{
  color: var(--vp-text-secondary) !important;
}}

/* ── Buttons ── */
.stButton > button {{
  background: var(--vp-accent) !important;
  color: white !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 0.75rem 1.5rem !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  transition: all 0.2s ease !important;
  box-shadow: 0 0 0 1px rgba(14,165,233,0.1), 0 4px 12px rgba(14,165,233,0.15) !important;
}}

.stButton > button:hover {{
  transform: translateY(-1px);
  box-shadow: 0 0 0 1px rgba(14,165,233,0.2), 0 6px 20px rgba(14,165,233,0.25) !important;
}}

.stButton > button:active {{
  transform: translateY(0);
}}

/* ── Cards ── */
.vp-card {{
  background: var(--vp-surface);
  border: 1px solid var(--vp-border);
  border-radius: 12px;
  padding: 1.25rem;
  transition: border-color 0.2s ease, background-color 0.45s ease;
}}

.vp-card:hover {{
  border-color: rgba(128, 128, 128, 0.2);
}}

/* ── Metric Cards ── */
.vp-metric {{
  text-align: center;
}}

.vp-metric-value {{
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--vp-text);
  line-height: 1.2;
  letter-spacing: -0.02em;
}}

.vp-metric-label {{
  font-size: 0.7rem;
  color: var(--vp-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 600;
  margin-top: 0.4rem;
}}

/* ── Section Header ── */
.vp-section-header {{
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 1.5rem 0 1rem 0;
}}

.vp-section-icon {{
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: var(--vp-accent-soft);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--vp-accent);
  flex-shrink: 0;
}}

.vp-section-title {{
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--vp-text);
}}

.vp-section-subtitle {{
  font-size: 0.8rem;
  color: var(--vp-text-muted);
  margin-top: 2px;
}}

/* ── Detection Cards ── */
.vp-detection-card {{
  background: var(--vp-surface);
  border: 1px solid var(--vp-border);
  border-radius: 10px;
  padding: 1rem;
  margin: 0.5rem 0;
}}

.vp-class-badge {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--vp-accent-soft);
  color: var(--vp-accent);
  padding: 4px 10px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}}

.vp-conf-bar-bg {{
  background: rgba(128, 128, 128, 0.08);
  height: 4px;
  border-radius: 2px;
  margin-top: 10px;
  overflow: hidden;
}}

.vp-conf-bar-fill {{
  height: 100%;
  border-radius: 2px;
  transition: width 0.4s ease;
}}

/* ── Status Dots ── */
.vp-status-dot {{
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 8px;
}}

.vp-status-good {{ background: var(--vp-status-good); box-shadow: 0 0 6px rgba(34, 197, 94, 0.4); }}
.vp-status-warn {{ background: var(--vp-status-warn); box-shadow: 0 0 6px rgba(245, 158, 11, 0.4); }}
.vp-status-bad  {{ background: var(--vp-status-bad);  box-shadow: 0 0 6px rgba(239, 68, 68, 0.4); }}

/* ── Spinner ── */
@keyframes vp-spin {{
  to {{ transform: rotate(360deg); }}
}}

/* ── JSON / Dataframes ── */
.stJson, .stDataFrame {{
  background: var(--vp-surface) !important;
  border: 1px solid var(--vp-border) !important;
  border-radius: 10px !important;
}}

/* ── Expander ── */
.streamlit-expanderHeader {{
  font-size: 0.85rem !important;
  color: var(--vp-text-secondary) !important;
  font-weight: 500 !important;
}}

/* ── Footer ── */
.vp-footer {{
  text-align: center;
  color: var(--vp-text-muted);
  font-size: 0.8rem;
  padding-top: 2rem;
}}

.vp-footer a {{
  color: var(--vp-accent);
  text-decoration: none;
}}

.vp-footer a:hover {{
  text-decoration: underline;
}}

/* ── Tooltip ── */
.vp-tooltip {{
  cursor: help;
  opacity: 0.5;
  transition: opacity 0.2s;
  display: inline-flex;
  vertical-align: middle;
}}

.vp-tooltip:hover {{
  opacity: 1;
}}

/* ── Upload Empty State ── */
.vp-upload-empty {{
  text-align: center;
  padding: 2.5rem 1rem;
  color: var(--vp-text-muted);
}}

/* ── Inline icon alignment ── */
.vp-icon-inline {{
  display: inline-flex;
  vertical-align: middle;
  margin-right: 6px;
}}

/* ── Chart area backgrounds ── */
[data-testid="stAreaChart"],
[data-testid="stBarChart"] {{
  background: var(--vp-surface) !important;
  border-radius: 10px;
  border: 1px solid var(--vp-border);
}}

/* ── DataFrame cells ── */
[data-testid="stDataFrame"] td,
[data-testid="stDataFrame"] th {{
  color: var(--vp-text) !important;
  border-color: var(--vp-border) !important;
}}

/* ── Divider ── */
hr {{
  border-color: var(--vp-border) !important;
  transition: border-color 0.45s ease;
}}

/* ── Alert / Info boxes ── */
[data-testid="stAlert"] {{
  background: var(--vp-surface) !important;
  border-color: var(--vp-border) !important;
  color: var(--vp-text-secondary) !important;
}}

/* ── Code / pre blocks ── */
[data-testid="stMarkdown"] code {{
  background: var(--vp-elevated) !important;
  color: var(--vp-accent) !important;
  border: 1px solid var(--vp-border);
}}
</style>

<script>
  // Apply theme attribute to <html> for CSS to pick up
  document.documentElement.setAttribute("data-theme", "{current_theme}");
</script>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════
def section_header(icon_key: str, title: str, subtitle: str = None):
    sub_html = f'<div class="vp-section-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="vp-section-header">
      <div class="vp-section-icon">{ICONS[icon_key]}</div>
      <div>
        <div class="vp-section-title">{title}</div>
        {sub_html}
      </div>
    </div>
    """, unsafe_allow_html=True)


def metric_card(label: str, value: str, color: str = None, icon_key: str = None):
    color_style = f"color: {color};" if color else ""
    icon_html = f'<div style="margin-bottom: 8px; color: var(--vp-text-muted);">{ICONS[icon_key]}</div>' if icon_key else ""
    st.markdown(f"""
    <div class="vp-card vp-metric">
      {icon_html}
      <div class="vp-metric-value" style="{color_style}">{value}</div>
      <div class="vp-metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def draw_detection_overlay(img: Image.Image, detections: list, font) -> Image.Image:
    draw = ImageDraw.Draw(img)
    w, h = img.size

    for det in detections:
        bbox = det["bbox"]
        cls = det["class"]
        conf = det["conf"]

        # Status color (semantic: confidence quality)
        if conf > 0.7:
            color = "#22c55e"
        elif conf > 0.4:
            color = "#f59e0b"
        else:
            color = "#ef4444"

        # Bounding box (2px, clean)
        draw.rectangle(bbox, outline=color, width=2)

        # Label chip
        label = f"{cls.upper()}  {conf:.0%}"
        try:
            tb = draw.textbbox((0, 0), label, font=font)
            tw, th = tb[2] - tb[0], tb[3] - tb[1]
        except Exception:
            tw, th = len(label) * 9, 16

        pad_x, pad_y = 10, 6
        chip_w = tw + pad_x * 2
        chip_h = th + pad_y * 2
        chip_x = bbox[0]
        chip_y = max(bbox[1] - chip_h, 0)

        if chip_x + chip_w > w:
            chip_x = w - chip_w
        if chip_y < 0:
            chip_y = bbox[1] + 4

        # Rounded chip background
        try:
            draw.rounded_rectangle(
                [chip_x, chip_y, chip_x + chip_w, chip_y + chip_h],
                radius=6, fill=color
            )
        except AttributeError:
            draw.rectangle([chip_x, chip_y, chip_x + chip_w, chip_y + chip_h], fill=color)

        draw.text((chip_x + pad_x, chip_y + pad_y - 1), label, fill="#ffffff", font=font)

    return img


# ═══════════════════════════════════════════════
# HEADER with THEME TOGGLE
# ═══════════════════════════════════════════════
header_left = st.container()

with header_left:
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: center; gap: 14px; margin-bottom: 0.25rem;">
      <div style="color: var(--vp-text);">{ICONS["logo"]}</div>
      <div style="font-size: 2.2rem; font-weight: 800; color: var(--vp-text); letter-spacing: -0.03em;">VisionPack AI</div>
    </div>
    <div style="text-align: center; color: var(--vp-text-muted); font-size: 0.95rem; font-weight: 400; margin-bottom: 2rem; letter-spacing: 0.02em;">
      Industrial Computer Vision · Real-Time Detection · Quality Monitoring
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["PREDICT", "ANALYTICS", "SYSTEM"])

# ═══════════════════════════════════════════════
# TAB 1: PREDICT
# ═══════════════════════════════════════════════
with tab1:
    col_left, col_right = st.columns([1, 1.2])

    with col_left:
        section_header("upload", "Upload Image", "JPG and PNG supported")

        uploaded = st.file_uploader(
            "Drag and drop or click to upload",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )

        if uploaded is not None:
            uploaded.seek(0)
            preview_img = Image.open(io.BytesIO(uploaded.getvalue()))
            st.image(preview_img, use_container_width=True)

            run_btn = st.button("Run Detection", use_container_width=True)
        else:
            run_btn = False
            st.markdown(f"""
            <div class="vp-upload-empty">
              <div style="color: var(--vp-text-muted); margin-bottom: 0.75rem;">{ICONS["image"]}</div>
              <div style="font-size: 0.9rem; color: var(--vp-text-secondary); font-weight: 500;">Drop an image here</div>
              <div style="font-size: 0.75rem; color: var(--vp-text-muted); margin-top: 4px;">or click to browse</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div style="margin-top: 1.5rem; margin-bottom: 0.5rem;"><span style="font-size: 0.7rem; color: var(--vp-text-muted); text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600;">Try a sample</span></div>', unsafe_allow_html=True)
            s1, s2, s3 = st.columns(3)
            for i, col in enumerate([s1, s2, s3]):
                with col:
                    if st.button(f"Sample {i+1}", key=f"sample_{i}", use_container_width=True):
                        st.info("Sample images not configured — upload your own image to test.")

    with col_right:
        if uploaded is not None and run_btn:
            # ── Designed Loading State ──
            loading = st.empty()
            loading.markdown("""
            <div class="vp-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 3rem;">
              <div style="width: 40px; height: 40px; border: 3px solid rgba(14, 165, 233, 0.08); border-top-color: var(--vp-accent); border-radius: 50%; animation: vp-spin 1s linear infinite;"></div>
              <div style="margin-top: 1rem; font-weight: 600; color: var(--vp-text-secondary);">Running YOLOv8 inference</div>
              <div style="font-size: 0.8rem; color: var(--vp-text-muted); margin-top: 4px;">Analyzing image contents…</div>
            </div>
            """, unsafe_allow_html=True)

            try:
                uploaded.seek(0)
                files = {"file": uploaded.getvalue()}
                start_req = time.time()
                resp = requests.post(f"{API_BASE}/predict", files=files, timeout=30)
                api_latency = (time.time() - start_req) * 1000
                data = resp.json()
            except Exception as e:
                loading.empty()
                st.error(f"API Error: {e}")
                st.stop()

            loading.empty()

            # ── INFERENCE METRICS ──
            section_header("metrics", "Inference Metrics")

            detections = data.get("detections", [])
            num_dets = len(detections)
            runtime = data.get("runtime_ms", 0)
            cached = data.get("cached", False)
            avg_conf = sum(d["conf"] for d in detections) / num_dets if num_dets else 0

            kpi1, kpi2, kpi3, kpi4 = st.columns(4)

            with kpi1:
                metric_card("Objects", f"{num_dets}", icon_key="box")

            with kpi2:
                # Latency is informational, not an error state
                lat_color = "var(--vp-text)" if runtime < 200 else "var(--vp-status-warn)"
                metric_card("Inference", f"{runtime:.0f} ms", color=lat_color, icon_key="target")

            with kpi3:
                conf_color = "var(--vp-status-good)" if avg_conf > 0.7 else "var(--vp-status-warn)" if avg_conf > 0.4 else "var(--vp-status-bad)"
                metric_card("Avg Confidence", f"{avg_conf:.0%}", color=conf_color, icon_key="metrics")

            with kpi4:
                cache_color = "var(--vp-accent)" if cached else "var(--vp-text-muted)"
                cache_icon = "zap" if cached else "refresh"
                cache_text = "HIT" if cached else "MISS"
                metric_card("Cache", f"{cache_text}", color=cache_color, icon_key=cache_icon)

            # ── VISUAL OUTPUT ──
            section_header("target", "Detection Visualization")

            uploaded.seek(0)
            img = Image.open(io.BytesIO(uploaded.getvalue())).convert("RGB")

            try:
                font = ImageFont.truetype("arial.ttf", 18)
            except Exception:
                try:
                    font = ImageFont.truetype("DejaVuSans.ttf", 18)
                except Exception:
                    font = ImageFont.load_default()

            img = draw_detection_overlay(img, detections, font)
            st.image(img, use_container_width=True)

            # ── DETECTION CARDS ──
            if detections:
                section_header("list", "Detection Details", f"{len(detections)} objects found")

                for det in detections:
                    conf = det["conf"]
                    conf_pct = f"{conf:.0%}"
                    if conf > 0.7:
                        bar_color = "var(--vp-status-good)"
                        status_icon = ICONS["check"]
                    elif conf > 0.4:
                        bar_color = "var(--vp-status-warn)"
                        status_icon = ICONS["alert"]
                    else:
                        bar_color = "var(--vp-status-bad)"
                        status_icon = ICONS["x"]

                    st.markdown(f"""
                    <div class="vp-detection-card">
                      <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                          <span class="vp-class-badge">{det["class"].upper()}</span>
                          <span style="color: var(--vp-text-muted); font-size: 0.8rem; font-family: 'SF Mono', monospace;">
                            {det["bbox"][0]:.0f}, {det["bbox"][1]:.0f} → {det["bbox"][2]:.0f}, {det["bbox"][3]:.0f}
                          </span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 6px; font-weight: 700; font-size: 0.9rem; color: {bar_color};">
                          {status_icon} {conf_pct}
                        </div>
                      </div>
                      <div class="vp-conf-bar-bg">
                        <div class="vp-conf-bar-fill" style="width: {conf*100}%; background: {bar_color};"></div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

            # ── QUALITY METRICS ──
            quality = data.get("quality", {})
            if quality:
                section_header("lab", "Image Quality Analysis")

                q1, q2, q3 = st.columns(3)

                blur = quality.get("sharpness", quality.get("blur_score", 0))
                blur_status = "Good" if blur > 200 else "Moderate" if blur > 100 else "Poor"
                blur_color = "var(--vp-status-good)" if blur > 200 else "var(--vp-status-warn)" if blur > 100 else "var(--vp-status-bad)"
                with q1:
                    st.markdown(f"""
                    <div class="vp-card vp-metric">
                      <div style="display: flex; align-items: center; justify-content: center; gap: 6px; margin-bottom: 4px;">
                        <span class="vp-metric-label">Sharpness</span>
                        <span class="vp-tooltip" title="Laplacian variance — higher is sharper">{ICONS["info"]}</span>
                      </div>
                      <div class="vp-metric-value" style="color: {blur_color};">{blur:.0f}</div>
                      <div style="font-size: 0.75rem; color: {blur_color}; font-weight: 600; margin-top: 4px;">{blur_status}</div>
                    </div>
                    """, unsafe_allow_html=True)

                bright = quality.get("brightness", 0)
                bright_status = "Good" if 0.2 < bright < 0.9 else "Check"
                bright_color = "var(--vp-status-good)" if 0.2 < bright < 0.9 else "var(--vp-status-warn)"
                with q2:
                    st.markdown(f"""
                    <div class="vp-card vp-metric">
                      <div class="vp-metric-label" style="margin-bottom: 4px;">Brightness</div>
                      <div class="vp-metric-value" style="color: {bright_color};">{bright:.2f}</div>
                      <div style="font-size: 0.75rem; color: {bright_color}; font-weight: 600; margin-top: 4px;">{bright_status}</div>
                    </div>
                    """, unsafe_allow_html=True)

                noise = quality.get("noise_level", 0)
                noise_status = "Clean" if noise < 10 else "Noisy" if noise < 20 else "High"
                noise_color = "var(--vp-status-good)" if noise < 10 else "var(--vp-status-warn)" if noise < 20 else "var(--vp-status-bad)"
                with q3:
                    st.markdown(f"""
                    <div class="vp-card vp-metric">
                      <div class="vp-metric-label" style="margin-bottom: 4px;">Noise Level</div>
                      <div class="vp-metric-value" style="color: {noise_color};">{noise:.1f}</div>
                      <div style="font-size: 0.75rem; color: {noise_color}; font-weight: 600; margin-top: 4px;">{noise_status}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # ── RAW JSON ──
            with st.expander("View Raw API Response"):
                st.json(data)

# ═══════════════════════════════════════════════
# TAB 2: ANALYTICS
# ═══════════════════════════════════════════════
with tab2:
    section_header("analytics", "Quality & Inference Analytics")

    log_file = Path("data/logs/inference_metrics.jsonl")
    if log_file.exists():
        rows = []
        with log_file.open() as f:
            for line in f:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        if rows:
            df = pd.DataFrame(rows)

            # Summary stats
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                metric_card("Total Inferences", f"{len(df)}", icon_key="metrics")
            with c2:
                avg_time = df["inference_time_ms"].mean() if "inference_time_ms" in df.columns else 0
                metric_card("Avg Latency", f"{avg_time:.1f} ms", icon_key="target")
            with c3:
                total_dets = df["num_detections"].sum() if "num_detections" in df.columns else 0
                metric_card("Total Detections", f"{int(total_dets)}", icon_key="box")
            with c4:
                if "avg_conf" in df.columns:
                    avg_c = df["avg_conf"].mean()
                    conf_color = "var(--vp-status-good)" if avg_c > 0.7 else "var(--vp-status-warn)" if avg_c > 0.4 else "var(--vp-status-bad)"
                    metric_card("Avg Confidence", f"{avg_c:.0%}", color=conf_color, icon_key="metrics")

            st.divider()

            # Recent table
            section_header("list", "Recent Inference Logs")
            display_cols = ["ts", "source", "inference_time_ms", "num_detections", "avg_conf"]
            available_cols = [c for c in display_cols if c in df.columns]
            st.dataframe(df[available_cols].tail(20), use_container_width=True, height=400)

            # Charts
            col_chart1, col_chart2 = st.columns(2)

            with col_chart1:
                if "inference_time_ms" in df.columns:
                    section_header("target", "Latency Trend", "Last 100 inferences")
                    chart_data = df[["inference_time_ms"]].tail(100).reset_index(drop=True)
                    st.area_chart(chart_data, color=["#0ea5e9"])

            with col_chart2:
                if "num_detections" in df.columns:
                    section_header("box", "Detections per Image")
                    det_counts = df["num_detections"].value_counts().sort_index()
                    st.bar_chart(det_counts, color="#818cf8")
        else:
            st.markdown(f"""
            <div class="vp-card" style="text-align: center; padding: 3rem;">
              <div style="color: var(--vp-text-muted); margin-bottom: 0.5rem;">{ICONS["metrics"]}</div>
              <div style="color: var(--vp-text-secondary); font-weight: 500;">Log file is empty</div>
              <div style="color: var(--vp-text-muted); font-size: 0.8rem; margin-top: 4px;">Valid entries will appear here after inference runs</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="vp-card" style="text-align: center; padding: 3rem;">
          <div style="color: var(--vp-text-muted); margin-bottom: 0.5rem;">{ICONS["metrics"]}</div>
          <div style="color: var(--vp-text-secondary); font-weight: 500;">No metrics logged yet</div>
          <div style="color: var(--vp-text-muted); font-size: 0.8rem; margin-top: 4px;">Run some predictions to populate this dashboard</div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# TAB 3: SYSTEM
# ═══════════════════════════════════════════════
with tab3:
    section_header("system", "System Health Monitor")

    try:
        resp = requests.get(f"{API_BASE}/status", timeout=5)
        status_data = resp.json()

        # Connection status
        if status_data.get("status") == "ok":
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 1rem;">
              <span class="vp-status-dot vp-status-good"></span>
              <span style="color: var(--vp-text-secondary); font-weight: 600; font-size: 0.9rem;">API Backend Online</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 1rem;">
              <span class="vp-status-dot vp-status-bad"></span>
              <span style="color: var(--vp-text-secondary); font-weight: 600; font-size: 0.9rem;">API Backend Issue</span>
            </div>
            """, unsafe_allow_html=True)

        # Status cards
        s1, s2, s3 = st.columns(3)

        with s1:
            model_loaded = status_data.get("model_loaded", False)
            model_color = "var(--vp-status-good)" if model_loaded else "var(--vp-status-bad)"
            model_text = "ONLINE" if model_loaded else "ERROR"
            st.markdown(f"""
            <div class="vp-card vp-metric">
              <div style="margin-bottom: 8px; color: var(--vp-text-muted);">{ICONS["brain"]}</div>
              <div class="vp-metric-value" style="color: {model_color};">{model_text}</div>
              <div class="vp-metric-label">YOLO Model</div>
            </div>
            """, unsafe_allow_html=True)

        with s2:
            uptime = status_data.get("uptime_seconds", 0)
            hours = int(uptime // 3600)
            mins = int((uptime % 3600) // 60)
            st.markdown(f"""
            <div class="vp-card vp-metric">
              <div style="margin-bottom: 8px; color: var(--vp-text-muted);">{ICONS["clock"]}</div>
              <div class="vp-metric-value">{hours}h {mins}m</div>
              <div class="vp-metric-label">Uptime</div>
            </div>
            """, unsafe_allow_html=True)

        with s3:
            mem = status_data.get("memory_mb", 0)
            st.markdown(f"""
            <div class="vp-card vp-metric">
              <div style="margin-bottom: 8px; color: var(--vp-text-muted);">{ICONS["memory"]}</div>
              <div class="vp-metric-value">{mem:.1f}</div>
              <div class="vp-metric-label">Memory (MB)</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("View Full System Details"):
            st.json(status_data)

    except Exception as e:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 1rem;">
          <span class="vp-status-dot vp-status-bad"></span>
          <span style="color: var(--vp-text-secondary); font-weight: 600; font-size: 0.9rem;">API Offline</span>
        </div>
        """, unsafe_allow_html=True)
        st.error(f"Could not connect to backend at {API_BASE}: {e}")
        st.info("Make sure the FastAPI server is running: `uvicorn src.api.main:app --reload --port 8000`")

# ═══════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════
st.divider()
st.markdown(f"""
<div class="vp-footer">
  {ICONS["logo"]}
  <div style="margin-top: 0.5rem;">VisionPack AI · Built with FastAPI + YOLOv8 + Streamlit</div>
  <div style="margin-top: 0.25rem;">
    <a href="https://github.com/DeepeshSherawat04/visionpack">GitHub</a>
  </div>
</div>
""", unsafe_allow_html=True)