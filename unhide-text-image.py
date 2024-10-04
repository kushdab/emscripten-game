from PIL import Image
import numpy as np

def extract_data(image_path):
    """Extracts hidden data from the image."""
    # Load the image
    img = Image.open(image_path)
    img = img.convert('RGB')
    np_img = np.array(img)
    
    # Flatten the image array
    flat_img = np_img.flatten()
    
    # Extract the LSBs to retrieve the hidden binary data
    binary_data = ''
    for pixel in flat_img:
        binary_data += str(pixel & 1)
    
    # Convert binary data back to text
    text = ''
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        # Stop when null terminator (00000000) is reached
        if byte == '00000000':
            break
        text += chr(int(byte, 2))
    
    return text

if __name__ == "__main__":
    # Path to the image where the secret message is hidden
    hidden_image = "output11_image.png"  # Replace with the actual name of your image file
    
    # Extract and print the hidden message
    secret_message = extract_data(hidden_image)
    print(f"Extracted message: {secret_message}")
