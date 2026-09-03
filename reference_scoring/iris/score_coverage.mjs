import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const experimentDir = path.dirname(fileURLToPath(import.meta.url));
const benchmarkDir = path.resolve(experimentDir, "../..");
const outputDir = path.join(experimentDir, "output");
const readJsonLines = (filePath) =>
  fs.readFileSync(filePath, "utf8").split(/\r?\n/).filter(Boolean).map(JSON.parse);

const questions = readJsonLines(path.join(experimentDir, "questions_blind.jsonl"));
const scores = readJsonLines(path.join(outputDir, "deterministic_scores.jsonl"));
const supported = readJsonLines(
  path.join(benchmarkDir, "iris-preflight", "iris_supported_questions.jsonl"),
);
const supportedById = new Map(supported.map((row) => [row.case_id, row]));
const scoreById = new Map(scores.map((row) => [row.case_id, row]));

const rows = questions.map((question) => {
  const score = scoreById.get(question.case_id);
  if (!score) throw new Error(`Missing deterministic score for ${question.case_id}`);
  return {
    case_id: question.case_id,
    task_type: question.task_type,
    iris_preflight_scope: supportedById.has(question.case_id) ? "supported" : "excluded",
    answer_mode: score.answer_mode,
    classification: score.classification,
    is_correct: score.is_correct,
  };
});

if (rows.filter((row) => row.iris_preflight_scope === "supported").length !== 22) {
  throw new Error("Expected exactly 22 Iris-supported cases.");
}

const summarize = (subset) => ({
  cases: subset.length,
  strict_correct: subset.filter((row) => row.is_correct).length,
  numeric_cases: subset.filter((row) => row.answer_mode === "numeric").length,
  numeric_correct: subset.filter((row) => row.answer_mode === "numeric" && row.is_correct).length,
  clarification_cases: subset.filter((row) => row.answer_mode === "clarification").length,
  clarification_correct: subset.filter((row) => row.answer_mode === "clarification" && row.is_correct).length,
  safe_abstentions: subset.filter((row) => row.classification === "safe_abstention").length,
});

const summary = {
  schema_version: "1.0.0",
  scope_definition: "Pre-registered Iris preflight mapping; computed before this condition was run.",
  overall: summarize(rows),
  supported: summarize(rows.filter((row) => row.iris_preflight_scope === "supported")),
  excluded: summarize(rows.filter((row) => row.iris_preflight_scope === "excluded")),
};

fs.writeFileSync(path.join(outputDir, "coverage_scores.jsonl"), `${rows.map(JSON.stringify).join("\n")}\n`, "utf8");
fs.writeFileSync(path.join(outputDir, "coverage_summary.json"), `${JSON.stringify(summary, null, 2)}\n`, "utf8");
console.log(JSON.stringify(summary, null, 2));
