import mediapipe as mp


def draw_face_mesh(image, face_landmarks):
    # 描画
    mp_drawing = mp.solutions.drawing_utils
    mp_face_mesh = mp.solutions.face_mesh

    # 顔のメッシュを描画
    drawing_specs = [
        (mp_face_mesh.FACEMESH_TESSELATION, (0, 255, 0), 1, 1),
        (mp_face_mesh.FACEMESH_CONTOURS, (255, 0, 0), 2, 0.5),
        (mp_face_mesh.FACEMESH_IRISES, (0, 0, 255), 1, 1),
    ]

    for connections, color, thickness, circle_radius in drawing_specs:
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=connections,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing.DrawingSpec(
                color=color, thickness=thickness, circle_radius=circle_radius
            ),
        )
