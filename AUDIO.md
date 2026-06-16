# TTS Audio with ElevenLabs

This file explains how to generate the presentation audio from
`presentation-tts-script.md` using the ElevenLabs API.

## Project Data

- Source script: `presentation-tts-script.md`
- Recommended output: `audio/presentation.mp3`
- Current default API voice ID: `JBFqnCBsd6RMkjVDRZzb`
- Preferred paid/library voice ID after account upgrade: `Gfpl8Yo74Is0W6cPUWWT`
- Recommended model: `eleven_multilingual_v2`
- Recommended format: `mp3_44100_128`
- Expected duration: about 13:30-14:30 minutes

The TTS file contains about 1873 words and 12893 characters. Since
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
default voice_id = JBFqnCBsd6RMkjVDRZzb
paid/library voice_id = Gfpl8Yo74Is0W6cPUWWT
model_id = eleven_multilingual_v2
output_format = mp3_44100_128
```

## Voice Direction

The voice must be used for a technical presentation in English:

- formal, clear, engineering-oriented tone;
- measured pace, not theatrical;
- target pace of about 130-135 words per minute;
- natural pauses between paragraphs;
- slightly longer pause when moving from the design section to the calibration section;
- do not rewrite, translate, summarize, or omit any part of the text.

Pronunciations to preserve:

- `QFD`: read as `Q-F-D`;
- `TRIZ`: read clearly as `triz`;
- `LIF sensors`: read as `L-I-F sensors`;
- ratios such as `one to twenty`: read naturally;
- decimals such as `zero point seven percent`: read clearly.

## Python Script

Use the repository script `generate_audio.py`. It reads `presentation-tts-script.md`,
loads the API key from `.env`, splits the text into chunks below the API
character limit, keeps moderate pauses between slides and stronger pauses at
section transitions, writes one MP3 part per chunk, and merges the parts into
`audio/presentation.mp3`.

By default it uses the API-compatible voice `JBFqnCBsd6RMkjVDRZzb`. After
upgrading the account, force the preferred library voice with:

```bash
export ELEVENLABS_VOICE_ID="Gfpl8Yo74Is0W6cPUWWT"
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
ls -lh audio/presentation.mp3
```

6. Listen to the audio and verify:

- duration around 14 minutes;
- correct voice;
- pronunciation of `QFD`, `TRIZ`, and `LIF`;
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
