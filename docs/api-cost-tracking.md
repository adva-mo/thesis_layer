# API Cost Tracking

After every paid API call, append one line to `output/history/costs`.

## Triggers

- `vo_combined.py --confirm-paid-api-call` → ElevenLabs
- `vo.py --confirm-paid-api-call` → ElevenLabs
- `kling_batch.py --confirm-paid-api-call` → fal.ai
- `kling.py --confirm-paid-api-call` → fal.ai

## Pricing

- ElevenLabs: $0.10 per 1,000 characters
- Kling v1 Standard: $0.22 / 5s clip
- Kling 2.5 Turbo: $0.35 / 5s clip
- Kling 3.0 Pro: $0.56 / 5s clip

## Line Format

```
DD/MM/YYYY - [project-slug] [reel context] - $X.XX [provider] ([details])
```

## Examples

```
22/6/2026 - binghatti-skyhall reel_01 - 0.04 11labs (399 chars, 3 calls)
22/6/2026 - binghatti-skyhall reel_01 - 1.10 fal (3 clips: 5s+10s+10s, 1 reuse free)
```

Calculate costs from the call output (chars sent, clip durations, model used). Do not leave TBD — compute and write before moving on.
