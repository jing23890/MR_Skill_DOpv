# Compositing and tool handoffs

Read only the section relevant to the chosen stack. The Blender/Pillow/FFmpeg path was exercised in the originating sample. Remotion, Three.js, AE and UE are optional architecture guidance here; this package does not ship their integrations. Check their current official documentation and locally installed versions before implementation.

## Shared contract

Assign one owner to the edit timeline and one renderer to each layer. Record frame rate, frame origin, dimensions, shot range, alpha convention, color space, view transform and audio start. Avoid importing the same display transform twice or mixing premultiplied and straight alpha unintentionally.

Use a full raster shot when no downstream separation is needed. For deeper compositing, export appropriate layers such as beauty, emission, depth and object masks; use linear EXR where necessary. Decide the actual downstream use before exporting every pass. Confirm the receiving tool supports the chosen EXR channels and alpha interpretation.

## Blender → simple raster composition → FFmpeg

Suitable for a short 3D-led proof of concept with restrained graphics. Draw frame-addressable annotations or contact sheets with Pillow or an equivalent library. Keep text, spacing and motion configurable.

Limit: simple per-frame drawing is not a substitute for a designed motion-graphics system. If typography, masking, transitions or graphic transformations drive the film, choose a richer compositor and explain the choice. A model turntable with data labels should not silently become the answer to a broad concept-PV brief.

## Remotion + Three.js / React Three Fiber

Use Remotion as the timing owner for code-driven graphics and typography. Bring Blender footage into that timeline. Use Three.js/R3F for abstract geometric scenes, wireframes, particles or shaders where they improve the concept rather than recreating every Blender shot.

All animation must be addressable by the requested frame. Derive state from the timeline, fix random seeds, and bake history-dependent simulations. Wall-clock time, requestAnimationFrame accumulation and unseeded randomness can disagree between preview and offline rendering. Use the integration's supported frame hooks and canvas components.

Check media/font readiness, alpha export, render backend and shader support in the actual renderer. A successful interactive browser preview is not proof that offline export works. Test a short encoded sequence before building a long composition.

Primary references: [Remotion Three integration](https://www.remotion.dev/docs/three), [official Remotion skills](https://www.remotion.dev/docs/ai/skills). Install or load an upstream skill only if the current task needs it; do not copy an entire library into this skill.

## After Effects

Use AE when layered compositing and editable finishing are valuable. Scripts can assemble compositions, import footage, create layers and keyframes, and automate repeated operations. Expressions can drive supported properties. Verify automation behavior and installed effects against the local AE version.

Keep a saved project and organized assets. Expose meaningful controls rather than generating hundreds of opaque layers. Verify render queue settings, working color space, frame rate, motion blur and alpha interpretation. Do not introduce unlicensed third-party effects as hidden requirements.

Primary reference: [Adobe scripting documentation](https://helpx.adobe.com/after-effects/desktop/automate-in-after-effects/automate-animation/scripts.html).

## Unreal Engine

Use UE for environments, existing project assets, Niagara or cinematic iteration that materially benefit the film. Render through the supported Movie Render Pipeline workflow for the installed version.

Inspect Sequencer timing, temporal sampling, motion blur, warm-up and deterministic simulation behavior. Verify particles, streaming, exposure and transparent elements in the actual output. A viewport capture is not equivalent to the final render. Choose the renderer and features supported by the project; do not label all UE output as path traced.

Primary reference: [Epic Movie Render Pipeline documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/movie-render-pipeline-in-unreal-engine).
