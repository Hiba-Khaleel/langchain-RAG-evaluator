# MMR Retrieval Measurements

## Evaluation Run

This experiment tested MMR retrieval after the baseline similarity-search evaluation.

MMR means Maximal Marginal Relevance. It tries to retrieve chunks that are both relevant and diverse, which can reduce repeated or near-duplicate context.

Command:

```bash
python evaluate.py --search-type mmr --k 3 --fetch-k 15 --output eval-mmr.json
```

Output file:

```text
evals/results/eval-mmr.json
```

Run timestamp:

```text
2026-04-20T11:47:58.553598
```

## Summary

```json
{
  "total_questions": 5,
  "source_hit_rate": 1.0,
  "average_keyword_score": 0.4333333333333333
}
```

## Comparison With Baseline

| Metric | Baseline Similarity | MMR |
| --- | ---: | ---: |
| Total questions | 5 | 5 |
| Source hit rate | 1.0 | 1.0 |
| Average keyword score | 0.4333 | 0.4333 |

## Interpretation

MMR preserved the source hit rate. The expected source file still appeared in the top 3 retrieved chunks for every evaluation question.

The average keyword score did not improve. It remained at `0.4333`.

This means MMR did not improve the current answer-quality metric for this evaluation set.

## Retrieval Changes

MMR changed the retrieved source mix for several questions.

For the loops question, baseline similarity search retrieved three chunks from the same source file:

```text
data/eiffel-guide/18-loops.md
data/eiffel-guide/18-loops.md
data/eiffel-guide/18-loops.md
```

MMR retrieved a more diverse set:

```text
data/eiffel-guide/18-loops.md
data/eiffel-guide/17-control-structures.md
data/eiffel-guide/22-garbage-collection.md
```

This confirms that MMR increased diversity. However, more diversity did not produce a better keyword score in this small evaluation.

## Per-Question Results

| ID | Expected Source Retrieved | Keyword Score | Matched Keywords | Top Retrieved Source |
| --- | --- | ---: | --- | --- |
| `classes-basic` | Yes | 0.67 | `class`, `feature` | `data/eiffel-guide/07-classes.md` |
| `loops-basic` | Yes | 0.50 | `until`, `loop` | `data/eiffel-guide/18-loops.md` |
| `agents-basic` | Yes | 0.33 | `agent` | `data/eiffel-guide/21-agents.md` |
| `contracts-basic` | Yes | 0.33 | `invariant` | `data/eiffel-guide/19-contracts.md` |
| `inheritance-basic` | Yes | 0.33 | `inherit` | `data/eiffel-guide/14-multiple-inheritance.md` |

## Conclusion

MMR was neutral for the current metrics:

- It preserved retrieval correctness.
- It increased source diversity.
- It did not improve keyword coverage.

For this small documentation corpus, the next optimization should focus on chunking and prompt quality rather than relying on MMR alone.

Recommended next experiment:

```text
Increase chunk size and reduce relative overlap.
```

Suggested test:

```text
chunk_size=800
chunk_overlap=120
```

Then rebuild the Chroma database and run the same evaluation again.
