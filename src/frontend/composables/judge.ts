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
        if (expressions.surprised > 0.85) {
            emotion.value = { show: "びっくり", judge: "surprised" };
        } else if (expressions.disgusted > 0.85) {
            emotion.value = { show: "嫌そうな顔...", judge: "disgusted" };
        } else if (expressions.fearful > 0.85) {
            emotion.value = { show: "怖がってる？", judge: "fearful" };
        } else if (expressions.angry > 0.85) {
            emotion.value = { show: "怒ってる？", judge: "angry" };
        } else if (expressions.sad > 0.85) {
            emotion.value = { show: "悲しそう...", judge: "sad" };
        } else if (expressions.happy > 0.85) {
            emotion.value = { show: "嬉しそう！", judge: "happy" };
        } else {
            emotion.value = { show: "無表情", judge: "neutral" };
        }
    }
    return emotion.value;
}
