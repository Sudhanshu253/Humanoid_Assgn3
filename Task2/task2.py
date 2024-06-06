import os
import random
import moviepy.editor as mp

# Set the path to the ffmpeg executable if needed
ffmpeg_path = "/usr/local/bin/ffmpeg"  # Adjust this path based on your installation
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path

# Load the video
input_video_path = "/Users/sudhanshu/Desktop/ML/Python/env/Assignment3_231045/Task2/Input_RoboClip.mp4"
video = mp.VideoFileClip(input_video_path)

# Get video duration
video_duration = video.duration

# Ensure the video is long enough for at least 24 seconds
if video_duration < 24:
    raise ValueError("The input video is shorter than 24 seconds.")

# Function to create a random 6-second clip with effects
def create_random_clip(video, clip_duration=6):
    start_time = random.uniform(0, video.duration - clip_duration)
    end_time = start_time + clip_duration
    clip = video.subclip(start_time, end_time)
    
    # Apply fade-in and fade-out effects to both video and audio
    clip = clip.fx(mp.vfx.fadein, 1, initial_color=(0, 0, 0))
    clip = clip.fx(mp.vfx.fadeout, 1, final_color=(0, 0, 0))
    clip = clip.audio_fadein(1).audio_fadeout(1)
    
    return clip

# Create four 6-second clips
clips = [create_random_clip(video) for _ in range(4)]

# Concatenate the clips
final_clip = mp.concatenate_videoclips(clips, method="compose")

# Save the final video with audio
output_video_path = "/Users/sudhanshu/Desktop/ML/Python/env/Assignment3_231045/Task2.mp4"
final_clip.write_videofile(output_video_path, codec="libx264", fps=24, audio_codec="aac")

print("Clip saved successfully.")
