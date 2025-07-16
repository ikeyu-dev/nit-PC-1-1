import { drawConnectors } from "@mediapipe/drawing_utils";
import {
    FACEMESH_FACE_OVAL, // 顔の輪郭
    FACEMESH_LEFT_EYE, // 左の目
    FACEMESH_LEFT_EYEBROW, // 左の眉
    FACEMESH_LEFT_IRIS, // 左の瞳
    FACEMESH_LIPS, // 唇
    FACEMESH_RIGHT_EYE, // 右の目
    FACEMESH_RIGHT_EYEBROW, // 右の眉
    FACEMESH_RIGHT_IRIS, // 右の瞳
    FACEMESH_TESSELATION, // 顔の表面(埋め尽くし)
} from "@mediapipe/face_mesh";
import type { NormalizedLandmark, Results } from "@mediapipe/face_mesh";
// NormalizedLandmark = 顔のランドマークの座標を表すオブジェクト。x, y, zプロパティを持つ
// Results = 顔の検出結果を含むオブジェクト。multiFaceLandmarksプロパティに複数のランドマークが格納されている
import { judge } from "~/composables/judge";

/**
 * canvasに描画
 * @param ctx コンテキスト
 * @param results 検出結果
 * @param bgImage capture imageを描画するか
 * @param emphasis 強調するlandmarkのindex
 * @param detections 検出結果の文字列
 */
export const draw = async (
    ctx: CanvasRenderingContext2D,
    results: Results,
    bgImage: boolean, // capture imageを描画するか
    emphasis: number[],
    detections: string
) => {
    const width = ctx.canvas.width; // canvasの幅
    const height = ctx.canvas.height; // canvasの高さ

    ctx.save(); // 現在のコンテキストを保存
    ctx.clearRect(0, 0, width, height); // canvasをクリア
    ctx.translate(width, 0);
    ctx.scale(-1, 1);

    // 背景にビデオフレームを描画
    if (bgImage) {
        ctx.drawImage(results.image, 0, 0, width, height); // 画像、x座標、y座標、幅、高さ
    }

    const tesselation = { color: "#f3f3f3", lineWidth: 0.2 }; // 顔の表面(埋め尽くし)のスタイル
    const right_eye = { color: "#FF0000", lineWidth: 2 }; // 右の目・眉・瞳のスタイルを強調
    const left_eye = { color: "#3eb370", lineWidth: 2 }; // 左の目・眉・瞳のスタイルを強調
    const face_oval = { color: "#E0E0E0", lineWidth: 1 }; // 顔の輪郭のスタイル

    for (const landmarks of results.multiFaceLandmarks) {
        // 顔の表面（埋め尽くし）
        drawConnectors(ctx, landmarks, FACEMESH_TESSELATION, tesselation);
        // 右の目・眉・瞳
        drawConnectors(ctx, landmarks, FACEMESH_RIGHT_EYE, right_eye);
        drawConnectors(ctx, landmarks, FACEMESH_RIGHT_EYEBROW, right_eye);
        drawConnectors(ctx, landmarks, FACEMESH_RIGHT_IRIS, right_eye);
        // 左の目・眉・瞳
        drawConnectors(ctx, landmarks, FACEMESH_LEFT_EYE, left_eye);
        drawConnectors(ctx, landmarks, FACEMESH_LEFT_EYEBROW, left_eye);
        drawConnectors(ctx, landmarks, FACEMESH_LEFT_IRIS, left_eye);
        // 顔の輪郭
        drawConnectors(ctx, landmarks, FACEMESH_FACE_OVAL, face_oval);
        // 唇
        drawConnectors(ctx, landmarks, FACEMESH_LIPS, face_oval);

        for (let i = 0; i < emphasis.length; i++) {
            const emphasisLandmark = landmarks[
                emphasis[i]
            ] as NormalizedLandmark;
            const x = emphasisLandmark.x * width; // x座標
            const y = emphasisLandmark.y * height; // y座標
            ctx.beginPath();
            ctx.arc(x, y, 5, 0, 2 * Math.PI); // 円を描く
            ctx.fillStyle = "red"; // 強調表示の色
            ctx.fill(); // 円を塗りつぶす

            ctx.font = "12px Arial";
            ctx.fillStyle = "white"; // 番号の色
            ctx.fillText(emphasis[i].toString(), x, y); // landmarkの番号を表示
        }
        const detectionData = JSON.parse(detections);
        // surprised: 驚き
        // disgusted: 嫌悪
        // fearful: 恐怖
        // angry: 怒り
        // sad: 悲しみ
        // happy: 幸福・喜び
        // neutral: 中立・無表情
        for (const detection of detectionData) {
            const box: {
                _x: number;
                _y: number;
                _width: number;
                _height: number;
            } = detection.box;
            const expressions: [] = detection.expressions;

            // BOXを描画
            ctx.beginPath();
            ctx.rect(box._x, box._y, box._width, box._height);
            ctx.lineWidth = 2;
            ctx.strokeStyle = "blue";
            ctx.stroke();

            // Reset transformation matrix for text
            ctx.save();
            ctx.setTransform(1, 0, 0, 1, 0, 0); // setTransform(a:水平移動, b:傾き, c:垂直傾き, d:垂直移動, e:水平移動, f:垂直移動)

            // BOXにラベルを描画
            let yOffset = box._y - 10;
            ctx.font = "15px Arial";
            ctx.fillStyle = "white";
            for (const [expression, value] of Object.entries(expressions)) {
                const emotionDrawText = `${expression}: ${(
                    (value as number) * 100
                ).toFixed(2)}%`;
                ctx.fillText(emotionDrawText, width - box._x, yOffset);
                yOffset -= 18;
            }
            ctx.restore();
        }
    }
    ctx.restore();
    const emotionJudgeResult = await judge(detections);
    return emotionJudgeResult;
};
