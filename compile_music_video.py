import os
import subprocess
import shutil

BASE_DIR = r"c:\books\08_acoustic_resonance_audio_forensics"
AUDIO_DIR = os.path.join(BASE_DIR, "video_assets", "audio")
FRAMES_DIR = os.path.join(BASE_DIR, "video_assets", "frames")
SEGMENTS_DIR = os.path.join(BASE_DIR, "video_assets", "segments")
os.makedirs(SEGMENTS_DIR, exist_ok=True)

FINAL_OUTPUT = os.path.join(BASE_DIR, "ACOUSTICSHIELD_HACKATHON_DEMO.mp4")

print("=== [1/3] Merging Scene 4 Voice Tracks (Alexa Intercept + Narrator) ===")
alexa_mp3 = os.path.join(AUDIO_DIR, "scene4_alexa.mp3")
narrator_mp3 = os.path.join(AUDIO_DIR, "scene4_narrator.mp3")
spacer_mp3 = os.path.join(AUDIO_DIR, "spacer.mp3")
scene4_full = os.path.join(AUDIO_DIR, "scene4_full.mp3")

# Generate 0.5s silence spacer
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", "0.5", "-c:a", "libmp3lame", spacer_mp3
], check=True, stderr=subprocess.DEVNULL)

concat4_txt = os.path.join(AUDIO_DIR, "concat4_music.txt")
with open(concat4_txt, "w", encoding="utf-8") as f:
    f.write(f"file '{alexa_mp3}'\nfile '{spacer_mp3}'\nfile '{narrator_mp3}'\n")

subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat4_txt, "-c", "copy", scene4_full
], check=True, stderr=subprocess.DEVNULL)
print("  Scene 4 audio merged successfully!")

SCENE_MAPPING = [
    (1, "slide_1.png", "scene1_crisis.mp3"),
    (2, "slide_2.png", "scene2_flaw.mp3"),
    (3, "slide_3.png", "scene3_resonance.mp3"),
    (4, "slide_4.png", "scene4_full.mp3"),
    (5, "slide_5.png", "scene5_benchmark.mp3"),
    (6, "slide_6.png", "scene6_architecture.mp3"),
]

print("\n=== [2/3] Compiling 1080p Video Segments with FFmpeg ===")
segment_files = []
for idx, slide_name, audio_name in SCENE_MAPPING:
    slide_path = os.path.join(FRAMES_DIR, slide_name)
    audio_path = os.path.join(AUDIO_DIR, audio_name)
    seg_path = os.path.join(SEGMENTS_DIR, f"seg_{idx}.mp4")

    # Compile 1080p 30fps H.264 segment
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-framerate", "30",
        "-i", slide_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        seg_path
    ]
    subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL)
    segment_files.append(seg_path)
    size_mb = os.path.getsize(seg_path) / (1024 * 1024)
    print(f"  [OK] Compiled Segment {idx}: {slide_name} + {audio_name} -> {size_mb:.2f} MB")

print("\n=== [3/3] Concatenating Final Master Video ===")
master_concat_txt = os.path.join(SEGMENTS_DIR, "master_concat.txt")
with open(master_concat_txt, "w", encoding="utf-8") as f:
    for seg in segment_files:
        f.write(f"file '{seg}'\n")

cmd_final = [
    "ffmpeg", "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", master_concat_txt,
    "-c", "copy",
    FINAL_OUTPUT
]
subprocess.run(cmd_final, check=True, stderr=subprocess.DEVNULL)

if os.path.exists(FINAL_OUTPUT):
    size_mb = os.path.getsize(FINAL_OUTPUT) / (1024 * 1024)
    print(f"\nSUCCESS! Master Hackathon Demo Video Created:")
    print(f"  Path: {FINAL_OUTPUT}")
    print(f"  Size: {size_mb:.2f} MB")

    # Copy to media directory as well
    media_dest = os.path.join(BASE_DIR, "media", "ACOUSTICSHIELD_HACKATHON_DEMO.mp4")
    shutil.copy(FINAL_OUTPUT, media_dest)
    print(f"  Mirrored to: {media_dest}")
else:
    print("Error: Output video was not created.")
