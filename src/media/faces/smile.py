import numpy as np
from landmarks import LandmarksNumber


def isSmile(face_landmarks):
    # 唇と瞼の座標から笑顔を判定

    # 開口部
    upper_lip_bottom = face_landmarks.landmark[
        LandmarksNumber.upper_lip_bottom
    ]  # 上唇の下部
    lower_lip_top = face_landmarks.landmark[LandmarksNumber.lower_lip_top]  # 下唇の上部

    # 唇の中心点と端
    lip_center_point = face_landmarks.landmark[
        LandmarksNumber.lip_center_point
    ]  # 唇の中心点
    lip_corner_left = face_landmarks.landmark[
        LandmarksNumber.lip_corner_left
    ]  # 左唇の端
    lip_corner_right = face_landmarks.landmark[
        LandmarksNumber.lip_corner_right
    ]  # 右唇の端

    # 瞼
    left_eye_top = face_landmarks.landmark[LandmarksNumber.left_eye_top]  # 左目の上部
    left_eye_bottom = face_landmarks.landmark[
        LandmarksNumber.left_eye_bottom
    ]  # 左目の下部
    right_eye_top = face_landmarks.landmark[LandmarksNumber.right_eye_top]  # 右目の上部
    right_eye_bottom = face_landmarks.landmark[
        LandmarksNumber.right_eye_bottom
    ]  # 右目の下部

    # 距離を計算
    mouth_opening_degree = abs(upper_lip_bottom.y - lower_lip_top.y)  # 唇の開き度合い

    eyelid_opening_degree = abs(
        np.mean(
            [
                abs(left_eye_top.y - left_eye_bottom.y),
                abs(right_eye_top.y - right_eye_bottom.y),
            ]
        )
    )  # 瞼の開き度合い(左右平均値)

    lip_coner_up = abs(
        np.mean(
            [
                abs(lip_center_point.y - lip_corner_left.y),
                abs(lip_center_point.y - lip_corner_right.y),
            ]
        )
    )  # 口角の上がり度合い(左右平均値)

    # smile = (
    #     True
    #     if mouth_opening_degree > 0.03
    #     and eyelid_opening_degree < 0.03
    #     and lip_coner_up > 0.03
    #     else (True if lip_coner_up > 0.04 and eyelid_opening_degree < 0.02 else False)
    # )  # 笑顔の判定
    smile = eyelid_opening_degree < 0.03 and lip_coner_up > 0.03
    return smile
