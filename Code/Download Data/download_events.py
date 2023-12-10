import os  # Import the os module for interacting with the operating system
import json  # Import the json module for parsing JSON files
from moviepy.editor import VideoFileClip  # Import VideoFileClip from moviepy for video editing tasks
import cv2  # Import OpenCV for image and video processing


# Function to extract frames from video and save them to folders based on labels and frame numbers
def extract_frames(video_path1, video_path2, output_folder, annotations, label_name):
    # Open video files for reading
    cap1 = cv2.VideoCapture(video_path1)
    cap2 = cv2.VideoCapture(video_path2)
    # Get frame rate and total frame count for both videos
    fps = cap1.get(cv2.CAP_PROP_FPS)
    total_frames1 = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
    total_frames2 = int(cap2.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_duration_milliseconds = 1000 / fps

    # Process each annotation
    for annotation in annotations:
        # Determine which half of the game the annotation refers to
        half_tracker = annotation["gameTime"][0]
        time_milli = int(annotation["position"])
        target_frame_number = int(time_milli / frame_duration_milliseconds)

        # Select the appropriate video based on the game half and read the frame
        if int(half_tracker) == 1:
            if target_frame_number < 0 or target_frame_number >= total_frames1:
                print("Invalid time in milliseconds provided.")
                continue
            cap1.set(cv2.CAP_PROP_POS_FRAMES, target_frame_number)
            success, image = cap1.read()
        if int(half_tracker) == 2:
            if target_frame_number < 0 or target_frame_number >= total_frames2:
                print("Invalid time in milliseconds provided.")
                continue
            cap2.set(cv2.CAP_PROP_POS_FRAMES, target_frame_number)
            success, image = cap2.read()

        # If frame is successfully extracted, save it in the designated folder
        if success:
            label_folder = os.path.join(output_folder, label_name)
            os.makedirs(label_folder, exist_ok=True)
            frame_path = os.path.join(label_folder, f"frame{target_frame_number}.jpg")
            flag = cv2.imwrite(frame_path, image)
            print(flag)

    # Release resources by closing video captures
    cap1.release()
    cap2.release()


# Function to extract frames and clips with audio using moviepy
def extract_clips(video_path1, video_path2, output_folder, annotations, label_name):
    # Load the two halves of the soccer game as video clips
    clip1 = VideoFileClip(video_path1)
    clip2 = VideoFileClip(video_path2)

    # Process each annotation to extract a clip
    for annotation in annotations:
        # Determine which half of the game the event occurred in
        half_tracker = annotation["gameTime"][0]
        # Convert event time from milliseconds to seconds
        event_time_milli = int(annotation["position"])
        event_time_seconds = event_time_milli / 1000

        # Define the time range for the clip ("X" seconds before and after the event.
        # X varies for different events.
        # Ranges:
        #       ["Corner", "Free-kick", "Penalty", "Open-play"] : ["2, 4", "3,4", "1, 2", "4,4"])
        # Current range is set for Corner. choose from the options
        range_x = 2
        range_y = 4
        start_time = max(0, int(event_time_seconds) - range_x)
        end_time = event_time_seconds + range_y

        # Choose the correct video clip based on the game half
        current_clip = clip1 if int(half_tracker) == 1 else clip2

        # Create a subclip centered around the event
        subclip = current_clip.subclip(start_time, end_time)

        # If the subclip exists, process and save it
        if subclip:
            # Create a folder for the label and determine the clip's file path
            label_folder = os.path.join(output_folder, label_name)
            os.makedirs(label_folder, exist_ok=True)
            clip_path = os.path.join(label_folder, f"clip_{int(start_time)}-{int(end_time)}.mp4")

            # Save the extracted subclip with audio
            subclip.write_videofile(clip_path, codec="libx264", audio_codec="aac")

    # Close the video clips to release system resources
    clip1.close()
    clip2.close()
    print("Clips extraction completed.")


# Function to extract specific frames from videos based on event annotations
def extract_frames_for_event(main_folder, subfolder, event_to_extract, label_name):
    # Construct the path to the JSON file containing annotations
    json_file_path = os.path.join(main_folder, subfolder, 'Labels-v2.json')

    # Open and load the JSON file to access annotations
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    annotations_to_extract = [ann for ann in data["annotations"] if ann[label_name] == event_to_extract]

    # Set the paths for the two halves of the soccer match videos
    video_path1 = os.path.join(main_folder, subfolder, '1_224p.mkv')
    video_path2 = os.path.join(main_folder, subfolder, '2_224p.mkv')

    # Define the directory where the extracted frames will be saved
    output_folder = os.path.join(main_folder, "Extracted_Events", event_to_extract)

    # Call a function to extract and save the frames based on the annotations
    extract_clips(video_path1, video_path2, output_folder, annotations_to_extract, label_name)


# Main directory where the dataset is located
main_folder = "directory_toProject/Dataset"

# List of subdirectories representing different soccer leagues
subfolders = ["england_epl", "europe_uefa-champions-league", "germany_bundesliga", "france_ligue-1",
              "italy_serie-a", "spain_laliga"]

# List of subdirectories representing different seasons
subfolders2 = ["2014-2015", "2015-2016", "2016-2017"]

# Initialize an empty list to store combinations of leagues and seasons
all_folder_combinations = []

# Event extraction code List of events to extract (label-v2) :: ["Corner", "Yellow card", "Red card", "Penalty",
# "Indirect free-kick", "Direct free-kick", "Goal"]
# List of events to extract (label-camera) :: ["change_type": # "logo", "label":"Close-up player or field referee",
# "Main camera center", "Close-up side staff", "Main camera left"]

# Filter annotations to find those matching the specified event
# label_options:
#              labels_camera : ["change_type", "label"]
#              labels_v2     : ["label"]

label_name = "label"  # choose from the options according to task

# Specify the event to extract
event_to_extract = "event_name"

# Loop through each league and season, creating a path for each combination
for subfolder in subfolders:
    for subfolder2 in subfolders2:
        # Join the league and season to create a specific folder path
        folder_combination = os.path.join(subfolder, subfolder2)
        # Add the folder combination to the list
        all_folder_combinations.append(folder_combination)
# Iterate through each folder combination (league and season)
for subfolder in all_folder_combinations:
    # List all game folders in the current league-season folder
    game_folders = [game_folder for game_folder in os.listdir(os.path.join(main_folder, subfolder)) if
                    os.path.isdir(os.path.join(main_folder, subfolder, game_folder))]

    # Iterate through each game folder
    for game_folder in game_folders:
        # Construct the full path to the current game folder
        folder_path = os.path.join(main_folder, subfolder)
        folder_path1 = os.path.join(folder_path, game_folder)
        # Call the function to extract frames for the specified event in the current game folder
        extract_frames_for_event(main_folder, folder_path1, event_to_extract, label_name)
