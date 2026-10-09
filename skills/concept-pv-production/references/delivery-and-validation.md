# Delivery and validation

## Before encoding

Confirm contiguous frames from the same render version, a fixed frame rate and expected dimensions. Do not infer success from process exit alone: some render tools can report a script error in their log without a useful failing exit code.

For fractional rates, store the rate as a rational value such as `24000/1001`. Duration equals frame count divided by frame rate. Do not round that rate or silently duplicate/drop frames to match an approximate duration.

Check text at playback scale; inspect clipping, safe margins, label collisions and transitions. Inspect beginning, ending, both sides of cuts, extremes of motion, and lighting handoffs. A contact sheet supports this review but does not replace watching motion.

## Sound

Choose licensed, user-provided, original recorded or procedurally synthesized audio. Keep provenance with the project. Avoid presenting arbitrary oscillators and noise as a finished music score; audition the result when playback is available.

Align transients with meaningful visual events. Check peaks, fades, discontinuities, duration and channel layout. Numerical checks can detect clipping and length errors but cannot establish musical quality.

## Portable encoder

Requirements: Python 3.10+ and a working FFmpeg executable with the `libx264` encoder. No Python packages are required by the helper.

```sh
python scripts/encode_sequence.py --frames-dir ./renders/final \
  --pattern core_%04d.png --start-number 1 --frames 240 --fps 24 \
  --audio ./audio/mix.wav --output ./delivery/concept.mp4
```

Use `--ffmpeg` with a discovered executable path if it is not on PATH. Use `--overwrite` only for an intentionally replaced deliverable. The encoder pads short audio with silence and trims audio to the video duration; this is a technical fallback, not a substitute for composing an ending.

The helper checks the frame sequence, encodes to a temporary MP4, fully decodes it to verify the video frame count, then publishes the local output and validation JSON. It does not assess visual quality, validate every color-management assumption or listen to the soundtrack.

## Export QA

- Fully decode the exported file and inspect errors.
- Verify resolution, rate, duration, codec and intended audio track with available media tools; distinguish declared metadata from measured decode results.
- Inspect frames extracted from the export and watch the encoded clip when possible. Watch for frame jumps, frozen segments, denoising shimmer and alpha/color differences.
- Clearly report any inability to audition or play the file; do not claim full playback review from still images alone.

Deliver the final video, editable scene/composition, source scripts, a brief reproduction note and key limitations. Keep full-resolution renders separate from the source package when they would make sharing impractical.

## Preparing a public package

Remove machine-specific paths, usernames, credentials, private reference URLs and account identifiers. Do not bundle proprietary fonts, application installations, downloaded dependencies or third-party assets without redistribution rights. License the authored package separately from external software and assets. Publishing to a remote account is a separate action from preparing local release files.
