export async function judge(detections: string) {
    const detectionData = !detections ? [] : JSON.parse(detections);
    const emotion = ref<{ show: string; judge: string }>({
        show: "",
        judge: "",
    });
    if (detectionData.length === 0) {
        emotion.value = { show: "表情が検出されませんでした", judge: "none" };
        return;
    } else {
        const expressions = detectionData[0].expressions;
        const emotionMap = [
            { threshold: 0.99, expression: "surprised", show: "びっくり" },
            { threshold: 0.99, expression: "disgusted", show: "嫌そうな顔..." },
            { threshold: 0.99, expression: "fearful", show: "怖がってる？" },
            { threshold: 0.99, expression: "angry", show: "怒ってる？" },
            { threshold: 0.99, expression: "sad", show: "悲しそう..." },
            { threshold: 0.99, expression: "happy", show: "嬉しそう！" },
        ];

        const matchedEmotion = emotionMap.find(
            ({ threshold, expression }) => expressions[expression] > threshold
        );

        emotion.value = matchedEmotion
            ? { show: matchedEmotion.show, judge: matchedEmotion.expression }
            : { show: "無表情", judge: "neutral" };
    }
    return emotion.value;
}
