# Baseline Measurements

## Evaluation Run

The first baseline evaluation was run before applying retrieval, chunking, prompt, or model optimizations.

Command:

```bash
python evaluate.py --k 3 --output eval-baseline.json
```

Output file:

```text
evals/results/eval-baseline.json
```

Run timestamp:

```text
2026-04-20T11:32:25.583478
```

## Summary

```json
{
  "total_questions": 5,
  "source_hit_rate": 1.0,
  "average_keyword_score": 0.4333333333333333
}
```

## Interpretation

The `source_hit_rate` is `1.0`, which means the expected source document appeared in the top 3 retrieved chunks for every evaluation question.

This shows that the current vector search is finding the correct source files for the small evaluation set.

The `average_keyword_score` is about `0.43`, which means the generated answers included about 43% of the expected keywords on average.

This suggests that the system retrieves relevant context, but the generated answers do not always include all expected technical terms. Some answers may still be conceptually correct even when the exact expected keywords are missing.

## Per-Question Results

| ID | Expected Source Retrieved | Keyword Score | Matched Keywords | Top Retrieved Source |
| --- | --- | ---: | --- | --- |
| `classes-basic` | Yes | 0.67 | `class`, `feature` | `data/eiffel-guide/07-classes.md` |
| `loops-basic` | Yes | 0.50 | `until`, `loop` | `data/eiffel-guide/18-loops.md` |
| `agents-basic` | Yes | 0.33 | `agent` | `data/eiffel-guide/21-agents.md` |
| `contracts-basic` | Yes | 0.33 | `invariant` | `data/eiffel-guide/19-contracts.md` |
| `inheritance-basic` | Yes | 0.33 | `inherit` | `data/eiffel-guide/14-multiple-inheritance.md` |

## Retrieval Observations

The retriever found the expected source file for all questions.

Some questions returned duplicate source files in the top 3 results. For example, the loops question retrieved three chunks from `data/eiffel-guide/18-loops.md`.

Duplicate retrieval is not always wrong, but it can reduce context diversity and may limit answer completeness for broader questions.

## Baseline Conclusion

The baseline is strong on source retrieval and weaker on answer completeness.

The next optimization should try to preserve the `1.0` source hit rate while improving the average keyword score and reducing duplicate context.

Recommended next experiment:

```text
MMR retrieval
```

Expected improvement target:

- Keep `source_hit_rate` close to `1.0`.
- Improve `average_keyword_score` above `0.43`.
- Reduce repeated chunks from the same source when possible.
