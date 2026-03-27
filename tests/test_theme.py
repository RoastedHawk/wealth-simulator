from wealth_simulator.theme import PRESET_THEMES, theme_css


def test_theme_css_contains_core_variables():
    theme = PRESET_THEMES["Neutral"]
    css = theme_css(theme)
    assert "--ws-bg" in css
    assert "--ws-accent" in css
    assert theme.background in css
    assert theme.accent in css


def test_presets_have_non_empty_chart_palettes():
    for theme in PRESET_THEMES.values():
        assert len(theme.chart_palette) >= 3
        assert all(isinstance(c, str) and c.startswith("#") for c in theme.chart_palette)