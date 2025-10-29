# 📚 Clothing Shop AI Assistant - Knowledge Base Guide

Your AI assistant is now configured as a **Clothing Shop Assistant** that answers customer questions based on YOUR shop's information.

## 🎯 How It Works

The AI assistant will:
1. Search through YOUR shop's files (products, policies, FAQs) FIRST
2. Use that information to answer customer questions
3. Only answer based on the information you provide
4. Politely say "I don't know" if the info isn't in your files

---

## 📁 Step 1: Edit Your Shop Information

I've created template files in `backend/knowledge_base/` folder:

### Files to Edit:

1. **product_catalog.txt** - Your products, prices, sizes, SKUs
   ```
   Edit: C:\Users\Hp\Downloads\localhost-openai-api-agent\backend\knowledge_base\product_catalog.txt
   ```

2. **store_policies.txt** - Shipping, returns, payment methods
   ```
   Edit: C:\Users\Hp\Downloads\localhost-openai-api-agent\backend\knowledge_base\store_policies.txt
   ```

3. **faq.txt** - Common customer questions and answers
   ```
   Edit: C:\Users\Hp\Downloads\localhost-openai-api-agent\backend\knowledge_base\faq.txt
   ```

### You Can Add More Files:

Add ANY of these file types to the `knowledge_base/` folder:
- `.txt` - Text files
- `.pdf` - PDF documents
- `.docx` - Word documents
- `.md` - Markdown files

**Examples of what to add:**
- Product catalogs (with images descriptions)
- Size charts
- Brand information
- Promotional policies
- Seasonal collections
- Care instructions
- Store locations
- Contact information

---

## 🚀 Step 2: Upload Your Knowledge Base

After editing the files, run this command:

```bash
cd C:\Users\Hp\Downloads\localhost-openai-api-agent\backend
venv\Scripts\activate
python upload_knowledge_base.py
```

### What This Does:

1. Creates a permanent "knowledge base" in OpenAI
2. Uploads all your files from `knowledge_base/` folder
3. Connects the AI assistant to your knowledge base
4. The AI can now search these files when answering questions!

### Expected Output:

```
============================================================
📚 KNOWLEDGE BASE UPLOAD TOOL
============================================================

🔍 Looking for existing vector store...
📦 Creating new vector store: '<PUT_YOUR_VECTOR_STORE_NAME_HERE>'...
✅ Vector store created: vs_xxxxx

📁 Scanning knowledge base directory: knowledge_base/
📄 Found 3 files to upload:
   - product_catalog.txt
   - store_policies.txt
   - faq.txt

⬆️  Uploading: product_catalog.txt...
   ✅ Uploaded successfully

⬆️  Uploading: store_policies.txt...
   ✅ Uploaded successfully

⬆️  Uploading: faq.txt...
   ✅ Uploaded successfully

🔗 Attaching 3 files to vector store...
   ✅ Files attached to vector store!

🤖 Updating assistant: 'Clothing Shop Assistant'...
✅ Assistant updated with knowledge base!

============================================================
✅ KNOWLEDGE BASE UPLOAD COMPLETE!
============================================================
```

---

## 🔄 Step 3: Restart Your Server

After uploading, restart the Flask backend:

1. Press `Ctrl+C` in the terminal running Flask
2. Start it again:
   ```bash
   python app.py
   ```

---

## 💬 Step 4: Test Your Assistant

Open your website: http://localhost:8080

### Example Questions to Test:

**About Products:**
- "Do you have any black t-shirts?"
- "How much is the summer floral dress?"
- "What sizes do you have for men's jeans?"

**About Policies:**
- "What is your return policy?"
- "How long does shipping take?"
- "Do you offer free shipping?"

**From FAQ:**
- "How can I track my order?"
- "Do you ship internationally?"
- "What payment methods do you accept?"

---

## 🔄 Updating Your Knowledge Base

### To Add/Edit Files:

1. Edit files in `backend/knowledge_base/` folder
2. Run the upload script again:
   ```bash
   python upload_knowledge_base.py
   ```
3. Restart Flask server

### To Add New Products:

Just edit `product_catalog.txt` and re-upload!

### To Change Policies:

Edit `store_policies.txt` and re-upload!

---

## 💡 Pro Tips

### 1. **Be Specific in Your Files**

Good:
```
Classic Cotton T-Shirt - Black
Price: $19.99
Sizes: S, M, L, XL, XXL
Material: 100% Cotton
In Stock: Yes
```

Bad:
```
T-shirt available in various colors and sizes
```

### 2. **Use Clear Formatting**

Use headings, bullet points, and clear sections:
```
## Men's Clothing

### T-Shirts
- Product 1
- Product 2

### Jeans
- Product 1
- Product 2
```

### 3. **Include Common Variations**

If customers might ask in different ways:
```
Q: What is your return policy?
Q: Can I return items?
Q: How do I return something?
A: [Your return policy]
```

### 4. **Keep Information Updated**

- Update prices when they change
- Mark items as "Out of Stock" when needed
- Update seasonal collections
- Re-upload after making changes

---

## 📊 Example Customer Conversation

**Customer:** "Hi! Do you have any dresses?"

**AI:** "Yes! We have several dresses available:

1. **Summer Floral Dress** - $49.99
   - Sizes: XS, S, M, L, XL
   - Material: Cotton Blend

2. **Evening Cocktail Dress** - $89.99
   - Available in Black, Red, Navy
   - Sizes: XS, S, M, L, XL
   - Material: Polyester

Would you like more information about any of these dresses?"

**Customer:** "What's your return policy?"

**AI:** "We accept returns within 30 days of purchase. Items must be unworn, unwashed, and with original tags attached. Return shipping is the customer's responsibility unless the item is defective. Refunds are processed within 5-7 business days after we receive the return."

---

## 🛠️ Troubleshooting

### AI says "I don't have that information"

- Make sure you added the info to your knowledge base files
- Run the upload script to update the AI
- Restart the Flask server

### Upload script fails

- Check your OpenAI API key in `.env` file
- Make sure you're in the `backend` folder
- Make sure virtual environment is activated
- Check internet connection

### AI gives wrong information

- Check the content in your knowledge base files
- Files might have old/incorrect information
- Update the files and re-upload

---

## 📞 Need Help?

Check the main setup guide: `SETUP.md`

---

## 🎉 You're All Set!

Your AI assistant now has access to your shop's knowledge and can answer customer questions accurately!

**Remember:**
- Edit files in `knowledge_base/` folder
- Run `python upload_knowledge_base.py` after changes
- Restart Flask server
- Test on the website
