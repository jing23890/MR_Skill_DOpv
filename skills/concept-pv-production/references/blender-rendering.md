# Scripted Blender rendering

Read for scene construction, camera animation, Cycles setup, or rendering failures. Resolve exact APIs against the installed Blender version; these notes are not a version-independent API contract.

## Scene construction

- Prefer `bpy.data` and direct properties for repeatable scene edits. Operators depend on selection, mode and context; set these explicitly when using them.
- Use named collections and parent transforms for assemblies. Geometry, materials, lights and shot cameras should remain separately editable.
- A clean dedicated background process is convenient for new scenes. When modifying a user's project, work on a versioned copy and scope edits to the intended objects.
- Discover nodes by type or stable identifiers rather than assuming English display names. A saved scene and a new node may have different localized names.
- Blender APIs change. In the worked Blender 5.1.2 project, Glare settings were input sockets and the scene used a compositor node group. Older examples using `glare_type` did not work. Inspect RNA and socket names before adapting examples.

## Camera and timing

Choose an explicit image-up direction for unusual camera axes. A tracking quaternion may roll unexpectedly near its up-axis singularity. For a forward vector `f` and chosen world-up `u`, compute `r = normalize(f × u)` and `v = r × f`; the camera rotation matrix has columns `(r, v, -f)`. If `f` is nearly parallel to `u`, choose another up vector before computing the basis.

Hard cuts and large angle changes can expose Euler discontinuities or Bezier overshoot. Use separate shot cameras, appropriate rotation interpolation, or bake camera transforms at each rendered frame. Check both sides of every cut and an intermediate frame of long moves. Do not repair a camera bug solely by repositioning the final image.

Keep a single frame mapping between Blender and the compositor. A 10-second film at 24 fps has 240 frames: Blender 1–240, compositor indices 0–239, time 0–239/24 seconds. A held final image still occupies its final frame duration.

## Rendering policy

Pick the engine for the result. Cycles is suitable for traced reflection, transmission and indirect illumination. Eevee can suit fast stylized rendering. State the actual renderer rather than promising “ray tracing” from appearance alone.

Inspect GPU availability and enable a supported backend. Do not assume NVIDIA/OptiX on every host. Preserve usable CPU or other supported device options. Check logs for silent CPU fallback, device errors and memory exhaustion.

Use adaptive sampling and a denoiser appropriate to the shot. Test textured metal, transparent surfaces, motion and dark regions for residual noise or temporal shimmer. Sample counts are quality controls, not style controls. The worked lighting revision used 128 maximum / 32 minimum adaptive samples with a 0.025 threshold; these are example settings, not a guarantee or universal preset.

Persistent render data can reduce repeated scene setup, at a memory cost. In the worked project, moving denoising to OptiX and retaining render data greatly reduced frame time. Benchmark representative frames on the actual machine before estimating total time.

Use PNG for a simple display-referred delivery chain. Use linear EXR and relevant passes for substantial compositing. Record the view transform, exposure and color space. Avoid baking a display transform and then applying it again downstream.

## Resume safely

Render each version into its own directory. Track the shot, frame range and render configuration together; a filename's presence alone does not prove it belongs to the current version or is complete.

Use a completed render process or a manifest/atomic rename to commit frames. File modification time alone is insufficient: a reader can observe a half-written PNG. In the worked production, concurrent encoding initially encountered a broken PNG while Blender was writing it. A public workflow should default to encoding completed sequences rather than copying that fragile synchronization pattern.

Identify a job by its owned process ID or exact task identity before interrupting it. Preserve completed valid frames and source files. Never stop all Blender processes to restart one render.

Primary references: [Blender Python API](https://docs.blender.org/api/current/), [Blender Manual](https://docs.blender.org/manual/en/latest/).
