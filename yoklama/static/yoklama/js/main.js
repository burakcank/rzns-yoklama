document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('rollCallForm');
    const messageDiv = document.getElementById('message');
    const loadingDiv = document.getElementById('loading');
    const submitBtn = document.getElementById('submitBtn');
    const studentSelect = document.getElementById('student');
    const selfConfirmation = document.getElementById('selfConfirmation');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const studentId = studentSelect.value;
        const confirmed = selfConfirmation.checked;

        if (!studentId) {
            showMessage('Lütfen açılır menüden isminizi seçin.', 'error');
            return;
        }

        if (!confirmed) {
            showMessage('Lütfen yalnızca kendiniz için katılım kaydettiğinizi onaylayın.', 'error');
            return;
        }

        // Show loading state
        submitBtn.disabled = true;
        loadingDiv.style.display = 'block';
        hideMessage();

        // Make the check-in request
        fetch('/api/katilim-kaydet/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                student_id: parseInt(studentId),
                confirmed: confirmed
            })
        })
        .then(response => response.json())
        .then(data => {
            loadingDiv.style.display = 'none';
            
            if (data.success) {
                showMessage(data.message + ' ✅', 'success');
                form.reset();
                submitBtn.disabled = false;
            } else {
                showMessage(data.error, 'error');
                submitBtn.disabled = false;
            }
        })
        .catch(error => {
            loadingDiv.style.display = 'none';
            showMessage('Katılımınız kaydedilirken bir hata oluştu. Lütfen tekrar deneyin.', 'error');
            submitBtn.disabled = false;
            console.error('Hata:', error);
        });
    });

    function showMessage(text, type) {
        messageDiv.textContent = text;
        messageDiv.className = `message ${type}`;
        messageDiv.style.display = 'block';
    }

    function hideMessage() {
        messageDiv.style.display = 'none';
    }
});
