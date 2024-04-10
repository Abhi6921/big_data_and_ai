from flask import Flask, Response, render_template, request, redirect, url_for
import torch
import cv2

app = Flask(__name__)

model_name = r'yolov5\runs\train\exp\weights\best.pt'
model = torch.hub.load('yolov5', 'custom', path=model_name, force_reload=True, source='local')

max_frame_limit = 150
average_height = 1
avg_distance_paddle = 1
avg_distance_participant = 1
distance_result = ""
video_path = ''


@app.route('/')
def index():
    return render_template('index.html', average_height=str(average_height),
                           avg_distance_paddle=str(avg_distance_paddle),
                           avg_distance_participant=str(avg_distance_participant),
                           distance_result=str(distance_result))


@app.route('/upload', methods=['POST'])
def upload():
    global video_path
    file = request.files['file']
    file.save('static/uploads/' + file.filename)
    video_path = 'static/uploads/' + file.filename
    return redirect(url_for('index'))


def generate_frames():
    global average_height, avg_distance_paddle, avg_distance_participant, distance_result

    paddle = "paddle"
    logo = "logo"
    person = "person"
    paddle_cm_width = 38
    y_max_person = 1
    paddle_to_ground_cm = 1
    pixel_to_cm_width = 1
    frame_counter = 0
    total_height = 0
    total_distance_paddle_ground = 0
    total_distance_participant_paddle = 0
    num_participants = 1

    vid = cv2.VideoCapture(video_path)
    while True:
        ret, frame = vid.read()
        if not ret or frame_counter >= max_frame_limit:
            break

        frame_counter += 1

        image = frame
        result = model(image)

        df = result.pandas().xyxy[0]
        df_sorted = df.sort_values('name')

        list_of_labels = []

        for ind in df_sorted.index:
            xMin, yMin = int(df['xmin'][ind]), int(df['ymin'][ind])
            xMax, yMax = int(df['xmax'][ind]), int(df['ymax'][ind])
            label = df['name'][ind]
            cv2.rectangle(image, (xMin, yMin), (xMax, yMax), (255, 0, 0), 2)
            cv2.putText(image, label, (xMin, yMin - 5), cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 2)
            list_of_labels.append(label)

            if paddle and logo in list_of_labels:
                if label == paddle:
                    paddle_width = xMax - xMin
                    pixel_to_cm_width = paddle_width / paddle_cm_width
                    cm_DST_to_ground = (10, 20)
                    cv2.putText(image, 'Paddle height to ground: ' + str(paddle_to_ground_cm)[:3] + ' CM',
                                cm_DST_to_ground, cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), 2)
                if label == logo:
                    paddle_to_ground_px = y_max_person - yMin
                    paddle_to_ground_cm = paddle_to_ground_px / pixel_to_cm_width

        if person in list_of_labels:
            person_distances = {}
            for ind in df_sorted.index:
                if df['name'][ind] == "person":
                    xMin, yMin = int(df['xmin'][ind]), int(df['ymin'][ind])
                    person_distances[xMin] = yMin

            sorted_distances = dict(sorted(person_distances.items()))
            person_heights = []
            for key in sorted_distances.keys():
                yMin = sorted_distances[key]
                y_max_person = yMax

                if yMin != y_max_person:
                    height_px = y_max_person - yMin
                    height_cm = height_px / pixel_to_cm_width
                    person_heights.append(height_cm)

            if person_heights:
                person_cm_height = max(person_heights)
                distance_between_person_and_paddle = person_cm_height - paddle_to_ground_cm + 10
                cm_ORG = (10, 40)
                cv2.putText(image, 'Participant height: ' + str(person_cm_height)[:3] + ' CM', cm_ORG,
                            cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), 2)
                cm_DST_to_paddle = (10, 340)
                cv2.putText(image,
                            'Distance between participant and paddle: ' + str(distance_between_person_and_paddle)[:3]
                            + ' CM', cm_DST_to_paddle, cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), 2)

                total_height += person_cm_height
                total_distance_paddle_ground += paddle_to_ground_cm
                total_distance_participant_paddle += distance_between_person_and_paddle
                num_participants += 1

        ret, buffer = cv2.imencode('.jpg', image)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    vid.release()

    average_height = int(total_height / num_participants)
    avg_distance_paddle = int(total_distance_paddle_ground / num_participants)
    avg_distance_participant = int(total_distance_participant_paddle / num_participants)

    if average_height >= 180 and 55 <= avg_distance_participant <= 59:
        distance_result = "Paddle distance is correct"
    elif 170 <= average_height <= 179 and 50 <= avg_distance_participant <= 54:
        distance_result = "Paddle distance is correct"
    elif 160 <= average_height <= 169 and 45 <= avg_distance_participant <= 49:
        distance_result = "Paddle distance is correct"
    elif 150 <= average_height <= 159 and 40 <= avg_distance_participant <= 44:
        distance_result = "Paddle distance is correct"
    elif 140 <= average_height <= 149 and 35 <= avg_distance_participant <= 39:
        distance_result = "Paddle distance is correct"
    else:
        distance_result = "Paddle distance is incorrect"


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run()