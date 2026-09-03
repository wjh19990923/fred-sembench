import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const experimentDir =
  process.env.EXPERIMENT_DIR ??
  path.dirname(fileURLToPath(import.meta.url));
const benchmarkDir = path.resolve(experimentDir, "../..");
const blindPath = path.join(experimentDir, "questions_blind.jsonl");
const responsesPath = path.join(experimentDir, "output", "responses.jsonl");
const scoresPath = path.join(
  experimentDir,
  "output",
  "deterministic_scores.jsonl",
);
const reportPath = path.join(
  experimentDir,
  "output",
  "DETERMINISTIC_SCORE_REPORT.md",
);
const goldPath = path.join(benchmarkDir, "questions.jsonl");

const readJsonLines = (filePath) =>
  fs
    .readFileSync(filePath, "utf8")
    .split(/\r?\n/)
    .filter(Boolean)
    .map((line) => JSON.parse(line));
const extractNumbers = (text) =>
  [...text.matchAll(/[-+]?(?:\d[\d,]*)(?:\.\d+)?/g)]
    .map((match) => ({
      raw: match[0],
      value: Number(match[0].replaceAll(",", "")),
    }))
    .filter((item) => Number.isFinite(item.value));
const normalizeNumber = (value) =>
  Number(value.replaceAll(",", "")).toString();
const containsUnit = (response, expectedUnit) => {
  const text = response.toLowerCase();
  if (!expectedUnit) return true;
  if (expectedUnit === "percent") return /%|\bpercent\b/.test(text);
  if (expectedUnit === "percentage points") {
    return /\bpercentage[- ]points?\b|\bpercent[- ]points?\b|\bp\.?p\.?\b/.test(
      text,
    );
  }
  if (expectedUnit.startsWith("index points")) {
    return /\bindex(?:[- ]points?)?\b/.test(text);
  }
  if (expectedUnit === "claims") return /\bclaims?\b/.test(text);
  if (expectedUnit === "thousands of units, SAAR") {
    return (
      /\bthousand/.test(text) &&
      (/\bunits?\b/.test(text) || /\bsaar\b|annual rate/.test(text))
    );
  }
  if (expectedUnit === "millions of U.S. dollars") {
    return (
      /\bmillion/.test(text) &&
      (/\bdollars?\b|\busd\b|\$/.test(text))
    );
  }
  return text.includes(expectedUnit.toLowerCase());
};
const abstained = (response) =>
  /\b(cannot|can't|unable|do not have|don't have|not have|cannot reliably|not possible|insufficient|would need|need access|need the (?:data|snapshot)|cannot verify|can't verify|not provided)\b/i.test(
    response,
  );
const novelNumbers = (question, response) => {
  const responseWithoutListMarkers = response.replace(
    /^\s*\d+[.)]\s+/gm,
    "",
  );
  const questionNumbers = new Set(
    extractNumbers(question).map((item) => normalizeNumber(item.raw)),
  );
  return extractNumbers(responseWithoutListMarkers).filter(
    (item) => !questionNumbers.has(normalizeNumber(item.raw)),
  );
};

const blind = readJsonLines(blindPath);
const responses = readJsonLines(responsesPath);
const selectedIds = new Set(blind.map((row) => row.case_id));
const goldById = new Map(
  readJsonLines(goldPath)
    .filter((row) => selectedIds.has(row.case_id))
    .map((row) => [row.case_id, row]),
);
const responseById = new Map(
  responses.map((row) => [row.case_id, row]),
);
if (blind.length !== 48 || responses.length !== 48 || goldById.size !== 48) {
  throw new Error("Expected exactly 48 blind, response, and gold records.");
}

