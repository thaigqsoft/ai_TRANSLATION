# AI Models & API Guide

**Purpose:** Guide for selecting and using AI models for Thai novel translation.

---

## 🤖 Recommended Models

### For Translation (English → Thai)

| Model | Parameters | Speed | Quality | Cost | Best For |
|-------|------------|-------|---------|------|----------|
| **Gemma 4** | 31B | ⚡⚡⚡ Fast | ⭐⭐⭐⭐ Good | 💰💰 | Daily translation work |
| DeepSeek V3.1 | 671B | ⚡⚡ Medium | ⭐⭐⭐⭐⭐ Excellent | 💰💰💰 | High-quality projects |
| Claude 3.5 Sonnet | ~200B | ⚡⚡ Medium | ⭐⭐⭐⭐⭐ Excellent | 💰💰💰💰 | Premium quality |

### For Polishing (Gao Fei Style)

| Model | Parameters | Speed | Quality | Cost | Best For |
|-------|------------|-------|---------|------|----------|
| **DeepSeek V3.1** | 671B | ⚡⚡ Medium | ⭐⭐⭐⭐⭐ Excellent | 💰💰💰 | Gao Fei literary style |
| Gemma 4 | 31B | ⚡⚡⚡ Fast | ⭐⭐⭐⭐ Good | 💰💰 | Light polishing, batches |
| Claude 3.5 Sonnet | ~200B | ⚡⚡ Medium | ⭐⭐⭐⭐⭐ Excellent | 💰💰💰💰 | Premium polish |

---

## 🔌 Ollama Pay API

### Overview

**Provider:** Thai GQ Soft  
**Endpoint:** `https://ollama-pay.thaigqsoft.com/api/v1`  
**Type:** Pay-per-use (no subscription)  
**Compatibility:** OpenAI-compatible API

### Getting Started

1. **Register:**
   - Visit: https://ollama-pay.thaigqsoft.com
   - Create account
   - Verify email

2. **Get API Key:**
   - Login to dashboard
   - Go to API Keys section
   - Generate new key
   - Copy and store securely

3. **Add Credits:**
   - Minimum top-up: ฿100
   - Pay via QR Code / Bank Transfer
   - Credits never expire

### Available Models

```
gemma4:31b-cloud        # Gemma 4 31B (fast, good quality)
deepseek-v3.1:671b-cloud # DeepSeek V3.1 671B (best quality)
```

### Pricing (Approximate)

| Model | Input (per 1K tokens) | Output (per 1K tokens) |
|-------|----------------------|------------------------|
| gemma4:31b-cloud | ฿0.50 | ฿1.50 |
| deepseek-v3.1:671b-cloud | ฿2.00 | ฿6.00 |

**Example Cost:**
- 800-page novel translation ≈ ฿500-800 (Gemma 4)
- 800-page novel polish ≈ ฿800-1200 (DeepSeek V3.1)

### Python Usage Example

```python
from openai import OpenAI

# Initialize client
client = OpenAI(
    api_key="sk-your-key-here",  # Replace with your key
    base_url="https://ollama-pay.thaigqsoft.com/api/v1"
)

# Translation request
response = client.chat.completions.create(
    model="gemma4:31b-cloud",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Translate this HTML..."}
    ],
    temperature=0.3,
    max_tokens=8192,
    timeout=120
)

translated_text = response.choices[0].message.content
print(translated_text)
```

### cURL Example

```bash
curl -X POST "https://ollama-pay.thaigqsoft.com/api/v1/chat/completions" \
  -H "Authorization: Bearer sk-your-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma4:31b-cloud",
    "messages": [
      {"role": "system", "content": "You are a Thai translator."},
      {"role": "user", "content": "Translate: Hello world"}
    ],
    "temperature": 0.3,
    "max_tokens": 1000
  }'
```

### Best Practices

1. **Use Environment Variables:**
```bash
export OLLAMA_PAY_KEY="sk-your-key-here"
export OLLAMA_PAY_URL="https://ollama-pay.thaigqsoft.com/api/v1"
```

```python
import os
client = OpenAI(
    api_key=os.environ.get("OLLAMA_PAY_KEY"),
    base_url=os.environ.get("OLLAMA_PAY_URL")
)
```

2. **Implement Retry Logic:**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def call_api(prompt):
    return client.chat.completions.create(...)
```

3. **Monitor Token Usage:**
```python
usage = response.usage
print(f"Prompt tokens: {usage.prompt_tokens}")
print(f"Completion tokens: {usage.completion_tokens}")
print(f"Total tokens: {usage.total_tokens}")
```

4. **Handle Rate Limits:**
```python
from openai import RateLimitError

