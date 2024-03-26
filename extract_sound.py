import dtcwt  # Importing the Dual-Tree Complex Wavelet Transform library
from scipy import ndimage  # Importing ndimage module from SciPy for multi-dimensional image processing
from scipy import signal  # Importing signal module from SciPy for signal processing
import numpy as np  # Importing NumPy for numerical computing
import cv2  # Importing OpenCV for image and video processing
import cmath  # Importing cmath for complex number operations
from scipy.io.wavfile import write  # Importing write function from scipy.io.wavfile for writing WAV files


def npTowav(np_file, output_name):
    """
    Convert a NumPy array to a WAV file.

    Parameters:
    - np_file (ndarray): Input NumPy array.
    - output_name (str): Output file name for the WAV file.
    """
    # Samples per second (sampling frequency of the audio file)
    sps = 1
    waveform_integers = np.int16(np_file * 32767)  # Scale the values and convert to 16-bit integers

    # Write the .wav file
    write(output_name, sps, waveform_integers)


def soundfromvid(input_data, frameCount, nlevels, orient, ref_no, ref_orient, ref_level):
    """
    Generate sound data from video frames using the Dual-Tree Complex Wavelet Transform.

    Parameters:
    - input_data (list): List of input video frames.
    - frameCount (int): Number of frames in the video.
    - nlevels (int): Number of decomposition levels for wavelet transform.
    - orient (int): Number of orientations for wavelet transform.
    - ref_no (int): Reference frame number for comparison.
    - ref_orient (int): Reference orientation for comparison.
    - ref_level (int): Reference decomposition level for comparison.

    Returns:
    - sound_data (ndarray): Sound data generated from the video frames.
    """

    tr = dtcwt.Transform2d()  # Create a DTCWT transform object

    ref_frame = tr.forward(input_data[ref_no], nlevels=nlevels)  # Forward transform of the reference frame

    data = np.zeros((frameCount, nlevels, orient))  # Initialize array for storing sound data

    # Iterate through each frame
    for fc in range(frameCount):
        frame = tr.forward(input_data[fc], nlevels=nlevels)  # Forward transform of the current frame

        # Iterate through each decomposition level
        for level in range(nlevels):
            xmax = len(frame.highpasses[level])  # Maximum x-coordinate
            ymax = len(frame.highpasses[level][0])  # Maximum y-coordinate

            # Iterate through each orientation
            for angle in range(orient):
                # Iterate through each pixel
                for x in range(xmax):
                    for y in range(ymax):
                        # Compute amplitude and phase difference
                        amp, phase = cmath.polar(frame.highpasses[level][x][y][angle])
                        ref_phase = cmath.polar(ref_frame.highpasses[level][x][y][angle])[1]

                        # Accumulate sound data
                        data[fc, level, angle] += (amp * amp) * (phase - ref_phase)

    print("Transform complete")

    # Compute shift matrix for time alignment
    shift_matrix = np.zeros((nlevels, orient))
    ref_vector = data[:, ref_level, ref_orient].reshape(-1)
    for i in range(nlevels):
        for j in range(orient):
            shift_matrix[i, j] = maxTime(ref_vector, data[:, i, j].reshape(-1))

    sound_raw = np.zeros(frameCount)  # Initialize array for raw sound data

    # Generate sound data by shifting and summing
    for fc in range(frameCount):
        for i in range(nlevels):
            for j in range(orient):
                sound_raw[fc] += data[fc - int(shift_matrix[i, j]), i, j]

     # Normalize the sound data
    p_min = sound_raw[0]
    p_max = sound_raw[0]
    for i in range(1, frameCount):
        if sound_raw[i] < p_min:
            p_min = sound_raw[i]
        if sound_raw[i] > p_max:
            p_max = sound_raw[i]
    sound_data = ((2 * sound_raw)- (p_min + p_max)) / (p_max - p_min)

    return sound_data


def main():
    cap = cv2.VideoCapture("/content/motion_magnification_learning-based/res_guitar/guitar/guitar_amp25.avi")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(frameCount, frameWidth, frameHeight)

    nlevels = 3
    orient = 6
    ref_no = 0
    ref_level = 0
    ref_orient = 0

    input_data = []

    # Read video frames and convert to grayscale
    for fc in range(frameCount):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        input_data.append(gray)

    cap.release()
    print("Video Loaded")

    # Generate sound from video frames and save as WAV file
    npTowav(soundfromvid(input_data, frameCount, nlevels, orient, ref_no, ref_orient, ref_level), "sound.wav")


if __name__ == "__main__":
    main()  # Execute the main function if the script is run directly
