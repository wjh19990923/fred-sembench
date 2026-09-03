import path from "node:path";
import { fileURLToPath } from "node:url";

process.env.EXPERIMENT_DIR = path.dirname(fileURLToPath(import.meta.url));
await import("../llm-only-codex-subscription/score_deterministic.mjs");

