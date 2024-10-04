from PIL import Image
import numpy as np

def text_to_bin(text):
    """Converts text to binary."""
    binary = ''.join([format(ord(i), '08b') for i in text])
    return binary

def bin_to_text(binary):
    """Converts binary to text."""
    text = ''.join([chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)])
    return text

def hide_data(image_path, data, output11_image):
    """Hides data (text) into the image."""
    # Load the image
    img = Image.open(image_path)
    img = img.convert('RGB')
    np_img = np.array(img)
    
    # Convert data to binary
    binary_data = text_to_bin(data)
    data_len = len(binary_data)
    
    # Flatten the image array
    flat_img = np_img.flatten()
    
    # Ensure the image can store the data
    if data_len > flat_img.size:
        raise ValueError("Data is too large to hide in the image.")
    
    # Embed the binary data into the LSB of the image
    for i in range(data_len):
        # Current pixel value
        pixel_value = flat_img[i]
        
        # Ensure the pixel_value is within the valid range for uint8
        if pixel_value < 0 or pixel_value > 255:
            raise ValueError(f"Invalid pixel value encountered: {pixel_value}")
        
        # Modify the LSB of the pixel to store the binary data bit
        flat_img[i] = (int(pixel_value) & ~1) | int(binary_data[i])
        
        # After modification, ensure the value is within the valid uint8 range
        flat_img[i] = np.clip(flat_img[i], 0, 255)
    
    # Reshape and save the modified image
    new_img = flat_img.reshape(np_img.shape)
    Image.fromarray(new_img.astype(np.uint8)).save(output11_image)
    print(f"[+] Data hidden successfully in {output11_image}")

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
    # 1. Hide data in the image
    original_image = "jesus-today.png"  # Path to the input image (make sure the image exists)
    
    # Hide the message: "Jesus came to save sinners"
    secret_message = "Jesus came to save sinners"
    
    output11_image = "output11_image.png"   # Path to the output image with the hidden data
    
    # Hide the secret message in the image
    hide_data(original_image, secret_message + chr(0), output11_image)
    
    # 2. Extract data from the image
    extracted_message = extract_data(output11_image)
    print(f"Extracted message: {extracted_message}")
