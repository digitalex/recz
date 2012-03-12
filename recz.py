from collections import defaultdict

class Recz:
    """Lightweight, fast recommendation system for item-to-item recommendations."""

    def __init__(self):
        self.sessions = {}
        self.items = {}

    def add_example(self, item_id, session_id):
        """Adds an example to the training data."""
        self.sessions.setdefault(item_id, set()).add(session_id)
        self.items.setdefault(session_id, set()).add(item_id)

    def compact(self):
        """Removes data that cannot help recommendations."""
        for key in filter(lambda k: len(self.sessions[k])<2, self.sessions.iterkeys()):
          del self.sessions[key]
        for key in filter(lambda k: len(self.items[k])<2, self.items.iterkeys()):
          del self.items[key]

    def recommend(self, item_id, k=5):
        """Build a list of k recommended items, based on the given item_id."""
        sessionset = self.sessions.get(item_id, set())
        itemcounts = defaultdict(int)

        # Count the occurrences of other items viewed by the same sessions.
        for session_id in sessionset:
            itemset = self.items.get(session_id, set())
            itemset.discard(item_id)
            for other_item_id in itemset:
                itemcounts[other_item_id] += 1

        # Sort by count, descending, then take the k first items.
        return sorted(
                itemcounts.iterkeys(),
                key=lambda k: itemcounts[k],
                reverse=True)[:k]

