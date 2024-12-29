

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
import os

# Scopes required for YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate_youtube():
    """Authenticate with YouTube Data API and return the API client."""
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json', SCOPES
    )
    credentials = flow.run_local_server(port=8080, prompt="consent", authorization_prompt_message="")
    youtube = build("youtube", "v3", credentials=credentials)
    return youtube

def upload_video(youtube, video_path, title, description, tags, category="22"):
    """
    Upload a video to YouTube Shorts.
    
    Args:
        youtube: Authenticated YouTube client.
        video_path (str): Path to the video file.
        title (str): Video title.
        description (str): Video description.
        tags (list): List of tags for the video.
        category (str): Video category ID (default: 22 for "People & Blogs").
    """
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category,
            },
            "status": {
                "privacyStatus": "public",  # Set to "unlisted" or "private" as needed
            },
        },
        media_body=media,
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")
    print(f"Uploaded: {response['snippet']['title']} (Video ID: {response['id']})")

def upload_multiple_videos(video_folder):
    """
    Upload multiple videos from a folder to YouTube Shorts.
    
    Args:
        video_folder (str): Path to the folder containing videos.
    """
    youtube = authenticate_youtube()
    for video_file in os.listdir(video_folder):
        if video_file.endswith(".mp4"):  # Check for MP4 files
            video_path = os.path.join(video_folder, video_file)
            title = os.path.splitext(video_file)[0]  # Use file name as title
            description = f"This is a YouTube Shorts video: {title}"
            tags = ["shorts", "YouTube Shorts"]  # Add relevant tags
            print(f"Uploading: {video_file}")
            upload_video(youtube, video_path, title, description, tags)

# Example usage
if __name__ == "__main__":
    video_folder = "output_videos"  # Replace with the folder containing your videos
    upload_multiple_videos(video_folder)


from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import moviepy.editor as mp  # For video metadata (ensure this package is installed)

# Scopes required for YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate_youtube():
    """Authenticate with YouTube Data API and return the API client."""
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json', SCOPES
    )
    credentials = flow.run_local_server(port=8080, prompt="consent", authorization_prompt_message="")
    youtube = build("youtube", "v3", credentials=credentials)
    return youtube

def validate_short(video_path):
    """Validate if the video meets YouTube Shorts requirements."""
    clip = mp.VideoFileClip(video_path)
    duration = clip.duration
    aspect_ratio = clip.size[0] / clip.size[1]  # width / height
    clip.close()
    return duration <= 60 and aspect_ratio < 1  # Video is less than 60 seconds and vertical

def upload_video(youtube, video_path, title, description, tags, category="22"):
    """
    Upload a video to YouTube Shorts.
    
    Args:
        youtube: Authenticated YouTube client.
        video_path (str): Path to the video file.
        title (str): Video title.
        description (str): Video description.
        tags (list): List of tags for the video.
        category (str): Video category ID (default: 22 for "People & Blogs").
    """
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category,
            },
            "status": {
                "privacyStatus": "public",  # Set to "unlisted" or "private" as needed
            },
        },
        media_body=media,
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")
    print(f"Uploaded: {response['snippet']['title']} (Video ID: {response['id']})")

def upload_multiple_videos(video_folder):
    """
    Upload multiple videos from a folder to YouTube Shorts.
    
    Args:
        video_folder (str): Path to the folder containing videos.
    """
    youtube = authenticate_youtube()
    for video_file in os.listdir(video_folder):
        if video_file.endswith(".mp4"):  # Check for MP4 files
            video_path = os.path.join(video_folder, video_file)
            if not validate_short(video_path):
                print(f"Skipping {video_file}: Not a valid Shorts video (must be vertical and <= 60 seconds).")
                continue
            title = os.path.splitext(video_file)[0]  # Use file name as title
            description = f"This is a YouTube Shorts video: {title}\n#Shorts"
            tags = ["shorts", "YouTube Shorts"]  # Add relevant tags
            print(f"Uploading: {video_file}")
            upload_video(youtube, video_path, title, description, tags)

# Example usage
if __name__ == "__main__":
    video_folder = "output_videos"  # Replace with the folder containing your videos
    upload_multiple_videos(video_folder)
