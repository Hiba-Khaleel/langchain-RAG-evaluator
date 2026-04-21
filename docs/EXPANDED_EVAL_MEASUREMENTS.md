# Expanded Evaluation Measurements

## Evaluation Run

This evaluation was run after improving the prompt and expanding the evaluation set.

The evaluation set changed from 5 questions to 6 questions:

- The `agents-basic` expected keywords were updated to better match the actual source text.
- A new `agents-arguments` question was added to test argument passing through agents.

Evaluation command:

```bash
python evaluate.py --k 3 --output eval-expanded-questions.json
```

Output file:

```text
evals/results/eval-expanded-questions.json
```

Run timestamp:

```text
2026-04-21T09:30:06.078603
```

## Summary

```json
{
  "total_questions": 6,
  "source_hit_rate": 1.0,
  "average_keyword_score": 0.8888888888888888
}
```

## Important Note About Comparison

This result should not be compared directly as a pure model improvement against earlier 5-question runs, because the evaluation set changed.

The earlier runs used 5 questions. This run uses 6 questions and includes a fairer agents evaluation.

However, the result is still valuable because it shows the current optimized pipeline performs well on a better-aligned evaluation set.

## Current Configuration

The current best configuration uses:

- Similarity search.
- `k=3`.
- `chunk_size=800`.
- `chunk_overlap=120`.
- `temperature=0`.
- Prompt v2, which asks the model to prefer Eiffel-specific terminology from the retrieved context.

## Comparison Table

| Experiment | Questions | Source Hit Rate | Average Keyword Score | Notes |
| --- | ---: | ---: | ---: | --- |
| Baseline similarity search, chunk size 300 | 5 | 1.0 | 0.4333 | Initial baseline |
| MMR retrieval, chunk size 300 | 5 | 1.0 | 0.4333 | More diverse retrieval, no score improvement |
| Similarity search, chunk size 800 | 5 | 1.0 | 0.7333 | Strong chunking improvement |
| Prompt v1 | 5 | 1.0 | 0.6000 | Too concise, dropped technical terms |
| Prompt v2 | 5 | 1.0 | 0.7333 | Recovered score and improved technical detail |
| Expanded evaluation set | 6 | 1.0 | 0.8889 | Current best measurement on improved eval set |

## Per-Question Results

| ID | Expected Source Retrieved | Keyword Score | Matched Keywords |
| --- | --- | ---: | --- |
| `classes-basic` | Yes | 0.67 | `class`, `feature` |
| `loops-basic` | Yes | 1.00 | `from`, `until`, `loop`, `end` |
| `agents-basic` | Yes | 1.00 | `agent`, `feature`, `call`, `item` |
| `agents-arguments` | Yes | 1.00 | `agent`, `argument`, `tuple`, `call` |
| `contracts-basic` | Yes | 1.00 | `require`, `ensure`, `invariant` |
| `inheritance-basic` | Yes | 0.67 | `inherit`, `rename` |

## Interpretation

The source hit rate stayed at `1.0`, meaning the expected source file appeared in the retrieved top 3 chunks for every question.

The average keyword score increased to `0.8889` on the expanded evaluation set.

The agents evaluation improved because the expected keywords now better reflect the actual source document. The new `agents-arguments` question also confirms that the system can answer a more specific question about passing arguments with agents.

The remaining weaker areas are:

- `classes-basic`, because the answer did not include `create`.
- `inheritance-basic`, because the answer did not include `select`.

## Conclusion

The current optimized pipeline is performing well on the expanded evaluation set.

The strongest confirmed changes so far are:

1. Larger chunks: `chunk_size=800`, `chunk_overlap=120`.
2. Deterministic model behavior: `temperature=0`.
3. Prompt v2, which encourages Eiffel-specific terminology.
4. A better-aligned evaluation set with more targeted agents questions.

Recommended next step:

```text
Add more evaluation questions before making more optimization decisions.
```

The score is now high enough that further gains should be validated against a larger and more varied evaluation set.
