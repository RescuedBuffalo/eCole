"""Utilities for generating sentence embeddings.

Currently this module exposes a ``DummyEmbeddingFunction`` used by the
memory store.  It returns a single dimensional embedding based on the
length of the input text and acts as a placeholder for a more sophisticated
embedding model in the future.
"""


class DummyEmbeddingFunction:
    """Very small embedding stub used for tests and development."""

    def __call__(self, texts):
        return [[float(len(t))] for t in texts]

