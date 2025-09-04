#!/bin/bash
export $(grep -v '^#' .env | xargs)

http POST https://api.anthropic.com/v1/messages \
  Content-Type:application/json \
  x-api-key:"$ANTHROPIC_API_KEY" \
  anthropic-version:2023-06-01 \
  model='claude-sonnet-4-20250514' \
  max_tokens:=1000 \
  messages:='[{"role": "user", "content": "Explain the concept of APIs in one sentence."}]'
