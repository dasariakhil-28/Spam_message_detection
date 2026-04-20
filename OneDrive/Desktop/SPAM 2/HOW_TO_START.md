# 🚀 HOW TO START YOUR SPAM DETECTION SYSTEM

## TWO OPTIONS TO START THE SERVER

### **OPTION 1: Batch File (Easiest) ⭐**

**For Windows Users - Just Double Click!**

1. Navigate to folder: `c:\Users\mekal\OneDrive\Desktop\SPAM 2\`
2. Find file: `start_app.bat`
3. **Double-click it** ✨
4. Wait 3 seconds...
5. Website opens automatically in browser!

**What happens:**
```
✅ Server starts on http://localhost:5000
✅ Browser automatically opens
✅ You can start using the spam detector
```

---

### **OPTION 2: PowerShell Script (Advanced)**

**For PowerShell Users**

1. Open PowerShell as Administrator
2. Navigate to folder:
   ```powershell
   cd "c:\Users\mekal\OneDrive\Desktop\SPAM 2"
   ```

3. Run the script:
   ```powershell
   .\start_app.ps1
   ```

4. If you get an error about execution policy, run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

5. Then run the script again

**What happens:**
```
✅ Activates virtual environment
✅ Checks for model file
✅ Starts server
✅ Opens browser automatically
✅ Shows status messages in terminal
```

---

### **OPTION 3: Manual Terminal Command**

**If you prefer typing in terminal/PowerShell:**

```powershell
cd "c:\Users\mekal\OneDrive\Desktop\SPAM 2"
.\.venv\Scripts\python.exe app.py
```

Then open browser manually: `http://localhost:5000`

---

## WHAT YOU'LL SEE

### Terminal Output:
```
==================================================
🚀 SPAM DETECTION SYSTEM STARTUP
==================================================

✅ Virtual environment found
✅ ML Model found (spam_model.pkl)

==================================================
🌐 Starting Flask Server
==================================================

📱 Website: http://localhost:5000
🔌 API Endpoint: http://localhost:5000/api

Press Ctrl+C to stop the server

✅ Server is running!
🌐 Opening browser...
✅ Browser opened!

==================================================
✨ SPAM DETECTION SYSTEM IS READY!
==================================================
```

### Browser Display:
```
Header: 🛡️ SPAM DETECTION SYSTEM
Status: 🟢 Online | 🟢 Active | 🟠 localhost:5000
Input: Text box for message
Output: Results with probabilities
```

---

## STOPPING THE SERVER

### If using Option 1 (Batch):
- Close the server window that opened
- Or press Ctrl+C in the server window

### If using Option 2 (PowerShell):
- Press **Ctrl+C** in the terminal
- Type `exit` and press Enter

### If using Option 3 (Manual):
- Press **Ctrl+C** in the terminal

---

## TROUBLESHOOTING

### Problem: "python.exe not found"
**Solution:** Virtual environment not activated
```
cd "c:\Users\mekal\OneDrive\Desktop\SPAM 2"
python -m venv .venv
```

### Problem: "Port 5000 already in use"
**Solution:** Another app is using port 5000
```
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Problem: "Model file not found"
**Solution:** Train the model first
```
python train_model.py
```

### Problem: Browser doesn't open automatically
**Solution:** Open manually
- Click in terminal or script and copy the URL
- Paste into browser: `http://localhost:5000`

---

## QUICK START (30 SECONDS)

```
1. Navigate to: c:\Users\mekal\OneDrive\Desktop\SPAM 2\
2. Double-click: start_app.bat
3. Wait 3 seconds
4. Browser opens with spam detector
5. Start typing messages to analyze!
```

**That's it! ✨**

---

## FILE DESCRIPTIONS

| File | Purpose | How to Use |
|------|---------|-----------|
| `start_app.bat` | Easiest launcher | Double-click |
| `start_app.ps1` | Advanced launcher | `.\start_app.ps1` |
| `app.py` | Flask server | `python app.py` |
| `index.html` | Website interface | Opened automatically |
| `spam_model.pkl` | ML model | Loaded automatically |

---

## YOUR SPAM DETECTOR IS READY! 🎉

Pick your favorite way to start and begin detecting spam!

**Recommended:** Use `start_app.bat` - it's the easiest! 👍
