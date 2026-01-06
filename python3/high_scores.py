"""High Scores module for the Numbers Game.

Handles saving and loading high scores to a JSON file.
"""

import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Default path for high scores file
SCORES_FILE = os.path.join(os.path.dirname(__file__), 'high_scores.json')


@dataclass
class ScoreEntry:
    """Represents a single high score entry."""
    player_name: str
    tries: int
    hints_used: int
    score: int
    difficulty: int
    date: str


def load_scores(filepath: str = SCORES_FILE) -> Dict[str, List[dict]]:
    """Load high scores from file.
    
    Args:
        filepath: Path to the scores JSON file.
        
    Returns:
        Dictionary with difficulty levels as keys and lists of scores as values.
    """
    if not os.path.exists(filepath):
        return {'4': [], '5': [], '6': []}
    
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {'4': [], '5': [], '6': []}


def save_scores(scores: Dict[str, List[dict]], filepath: str = SCORES_FILE) -> None:
    """Save high scores to file.
    
    Args:
        scores: Dictionary of scores to save.
        filepath: Path to the scores JSON file.
    """
    with open(filepath, 'w') as f:
        json.dump(scores, f, indent=2)


def add_score(
    player_name: str,
    tries: int,
    hints_used: int,
    score: int,
    difficulty: int,
    filepath: str = SCORES_FILE
) -> int:
    """Add a new score and return the player's rank.
    
    Args:
        player_name: Name of the player.
        tries: Number of tries to solve.
        hints_used: Number of hints used.
        score: Final calculated score.
        difficulty: Digit count (4, 5, or 6).
        filepath: Path to scores file.
        
    Returns:
        The player's rank (1-indexed) for this difficulty.
    """
    scores = load_scores(filepath)
    difficulty_key = str(difficulty)
    
    entry = ScoreEntry(
        player_name=player_name,
        tries=tries,
        hints_used=hints_used,
        score=score,
        difficulty=difficulty,
        date=datetime.now().strftime('%Y-%m-%d %H:%M')
    )
    
    scores[difficulty_key].append(asdict(entry))
    
    # Sort by score (descending), then by tries (ascending)
    scores[difficulty_key].sort(key=lambda x: (-x['score'], x['tries']))
    
    # Keep only top 10 scores per difficulty
    scores[difficulty_key] = scores[difficulty_key][:10]
    
    save_scores(scores, filepath)
    
    # Find and return rank
    for i, s in enumerate(scores[difficulty_key]):
        if s['player_name'] == player_name and s['score'] == score:
            return i + 1
    return len(scores[difficulty_key])


def get_top_scores(difficulty: int, limit: int = 5, filepath: str = SCORES_FILE) -> List[dict]:
    """Get top scores for a difficulty level.
    
    Args:
        difficulty: Digit count (4, 5, or 6).
        limit: Maximum number of scores to return.
        filepath: Path to scores file.
        
    Returns:
        List of top score entries.
    """
    scores = load_scores(filepath)
    return scores.get(str(difficulty), [])[:limit]


def display_leaderboard(difficulty: int, filepath: str = SCORES_FILE) -> str:
    """Generate a formatted leaderboard string.
    
    Args:
        difficulty: Digit count (4, 5, or 6).
        filepath: Path to scores file.
        
    Returns:
        Formatted leaderboard string.
    """
    difficulty_names = {4: 'Easy', 5: 'Medium', 6: 'Hard'}
    top_scores = get_top_scores(difficulty, limit=10, filepath=filepath)
    
    if not top_scores:
        return f"\n🏆 {difficulty_names[difficulty]} Leaderboard\nNo scores yet!\n"
    
    lines = [f"\n🏆 {difficulty_names[difficulty]} Leaderboard"]
    lines.append("-" * 50)
    lines.append(f"{'Rank':<6}{'Name':<15}{'Score':<10}{'Tries':<8}{'Date'}")
    lines.append("-" * 50)
    
    for i, entry in enumerate(top_scores, 1):
        lines.append(
            f"{i:<6}{entry['player_name']:<15}{entry['score']:<10}"
            f"{entry['tries']:<8}{entry['date']}"
        )
    
    return "\n".join(lines)
