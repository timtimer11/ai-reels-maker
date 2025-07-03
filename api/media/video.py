import os
import tempfile
from io import BytesIO
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
from clients.deepgram import DeepgramService
import subprocess


deepgram_service = DeepgramService()

def get_audio_duration(file_path: str) -> float:
    """Return the duration of an audio file in seconds."""
    return AudioFileClip(file_path).duration


def get_video_duration(file_path: str) -> float:
    """Return the duration of a video file in seconds."""
    return VideoFileClip(file_path).duration


def subtitle_generator(txt: str) -> TextClip:
    """Generate a TextClip for subtitles."""
    return TextClip(text=txt, font_size=24, color='white', stroke_color='black', stroke_width=1)


def process_video_streaming(audio_bytes: bytes, video_bytes: BytesIO) -> BytesIO:
    """
    Merge video, audio, and captions with length check using MoviePy.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write input bytes to temp files
        audio_path = os.path.join(tmpdir, "audio.wav")
        video_path = os.path.join(tmpdir, "video.mp4")
        srt_path   = os.path.join(tmpdir, "captions.srt")
        output_path= os.path.join(tmpdir, "output.mp4")

        with open(audio_path, "wb") as f:
            f.write(audio_bytes)
        video_bytes.seek(0)
        with open(video_path, "wb") as f:
            f.write(video_bytes.read())

        # Duration checks
        a_duration = get_audio_duration(audio_path)
        v_duration = get_video_duration(video_path)
        if a_duration >= v_duration:
            raise ValueError(f"Audio duration ({a_duration:.2f}s) >= video duration ({v_duration:.2f}s)")

        # Load clips
        audio_clip = AudioFileClip(audio_path)
        print("Loaded audio clip")
        video_clip = VideoFileClip(video_path).with_audio(audio_clip)
        print("Combined audio and video clips")
        # Generate and write captions (SRT)
        srt_content = deepgram_service.generate_captions_with_deepgram(audio_path)
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt_content)
        
        print('Generated captions with Deepgram')

        # # Create subtitles overlay
        # subtitles = SubtitlesClip(
        #     srt_path,
        #     make_textclip=subtitle_generator,
        #     encoding='utf-8'
        # )
        # print('Created subtitles overlay')

        # # Compose final clip
        # final = CompositeVideoClip([video_clip, subtitles])

        # print('Composed a final clip')

        # # Export
        # final.write_videofile(
        #     output_path,
        #     codec="libx264",
        #     audio_codec="aac",
        #     fps=video_clip.fps,
        #     threads=1,
        #     ffmpeg_params=["-movflags", "frag_keyframe+empty_moov+default_base_moof"],
        #     logger=None,
        #     write_logfile=False,
        # )
        # print('Wrote final video file')
        # # Close clips to free resources and avoid broken pipes
        # final.close()
        # video_clip.close()
        # audio_clip.close()

        # # Read output bytes and return
        # with open(output_path, "rb") as f:
        #     data = f.read()
        # # Return an in-memory bytes buffer so upload_file_to_s3 (which expects a file-like) works
        # return BytesIO(data)
        # Use FFmpeg for fast final export
        # FFmpeg command with proper audio mapping
        cmd = [
            'ffmpeg',
            '-y',  # Overwrite output
            '-i', video_path,
            '-i', audio_path,
            '-vf', f"subtitles='{srt_path}':force_style='Fontsize=24'",  # Burn subtitles
            '-c:v', 'libx264',  # Video codec
            '-preset', 'veryfast',
            '-c:a', 'aac',  # Audio codec
            '-b:a', '192k',
            '-map', '0:v',  # Map video from first input
            '-map', '1:a',  # Map audio from second input
            '-shortest',  # End with shortest stream
            output_path
        ]

        # Execute FFmpeg
        try:
            subprocess.run(cmd, check=True, stderr=subprocess.PIPE, timeout=300)
            
            # Verify and return output
            with open(output_path, "rb") as f:
                if f.read(1):  # Check not empty
                    f.seek(0)
                    return BytesIO(f.read())
                raise RuntimeError("Empty output file")
                
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg failed with error:\n{e.stderr.decode()}")
            raise RuntimeError("Video processing failed")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Processing timed out after 5 minutes")