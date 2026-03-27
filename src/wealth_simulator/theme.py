from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    name: str
    background: str
    surface: str
    text: str
    muted_text: str
    border: str
    accent: str
    chart_palette: tuple[str, ...]


PRESET_THEMES: dict[str, Theme] = {
    "Neutral": Theme(
        name="Neutral",
        background="#0f172a",
        surface="rgba(255,255,255,0.06)",
        text="#e5e7eb",
        muted_text="rgba(229,231,235,0.75)",
        border="rgba(229,231,235,0.18)",
        accent="#60a5fa",
        chart_palette=("#60a5fa", "#34d399", "#fbbf24", "#f472b6", "#a78bfa"),
    ),
    "Pastel": Theme(
        name="Pastel",
        background="#0b1220",
        surface="rgba(255,255,255,0.07)",
        text="#f3f4f6",
        muted_text="rgba(243,244,246,0.75)",
        border="rgba(243,244,246,0.16)",
        accent="#a5b4fc",
        chart_palette=("#a5b4fc", "#6ee7b7", "#fdba74", "#f9a8d4", "#c4b5fd"),
    ),
    "High contrast": Theme(
        name="High contrast",
        background="#000000",
        surface="rgba(255,255,255,0.08)",
        text="#ffffff",
        muted_text="rgba(255,255,255,0.78)",
        border="rgba(255,255,255,0.22)",
        accent="#22c55e",
        chart_palette=("#22c55e", "#3b82f6", "#f97316", "#ef4444", "#a855f7"),
    ),
}


def theme_css(theme: Theme) -> str:
    """
    Return CSS that restyles the app instantly using CSS variables + conservative selectors.
    """
    return f"""
<style>
:root {{
  --ws-bg: {theme.background};
  --ws-surface: {theme.surface};
  --ws-text: {theme.text};
  --ws-muted: {theme.muted_text};
  --ws-border: {theme.border};
  --ws-accent: {theme.accent};
}}

.stApp {{
  background: var(--ws-bg);
  color: var(--ws-text);
}}

h1, h2, h3, h4, h5, h6 {{
  color: var(--ws-text) !important;
}}

[data-testid="stCaptionContainer"] {{
  color: var(--ws-muted) !important;
}}

.card {{
  border: 1px solid var(--ws-border) !important;
  background: var(--ws-surface) !important;
}}
.card-title {{
  color: var(--ws-muted) !important;
}}
.card-value {{
  color: var(--ws-text) !important;
}}

[data-testid="stExpander"] {{
  border: 1px solid var(--ws-border);
  border-radius: 14px;
  background: var(--ws-surface);
}}

.stButton > button {{
  border-radius: 10px;
  border: 1px solid var(--ws-border);
}}
.stButton > button:hover {{
  border-color: var(--ws-accent);
}}
</style>
""".strip()