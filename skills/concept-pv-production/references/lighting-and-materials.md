# Lighting and material revisions

Read when the result looks flat, plastic, overly bright, or when the user requests ray tracing or alternating light and shadow.

## Diagnose the image before changing settings

Confirm the actual engine and current render settings. A path-traced image can still look poor. Broad frontal illumination, large emissive surfaces, weak roughness separation, missing edge detail and excessive bloom can remove depth even with many samples.

Separate the likely causes:

| Symptom | Inspect first |
|---|---|
| Everything has the same brightness | Light placement, fill level, environment strength, emissive contribution |
| Metal looks plastic | Metalness, roughness, reflected source shapes, normals and bevel scale |
| Core is a white patch | Emission energy, exposure, view transform and bloom; do not merely recolor the white patch |
| Dark areas crawl during motion | Sampling, denoising consistency, fine texture frequency and temporal preview |
| Detail looks like orange peel | Bump distance/strength and texture scale relative to the model |

## Design a light sequence

Give the light a job in each shot: reveal a silhouette, describe the material, expose internal structure, withhold information, or punctuate ignition. A possible progression is narrow rim → moving reflection → dark pause → internal activation → readable hero hold. Adapt it to the subject; cold blue and amber are not required.

For true moving shadows, animate a light or a physical occluder. For moving specular highlights, animate a shaped source relative to the object. Document any deliberate camera-ray visibility tricks. A full-screen brightness multiplier or color overlay is a grading effect, not geometric relighting.

Use distinct key, rim and minimal fill roles. Narrow rectangular sources can create readable reflections on machined surfaces. Do not remove all fill if it destroys the intended silhouette or makes critical details invisible at normal playback size.

Animate intensity handoffs with purposeful timing. Keep dark intervals readable, and avoid arbitrary high-frequency flashing. Evaluate the animation at delivery speed: attractive isolated stills can hide distracting flicker or inconsistent reflections.

## Material hierarchy

Separate dark structural metal, brighter machined edges, recesses, indicators and optical elements. Adjust roughness and source shape together. Keep bevels and micro-normal variation proportional to object scale.

A transmissive shell around a smaller emissive source can retain more shape than making the entire core a strong emitter. Test actual glass depth and internal visibility; transmission settings alone do not guarantee convincing refraction. Thin glowing accents often need less energy than expected once bloom is added.

## Review a representative set

Inspect a lit frame, a dark frame, a handoff midpoint and an activation frame at the same display transform. Compare old and new versions at matching camera/time. Keep the approved camera/edit when the request concerns lighting unless another defect requires changing it.

Judge material readability and narrative contrast, not just average brightness or sample count. Then render a short moving segment to inspect noise, reflection movement and light transitions before committing the full revision.
