// Testes de aceite — Coletar feedback. Um por AC (rastreabilidade spec→teste).
import { test } from "node:test";
import assert from "node:assert/strict";
import { submitFeedback } from "./feedback.mjs";

test("AC-1: feedback válido é aceito e retorna id", () => {
  const r = submitFeedback({ text: "ótimo produto", context: "/home" });
  assert.ok(r.id, "deveria retornar um id");
});

test("AC-2: feedback vazio é rejeitado", () => {
  const r = submitFeedback({ text: "   " });
  assert.ok(r.error, "deveria retornar erro");
});

test("AC-3: feedback acima do limite é rejeitado", () => {
  const r = submitFeedback({ text: "x".repeat(1001) });
  assert.ok(r.error, "deveria retornar erro");
});
