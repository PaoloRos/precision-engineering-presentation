import argparse
import re
import subprocess
from pathlib import Path

import generate_audio


DEFAULT_START_LINE = 29
DEFAULT_END_LINE = 33
DEFAULT_OUTPUT_DIR = Path("audio/modified-chunk")
DEFAULT_OUTPUT_FILE = "modified_part.mp3"
DEFAULT_NEUTRAL_CONTINUATION = (
    "This is the neutral continuation required to keep the speech flowing "
    "naturally during synthesis. This extra sentence is only used as audio "
    "context and will be removed from the final exported chunk."
)


def extract_line_range(path, start_line, end_line):
    lines = path.read_text(encoding="utf-8").splitlines()
    if start_line < 1 or end_line < start_line or end_line > len(lines):
        raise ValueError(
            f"Invalid line range {start_line}-{end_line} for {path} "
            f"with {len(lines)} lines."
        )
    return "\n".join(lines[start_line - 1 : end_line]).strip()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate TTS only for a selected line range."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=generate_audio.INPUT_FILE,
        help="Markdown TTS script to read.",
    )
    parser.add_argument(
        "--start-line",
        type=int,
        default=DEFAULT_START_LINE,
        help="First 1-based line to synthesize.",
    )
    parser.add_argument(
        "--end-line",
        type=int,
        default=DEFAULT_END_LINE,
        help="Last 1-based line to synthesize.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for the generated chunk.",
    )
    parser.add_argument(
        "--output-file",
        default=DEFAULT_OUTPUT_FILE,
        help="MP3 filename for the generated chunk.",
    )
    parser.add_argument(
        "--neutral-continuation",
        default=None,
        help=(
            "Append neutral continuation text during synthesis, then trim it "
            "from the normalized output."
        ),
    )
    parser.add_argument(
        "--auto-trim",
        action="store_true",
        help="Trim the normalized output at the final paragraph-boundary silence.",
    )
    parser.add_argument(
        "--trim-at-seconds",
        type=float,
        default=None,
        help="Trim the normalized output at an explicit timestamp in seconds.",
    )
    return parser.parse_args()


def silence_intervals(audio_path):
    result = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-i",
            str(audio_path),
            "-af",
            "silencedetect=n=-42dB:d=0.25",
            "-f",
            "null",
            "-",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    intervals = []
    current_start = None
    for line in result.stderr.splitlines():
        start_match = re.search(r"silence_start: ([0-9.]+)", line)
        if start_match:
            current_start = float(start_match.group(1))
            continue

        end_match = re.search(r"silence_end: ([0-9.]+)", line)
        if end_match and current_start is not None:
            intervals.append((current_start, float(end_match.group(1))))
            current_start = None

    return intervals


def trim_at_context_boundary(normalized_path, trimmed_path):
    intervals = silence_intervals(normalized_path)
    if not intervals:
        raise RuntimeError(f"No silence boundary found in {normalized_path}")

    # The appended neutral continuation is the final paragraph before the true
    # end, so the cut point is the penultimate detected silence boundary.
    boundary = intervals[-2] if len(intervals) >= 2 else intervals[-1]
    cut_time = boundary[0] + min((boundary[1] - boundary[0]) / 2, 0.25)

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(normalized_path),
            "-t",
            f"{cut_time:.3f}",
            "-codec:a",
            "libmp3lame",
            "-b:a",
            "128k",
            str(trimmed_path),
        ],
        check=True,
    )
    return cut_time


def trim_at_time(normalized_path, trimmed_path, cut_time):
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(normalized_path),
            "-t",
            f"{cut_time:.3f}",
            "-codec:a",
            "libmp3lame",
            "-b:a",
            "128k",
            str(trimmed_path),
        ],
        check=True,
    )


def main():
    args = parse_args()
    generate_audio.load_env()

    api_key = generate_audio.get_api_key()
    voice_id = generate_audio.get_configured_voice_id()
    voice_speed = generate_audio.get_configured_voice_speed()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.output_dir / args.output_file
    normalized_path = generate_audio.normalized_audio_path(output_path)
    trimmed_path = normalized_path.with_name(
        f"{normalized_path.stem}_trimmed{normalized_path.suffix}"
    )
    text = extract_line_range(args.input, args.start_line, args.end_line)
    synthesis_text = text
    if args.neutral_continuation:
        synthesis_text = f"{text}\n\n{args.neutral_continuation.strip()}"

    print(f"Input: {args.input}")
    print(f"Line range: {args.start_line}-{args.end_line}")
    print(f"Voice ID: {voice_id}")
    print(f"Voice speed: {voice_speed}")
    print(f"Output: {output_path}")
    print(f"Characters: {len(synthesis_text)}")

    if generate_audio.audio_part_is_current(
        output_path, voice_id, voice_speed, synthesis_text
    ):
        print(f"Reusing existing {output_path}")
    else:
        voice_id = generate_audio.synthesize_with_fallback(
            api_key, voice_id, voice_speed, synthesis_text, output_path
        )
        generate_audio.write_audio_part_hash(
            output_path, voice_id, voice_speed, synthesis_text
        )

    generate_audio.normalize_loudness(output_path, normalized_path)
    print(f"Done: {normalized_path}")
    if args.trim_at_seconds is not None:
        trim_at_time(normalized_path, trimmed_path, args.trim_at_seconds)
        print(f"Trimmed at {args.trim_at_seconds:.3f}s: {trimmed_path}")
    elif args.auto_trim:
        cut_time = trim_at_context_boundary(normalized_path, trimmed_path)
        print(f"Trimmed at {cut_time:.3f}s: {trimmed_path}")


if __name__ == "__main__":
    main()
