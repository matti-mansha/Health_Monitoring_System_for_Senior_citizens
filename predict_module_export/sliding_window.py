from predict import predict_function
import numpy as np
import os
import requests


# Initialize window size and stride
window_size = 80
stride = 20

txt_file_path = "C:\\Users\\javairia rehman\\Desktop\\kinect_module\\text.txt"

def get_next_frame_from_camera(file_path):
    with open(file_path, 'r') as f:
        first_line = f.readline().strip()

    with open(file_path, 'r') as f_in, open('temp_file', 'w') as f_out:
        next(f_in)  # skip first line
        for line in f_in:
            f_out.write(line)

    os.replace('temp_file', file_path)  # replace original file with modified file

    return first_line

# print(np.array(get_next_frame_from_camera(txt_file_path)))


# Initialize window
window = []
for i in range(window_size):
    frame = get_next_frame_from_camera(txt_file_path)
    window.append(np.array(eval(frame)))

# print(type(window))
# print(len(window))
# print(np.array(window))
# print(np.array(window).shape)



# Loop over frames and slide window
while True:
    # Call predict function on current window
    predictions = predict_function(np.array(window))
    print(predictions)
    # Setting Msg 
    activity_name="Coughing"
    # define the request payload
    payload = {
        'message': activity_name
    }

    # send the POST request
    response = requests.post('http://192.168.137.213:3000/api/recmessage', json=payload)

    # print the response from the server
    print(response.json())
    
#     # Process predictions as needed
#     # process_predictions(predictions)

    # Slide window
    for i in range(stride):
        window.pop(0)
        frame = get_next_frame_from_camera(txt_file_path)
        window.append(np.array(eval(frame)))

    # # Check if we have processed all frames
    # if end_of_camera_feed:
    #     break
