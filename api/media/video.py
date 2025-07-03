import os
import tempfile
from io import BytesIO
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
from clients.deepgram import DeepgramService
import subprocess
import time

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


# def process_video_streaming(audio_bytes: bytes, video_bytes: BytesIO) -> BytesIO:
#     """
#     Merge video, audio, and captions with length check using MoviePy.
#     """
#     with tempfile.TemporaryDirectory() as tmpdir:
#         # Write input bytes to temp files
#         audio_path = os.path.join(tmpdir, "audio.wav")
#         video_path = os.path.join(tmpdir, "video.mp4")
#         srt_path   = os.path.join(tmpdir, "captions.srt")
#         output_path= os.path.join(tmpdir, "output.mp4")

#         with open(audio_path, "wb") as f:
#             f.write(audio_bytes)
#         video_bytes.seek(0)
#         with open(video_path, "wb") as f:
#             f.write(video_bytes.read())

#         # Duration checks
#         a_duration = get_audio_duration(audio_path)
#         v_duration = get_video_duration(video_path)
#         if a_duration >= v_duration:
#             raise ValueError(f"Audio duration ({a_duration:.2f}s) >= video duration ({v_duration:.2f}s)")

#         # Load clips
#         audio_clip = AudioFileClip(audio_path)
#         print("Loaded audio clip")
#         video_clip = VideoFileClip(video_path).with_audio(audio_clip)
#         print("Combined audio and video clips")
#         # Generate and write captions (SRT)
#         srt_content = deepgram_service.generate_captions_with_deepgram(audio_path)
#         with open(srt_path, "w", encoding="utf-8") as f:
#             f.write(srt_content)
        
#         print('Generated captions with Deepgram')

#         # # Create subtitles overlay
#         # subtitles = SubtitlesClip(
#         #     srt_path,
#         #     make_textclip=subtitle_generator,
#         #     encoding='utf-8'
#         # )
#         # print('Created subtitles overlay')

#         # # Compose final clip
#         # final = CompositeVideoClip([video_clip, subtitles])

#         # print('Composed a final clip')

#         # # Export
#         # final.write_videofile(
#         #     output_path,
#         #     codec="libx264",
#         #     audio_codec="aac",
#         #     fps=video_clip.fps,
#         #     threads=1,
#         #     ffmpeg_params=["-movflags", "frag_keyframe+empty_moov+default_base_moof"],
#         #     logger=None,
#         #     write_logfile=False,
#         # )
#         # print('Wrote final video file')
#         # # Close clips to free resources and avoid broken pipes
#         # final.close()
#         # video_clip.close()
#         # audio_clip.close()

#         # # Read output bytes and return
#         # with open(output_path, "rb") as f:
#         #     data = f.read()
#         # # Return an in-memory bytes buffer so upload_file_to_s3 (which expects a file-like) works
#         # return BytesIO(data)
#         # Use FFmpeg for fast final export
#         cmd = [
#             'ffmpeg',
#             '-y',  # Overwrite without asking
#             '-i', video_path,
#             '-i', audio_path,
#             '-filter_complex',
#             f"[0:v]subtitles='{srt_path}':force_style='Fontsize=24,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BorderStyle=3'[subs]",
#             '-map', '[subs]',  # Use subtitled video stream
#             '-map', '1:a:0',   # Use first audio stream from second input
#             '-c:v', 'libx264',
#             '-preset', 'veryfast',  # Better than ultrafast for production
#             '-crf', '23',
#             '-c:a', 'aac',
#             '-b:a', '192k',
#             '-ar', '48000',
#             '-ac', '2',
#             '-shortest',
#             '-movflags', 'frag_keyframe+empty_moov+default_base_moof',
#             '-f', 'mp4',
#             'pipe:1'  # Stream directly to stdout
#         ]

#         # Execute with proper resource limits
#         try:
#             process = subprocess.Popen(
#                 cmd,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 stdin=subprocess.DEVNULL
#             )
            
#             # Read output in chunks to avoid memory issues
#             output = BytesIO()
#             while True:
#                 chunk = process.stdout.read(4096)
#                 if not chunk:
#                     break
#                 output.write(chunk)
            
#             # Check for errors
#             if process.wait() != 0:
#                 error_msg = process.stderr.read().decode()
#                 raise RuntimeError(f"FFmpeg failed: {error_msg}")
            
#             output.seek(0)
#             return output
            
#         except Exception as e:
#             print(f"Error during processing: {str(e)}")
#             raise

def process_video_streaming(audio_bytes: bytes, video_bytes: BytesIO) -> BytesIO:
    """
    Merge video, audio, and captions with length check using MoviePy for validation
    and FFmpeg for efficient processing.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write input files
        audio_path = os.path.join(tmpdir, "audio.wav")
        video_path = os.path.join(tmpdir, "video.mp4")
        srt_path = os.path.join(tmpdir, "captions.srt")

        with open(audio_path, "wb") as f:
            f.write(audio_bytes)
        with open(video_path, "wb") as f:
            video_bytes.seek(0)
            f.write(video_bytes.read())

        # Validate durations
        a_duration = get_audio_duration(audio_path)
        v_duration = get_video_duration(video_path)
        if a_duration >= v_duration:
            raise ValueError(f"Audio duration ({a_duration:.2f}s) >= video duration ({v_duration:.2f}s)")

        # Generate subtitles
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(deepgram_service.generate_captions_with_deepgram(audio_path))

        # FFmpeg command with proper streaming and timeout
        cmd = [
            'ffmpeg',
            '-y',
            '-i', video_path,
            '-i', audio_path,
            '-filter_complex',
            f"[0:v]subtitles='{srt_path}':force_style='Fontsize=24,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BorderStyle=3'[v];"
            "[v][1:a]concat=n=1:v=1:a=1[out]",
            '-map', '[out]',
            '-c:v', 'libx264',
            '-preset', 'veryfast',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-movflags', 'frag_keyframe+empty_moov',
            '-f', 'mp4',
            'pipe:1'
        ]

        # Execute with timeout and proper stream handling
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
                bufsize=10*1024*1024  # 10MB buffer
            )

            # Stream output with timeout
            output = BytesIO()
            start_time = time.time()
            while True:
                if time.time() - start_time > 300:  # 5 minute timeout
                    process.kill()
                    raise RuntimeError("FFmpeg processing timed out")

                chunk = process.stdout.read(4096)
                if not chunk:
                    break
                output.write(chunk)

            # Verify successful completion
            if process.poll() is None:
                process.kill()
                raise RuntimeError("FFmpeg process didn't terminate")
                
            if process.returncode != 0:
                error = process.stderr.read().decode()
                raise RuntimeError(f"FFmpeg failed: {error}")

            output.seek(0)
            return output

        except Exception as e:
            if 'process' in locals():
                process.kill()
            raise RuntimeError(f"Video processing failed: {str(e)}")