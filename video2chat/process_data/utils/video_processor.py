import cv2

def time_to_frame(video_path: str, times: list, output_folder: str):
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    for time_sec in times:
        frame_num = int(time_sec * fps)
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        success, image = video_capture.read()
        if success:
            cv2.imwrite(f"{output_folder}/frame_{frame_num}.jpg", image)

    video_capture.release()