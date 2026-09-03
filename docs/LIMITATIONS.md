# Limitations

- The primary supported slice contains 22 questions, one model, and one run.
- The 200 questions remain a benchmark candidate pending full independent
  domain adjudication.
- Strict scoring can reject semantically equivalent conversions or paraphrases.
- Raw FRED snapshots are excluded because individual series can carry distinct
  third-party redistribution conditions.
- Live FRED retrieval cannot reconstruct the exact byte-frozen July 29, 2026
  responses after revisions or later observations.
- Iris results are auditable from recorded artifacts, but the proprietary
  production implementation is not independently rerunnable from this release.
- Accuracy on the 22-question supported slice is conditional on declared Iris
  coverage and does not establish system-wide superiority.
