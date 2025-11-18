const form = document.getElementById('post-form');
const resultEl = document.getElementById('result');
const statusEl = document.getElementById('status');
const copyBtn = document.getElementById('copy-btn');
const contactForm = document.getElementById('contact-form');
const contactStatus = document.getElementById('contact-status');

if (form) {
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        statusEl.textContent = 'Generating personalized copy…';
        resultEl.innerHTML = '<p class="placeholder">Hold tight while we analyze your previous posts.</p>';

        const payload = {
            tag: form.tag.value,
            length: form.length.value,
            language: form.language.value,
        };

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            const json = await response.json();
            if (!response.ok || json.error) {
                throw new Error(json.error || 'Unable to generate content.');
            }

            resultEl.textContent = json.post;
            statusEl.textContent = 'Post ready. Adjust selections to explore more.';
        } catch (error) {
            statusEl.textContent = error.message;
            resultEl.innerHTML = '<p class="placeholder">We hit a snag. Update your inputs or try again in a moment.</p>';
        }
    });
}

if (copyBtn) {
    copyBtn.addEventListener('click', async () => {
        const text = resultEl.textContent.trim();
        if (!text) {
            statusEl.textContent = 'Generate a post before copying.';
            return;
        }

        try {
            await navigator.clipboard.writeText(text);
            statusEl.textContent = 'Copied to clipboard.';
        } catch (error) {
            statusEl.textContent = 'Clipboard unavailable. Select and copy manually.';
        }
    });
}

if (contactForm) {
    contactForm.addEventListener('submit', (event) => {
        event.preventDefault();
        contactStatus.textContent = 'Thanks! We will reach out shortly.';
        contactForm.reset();
    });
}
