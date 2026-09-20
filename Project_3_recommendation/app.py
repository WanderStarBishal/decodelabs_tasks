from dataclasses import dataclass
from typing import List, Set, Tuple


@dataclass
class Movie:
    title: str
    genres: Set[str]
    year: int


CATALOG: List[Movie] = [
    Movie("Inception", {"sci-fi", "thriller", "action"}, 2010),
    Movie("The Notebook", {"romance", "drama"}, 2004),
    Movie("Interstellar", {"sci-fi", "drama", "adventure"}, 2014),
    Movie("The Hangover", {"comedy"}, 2009),
    Movie("John Wick", {"action", "thriller"}, 2014),
    Movie("La La Land", {"romance", "drama", "musical"}, 2016),
    Movie("The Conjuring", {"horror", "thriller"}, 2013),
    Movie("Superbad", {"comedy", "drama"}, 2007),
    Movie("Mad Max: Fury Road", {"action", "sci-fi", "adventure"}, 2015),
    Movie("A Quiet Place", {"horror", "sci-fi", "thriller"}, 2018),
    Movie("Pride & Prejudice", {"romance", "drama"}, 2005),
    Movie("The Grand Budapest Hotel", {"comedy", "adventure"}, 2014),
    Movie("Get Out", {"horror", "thriller", "drama"}, 2017),
    Movie("Dune", {"sci-fi", "adventure", "drama"}, 2021),
    Movie("Crazy Rich Asians", {"romance", "comedy"}, 2018),
]



def jaccard_similarity(a: Set[str], b: Set[str]) -> float:
    """Return overlap between two sets as a fraction from 0.0 to 1.0."""
    if not a or not b:
        return 0.0
    intersection = len(a & b)
    union = len(a | b)
    return intersection / union


def recommend(
    user_prefs: Set[str],
    catalog: List[Movie],
    top_n: int = 5,
) -> List[Tuple[Movie, float]]:
    """
    Score every movie in the catalog against the user's preferences
    and return the top_n highest-scoring (movie, score) pairs.
    Items with a score of 0 (no overlap at all) are excluded.
    """
    scored = [
        (movie, jaccard_similarity(user_prefs, movie.genres))
        for movie in catalog
    ]
    scored = [pair for pair in scored if pair[1] > 0]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:top_n]


def display_recommendations(results: List[Tuple[Movie, float]]) -> None:
    if not results:
        print("\nNo matches found for those interests. Try different genres.\n")
        return

    print(f"\nTop {len(results)} recommendations for you:\n")
    print(f"{'#':<3}{'Title':<28}{'Year':<6}{'Match':<8}{'Genres'}")
    print("-" * 70)
    for rank, (movie, score) in enumerate(results, start=1):
        match_pct = f"{score * 100:.0f}%"
        genres_str = ", ".join(sorted(movie.genres))
        print(f"{rank:<3}{movie.title:<28}{movie.year:<6}{match_pct:<8}{genres_str}")
    print()



def get_user_preferences() -> Set[str]:
    all_genres = sorted({g for movie in CATALOG for g in movie.genres})
    print("Available genres:", ", ".join(all_genres))
    raw = input("Enter genres you like (comma-separated): ")
    prefs = {g.strip().lower() for g in raw.split(",") if g.strip()}
    return prefs


def main() -> None:
    print("=" * 70)
    print("  MOVIE RECOMMENDER — content-based filtering demo")
    print("=" * 70)

    while True:
        prefs = get_user_preferences()
        if not prefs:
            print("No genres entered — please try again.\n")
            continue

        results = recommend(prefs, CATALOG, top_n=5)
        display_recommendations(results)

        again = input("Try another set of preferences? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()