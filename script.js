document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const resultSection = document.getElementById('result-section');
    const riskBadge = document.getElementById('risk-badge');
    const riskText = document.getElementById('risk-text');
    const confidenceBar = document.getElementById('confidence-bar');
    const confidenceValue = document.getElementById('confidence-value');
    const predictBtn = document.querySelector('.btn-predict');
    const resetBtn = document.getElementById('reset-btn');
    const loadingState = document.getElementById('loading-state');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Show loading state
        const originalBtnText = predictBtn.innerHTML;
        predictBtn.innerHTML = '⚙️ Analyzing...';
        predictBtn.disabled = true;
        resultSection.classList.add('hidden');
        loadingState.classList.add('hidden');

        // Gather form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Convert string values to numbers where necessary
        for (let key in data) {
            data[key] = parseFloat(data[key]);
        }

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();
            
            // Show result
            displayResult(result);
            
        } catch (error) {
            console.error('Error:', error);
            loadingState.classList.remove('hidden');
            loadingState.innerHTML = '<p>ML service unavailable. Please check backend connection or wait for model to load.</p>';
        } finally {
            predictBtn.innerHTML = originalBtnText;
            predictBtn.disabled = false;
        }
    });

    resetBtn.addEventListener('click', () => {
        resultSection.classList.add('hidden');
        loadingState.classList.add('hidden');
    });

    function displayResult(result) {
        resultSection.classList.remove('hidden');
        loadingState.classList.add('hidden');

        // Update confidence bar and text
        const confidenceScore = Math.round(result.probability * 100);
        confidenceBar.style.width = `${confidenceScore}%`;
        confidenceValue.textContent = `${confidenceScore}% confidence`;

        // Update risk styling
        riskBadge.className = 'risk-badge'; // reset
        confidenceBar.className = 'progress-bar'; // reset

        if (result.prediction === 1) {
            riskBadge.classList.add('risk-high');
            riskBadge.innerHTML = '<span class="icon">⚠️</span> <span id="risk-text">High Risk</span>';
            confidenceBar.classList.add('progress-high');
        } else {
            riskBadge.classList.add('risk-low');
            riskBadge.innerHTML = '<span class="icon">✅</span> <span id="risk-text">Low Risk</span>';
            confidenceBar.classList.add('progress-low');
        }
        
        // Scroll to result slightly delayed for smooth UX
        setTimeout(() => {
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }, 100);
    }
});
