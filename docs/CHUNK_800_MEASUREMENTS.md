# Chunk Size 800 Measurements

## Evaluation Run

This experiment tested larger chunks after the baseline and MMR experiments.

The Chroma database was rebuilt after changing the text splitter in `create_db.py` to:

```python
chunk_size=800
chunk_overlap=120
```

Evaluation command:

```bash
python evaluate.py --k 3 --output eval-chunk-800.json
```

Output file:

```text
evals/results/eval-chunk-800.json
```

Run timestamp:

```text
2026-04-20T21:20:46.111244
```

## Summary

```json
{
  "total_questions": 5,
  "source_hit_rate": 1.0,
  "average_keyword_score": 0.7333333333333333
}
```

## Comparison

| Metric | Baseline Similarity | MMR | Chunk 800 |
| --- | ---: | ---: | ---: |
| Total questions | 5 | 5 | 5 |
| Source hit rate | 1.0 | 1.0 | 1.0 |
| Average keyword score | 0.4333 | 0.4333 | 0.7333 |

## Interpretation

The larger chunk configuration preserved retrieval correctness. The expected source file still appeared in the top 3 retrieved chunks for every evaluation question.

The average keyword score improved from `0.4333` to `0.7333`.

This is the strongest improvement so far. It suggests that the original chunks were too small for the model to consistently receive enough context for complete answers.

## Per-Question Results

| ID | Expected Source Retrieved | Baseline Keyword Score | Chunk 800 Keyword Score | Matched Keywords |
| --- | --- | ---: | ---: | --- |
| `classes-basic` | Yes | 0.67 | 0.67 | `class`, `feature` |
| `loops-basic` | Yes | 0.50 | 1.00 | `from`, `until`, `loop`, `end` |
| `agents-basic` | Yes | 0.33 | 0.33 | `agent` |
| `contracts-basic` | Yes | 0.33 | 1.00 | `require`, `ensure`, `invariant` |
| `inheritance-basic` | Yes | 0.33 | 0.67 | `inherit`, `rename` |

## Key Observations

The loops answer improved substantially. With larger chunks, the answer included `from`, `until`, `loop`, and `end`.

The contracts answer also improved substantially. It included the Eiffel-specific terms `require`, `ensure`, and `invariant`.

The inheritance answer improved from one matched keyword to two matched keywords.

The agents answer did not improve according to the keyword metric. It still matched only `agent`, not `routine` or `argument`.

## Conclusion

Increasing chunk size to `800` with `120` overlap improved answer completeness while preserving source retrieval accuracy.

This optimization should be kept for now.

Recommended next experiment:

```text
Improve the prompt and make model behavior deterministic with temperature=0.
```

The goal of the next experiment is to improve answer completeness, especially for the agents question, without reducing source hit rate.
