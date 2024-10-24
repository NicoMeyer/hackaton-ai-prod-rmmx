#!/bin/sh -l

echo "Hello, $1 | $2 | $3 | $4 | $5 | $6 | $7\n"
python /main.py --openai-api-key "$1" --github-token "$2" --github-pr-id "$3" --dev-lang "$4" --openai-engine "$5" --openai-temperature "$6" --openai-max-tokens "$7"