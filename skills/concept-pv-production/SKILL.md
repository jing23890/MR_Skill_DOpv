---
name: concept-pv-production
description: Create or revise concept trailers, promotional videos (PVs), and motion-design films using scripted 3D rendering and code-driven compositing. Use for original visual concepts, shot planning, procedural scenes, lighting revisions, motion graphics, and video delivery; especially when the user wants AI to author editable scenes and code rather than generate video pixels.
---

# Concept PV Production

Produce a watchable film and editable source, not only a storyboard, browser animation, or rendering script. Use AI to author scenes, animation, graphics and orchestration. Follow the user's chosen visual medium; this workflow defaults to deterministic rendering rather than generative images/video.

## Decide the visual idea before the stack

Extract the subject, message, emotional progression, reference traits, duration, aspect ratio and audio intent from the request. For a loosely specified sample, choose and state a concrete concept, then proceed. Ask only when missing information materially blocks the work.

Observe actual reference frames before describing their visual content, and multiple moments before describing motion. If access fails, explain the limitation and separate original design suggestions from observations. Do not claim to have watched a reference from its title or thumbnail.

Write a compact shot plan: time range, narrative purpose, dominant visual, camera/graphic motion, lighting change, sound cue and implementation owner. Use [the shot-plan example](assets/shot-plan.example.json) as an adaptable starting point. Treat brand, palette, industrial styling and shot count as choices, not defaults.

A PV needs progression and visual transformation. A rotating model with labels is a product showcase unless that is the user's intent. Consider changes in scale, abstraction, negative space, typography, environment and sound. Do not equate “technical” with more HUD elements, bloom or random glitch.

## Assign tools to shots and layers

Choose the smallest stack that can deliver the intended visual language. Explain meaningful simplifications. User-requested tools take precedence over these defaults.

| Need | Candidate | Decision |
|---|---|---|
| Hero objects, procedural structures, close-up materials, traced reflections | Blender + Python | A strong 3D source renderer; not automatically the complete PV pipeline |
| Kinetic typography, graphic transitions, parameterized edits, unified video timeline | Remotion | Preferred candidate when code-driven motion graphics are a substantial part of the film |
| Abstract particles, points, wireframes, shader fields in a code timeline | Three.js / React Three Fiber in Remotion | Frame-addressable rendering; do not assume it matches a path tracer's material output |
| Detailed layer compositing, optical treatments, artist-editable finishing | After Effects | Script repetitive assembly; retain editable compositions |
| Environments, existing Unreal assets, Niagara, fast cinematic iteration | Unreal Engine | Use Sequencer and Movie Render Pipeline where those capabilities justify the handoff |
| Simple annotations, raster operations, contact sheets | Pillow or equivalent | Efficient support tool; do not silently substitute it for complex motion design |
| Encoding, decoding checks and audio muxing | FFmpeg | Delivery stage, not the creative design engine |

Read [compositing-and-handoffs.md](references/compositing-and-handoffs.md) only for the relevant integration. This package's worked production path was Blender → PNG → Pillow → FFmpeg. The other paths are design guidance, not bundled or validated integrations.

## Build and iterate

1. Inspect the relevant installed tools, versions, GPU and existing project instructions. Use project-local dependencies where practical. Do not install every candidate application. Discover executables and fonts; never copy a previous machine's paths into reusable code.
2. Create a project manifest with duration, rational frame rate, dimensions, frame numbering, audio format and output paths. Keep one time convention: zero-based video frame `i` maps to time `i / fps`; Blender can use scene frame `i + 1`.
3. Establish a few style frames and a low-cost motion preview. Inspect them yourself before expensive rendering. Ask for artistic approval only when the user requests that checkpoint or a consequential decision remains unresolved; do not add a mandatory approval gate.
4. Separate scene generation, motion, lighting, graphics and delivery code so revisions affect the relevant layer. Keep a prior deliverable when making a new version.
5. Render selected final-quality frames, including dark and bright lighting states. A script finishing without error is not evidence that the frame looks right.
6. Render shots independently and cache completed outputs. Re-render changed shots or layers, not the entire project by default. For streamed rendering, consume only committed frames; otherwise finish the sequence before encoding.

For Blender, read [blender-rendering.md](references/blender-rendering.md). For lighting/material feedback or requests for “ray tracing,” read [lighting-and-materials.md](references/lighting-and-materials.md).

## Finish and inspect

Follow [delivery-and-validation.md](references/delivery-and-validation.md). Verify narrative timing, typography, transitions, lighting continuity, audio, frame count and complete video decoding. Inspect the exported file, not just the source frames. Watch the export where playback is available; report any inspection limitations accurately.

For a completed PNG sequence, `scripts/encode_sequence.py` provides a portable FFmpeg encoder with contiguous-frame checks, optional audio, temporary output, full decode validation and a JSON report. Run `--help` for parameters. It is intentionally a delivery utility, not a scene or compositor template.

Deliver the playable video, concise changes, editable project/source and any material limitations. Say which tools were actually used. Never present proposed integrations, optical fakes, or simple grading as completed path-traced effects.

## Reuse efficiently

- Read only the references relevant to the current phase.
- Store shot decisions, versions, seeds and render settings in files so another session can resume.
- Reuse components such as typography timing and frame exporters, not a single visual identity.
- Batch independent inspections; use narrow previews before full renders.
- Prefer supported scripting interfaces and saved source over repeated GUI manipulation.
- If a render fails, inspect its log and change the cause before retrying. Resume from verified frames; do not overwrite unrelated files or stop other projects' processes.
- Public packages should contain authored workflow/source and explicit licenses, not vendor binaries, proprietary fonts, access tokens, local paths, or unlicensed reference media.
