document.addEventListener('DOMContentLoaded', () => {
    const content = document.getElementById('content');
    if (content) {
        content.addEventListener('click', (event) => {
            if (event.target.tagName === 'A') {
                event.preventDefault();
                const topic = event.target.textContent;
                fetch('/recursive_search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ topic: topic }),
                })
                .then(response => response.json())
                .then(data => {
                    content.innerHTML = data.content;
                    document.getElementById('diagram').innerHTML = `
                        <video width="640" height="360" controls>
                            <source src="${data.diagram}" type="video/mp4">
                            Your browser does not support the video tag.
                        </video>
                    `;
                });
            }
        });
    }
});