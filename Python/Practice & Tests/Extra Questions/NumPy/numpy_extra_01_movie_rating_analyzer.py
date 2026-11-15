"""
================================================================================
PYTHON: NUMPY - EXTRA QUESTION 1
================================================================================

Question: Movie Rating Analyzer
Class: MovieRatingAnalyzer

Problem Statement:
Process viewer movie ratings (out of 100) using NumPy arrays.

Operations Required:
- create_rating_array(self, ratings_array: list) -> np.ndarray
  Convert input list to a NumPy array of integer type and return it.

- validate_ratings(self, rating_array: np.ndarray) -> bool
  Check for non-empty array (return False if empty). Ensure all values are between
  0 and 100 inclusive using np.any; return True if valid, else False.

- compute_rating_summary(self, rating_array: np.ndarray) -> tuple
  Convert input to numeric array. Compute Total (sum), Average (rounded to 1 decimal place),
  and Maximum value. Return tuple: (total, average, maximum).

- apply_bonus(self, rating_array: np.ndarray) -> np.ndarray
  Convert elements to float datatype. Increase ratings > 85 by 5%. Clip values to a
  maximum of 100 and round to 1 decimal place. Return updated array.

- categorize_movies(self, rating_array: np.ndarray) -> np.ndarray
  Categorize values using thresholds: >= 90 -> "Excellent", 80-89 -> "Good",
  < 80 -> "Needs Improvement". Return string array.

- format_ratings_with_grades(self, rating_array: np.ndarray) -> np.ndarray
  Iterate using a for loop over input. Map ratings: >= 90 -> "A", 80-89 -> "B",
  70-79 -> "C", < 70 -> "D". Return grade labels as a string array.
"""

import numpy as np


class MovieRatingAnalyzer:
    def create_rating_array(self, ratings_array: list) -> np.ndarray:
        """Convert input list to an integer NumPy array."""
        return np.asarray(ratings_array, dtype=int)

    def validate_ratings(self, rating_array: np.ndarray) -> bool:
        """
        Return False if empty. Validate that all elements are between 0 and 100
        inclusive using np.any. Return True if valid, else False.
        """
        arr = np.asarray(rating_array)
        if arr.size == 0:
            return False
        # If any element is < 0 or > 100, ratings are invalid
        if np.any((arr < 0) | (arr > 100)):
            return False
        return True

    def compute_rating_summary(self, rating_array: np.ndarray) -> tuple:
        """
        Compute Total (sum), Average (rounded to 1 decimal place), and Maximum.
        Return tuple: (total, average, maximum).
        """
        arr = np.asarray(rating_array, dtype=float)
        total = float(np.sum(arr))
        # Cast total to int if it is a whole number integer sum
        if total.is_integer():
            total = int(total)
        avg = round(float(np.mean(arr)), 1)
        max_val = float(np.max(arr))
        if max_val.is_integer():
            max_val = int(max_val)
        return (total, avg, max_val)

    def apply_bonus(self, rating_array: np.ndarray) -> np.ndarray:
        """
        Convert to float array. Increase ratings > 85 by 5%, clip to 100,
        and round to 1 decimal place. Return updated array.
        """
        arr = np.asarray(rating_array, dtype=float).copy()
        mask = arr > 85.0
        arr[mask] = arr[mask] * 1.05
        arr = np.clip(arr, 0.0, 100.0)
        return np.round(arr, 1)

    def categorize_movies(self, rating_array: np.ndarray) -> np.ndarray:
        """
        Categorize ratings:
          >= 90: 'Excellent'
          80-89 (>= 80 and < 90 or <= 89): 'Good'
          < 80: 'Needs Improvement'
        """
        arr = np.asarray(rating_array)
        conditions = [
            arr >= 90,
            (arr >= 80) & (arr < 90),
            arr < 80
        ]
        choices = ["Excellent", "Good", "Needs Improvement"]
        return np.select(conditions, choices, default="Needs Improvement")

    def format_ratings_with_grades(self, rating_array: np.ndarray) -> np.ndarray:
        """
        Iterate using a for loop over the input array.
        Map ratings:
          >= 90 -> 'A'
          80-89 -> 'B'
          70-79 -> 'C'
          < 70  -> 'D'
        Return grade labels as a string array.
        """
        arr = np.asarray(rating_array)
        grades = []
        for val in arr:
            if val >= 90:
                grades.append("A")
            elif 80 <= val < 90:
                grades.append("B")
            elif 70 <= val < 80:
                grades.append("C")
            else:
                grades.append("D")
        return np.array(grades, dtype=str)


if __name__ == "__main__":
    analyzer = MovieRatingAnalyzer()
    raw = [95, 88, 72, 60, 86, 100, 45]
    arr = analyzer.create_rating_array(raw)
    print("Rating Array:", arr)
    print("Valid:", analyzer.validate_ratings(arr))
    print("Summary (sum, avg, max):", analyzer.compute_rating_summary(arr))
    print("With Bonus:", analyzer.apply_bonus(arr))
    print("Categories:", analyzer.categorize_movies(arr))
    print("Grades:", analyzer.format_ratings_with_grades(arr))
