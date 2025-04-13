function toggleDarkMode() {
    const isDark = document.body.classList.toggle('dark-mode');

    fetch('/set-dark-mode/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'dark_mode=' + isDark
    });
}

const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
