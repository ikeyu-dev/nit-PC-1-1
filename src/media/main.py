import time
import cv2
import mediapipe as mp

# 描画
mp_drawing = mp.solutions.drawing_utils
# 顔メッシュ
mp_face_mesh = mp.solutions.face_mesh

# カメラ
cap = cv2.VideoCapture(0)

# 笑顔判定変数を初期化
smile: bool = False

with mp_face_mesh.FaceMesh(
    max_num_faces=100,  # 検出する顔max数
    refine_landmarks=True,  # 唇やまぶた周りのランドマークを詳細に取得
    min_detection_confidence=0.5,  # 検出の信頼度
    min_tracking_confidence=0.5,  # トラッキングの信頼度
) as face_mesh:

    while cap.isOpened():
        _, image = cap.read()

        # パフォーマンス向上のため画像を書き込み不可として参照渡しする
        image.flags.writeable = False
        # MediapipeはRGB形式を期待するのでBGRをRGBに変換
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image_rgb)

        # 描画のために画像を書き込み可に戻す
        image.flags.writeable = True

        # 表示用にBGRに戻す
        # image = cv2.cvtColor(
        #     image_rgb, cv2.COLOR_RGB2BGR
        # )

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # 唇と瞼の座標から笑顔を判定

                # 開口部
                upper_lip_bottom = face_landmarks.landmark[13]  # 上唇の下部
                lower_lip_top = face_landmarks.landmark[14]  # 下唇の上部

                # 唇の中心点と端
                lip_center_point = face_landmarks.landmark[14]  # 唇の中心点
                lip_corner_left = face_landmarks.landmark[61]  # 左唇の端
                lip_corner_right = face_landmarks.landmark[291]  # 右唇の端

                # 瞼
                left_eye_top = face_landmarks.landmark[159]  # 左目の上部
                left_eye_bottom = face_landmarks.landmark[145]  # 左目の下部

                # 距離を計算
                mouth_opening_degree = abs(
                    upper_lip_bottom.y - lower_lip_top.y
                )  # 唇の開き度合い

                eyelid_opening_degree = abs(
                    left_eye_top.y - left_eye_bottom.y
                )  # 瞼の開き度合い

                lip_coner_up = abs(
                    (
                        abs(lip_center_point.y - lip_corner_left.y)
                        + abs(lip_center_point.y - lip_corner_right.y)
                    )
                    / 2
                )  # 口角の上がり度合いの平均

                smile = (
                    True
                    if mouth_opening_degree > 0.03
                    and eyelid_opening_degree < 0.03
                    and lip_coner_up > 0.03
                    else (
                        True
                        if lip_coner_up > 0.03 and eyelid_opening_degree < 0.03
                        else False
                    )
                )  # 笑顔の判定

                # TODO: 笑顔以外の表情判定についても実装する

                # 顔のメッシュを描画
                mp_drawing.draw_landmarks(
                    # 描画する画像
                    image=image,
                    # ランドマーク
                    landmark_list=face_landmarks,
                    # 顔におけるメッシュ線
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    # ランドマークの描画スタイル
                    landmark_drawing_spec=None,
                    # 線の描画スタイル
                    connection_drawing_spec=mp_drawing.DrawingSpec(
                        color=(0, 255, 0), thickness=1, circle_radius=1
                    ),
                )

                # 顔の輪郭を描画
                mp_drawing.draw_landmarks(
                    # 描画する画像
                    image=image,
                    # ランドマーク
                    landmark_list=face_landmarks,
                    # 輪郭線
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    # ランドマークの描画スタイル
                    landmark_drawing_spec=None,
                    # 線の描画スタイル
                    connection_drawing_spec=mp_drawing.DrawingSpec(
                        color=(255, 0, 0), thickness=2, circle_radius=0.5
                    ),
                )

                # 虹彩の輪郭を描画
                mp_drawing.draw_landmarks(
                    # 描画する画像
                    image=image,
                    # ランドマーク
                    landmark_list=face_landmarks,
                    # 目の周りのメッシュ線
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    # ランドマークの描画スタイル
                    landmark_drawing_spec=None,
                    # 線の描画スタイル
                    connection_drawing_spec=mp_drawing.DrawingSpec(
                        color=(0, 0, 255), thickness=1, circle_radius=1
                    ),
                )
        #  表示
        cv2.putText(
            image,
            f"smile: {smile}",  # 表示する文字列
            (10, 30),  # 文字の位置
            cv2.FONT_HERSHEY_SIMPLEX,  # フォント
            1,  # フォントサイズ
            (0, 255, 0),
            2,  # フォントの太さ
        )
        cv2.imshow("Mediapipe Face Mesh", image)

        # TODO: 画像をfastAPIに送信する処理を追加

        # qキー押すと終了
        if cv2.waitKey(5) & 0xFF == ord("q"):
            break

# カメラを解放
cap.release()
cv2.destroyAllWindows()
