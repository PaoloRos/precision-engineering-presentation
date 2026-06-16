# TTS Audio with ElevenLabs

This file explains how to generate the presentation audio from
`presentation-tts-script.md` using the ElevenLabs API.

## Project Data

- Source script: `presentation-tts-script.md`
- Base output: `audio/presentation.mp3`
- Recommended output: `audio/presentation_normalized.mp3`
- Selected ElevenLabs voice ID: `Gfpl8Yo74Is0W6cPUWWT`
- Fallback API example voice ID: `JBFqnCBsd6RMkjVDRZzb`
- Recommended model: `eleven_multilingual_v2`
- Recommended format: `mp3_44100_128`
- Expected duration: about 13:30-14:30 minutes

The TTS file contains about 1863 words and 12820 characters. Since
`eleven_multilingual_v2` supports about 10000 characters per single TTS request,
the script must split the text into multiple parts and then merge the MP3 files.
The generation script uses two pause levels before sending each chunk to
ElevenLabs: a moderate pause between slide paragraphs and a stronger pause
around section transition paragraphs.

## Relevant API Information

ElevenLabs endpoint for speech generation:

```text
POST https://api.elevenlabs.io/v1/text-to-speech/:voice_id
```

Required headers:

```text
xi-api-key: $ELEVENLABS_API_KEY
Content-Type: application/json
```

Recommended query parameter:

```text
output_format=mp3_44100_128
```

Minimum body:

```json
{
  "text": "Text to synthesize",
  "model_id": "eleven_multilingual_v2"
}
```

For this project, use:

```text
selected voice_id = Gfpl8Yo74Is0W6cPUWWT
fallback voice_id = JBFqnCBsd6RMkjVDRZzb
model_id = eleven_multilingual_v2
output_format = mp3_44100_128
voice speed = 1.12
```

## Voice Direction

The voice must be used for a technical presentation in English:

- formal, clear, engineering-oriented tone;
- measured but not slow pace;
- native ElevenLabs voice speed set to `1.12`;
- natural pauses between paragraphs;
- slightly longer pause when moving from the design section to the calibration section;
- do not rewrite, translate, summarize, or omit any part of the text.

Pronunciations to preserve:

- `Q F D`: written with spaces in the TTS script so it is read as three separate letters;
- `Triz`: written this way in the TTS script so it is read as one word, not as `T-R-I-Z`;
- `LIF sensors`: read as `L-I-F sensors`;
- ratios such as `one to twenty`: read naturally;
- decimals such as `zero point seven percent`: read clearly.

## Python Script

Use the repository script `generate_audio.py`. It reads `presentation-tts-script.md`,
loads the API key from `.env`, splits the text into chunks below the API
character limit, keeps moderate pauses between slides and stronger pauses at
section transitions, writes one MP3 part per chunk, merges the parts into
`audio/presentation.mp3`, and creates a loudness-normalized version at
`audio/presentation_normalized.mp3`.

The speaking pace is controlled directly in the ElevenLabs request through:

```python
"speed": 1.12
```

This is different from post-processing with `ffmpeg atempo`: the voice is
generated faster by ElevenLabs itself, which should sound more natural than
speeding up an already-generated MP3.

The final loudness is normalized with `ffmpeg loudnorm` so that the perceived
volume is more consistent:

```text
loudnorm=I=-16:TP=-1.5:LRA=11
```

By default it uses the selected voice `Gfpl8Yo74Is0W6cPUWWT`. To override it
temporarily, set:

```bash
export ELEVENLABS_VOICE_ID="VOICE_ID_TO_USE"
```

To generate a low-credit sample instead of the full presentation, set the number
of initial paragraphs and a dedicated output folder:

```bash
ELEVENLABS_VOICE_ID="Gfpl8Yo74Is0W6cPUWWT" \
ELEVENLABS_VOICE_SPEED=1.0 \
ELEVENLABS_SAMPLE_PARAGRAPHS=4 \
ELEVENLABS_OUTPUT_DIR="audio/sample_gfpl_speed1" \
ELEVENLABS_OUTPUT_FILE="sample_first4.mp3" \
python3 generate_audio.py
```

## Terminal Steps

1. Enter the project folder:

```bash
cd /Users/paolorossi/Develop/dev_universita/precision-engineering-presentation
```

2. Export your ElevenLabs API key:

```bash
export ELEVENLABS_API_KEY="INSERT_YOUR_API_KEY"
```

3. Check that `ffmpeg` is available:

```bash
ffmpeg -version
```

If it is not installed, install it before merging the MP3 parts. On macOS, if
you use Homebrew:

```bash
brew install ffmpeg
```

4. Run the script:

```bash
python3 generate_audio.py
```

5. Check the generated file:

```bash
ls -lh audio/presentation.mp3 audio/presentation_normalized.mp3
```

6. Listen to the audio and verify:

- duration around 14 minutes;
- consistent perceived loudness in `audio/presentation_normalized.mp3`;
- correct voice;
- pronunciation of `Q F D`, `Triz`, and `LIF`;
- no skipped or truncated section;
- transition to the calibration section is not too rushed.

## Operational Notes

- Never put the API key in Git or directly inside the script: always use the
  `ELEVENLABS_API_KEY` environment variable.
- If the audio is too fast, regenerate it with stronger textual pauses in the
  TTS file, for example by adding blank lines between main sections.
- If ElevenLabs returns a character limit error, lower `MAX_CHARS` to `7000`.
- If you want to regenerate only one part, temporarily modify the script to call
  `synthesize_chunk` only on the relevant chunk.

## ElevenLabs Sources

- API dashboard: https://elevenlabs.io/app/api
- Text to Speech API: https://elevenlabs.io/docs/api-reference/text-to-speech/convert
- Authentication: https://elevenlabs.io/docs/api-reference/authentication
- Models and character limits: https://elevenlabs.io/docs/overview/models
