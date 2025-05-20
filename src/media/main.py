import cv2
import mediapipe as mp
from landmarks import LandmarksNumber


def main():
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

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # 唇と瞼の座標から笑顔を判定

                    # 開口部
                    upper_lip_bottom = face_landmarks.landmark[
                        LandmarksNumber.upper_lip_bottom
                    ]  # 上唇の下部
                    lower_lip_top = face_landmarks.landmark[
                        LandmarksNumber.lower_lip_top
                    ]  # 下唇の上部

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
                    left_eye_top = face_landmarks.landmark[
                        LandmarksNumber.left_eye_top
                    ]  # 左目の上部
                    left_eye_bottom = face_landmarks.landmark[
                        LandmarksNumber.left_eye_bottom
                    ]  # 左目の下部
                    right_eye_top = face_landmarks.landmark[
                        LandmarksNumber.right_eye_top
                    ]  # 右目の上部
                    right_eye_bottom = face_landmarks.landmark[
                        LandmarksNumber.right_eye_bottom
                    ]  # 右目の下部

                    # 距離を計算
                    mouth_opening_degree = abs(
                        upper_lip_bottom.y - lower_lip_top.y
                    )  # 唇の開き度合い

                    eyelid_opening_degree = abs(
                        (
                            abs(left_eye_top.y - left_eye_bottom.y)
                            + abs(right_eye_top.y - right_eye_bottom.y)
                        )
                        / 2
                    )  # 瞼の開き度合い(左右平均値)

                    lip_coner_up = abs(
                        (
                            abs(lip_center_point.y - lip_corner_left.y)
                            + abs(lip_center_point.y - lip_corner_right.y)
                        )
                        / 2
                    )  # 口角の上がり度合い(左右平均値)

                    smile = (
                        True
                        if mouth_opening_degree > 0.03
                        and eyelid_opening_degree < 0.03
                        and lip_coner_up > 0.03
                        else (
                            True
                            if lip_coner_up > 0.04 and eyelid_opening_degree < 0.02
                            else False
                        )
                    )  # 笑顔の判定

                    # TODO: 笑顔以外の表情判定についても実装する

                    # 顔のメッシュを描画
                    mp_drawing.draw_landmarks(
                        image=image,  # 描画する画像
                        landmark_list=face_landmarks,  # ランドマーク
                        connections=mp_face_mesh.FACEMESH_TESSELATION,  # 顔におけるメッシュ線
                        landmark_drawing_spec=None,  # ランドマークの描画スタイル
                        connection_drawing_spec=mp_drawing.DrawingSpec(
                            color=(0, 255, 0), thickness=1, circle_radius=1
                        ),  # 線の描画スタイル
                    )

                    # 顔の輪郭を描画
                    mp_drawing.draw_landmarks(
                        image=image,  # 描画する画像
                        landmark_list=face_landmarks,  # ランドマーク
                        connections=mp_face_mesh.FACEMESH_CONTOURS,  # 輪郭線
                        landmark_drawing_spec=None,  # ランドマークの描画スタイル
                        connection_drawing_spec=mp_drawing.DrawingSpec(
                            color=(255, 0, 0), thickness=2, circle_radius=0.5
                        ),  # 線の描画スタイル
                    )

                    # 虹彩の輪郭を描画
                    mp_drawing.draw_landmarks(
                        image=image,  # 描画する画像
                        landmark_list=face_landmarks,  # ランドマーク
                        connections=mp_face_mesh.FACEMESH_IRISES,  # 目の周りのメッシュ線
                        landmark_drawing_spec=None,  # ランドマークの描画スタイル
                        connection_drawing_spec=mp_drawing.DrawingSpec(
                            color=(0, 0, 255), thickness=1, circle_radius=1
                        ),  # 線の描画スタイル
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


if __name__ == "__main__":
    main()
