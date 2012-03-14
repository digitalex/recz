from collections import defaultdict
from db import Db

class Recz:
    """Lightweight, fast recommendation system for item-to-item recommendations."""

    def __init__(self):
        self.db = Db()

    def add_example(self, item_id, session_id):
        """Adds an example to the training data."""
        self.db.add_example(item_id, session_id)

    def recommend(self, item_id, k=5):
        """Build a list of k recommended items, based on the given item_id."""
        sessionset = self.db.get_sessionset(item_id)
        itemcounts = defaultdict(int)

        # Count the occurrences of other items viewed by the same sessions.
        for session_id in sessionset:
            itemset = self.db.get_itemset(session_id)
            itemset.discard(item_id)
            for other_item_id in itemset:
                itemcounts[other_item_id] += 1

        # Sort by count, descending, then take the k first items.
        return sorted(
                itemcounts.iterkeys(),
                key=lambda k: itemcounts[k],
                reverse=True)[:k]

