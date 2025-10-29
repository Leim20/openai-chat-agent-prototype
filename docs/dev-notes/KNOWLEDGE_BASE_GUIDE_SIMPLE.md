# 📚 Simple Knowledge Base Setup for Clothing Shop

## Quick Setup (Easier Method)

Since you want the AI to have permanent access to your shop information, here's the simplest approach:

### Option 1: Put Info in the System Instructions (Recommended for Small Shops)

1. **Edit the `.env` file:**
   ```
   C:\Users\Hp\Downloads\localhost-openai-api-agent\backend\.env
   ```

2. **Update `ASSISTANT_INSTRUCTIONS` with your shop info:**
   ```
   ASSISTANT_INSTRUCTIONS=You are a professional clothing shop assistant.

   PRODUCTS WE SELL:
   - Men's T-Shirts: $19.99-$24.99 (S-XXL, various colors)
   - Men's Jeans: $54.99-$59.99 (sizes 28-38)
   - Women's Dresses: $49.99-$89.99 (XS-XL)
   - Women's Blouses: $39.99 (XS-XL)

   SHIPPING:
   - Standard: 5-7 days, $5.99
   - Express: 2-3 days, $12.99
   - Free shipping over $75

   RETURNS:
   - 30 days return policy
   - Items must be unworn with tags
   - Refund in 5-7 business days

   Answer customer questions professionally based on this information.
   ```

3. **Restart Flask server**

### Option 2: Create a Master Knowledge File

1. **Create ONE comprehensive file with ALL your shop info:**

   File: `C:\Users\Hp\Downloads\localhost-openai-api-agent\backend\shop_info.txt`

2. **Put everything in it:**
   - All products
   - All policies
   - All FAQs
   - Contact info

3. **Customers upload this file at the start of chat**
   - Or you can manually upload it in each conversation

### Option 3: Use the Web Interface

1. When a customer starts chatting, they can upload files
2. Upload your product catalog PDF/document
3. The AI will read it and answer based on it
4. This works for each individual conversation

---

## For Now: Test With Current Setup

Your assistant is already configured as a "Clothing Shop Assistant"!

Try asking it:
- "What products do you sell?"
- "What is your shipping policy?"
- "Do you have any dresses?"

The AI will respond professionally, though it won't have specific details until you add them.

---

## Recommended: Update .env with Your Basic Info

Edit `.env` and add your shop's key information to `ASSISTANT_INSTRUCTIONS`:

```bash
ASSISTANT_INSTRUCTIONS=You are a professional assistant for [YOUR SHOP NAME].

We sell:
[List your main categories]

Our prices range from $X to $Y.

Shipping: [Your shipping info]
Returns: [Your return policy]
Contact: [Your contact info]

Always be helpful and professional. If you don't have specific information, politely say so.
```

Then restart the server!

---

## Need the Advanced Version?

The upload script requires a newer OpenAI SDK version. For now, the simple methods above work perfectly for most clothing shops.
