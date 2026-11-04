#!/usr/bin/env python3
"""
jev_gate.py — Hook PreToolUse para Claude Code usando Jev (Sistema 1)
Avalia comandos Bash em ~150ms e retorna permissionDecision: allow | ask | deny.
"""
import json
import os
import sys
import urllib.request

TYPESAFE_API_KEY = os.environ.get("TYPESAFE_API_KEY", "")
ENDPOINT = "https://api.typesafe.ai/v1/systemone"


def decide_with_jev(command: str, cwd: str) -> dict:
    payload = {
        "model": "jev-latest",
        "context": f"CWD: {cwd}\nBash Command: {command}",
        "decisions": [
            {
                "name": "decision",
                "type": "choice",
                "prompt": (
                    "Classifique este comando de terminal executado por um agente de IA: "
                    "'allow' para leitura/testes/git seguro; "
                    "'ask' para alterações de estado, instalações ou rede; "
                    "'deny' para exclusão destrutiva, force push em main/master ou vazamento de segredos."
                ),
                "options": ["allow", "ask", "deny"],
            },
            {
                "name": "risk",
                "type": "score",
                "prompt": "Nível de risco operacional de 0.0 (inofensivo) a 1.0 (catastrófico).",
            },
            {
                "name": "target",
                "type": "noul",
                "prompt": "Qual recurso, arquivo ou banco principal é afetado pelo comando?",
            },
        ],
    }

    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {TYPESAFE_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=2.5) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data.get("results", {})


def main():
    raw = sys.stdin.read()
    if not raw.strip():
        sys.exit(0)

    event = json.loads(raw)
    tool_name = event.get("tool_name", "")
    tool_input = event.get("tool_input", {})
    command = tool_input.get("command", "")
    cwd = event.get("cwd", "")

    if tool_name != "Bash" or not command or not TYPESAFE_API_KEY:
        sys.exit(0)

    try:
        res = decide_with_jev(command, cwd)
        decision = res.get("decision", "ask")
        risk = float(res.get("risk", 0.5))
        target = res.get("target") or "ambiente local"

        # Regra adicional por score: se risco > 0.85, força deny; se > 0.55 e era allow, sobe para ask
        if risk >= 0.85:
            decision = "deny"
        elif risk >= 0.55 and decision == "allow":
            decision = "ask"

        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": decision,
                "permissionDecisionReason": f"[Jev Sistema 1] decision={decision} | risk={risk:.2f} | target={target}",
            }
        }
        print(json.dumps(output))
    except Exception as e:
        # Fail-safe: em caso de timeout de rede, delega ao prompt padrão do Claude Code
        fallback = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": f"[Jev Fallback] {e}",
            }
        }
        print(json.dumps(fallback))


if __name__ == "__main__":
    main()
