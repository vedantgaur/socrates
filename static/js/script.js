document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('search-form');
    const gifContainer = document.getElementById('gif-container');
    const scrollArrow = document.getElementById('scroll-arrow');

    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        const query = form.querySelector('input[name="query"]').value;

        // Show the rabbit GIF briefly
        gifContainer.style.display = 'block';
        setTimeout(() => {
            gifContainer.style.display = 'none';
        }, 700); // Show for 2 seconds

        try {
            const response = await fetch('/process_query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }

            const data = await response.json();
            console.log('Received data:', data);

            // Handle data (e.g., display content, animation, music)
            document.getElementById('content').innerText = data.content;
            document.getElementById('content').style.display = 'block';

            // Show the arrow after query processing
            scrollArrow.style.display = 'block';

            // Optionally handle animation and music if provided
            if (data.animation) {
                // Handle animation
            }
            if (data.music) {
                // Handle music
            }

        } catch (error) {
            console.error('Error fetching the query:', error);
        }
    });
});
