# BRSR Tool — Integration Setup Guide

This guide shows you how to restructure your existing files into a single unified Streamlit app.

---

## Step 1: New Folder Structure

Create this exact structure on your Mac:

```
brsr-tool-v2/                                    ← NEW folder
├── Home.py                                      ← download from Claude
├── business_profile.py                          ← download from Claude
├── pdf_generator.py                             ← copy from old folder
├── requirements.txt                             ← copy from old folder
└── pages/                                       ← create this folder
    ├── 1_📋_Section_A.py                        ← copy of your app.py
    ├── 2_🧭_Section_B.py                        ← copy of your sectionB.py
    ├── 3_⚖️_Principle_1.py                      ← copy of your Section_c_p1.py
    ├── 4_🔄_Principle_2.py                      ← copy of your section_c_p2.py
    ├── 5_👥_Principle_3.py                      ← copy of your section_c_p3.py
    ├── 6_🤝_Principle_4_5.py                    ← copy of your section_c_p4_5.py
    ├── 7_🌿_Principle_6.py                      ← copy of your section_c_p6.py
    ├── 8_🤝_Principle_7_8_9.py                  ← copy of your section_c_p789.py
    └── 9_📄_Generate_Report.py                  ← rename from 9_generate_report_page.py
```

---

## Step 2: Copy Your Existing Files

Open Terminal on Mac and run:

```bash
cd ~/Desktop
mkdir brsr-tool-v2
cd brsr-tool-v2
mkdir pages

# Copy infrastructure files (not renamed)
cp ~/Desktop/brsr-tool/pdf_generator.py .
cp ~/Desktop/brsr-tool/requirements.txt .

# Copy each principle into pages folder with NEW names
cp ~/Desktop/brsr-tool/app.py pages/1_📋_Section_A.py
cp ~/Desktop/brsr-tool/sectionB.py pages/2_🧭_Section_B.py
cp ~/Desktop/brsr-tool/Section_c_p1.py pages/3_⚖️_Principle_1.py
cp ~/Desktop/brsr-tool/section_c_p2.py pages/4_🔄_Principle_2.py
cp ~/Desktop/brsr-tool/section_c_p3.py pages/5_👥_Principle_3.py
cp ~/Desktop/brsr-tool/section_c_p4_5.py pages/6_🤝_Principle_4_5.py
cp ~/Desktop/brsr-tool/section_c_p6.py pages/7_🌿_Principle_6.py
cp ~/Desktop/brsr-tool/section_c_p789.py pages/8_🤝_Principle_7_8_9.py
```

Then save the files I gave you:
- `Home.py` → into `brsr-tool-v2/`
- `business_profile.py` → into `brsr-tool-v2/`
- The `9_generate_report_page.py` → rename to `9_📄_Generate_Report.py` and put in `pages/`

---

## Step 3: Add Tier Logic to Each Page (Small Edit)

Open each file inside `pages/` and add these **3 lines at the very top** (after `import streamlit as st`):

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from business_profile import init_business_profile, show_tier_badge
init_business_profile()
show_tier_badge()
```

This does 3 things:
1. Lets the page find `business_profile.py` (which lives in the parent folder)
2. Initialises the business type (defaults to Pvt Ltd)
3. Shows a small badge at the top of the page so users see which tier they're in

**Do this for all 8 pages.** It takes ~30 seconds per file.

---

## Step 4: Remove Old `st.set_page_config()` From Principle Files (If Needed)

Streamlit only allows ONE `st.set_page_config()` call across your app, and it must be the first Streamlit command. Since `Home.py` already sets it, you need to either:
- Remove `st.set_page_config()` from each page file, OR
- Leave it — Streamlit will just show a warning but still run

The easier option is to leave them as they are. The warning is harmless.

---

## Step 5: Run the Unified App

```bash
cd ~/Desktop/brsr-tool-v2
streamlit run Home.py
```

You should now see:
- **Home page** with business type selector + progress tracker
- **Sidebar** with all 9 pages numbered and ordered
- **Click each page** in sidebar to fill it — data persists across pages

---

## Step 6: Test End-to-End

1. Open the app (`streamlit run Home.py`)
2. On Home, select your business type (e.g. "Private Limited")
3. Click **"1 📋 Section A"** in sidebar → fill it fully
4. Return to Home — you should see "✅ Section A" marked as complete
5. Click **"2 🧭 Section B"** — it should pre-fill company name from Section A
6. Continue through all 9 pages
7. Finally click **"9 📄 Generate Report"** to download PDF

---

## Step 7: GitHub + Streamlit Cloud Deployment

Once everything works locally:

1. **Initialize Git:**
```bash
cd ~/Desktop/brsr-tool-v2
git init
git add .
git commit -m "Initial integrated BRSR tool"
```

2. **Create GitHub repo:** Go to github.com, create a new repo called `brsr-msme-tool` (public)

3. **Push code:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/brsr-msme-tool.git
git branch -M main
git push -u origin main
```

4. **Deploy on Streamlit Cloud:**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repo
   - **Main file:** `Home.py` (important!)
   - Click Deploy

In 2-3 minutes you'll have a live URL like `https://brsr-msme-tool.streamlit.app`

---

## Common Issues

### "ModuleNotFoundError: No module named 'business_profile'"
The `sys.path.insert` lines in Step 3 weren't added to that page.

### "set_page_config() can only be called once"
Remove the `st.set_page_config()` line from the page file (Home.py already has it).

### "Page not showing in sidebar"
Make sure the file is inside the `pages/` folder AND has a `.py` extension.

### Emojis not showing in filenames on Windows
Emojis in filenames work on Mac/Linux. On Windows, you can remove emojis: `1_Section_A.py` works fine.

---

## What This Integration Gives You

- ✅ Single URL / app for entire BRSR tool
- ✅ Data flows between sections (Section A → all principles)
- ✅ Business tier auto-hides irrelevant questions
- ✅ Master progress tracker + overall score on Home
- ✅ Single BRSR PDF generator
- ✅ Ready to deploy on Streamlit Cloud

---

## Next Steps After Integration Works

1. Extend `pdf_generator.py` to cover all 9 principles in BRSR-audit format
2. Add tier-based question hiding inside each principle file (replace `show_X_questions()` checks)
3. Deploy to Streamlit Cloud
4. Phase 2 (later): SQLite backend for multi-year data
