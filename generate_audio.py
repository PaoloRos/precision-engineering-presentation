import hashlib
import json
import os
import subprocess
import textwrap
import urllib.error
import urllib.request
from pathlib import Path


PREFERRED_VOICE_ID = "Gfpl8Yo74Is0W6cPUWWT"
FALLBACK_API_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
MODEL_ID = "eleven_multilingual_v2"
OUTPUT_FORMAT = "mp3_44100_128"
DEFAULT_VOICE_SPEED = 1.12

INPUT_FILE = Path("presentation-tts-script.md")
MAX_CHARS = 9000
NORMALIZED_SUFFIX = "_normalized"
LOUDNESS_FILTER = "dynaudnorm=f=250:g=15:p=0.90:m=12:s=8,loudnorm=I=-16:TP=-1.5:LRA=7"
SLIDE_PAUSE_SEPARATOR = "\n\n"
SECTION_PAUSE_SEPARATOR = "\n\n\n\n"
SECTION_TRANSITION_PREFIXES = (
    "The first part concerns",
    "The next part introduces",
)


def load_env(path=Path(".env")):
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def get_api_key():
    load_env()
    api_key = os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("XI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing API key. Set ELEVENLABS_API_KEY in .env or in the shell."
        )
    return api_key


def get_json(api_key, url):
    request = urllib.request.Request(
        url,
        headers={"xi-api-key": api_key},
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"ElevenLabs API returned HTTP {error.code}: {details}"
        ) from error


def choose_available_voice(api_key):
    try:
        data = get_json(api_key, "https://api.elevenlabs.io/v1/voices")
        voices = data.get("voices", [])
        if voices:
            premade_voices = [
                voice for voice in voices if voice.get("category") == "premade"
            ]
            selected = premade_voices[0] if premade_voices else voices[0]
            name = selected.get("name", "Unnamed voice")
            voice_id = selected["voice_id"]
            print(f"Using fallback voice: {name} ({voice_id})")
            return voice_id
    except RuntimeError as error:
        print(f"Could not list voices with this API key: {error}")

    print(f"Using ElevenLabs API example voice: {FALLBACK_API_VOICE_ID}")
    return FALLBACK_API_VOICE_ID


def get_configured_voice_id():
    return os.environ.get("ELEVENLABS_VOICE_ID", PREFERRED_VOICE_ID)


def get_configured_voice_speed():
    return float(os.environ.get("ELEVENLABS_VOICE_SPEED", DEFAULT_VOICE_SPEED))


def get_output_dir():
    return Path(os.environ.get("ELEVENLABS_OUTPUT_DIR", "audio"))


def get_final_audio_path(output_dir):
    return output_dir / os.environ.get("ELEVENLABS_OUTPUT_FILE", "presentation.mp3")


def get_sample_paragraph_count():
    value = os.environ.get("ELEVENLABS_SAMPLE_PARAGRAPHS")
    return int(value) if value else None


def is_section_transition(paragraph):
    return paragraph.startswith(SECTION_TRANSITION_PREFIXES)


def pause_separator(previous_paragraph, next_paragraph):
    if is_section_transition(previous_paragraph) or is_section_transition(next_paragraph):
        return SECTION_PAUSE_SEPARATOR
    return SLIDE_PAUSE_SEPARATOR


def get_paragraphs(text):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    sample_count = get_sample_paragraph_count()
    if sample_count:
        paragraphs = paragraphs[:sample_count]
    return paragraphs


def split_text_by_paragraphs(text, max_chars):
    paragraphs = get_paragraphs(text)
    chunks = []
    current = ""
    previous_paragraph = ""

    for paragraph in paragraphs:
        separator = pause_separator(previous_paragraph, paragraph)
        candidate = (
            f"{current}{separator}{paragraph}".strip()
            if current
            else paragraph
        )
        if len(candidate) <= max_chars:
            current = candidate
            previous_paragraph = paragraph
            continue

        if current:
            chunks.append(current)
            current = ""

        if len(paragraph) <= max_chars:
            current = paragraph
        else:
            wrapped = textwrap.wrap(paragraph, width=max_chars)
            chunks.extend(wrapped[:-1])
            current = wrapped[-1]

        previous_paragraph = paragraph

    if current:
        chunks.append(current)

    return chunks