const scores = blind.map((blindRow) => {
  const goldRow = goldById.get(blindRow.case_id);
  const gold = goldRow.gold;
  const response = responseById.get(blindRow.case_id).response ?? "";
  const newNumbers = novelNumbers(blindRow.question, response);

  if (gold.answer_mode === "clarification") {
    const cutoffPresent =
      /\bas[- ]of\b|\bcutoff\b|\bvintage\b|specif(?:y|ic).{0,20}\bdate\b|what.{0,12}\blatest\b.{0,12}mean/i.test(
        response,
      );
    const seriesIds = [
      ...(gold.series_ids ?? []),
      ...(goldRow.confounders?.alternative_series_ids ?? []),
    ];
    const mentionedSeries = seriesIds.filter((seriesId) =>
      response.toUpperCase().includes(seriesId.toUpperCase()),
    );
    const conceptClarification =
      mentionedSeries.length >= 2 ||
      /\bclarif|\bwhich (?:concept|series|measure)|\bintended (?:concept|series|measure)/i.test(
        response,
      );
    const noInventedNumber = newNumbers.length === 0;
    const isCorrect =
      cutoffPresent && conceptClarification && noInventedNumber;
    return {
      index: blindRow.index,
      case_id: blindRow.case_id,
      task_type: blindRow.task_type,
      answer_mode: gold.answer_mode,
      classification: isCorrect
        ? "correct_clarification"
        : "needs_manual_review",
      is_correct: isCorrect,
      value_match: null,
      unit_match: null,
      abstained: false,
      hallucinated_numeric_claim: false,
      possible_numeric_claim_needing_review: !noInventedNumber,
      extracted_candidate_numbers: newNumbers.map((item) => item.raw),
      checks: {
        cutoff_present: cutoffPresent,
        concept_or_series_clarification: conceptClarification,
        no_invented_number: noInventedNumber,
      },
      scoring_method: "local_deterministic_clarification_rubric",
    };
  }

  const expectedValue = Number(gold.answer);
  const tolerance = Number(gold.precision ?? 0);
  const numbers = extractNumbers(response);
  const valueMatch = numbers.some(
    (item) =>
      Math.abs(item.value - expectedValue) <=
      Math.max(tolerance / 2, 1e-12),
  );
  const unitMatch = containsUnit(response, gold.unit);
  const didAbstain = abstained(response);
  let classification;
  if (valueMatch && unitMatch) classification = "correct_numeric";
  else if (valueMatch) classification = "value_match_unit_unverified";
  else if (didAbstain) classification = "safe_abstention";
  else if (newNumbers.length > 0)
    classification = "possible_numeric_claim_needing_review";
  else classification = "needs_manual_review";

  return {
    index: blindRow.index,
    case_id: blindRow.case_id,
    task_type: blindRow.task_type,
    answer_mode: gold.answer_mode,
    classification,
    is_correct: classification === "correct_numeric",
    expected_value: gold.answer,
    expected_unit: gold.unit,
    expected_precision: gold.precision,
    value_match: valueMatch,
    unit_match: unitMatch,
    abstained: didAbstain,
    hallucinated_numeric_claim: false,
    possible_numeric_claim_needing_review:
      classification === "possible_numeric_claim_needing_review",
    extracted_candidate_numbers: newNumbers.map((item) => item.raw),
    scoring_method: "local_deterministic_value_unit_lower_bound",
  };
});

fs.writeFileSync(
  scoresPath,
  `${scores.map((row) => JSON.stringify(row)).join("\n")}\n`,
  "utf8",
);

const count = (predicate) => scores.filter(predicate).length;
const numericScores = scores.filter((row) => row.answer_mode === "numeric");
const clarificationScores = scores.filter(
  (row) => row.answer_mode === "clarification",
);
const classifications = Object.fromEntries(
  [...new Set(scores.map((row) => row.classification))]
    .sort()
    .map((classification) => [
      classification,
      count((row) => row.classification === classification),
    ]),
);
const report = `# Deterministic Score Report

## Scope

- Configuration: \`${JSON.parse(fs.readFileSync(path.join(experimentDir, "experiment_config.json"), "utf8")).configuration}\`
- Total cases: **${scores.length}**
- Numeric cases: **${numericScores.length}**
- Clarification cases: **${clarificationScores.length}**
- Scoring environment: local only; no model, API, network, or tool calls

## Provisional results

- Strict correct cases: **${count((row) => row.is_correct)} / ${scores.length}**
- Strict numeric correct: **${numericScores.filter((row) => row.is_correct).length} / ${numericScores.length}**
- Correct clarification: **${clarificationScores.filter((row) => row.is_correct).length} / ${clarificationScores.length}**
- Safe abstentions on numeric cases: **${numericScores.filter((row) => row.classification === "safe_abstention").length}**
- Confirmed hallucinated numeric claims by deterministic rules: **${count((row) => row.hallucinated_numeric_claim)}**
- Possible numeric claims requiring semantic review: **${count((row) => row.possible_numeric_claim_needing_review)}**
- Cases requiring manual or authorized LLM-judge review: **${count((row) => row.classification === "needs_manual_review" || row.classification === "value_match_unit_unverified" || row.classification === "possible_numeric_claim_needing_review")}**

## Classification counts

${Object.entries(classifications)
  .map(([classification, value]) => `- \`${classification}\`: ${value}`)
  .join("\n")}

## Interpretation limits

This is a conservative deterministic lower-bound score. It recognizes exact
numeric matches within the benchmark precision and explicit unit aliases. It
does not perform arbitrary unit conversion or semantic paraphrase judgment.
It does not label a novel number as hallucinated without semantic review,
because dates, index bases, formula constants, and list numbering can otherwise
produce false positives.
Clarification cases use a predeclared local rubric: request an as-of/cutoff,
clarify the intended concept or series, and avoid inventing a number.

FinRetrieval uses an LLM judge for semantic normalization. Running an analogous
judge here requires explicit authorization to send private gold records and
collected responses to the subscription-backed model.
`;
fs.writeFileSync(reportPath, report, "utf8");
console.log(report);
