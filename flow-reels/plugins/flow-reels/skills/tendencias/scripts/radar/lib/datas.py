# -*- coding: utf-8 -*-
"""Datas do radar: a janela de busca e as conversoes entre formatos."""

from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple


def janela(dias: int = 30) -> Tuple[str, str]:
    """Devolve (de, ate) em AAAA-MM-DD para os ultimos `dias` dias."""
    hoje = datetime.now(timezone.utc).date()
    return (hoje - timedelta(days=dias)).isoformat(), hoje.isoformat()


def de_iso(valor: Optional[str]) -> Optional[str]:
    """'2026-05-20T18:48:31+00:00' vira '2026-05-20'. None se nao der."""
    if not valor:
        return None
    try:
        return datetime.fromisoformat(valor.strip()).date().isoformat()
    except (ValueError, TypeError):
        return None


def iso_para_epoch(valor: Optional[str]) -> Optional[float]:
    if not valor:
        return None
    try:
        dt = datetime.fromisoformat(valor.strip())
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.timestamp()
    except (ValueError, TypeError):
        return None


def de_epoch(ts) -> Optional[str]:
    if ts is None:
        return None
    try:
        return datetime.fromtimestamp(float(ts), tz=timezone.utc).date().isoformat()
    except (ValueError, TypeError, OSError):
        return None


def para_epoch(data: str) -> int:
    """'AAAA-MM-DD' vira o epoch do comeco do dia em UTC."""
    ano, mes, dia = (int(p) for p in data.split("-"))
    return int(datetime(ano, mes, dia, tzinfo=timezone.utc).timestamp())


def confianca(data: Optional[str], de: str, ate: str) -> str:
    """'alta' quando a data cai dentro da janela, 'baixa' no resto."""
    if not data:
        return "baixa"
    return "alta" if de <= data <= ate else "baixa"


def dias_atras(data: Optional[str]) -> Optional[int]:
    if not data:
        return None
    try:
        dt = datetime.strptime(data, "%Y-%m-%d").date()
    except ValueError:
        return None
    return (datetime.now(timezone.utc).date() - dt).days


def nota_de_recencia(data: Optional[str], janela_dias: int = 30) -> int:
    """0 a 100: hoje vale 100, o ultimo dia da janela vale 0."""
    idade = dias_atras(data)
    if idade is None:
        return 0
    if idade < 0:
        return 100
    if idade >= janela_dias:
        return 0
    return int(100 * (1 - idade / janela_dias))


def periodo_reddit(dias: int) -> str:
    """O parametro t= do Reddit que cobre a janela pedida, sem ficar curto."""
    if dias <= 1:
        return "day"
    if dias <= 7:
        return "week"
    if dias <= 31:
        return "month"
    return "year"
