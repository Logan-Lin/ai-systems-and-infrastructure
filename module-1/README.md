Here are two reference programs for the post-lecture exercise, demonstrating the core concepts from the API Fundamentals course. Both programs use the `requests` library to interact directly with Claude's API, providing transparency into HTTP mechanics. They also use the `dotenv` library to load environment variables from the `.env` file, which in this case is used for storing our API keys.

## API Key Setup

### Why Use .env Files?
Storing API keys in `.env` files is a security best practice that prevents accidentally exposing credentials when sharing code.

### Setup Instructions

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Get your Anthropic API key:**
   - Go to https://console.anthropic.com/
   - Sign in or create an account
   - Navigate to "API Keys" section
   - Create a new API key

3. **Edit the .env file:**
   Open `.env` in a text editor and replace `your-api-key-here` with your actual API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
   ```

   The API key format:
   - Starts with `sk-ant-`
   - Followed by additional characters
   - Keep it secret and never commit it to version control

This process works a bit differently for other providers (like OpenAI), but the idea is similar.

## Code Walkthrough

### claude_chatbot.py

An interactive command-line chatbot that demonstrates core API concepts:

- **HTTP Headers:** Sets up authorization (`x-api-key`), content type, and API version
- **Request Body:** Sends JSON payload with model selection and conversation messages
- **Statelessness:** Includes full conversation history in each request (REST principle)
- **Response Parsing:** Extracts assistant's message from JSON response

**Key Features:**
- Maintains conversation context
- Commands: `clear` (reset conversation), `system` (change prompt), `quit`/`exit`
- Error handling for network issues and API errors

### image_analyzer.py

A command-line tool for analyzing images using Claude's vision capabilities:

- **Multi-modal Content:** Sends both text and image in a single API request
- **Base64 Encoding:** Converts binary image data to text format for JSON transport
- **Content-Type Handling:** Maps image formats to appropriate MIME types
- **Same API Endpoint:** Uses the same `/v1/messages` endpoint as text-only requests

**Key Features:**
- Supports jpg, png, gif, webp formats
- Custom prompts via `--prompt` flag
- Comprehensive error handling
- File validation before upload

## Usage Examples

### Running the Chatbot

```bash
python claude_chatbot.py
```

**Sample interaction:**
```
==================================================
Claude Command Line Chatbot
==================================================
Commands:
  • Type 'quit' or 'exit' to end
  • Type 'clear' to reset conversation
  • Type 'system' to change system message
==================================================

You: What are APIs?

Claude:
APIs (Application Programming Interfaces) are standardized ways for different software applications to communicate and share data with each other, acting like a contract that defines how programs can request services and exchange information.

You: Can you give me an example?

Claude:
Sure! A common example is a weather app on your phone. When you open it, the app uses a weather service's API to request current conditions for your location. The API processes this request and sends back data like temperature, humidity, and forecast, which your app then displays in a user-friendly format. The app doesn't need to collect weather data itself—it just asks the weather service's API for the information it needs.

You: clear
Conversation cleared.

You: exit
Goodbye!
```

### Analyzing Images

**Basic usage:**
```bash
python image_analyzer.py photo.jpg
```

**With custom prompt:**
```bash
python image_analyzer.py screenshot.png --prompt "What UI elements are visible in this interface?"
```

**Example output:**
```
==================================================
Analyzing Image: photo.jpg
==================================================
Processing image...

Analysis Result:

This image shows the famous Shibuya Crossing in Tokyo, Japan, captured during what appears to be a quiet moment, likely during the pandemic period given the notably sparse foot traffic.
```

## Understanding the Code

### HTTP Request Components

Both programs demonstrate the three key parts of HTTP requests:

1. **Headers** - Metadata about the request:
   - `x-api-key`: Authentication credential
   - `anthropic-version`: API version specification
   - `content-type`: Indicates JSON payload

2. **Body** - The actual data being sent:
   - JSON format with model, messages, and parameters
   - For images: includes base64-encoded data

3. **Method** - POST for sending data and expecting response

### HTTP Response Handling

The programs parse responses following standard patterns:

- **Status Codes**: Check for 200 (success) vs errors (4xx, 5xx)
- **JSON Parsing**: Extract content from structured response
- **Error Messages**: Parse error details when requests fail

### REST Principles in Practice

1. **Statelessness**: Each request contains complete context (full conversation history)
2. **Uniform Interface**: Same endpoint (`/v1/messages`) for different content types
3. **Standard Methods**: POST for data submission, consistent URL structure

### Security Best Practices

- **Environment Variables**: API keys stored in `.env`, never hardcoded
- **Error Handling**: Sensitive information not exposed in error messages
- **Timeout Settings**: Prevent hanging on slow connections

## Common Issues & Troubleshooting

### "ANTHROPIC_API_KEY not found"
- **Cause**: Missing or incorrectly named `.env` file
- **Solution**: Ensure `.env` exists in the same directory and contains your API key

### "401 Unauthorized" or "Invalid API key"
- **Cause**: Incorrect or expired API key
- **Solution**: Verify your API key in the Anthropic console and update `.env`

### "402 Payment Required" or "Insufficient credits"
- **Cause**: Your API key has no remaining credits or usage quota
- **Solution**: 
  - Check your usage and billing at https://console.anthropic.com/settings/billing
  - Add credits to your account or upgrade your plan
  - For new accounts, ensure you've added a payment method and purchased credits

### "Request timed out"
- **Cause**: Large image file or slow network connection
- **Solution**: Try a smaller image or increase the timeout value in the code

### "Unsupported format"
- **Cause**: Trying to analyze an unsupported image type
- **Solution**: Convert image to jpg, png, gif, or webp format

### "429 Too Many Requests"
- **Cause**: Hitting API rate limits
- **Solution**: Wait a few moments before making more requests

### Network Errors
- **Cause**: No internet connection or firewall blocking
- **Solution**: Check your internet connection and firewall settings

