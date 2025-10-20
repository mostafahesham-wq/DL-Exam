const form = document.getElementById('predictionForm');
const loading = document.getElementById('loading');
const resultDiv = document.getElementById('result');
const predictionText = document.getElementById('predictionText');
const probabilityText = document.getElementById('probabilityText');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    loading.style.display = 'block';
    resultDiv.style.display = 'none';

    // جمع البيانات من الفورم
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => data[key] = parseFloat(value));

    try {
        const response = await fetch('http://127.0.0.1:8000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': '1234567890abcdef' // استبدل بالمفتاح الصح
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            // لو فيه خطأ من السيرفر
            throw new Error(JSON.stringify(result, null, 2));
        }

        // عرض النتيجة على الـ UI
        predictionText.innerText = `Prediction: ${result.class_name} (${result.prediction})`;
        probabilityText.innerText = `Probability: ${(result.probability * 100).toFixed(2)}%`;
        resultDiv.style.display = 'block';
    } catch (err) {
        // عرض الأخطاء بشكل واضح
        resultDiv.style.display = 'block';
        predictionText.inne
