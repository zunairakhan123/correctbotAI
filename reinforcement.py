def detect_positive_themes(text: str) -> str:
    """Detect the most relevant positive theme based on keyword frequency."""
    themes = {
        "Creativity": ["imagine", "creative", "build", "make", "design", "create"],
        "Curiosity": ["learn", "explore", "discover", "question", "wonder", "investigate"],
        "Kindness": ["help", "kind", "share", "care", "support", "love"],
        "Exploration": ["adventure", "journey", "explore", "travel", "discover", "seek"],
        "Reflection": ["reflect", "think", "contemplate", "consider", "ponder"],
        "Problem Solving": ["solve", "resolve", "figure out", "troubleshoot", "challenge"],
        "Bravery": ["courage", "brave", "fearless", "risk", "adventure"],
        "Resilience": ["persist", "overcome", "endure", "strong", "bounce back"],
        "Empathy": ["understand", "sympathize", "care", "compassion", "relate"],
        "Teamwork": ["collaborate", "team", "work together", "help each other", "cooperate"]
    }

    text = text.lower()
    theme_scores = {}

    for theme, keywords in themes.items():
        score = sum(text.count(keyword) for keyword in keywords)
        if score > 0:
            theme_scores[theme] = score

    if not theme_scores:
        return None  # no match

    # Return theme with the highest score
    most_relevant_theme = max(theme_scores, key=theme_scores.get)
    return most_relevant_theme
