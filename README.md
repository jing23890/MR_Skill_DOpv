# Concept PV Production

[中文说明](README.zh-CN.md)

An agent skill for making **editable concept films through code, 3D rendering and compositing**. AI authors the production logic; the scene renderer and compositor produce the frames. It does not require generative video or image services.

The skill covers shot planning, tool selection, procedural scenes, cinematic lighting, motion graphics, sound, sequence rendering and verified video delivery. It emphasizes visual progression over decorating a rotating model with HUD labels.

## What has actually been exercised

- A 10-second, 1920×1080, 24 fps film: Blender Python → Cycles/OptiX → 240 PNG frames → Pillow graphics → FFmpeg H.264/AAC.
- A lighting revision: moving narrow area lights, cold/warm handoffs, physical shadow shutters, a transmissive core and a separate internal emitter.
- The originating project used Blender 5.1.2 on Windows with an NVIDIA GPU. This is evidence for that workflow, not a compatibility claim for every operating system or application version.
- Remotion/Three.js, After Effects and Unreal Engine are documented as optional tool routes. Their integrations are **not shipped or end-to-end tested** by this package.

The example film, fonts, application binaries and downloaded dependencies are not bundled. The skill is a reusable workflow, not the original scene preset.

## Install

Copy the folder `skills/concept-pv-production` into your agent's skill directory. For Codex, the default location is `~/.codex/skills/concept-pv-production` (or `$CODEX_HOME/skills/concept-pv-production` when customized). Other Agent Skills-compatible tools may use a different location; follow their documentation.

The optional `agents/openai.yaml` provides Codex UI metadata. No MCP server or account connection is required by the skill itself.

## Invoke

```text
Use $concept-pv-production to make a 10-second concept PV for an original
orbital observatory. Use rendered scenes and code-driven graphics, not generated
video. Give the film a visual progression, an original sound bed, and editable sources.
```

```text
Use $concept-pv-production to revise this film's lighting. Preserve the camera
edit, alternate narrow cold and warm light, and improve metal reflections.
```

```text
Use $concept-pv-production for a typography-led PV. Make Remotion the timeline
owner and use Blender only for two hero shots. Test the export handoff early.
```

## Contents

```text
skills/concept-pv-production/
  SKILL.md
  agents/openai.yaml
  references/
    blender-rendering.md
    lighting-and-materials.md
    compositing-and-handoffs.md
    delivery-and-validation.md
  assets/shot-plan.example.json
  scripts/encode_sequence.py
```

The entrypoint routes to relevant references instead of loading every application's instructions. Tool choice and render settings are contextual; no single visual style or application stack is mandatory.

## Encoder

Requires Python 3.10+ and FFmpeg with `libx264`. The Python script uses only the standard library.

```sh
python skills/concept-pv-production/scripts/encode_sequence.py \
  --frames-dir ./renders/final --pattern core_%04d.png \
  --start-number 1 --frames 240 --fps 24 \
  --audio ./audio/mix.wav --output ./delivery/concept.mp4
```

It checks contiguous PNG headers/dimensions, encodes to a temporary file, fully decodes the output and verifies frame count, then writes the MP4 and a validation report. It refuses existing destinations unless `--overwrite` is passed. Short audio is padded; long audio is trimmed. Complete rendering before using this utility.

Run `--help` for all options. Validation reports distinguish measured frame count from configured rate and expected duration; they are not claims of artistic review.

## Contributing

Run the encoder checks with `python -m unittest discover -s tests -v`. Set the `FFMPEG` environment variable if necessary. The eight end-to-end cases cover fractional frame rates, audio inclusion, missing/corrupt frames, inconsistent dimensions, destination protection, explicit overwrite and pattern containment. Fixtures are generated with the Python standard library and leave no media in the repository. Tests are skipped when FFmpeg is unavailable; a skipped run is not a validation result.

Prefer a small reproducible case and the exact application version over broad “always use this tool” rules. For new integrations, provide a short exported film and explain what was actually tested. Keep examples portable and do not add private paths, credentials, bundled proprietary fonts or unlicensed reference media. Run changed helper scripts, not only a Markdown/frontmatter validator.

Upstream documentation is linked in the relevant references. This project is independent and is not affiliated with Blender, Remotion, Adobe, Epic Games or OpenAI. The MIT license covers the authored package; external applications and assets keep their own licenses.

## License

[MIT](LICENSE).
