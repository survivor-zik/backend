document.addEventListener('DOMContentLoaded', () => {
    const imageContainer = document.getElementById('image-container');

    // Fetch the images from the FastAPI endpoint
    fetch('http://localhost:8000/products/images/')
        .then(response => response.json())
        .then(images => {
            images.forEach(image => {
                // Create a new image element
                const img = document.createElement('img');
                img.src = `data:image/jpeg;base64,${image.image_data}`;
                img.alt = image.image_name;
                img.style.width = '200px'; // You can adjust the size as needed
                img.style.margin = '10px';
                console.log(img.alt)
                // Append the image to the container
                imageContainer.appendChild(img);
            });
        })
        .catch(error => console.error('Error fetching images:', error));
});