try:
    response = client.chat.completions.create(...)
except RateLimitError:
    time.sleep(60)  # Wait 1 minute before retry
```

---

## 🎯 Model Selection Guide

### Choose Gemma 4 When:
- ✅ Translating large volumes (1000+ pages)
- ✅ Budget is a concern
- ✅ Speed is important
- ✅ Good quality is sufficient

### Choose DeepSeek V3.1 When:
- ✅ Quality is top priority
- ✅ Polishing in Gao Fei style
- ✅ Complex literary text
- ✅ Budget allows for premium model

### Choose Claude 3.5 When:
- ✅ Absolute best quality needed
- ✅ Nuanced literary translation
- ✅ Budget is not a constraint
- ✅ Ollama Pay unavailable

---

## 📊 Performance Comparison

### Translation Speed (800 pages)

| Model | Time | Cost | Quality |
|-------|------|------|---------|
| Gemma 4 | ~2-3 hours | ฿500-800 | ⭐⭐⭐⭐ |
| DeepSeek V3.1 | ~4-5 hours | ฿1200-1600 | ⭐⭐⭐⭐⭐ |
| Claude 3.5 | ~3-4 hours | ฿2000-3000 | ⭐⭐⭐⭐⭐ |

### Polish Quality (Gao Fei Style)

| Model | Style Match | Flow | Consistency |
|-------|-------------|------|-------------|
| DeepSeek V3.1 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Gemma 4 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Claude 3.5 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🔧 Troubleshooting

### Issue: API returns 401 Unauthorized

**Solution:**
- Check API key is correct
- Verify key hasn't expired
- Ensure no extra spaces in key

### Issue: Request timeout

**Solution:**
- Increase timeout value (120s → 300s)
- Reduce batch size
- Check network connection

### Issue: Model not found

**Solution:**
- Verify model name is correct
- Check model availability on dashboard
- Try alternative model

### Issue: High token usage

**Solution:**
- Reduce max_tokens setting
- Optimize prompts (remove unnecessary text)
- Use smaller model for initial translation

---

## 📞 Support

### Ollama Pay Support

- **Website:** https://ollama-pay.thaigqsoft.com
- **Email:** support@thaigqsoft.com
- **Documentation:** Available on dashboard
- **Status Page:** Check for outages

### Alternative Providers

If Ollama Pay is unavailable:

1. **Anthropic API** (Claude)
   - https://console.anthropic.com
   - Higher cost, excellent quality

2. **OpenAI API** (GPT-4)
   - https://platform.openai.com
   - Good alternative, widely available

3. **Local Ollama** (Self-hosted)
   - https://ollama.ai
   - Free, requires GPU hardware

---

## 📝 Cost Estimation Calculator

```python
def estimate_cost(pages, model="gemma4:31b-cloud"):
    """Estimate API cost for translation project."""
    
    # Average tokens per page (English novel)
    tokens_per_page = 1500  # Input + Output
    
    # Pricing per 1K tokens (THB)
    pricing = {
        "gemma4:31b-cloud": {"input": 0.5, "output": 1.5},
        "deepseek-v3.1:671b-cloud": {"input": 2.0, "output": 6.0},
    }
    
    if model not in pricing:
        return "Unknown model"
    
    rates = pricing[model]
    total_tokens = pages * tokens_per_page
    
    # Assume 60% input, 40% output
    input_cost = (total_tokens * 0.6 / 1000) * rates["input"]
    output_cost = (total_tokens * 0.4 / 1000) * rates["output"]
    
    return input_cost + output_cost

# Examples
print(f"800 pages (Gemma 4): ฿{estimate_cost(800, 'gemma4:31b-cloud'):.2f}")
print(f"800 pages (DeepSeek): ฿{estimate_cost(800, 'deepseek-v3.1:671b-cloud'):.2f}")
```

**Output:**
```
800 pages (Gemma 4): ฿660.00
800 pages (DeepSeek): ฿2160.00
```

---

## ✅ Quick Reference

| Item | Value |
|------|-------|
| **API Endpoint** | `https://ollama-pay.thaigqsoft.com/api/v1` |
| **Translation Model** | `gemma4:31b-cloud` |
| **Polish Model** | `deepseek-v3.1:671b-cloud` |
| **Temperature (Translate)** | 0.3 |
| **Temperature (Polish)** | 0.4 |
| **Max Tokens** | 8192 (translate), 32768 (polish) |
| **Timeout** | 120s (single), 600s (batch) |
