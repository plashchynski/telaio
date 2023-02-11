import numpy as np
import ffmpeg
import av
import cv2

class VideoFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.probe = ffmpeg.probe(file_path)
        self.video_stream_info = next((stream for stream in self.probe['streams'] if stream['codec_type'] == 'video'), None)
        self.frames_count = int(self.video_stream_info['nb_frames'])

        self.rotate = 0

        if 'side_data_list' in self.video_stream_info:
            side_data_list = self.video_stream_info['side_data_list']
            displaymatrix = [x for x in side_data_list if x['side_data_type'] == 'Display Matrix']
            if len(displaymatrix) > 0:
                self.rotate = displaymatrix[0]['rotation']

        if 'rotate' in self.video_stream_info['tags']:
            self.rotate = int(self.video_stream_info['tags']['rotate'])

        self.width = int(self.video_stream_info['width'])
        self.height = int(self.video_stream_info['height'])

        if abs(self.rotate) == 90:
            self.width, self.height = self.height, self.width

        a1, a2 = self.video_stream_info['avg_frame_rate'].split('/')
        self.fps = float(a1)/float(a2)

    # Returns the number of frames in the video
    # Can be used as len(VideoFile('video.mp4'))
    def __len__(self):
        return self.frames_count

    # Can be used as an iterator, example:
    # for (frame_index, frame) in Telaio('video.mp4').frames():
    #     print(frame)
    # The limit parameter can be used to limit the number of frames returned
    # The batch_size parameter can be used to return a batch of frames at a time
    def frames(self, batch_size = None, limit=None):
        v = av.open(self.file_path)
        for frame_index, frame in enumerate(v.decode(video=0)):
            if limit and frame_index > limit:
                break

            frame = np.asarray(frame.to_image())
            if abs(self.rotate) == 90:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

            if batch_size:
                if frame_index % batch_size == 0:
                    # Start a new batch
                    batch = [frame]
                    frame_indexes = [frame_index]
                else:
                    batch.append(frame)
                    frame_indexes.append(frame_index)
                    if frame_index % batch_size == batch_size - 1:
                        yield (frame_indexes, batch)
            else:
                yield (frame_index, frame)

        # Return the last batch
        if batch_size and len(batch) > 0:
            yield (frame_indexes, batch)

    # Returns the first frame of the video
    def first_frame(self):
        _, frame = next(self.frames())
        return frame
