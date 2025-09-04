#!/usr/bin/env python3
"""
Example implementation for API Fundamentals course.
Demonstrates multi-modal content handling, base64 encoding, and content-type management.
"""

import os
import sys
import base64  # For encoding binary image data to text format
import json
import requests  # Direct HTTP interaction for educational transparency
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Security: Load sensitive data from environment
load_dotenv()

# Content-Type handling: Different image formats require different MIME types
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}


def encode_image(image_path: str) -> tuple[str, str]:
    """Encode image to base64 and return with media type.
    
    Base64 encoding converts binary image data to text format,
    allowing images to be included in JSON payloads.
    Alternative to multipart/form-data for simpler implementation.
    """
    path = Path(image_path)
    suffix = path.suffix.lower()
    
    # Map file extensions to MIME types (media types)
    # These tell the API how to interpret the image data
    if suffix == '.jpg':
        media_type = "image/jpeg"
    elif suffix == '.jpeg':
        media_type = "image/jpeg"
    elif suffix == '.png':
        media_type = "image/png"
    elif suffix == '.gif':
        media_type = "image/gif"
    elif suffix == '.webp':
        media_type = "image/webp"
    else:
        raise ValueError(f"Unsupported image format: {suffix}")
    
    # Read binary image data and encode to base64 text
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')
    
    return encoded, media_type


def analyze_image(image_path: str, prompt: str = None) -> str:
    """Analyze image using OpenAI API.
    
    Demonstrates sending multi-modal content (text + image)
    through a single API endpoint.
    """
    # Security best practice: API key from environment, never hardcoded
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.", file=sys.stderr)
        print("Please create a .env file with your API key:")
        print("OPENAI_API_KEY=your-api-key-here")
        sys.exit(1)
    
    # Same endpoint as text-only chatbot - REST uniform interface principle
    # The API determines behavior based on content, not different URLs
    api_url = "https://api.openai-proxy.org/v1/chat/completions"
    
    try:
        base64_image, media_type = encode_image(image_path)
        
        user_prompt = prompt or "Please analyze this image and describe what you see in detail."
        
        # HTTP Headers - same structure as text-only requests
        headers = {
            "Authorization": f"Bearer {api_key}",  # Bearer token authentication (OpenAI format)
            "Content-Type": "application/json"     # We're sending JSON (with embedded base64)
        }
        
        # Multi-modal content in request body (OpenAI format)
        payload = {
            "model": "gpt-4o-mini",  # OpenAI's vision-capable model
            "max_tokens": 4096,
            "messages": [{
                "role": "user",
                # Content array can mix different types (text, image, etc.)
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{media_type};base64,{base64_image}"  # Data URL format
                        }
                    }
                ]
            }]
        }
        
        # POST request with longer timeout for image processing
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=60  # Larger timeout for image uploads and processing
        )
        
        # HTTP Status Code checking - essential for robust API interaction
        if response.status_code != 200:
            # Parse error response for helpful debugging info
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', f'API Error: {response.status_code}')
            raise Exception(error_msg)
        
        # Extract text response from OpenAI's response structure
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
        
    # Comprehensive error handling for different failure modes
    except requests.exceptions.Timeout:
        raise Exception("Request timed out - the image may be too large or the API is slow")
    except requests.exceptions.RequestException as e:
        # Network-level errors (connection, DNS, etc.)
        raise Exception(f"Network error: {str(e)}")
    except Exception as e:
        # API-level or parsing errors
        raise Exception(f"Error analyzing image: {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze images using OpenAI GPT-4o-mini",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example:\n  python image_analyzer.py photo.jpg\n  python image_analyzer.py photo.png --prompt 'What objects are in this image?'"
    )
    
    parser.add_argument('image_path', help='Path to the image file')
    parser.add_argument(
        '--prompt', '-p',
        help='Custom prompt for image analysis (default: general description)',
        default=None
    )
    
    args = parser.parse_args()
    
    # Validate image path
    image_path = Path(args.image_path)
    
    if not image_path.exists():
        print(f"Error: File not found: {args.image_path}", file=sys.stderr)
        sys.exit(1)
    
    if not image_path.is_file():
        print(f"Error: Not a file: {args.image_path}", file=sys.stderr)
        sys.exit(1)
    
    if image_path.suffix.lower() not in SUPPORTED_FORMATS:
        print(f"Error: Unsupported format: {image_path.suffix}", file=sys.stderr)
        print(f"Supported formats: {', '.join(SUPPORTED_FORMATS)}")
        sys.exit(1)
    
    # Analyze image
    print("="*50)
    print(f"Analyzing Image: {image_path.name}")
    print("="*50)
    
    print("Processing image...")
    try:
        result = analyze_image(str(image_path), args.prompt)
        
        print("\nAnalysis Result:\n")
        print(result)
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
