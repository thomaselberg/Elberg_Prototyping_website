# Clap Detection Improvement

File: `Own project folders/Bio Lamp/s3_full_prototype/s3_full_prototype.ino`
Section: `loop()` function, starting around line 1099

---

## What is wrong with the current implementation

The main issue is that `CHUNK = 1600` samples = **100ms of audio**. A hand clap is a transient lasting ~10–20ms. When it lands in the middle of a 100ms window, its peak energy is diluted against 80ms of silence, so the peak threshold often fails to trigger.

Additionally, the double-clap requirement means two detections must succeed in sequence — if the first is missed due to chunk timing, the whole trigger fails.

---

## Changes to make

### 1. Reduce chunk size from 1600 to 128 samples (~8ms)

```cpp
// BEFORE
const size_t CHUNK = 1600;

// AFTER
const size_t CHUNK = 128;
```

A clap now fills most of the window instead of being averaged away. This is the single biggest fix.

---

### 2. Replace absolute thresholds with a crest factor check

The current condition `peak > 11000 && rms < 5000` uses hardcoded values that depend on microphone gain, distance, and room acoustics.

Replace with a **crest factor** (peak ÷ RMS). Claps have a very high crest factor (sharp spike vs silence). Voices and music have a low one (~2–4). This adapts automatically to any room.

```cpp
// BEFORE
if (peak > 11000 && rms < 5000) {

// AFTER
float crest = (rms > 80) ? (float)peak / (float)rms : 0.0f;
if (peak > 2500 && crest > 5.5f) {
```

Tune `peak > 2500` up if false positives occur, down if real claps are missed. `crest > 5.5f` can similarly be tuned — higher = stricter.

---

### 3. Keep double-clap detection but use the crest factor for each spike

The double-clap window (two qualifying spikes 200–800ms apart) is intentional — keep it. Only replace the spike-qualification condition from absolute thresholds to crest factor:

```cpp
// BEFORE
if (peak > 11000 && rms < 5000) {
    if (n - lastSpike > 150) {
        if (n - lastSpike >= 200 && n - lastSpike <= 800) {
            if (n - lastLegitTrigger > 1500) {
                clapDetectedTrigger = true;
                lastLegitTrigger = n;
            }
            lastSpike = 0;
        } else {
            lastSpike = n;
        }
    }
}

// AFTER — same double-clap window, crest factor replaces absolute thresholds
float crest = (rms > 80) ? (float)peak / (float)rms : 0.0f;
if (peak > 2500 && crest > 5.5f) {
    if (n - lastSpike > 150) {
        if (n - lastSpike >= 200 && n - lastSpike <= 800) {
            if (n - lastLegitTrigger > 1500) {
                clapDetectedTrigger = true;
                lastLegitTrigger = n;
            }
            lastSpike = 0;
        } else {
            lastSpike = n;
        }
    }
}
```

`lastSpike` stays — it is still needed for the two-clap timing window.

---

## Full replacement block for the loop() audio section

Replace everything from `// Poll Audio Rapidly for Claps!` down to the closing `}` of `loop()`:

```cpp
// Poll Audio Rapidly for Claps!
const size_t CHUNK = 128;
int16_t chunkBuffer[CHUNK];

size_t c_read = i2s.readBytes((char*)chunkBuffer, CHUNK * sizeof(int16_t));
if (c_read == CHUNK * sizeof(int16_t)) {
    int32_t peak = 0;
    int64_t sum_sq = 0;

    for (size_t i = 0; i < CHUNK; i++) {
        int32_t v = abs(chunkBuffer[i]);
        if (v > peak) peak = v;
        sum_sq += v * v;
    }
    int32_t rms = (int32_t)sqrt((double)sum_sq / CHUNK);

    static unsigned long lastSpike = 0;
    static unsigned long lastLegitTrigger = 0;
    unsigned long n = millis();

    float crest = (rms > 80) ? (float)peak / (float)rms : 0.0f;
    if (peak > 2500 && crest > 5.5f) {
        if (n - lastSpike > 150) {
            if (n - lastSpike >= 200 && n - lastSpike <= 800) {
                if (n - lastLegitTrigger > 1500) {
                    clapDetectedTrigger = true;
                    lastLegitTrigger = n;
                }
                lastSpike = 0;
            } else {
                lastSpike = n;
            }
        }
    }
} else {
    delay(1);
}
```

---

## Tuning guide after flashing

| Symptom | Adjustment |
|---|---|
| False triggers from speech/noise | Raise `peak > 2500` to `peak > 4000`, or raise crest factor to `> 7.0f` |
| Real claps not detected | Lower `peak > 2500` to `peak > 1500`, or lower crest factor to `> 4.0f` |
| Triggers too easily repeated | Raise cooldown from `1500` ms to `2000` ms |
| Occasional missed clap (boundary timing) | Reduce CHUNK further to `64` |

---

## Why this works better

| | Before | After |
|---|---|---|
| Chunk duration | 100ms | 8ms |
| Clap fills chunk | ~15% | ~100% |
| Threshold type | Absolute (room-dependent) | Ratio (self-adapting) |
| Claps required | 2 within 200–800ms | 2 within 200–800ms (unchanged) |
| False positive filter | `rms < 5000` (weak) | Crest factor (strong) |
