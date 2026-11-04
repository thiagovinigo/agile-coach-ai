# Observability

High-level view of your agent activity - session counts, cost tracking, error rates, and usage trends.

## Overview

The dashboard gives you two levels of visibility into your agents. This page covers the high-level metrics. For drilling into individual sessions and conversation turns, see [Logs](/an/docs/deploy/logs).

## Dashboard layout

The overview chart at the top shows sessions and dialogs over time - toggle between the two views. Below it, three metric cards track cost, duration, and errors.

- **Cost** - Total USD spend over the selected period.
- **Duration** - Average execution time per dialog.
- **Errors** - Error rate (%) and absolute count. Recent errors are listed below the cards.

## Date range filtering

All metrics can be filtered by date range: 1h, 24h, 7d, 30d, or a custom range. Granularity auto-adjusts (hourly for short ranges, daily for longer ones).

## Live monitoring

When any dialog is actively streaming, a pulsing blue **Live** indicator appears next to the date picker. The dashboard auto-refreshes while streams are active.

## Debugging tips

- **Recent errors** - scroll below the metric cards to see the latest errors with timestamps
- **Cost spikes** - switch between date ranges to narrow down when costs jumped, then drill into [Logs](/an/docs/deploy/logs)
- **Slow responses** - check the Duration card, then replay slow dialogs in Logs