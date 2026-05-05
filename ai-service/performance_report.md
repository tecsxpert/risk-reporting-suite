# Week 3 Day 2 — Performance Benchmark Report

## Endpoint Tested
GET /health

## Benchmark Results (50 requests)

- p50: 6.33 ms
- p95: 36.06 ms
- p99: 400.88 ms
- Average: 16.62 ms

## Optimisations Applied

- Implemented response caching
- Added async background processing
- Lightweight health monitoring endpoint
- Reduced blocking operations

## Observation

The endpoint performed efficiently under repeated requests.
Most responses completed within a few milliseconds.