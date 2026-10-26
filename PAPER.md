# FRED-SemBench: Evaluating Semantic Reliability in LLM Access to Macroeconomic Data

**Authors:** Wilson Wang, Chandler Han, and Peter Zhang (Kairos-AI)  
**Corresponding author:** Peter Zhang, founders@kairos-ai.io  
**Venue:** Proceedings of the 11th Workshop on Financial Technology and Natural Language Processing (FinNLP 2026), pages 237–242

**Published paper:** <https://aclanthology.org/2026.finnlp-1.19/>

## Abstract

Access to authoritative financial data does not ensure semantically correct
answers: a language model may retrieve a valid observation associated with the
wrong series, transformation, unit, or temporal interpretation. FRED-SemBench
evaluates these failures with 200 questions over independently selected FRED
concepts. A controlled comparison of an unaided model, FRED and Web access, and
the Kairos-AI Iris semantic layer shows that retrieval improves numerical
answering but can weaken appropriate clarification on underspecified requests.
Within its declared support set, Iris preserves the numerical benefit and
restores clarification behavior.

## Public research artifacts

- Code, prompts, recorded outputs, scores, and reproducibility tools:
  <https://github.com/wjh19990923/fred-sembench>
- Structured dataset and Dataset Viewer:
  <https://huggingface.co/datasets/wangjinh/FRED-SemBench>
- Paper-aligned immutable release:
  <https://github.com/wjh19990923/fred-sembench/releases/tag/v1.0.0-paper>

The paper is available in [ACL Anthology](https://aclanthology.org/2026.finnlp-1.19/).
This repository is the code and reproducibility companion; Hugging Face hosts
the structured dataset and Dataset Viewer.

## Artifact boundary

The public release contains the materials required to audit the reported
results. Iris is a commercial Kairos-AI system; its production implementation
and commercial access are not included or implied by this release.
