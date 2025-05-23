import cv2
import mediapipe as mp
from faces.smile import isSmile
from drawing import draw_face_mesh


def main():
    # 顔メッシュ
    mp_face_mesh = mp.solutions.face_mesh

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

                    # TODO: 笑顔以外の表情判定についても実装する
                    smile = isSmile(face_landmarks)

                    draw_face_mesh(image, face_landmarks)

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
