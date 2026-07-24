// Coletar feedback — implementação mínima (exemplo golden).
// Cobre AC-1 (aceita válido), AC-2 (rejeita vazio), AC-3 (rejeita acima do limite).

const MAX = 1000;
const store = [];

export function submitFeedback({ text, context } = {}) {
  if (!text || !text.trim()) return { error: "texto vazio" };          // AC-2
  if (text.length > MAX) return { error: "texto muito longo" };        // AC-3
  const id = String(store.length + 1);
  store.push({ id, text, context });                                    // AC-1
  return { id };
}

export const _store = store;