def synthesize_chunk(api_key, voice_id, voice_speed, text, output_path):
    url = (
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        f"?output_format={OUTPUT_FORMAT}"
    )
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "language_code": "en",
        "apply_text_normalization": "on",
        "voice_settings": {
            "stability": 0.55,
            "similarity_boost": 0.80,
            "style": 0.15,
            "speed": voice_speed,
            "use_speaker_boost": True,
        },
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            output_path.write_bytes(response.read())
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"ElevenLabs API returned HTTP {error.code}: {details}"
        ) from error


def synthesize_with_fallback(api_key, voice_id, voice_speed, text, output_path):
    try:
        synthesize_chunk(api_key, voice_id, voice_speed, text, output_path)
        return voice_id
    except RuntimeError as error:
        message = str(error)
        can_fallback = (
            "HTTP 402" in message
            and "paid_plan_required" in message
            and "ELEVENLABS_VOICE_ID" not in os.environ
        )
        if not can_fallback:
            raise

        print("Preferred voice is not available for this plan via API.")
        fallback_voice_id = choose_available_voice(api_key)
        synthesize_chunk(api_key, fallback_voice_id, voice_speed, text, output_path)
        return fallback_voice_id


def normalized_audio_path(final_audio):
    return final_audio.with_name(f"{final_audio.stem}{NORMALIZED_SUFFIX}{final_audio.suffix}")


def merge_audio_parts(output_dir, final_audio, part_files):
    concat_file = output_dir / "concat.txt"
    concat_file.write_text(
        "\n".join(f"file '{path.name}'" for path in part_files),
        encoding="utf-8",
    )

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            concat_file.name,
            "-c",
            "copy",
            final_audio.name,
        ],
        cwd=output_dir,
        check=True,
    )


def normalize_loudness(input_audio, output_audio):
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(input_audio),
            "-af",
            LOUDNESS_FILTER,
            "-codec:a",
            "libmp3lame",
            "-b:a",
            "128k",
            str(output_audio),
        ],
        check=True,
    )


def chunk_digest(voice_id, voice_speed, text):
    settings = {
        "model_id": MODEL_ID,
        "voice_id": voice_id,
        "output_format": OUTPUT_FORMAT,
        "stability": 0.55,
        "similarity_boost": 0.80,
        "style": 0.15,
        "speed": voice_speed,
        "use_speaker_boost": True,
    }
    payload = json.dumps(settings, sort_keys=True) + "\n" + text
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def sidecar_hash_file(audio_path):
    return audio_path.with_suffix(audio_path.suffix + ".sha256")


def audio_part_is_current(audio_path, voice_id, voice_speed, text):
    hash_path = sidecar_hash_file(audio_path)
    if not audio_path.exists() or audio_path.stat().st_size == 0 or not hash_path.exists():
        return False
    return hash_path.read_text(encoding="utf-8").strip() == chunk_digest(
        voice_id, voice_speed, text
    )


def write_audio_part_hash(audio_path, voice_id, voice_speed, text):
    sidecar_hash_file(audio_path).write_text(
        chunk_digest(voice_id, voice_speed, text),
        encoding="utf-8",
    )


def main():
    api_key = get_api_key()
    voice_id = get_configured_voice_id()
    voice_speed = get_configured_voice_speed()
    output_dir = get_output_dir()
    final_audio = get_final_audio_path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    text = INPUT_FILE.read_text(encoding="utf-8").strip()
    chunks = split_text_by_paragraphs(text, MAX_CHARS)
    print(f"Voice ID: {voice_id}")
    print(f"Voice speed: {voice_speed}")
    print(f"Output: {final_audio}")
    print(f"Generating {len(chunks)} audio part(s).")

    part_files = []
    for index, chunk in enumerate(chunks, start=1):
        output_path = output_dir / f"presentation_part_{index:02d}.mp3"
        if audio_part_is_current(output_path, voice_id, voice_speed, chunk):
            print(f"Reusing existing {output_path}")
        else:
            print(f"Generating {output_path} ({len(chunk)} characters)")
            voice_id = synthesize_with_fallback(
                api_key, voice_id, voice_speed, chunk, output_path
            )
            write_audio_part_hash(output_path, voice_id, voice_speed, chunk)
        part_files.append(output_path)

    merge_audio_parts(output_dir, final_audio, part_files)
    print(f"Done: {final_audio}")
    normalized_audio = normalized_audio_path(final_audio)
    normalize_loudness(final_audio, normalized_audio)
    print(f"Done: {normalized_audio}")


if __name__ == "__main__":
    main()
