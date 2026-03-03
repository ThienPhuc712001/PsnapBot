# 🚀 Quick Start - Chạy PSnapBOT ngay

## 📍 Bước 1: Đúng thư mục
```bash
# Bạn đang ở: d:\PsnapBot>
# Cần chuyển đến: d:\PsnapBot\dev_agent>

cd dev_agent
```

## 🔧 Cách chạy (Windows CMD):

### Method 1: Dùng batch file (không cần Python PATH)
```cmd
d:\PsnapBot\dev_agent> run_psnappbot.bat --project . --info
```

### Method 2: Dùng Python trực tiếp
```cmd
d:\PsnapBot\dev_agent> "C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" main.py --project . --info
```

## 🧪 Test nhanh:

### 1. Test file Hello World
```cmd
d:\PsnapBot\dev_agent> "C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test.py
```

### 2. Test offline demo
```cmd
d:\PsnapBot\dev_agent> "C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test_offline_demo.py"
```

### 3. Test API connection
```cmd
d:\PsnapBot\dev_agent> "C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test_simple_final.py"
```

## 📋 Lệnh đầy đủ:

```cmd
# Chuyển đến thư mục đúng
cd d:\PsnapBot\dev_agent

# Test 1: File Hello World
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test.py

# Test 2: PSnapBOT info
run_psnappbot.bat --project . --info

# Test 3: PSnapBOT status  
run_psnappbot.bat --project . --status

# Test 4: Demo hoàn chỉnh
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" demo_final.py"
```

## ⚠️ Lỗi thường gặp:

### Lỗi "command not found":
```cmd
# Sai:
d:\PsnapBot> run_psnappbot.bat

# Đúng:
d:\PsnapBot\dev_agent> run_psnappbot.bat
```

### Lỗi "bash not recognized":
```cmd
# Bạn đang dùng Windows CMD, không phải bash
# Dùng lệnh Windows CMD thay vì bash
```

## 🎯 Kết quả mong đợi:

### test.py:
```
Hello World!
PSnapBOT Test File - Hello World!
This file is used to test PSnapBOT functionality.
```

### PSnapBOT info:
```
PSnapBOT v1.0.0
=====================================
Components:
  memory: SQLite-based memory system
  llm: GLM-4.6 via AgentRouter
  tools: Shell, File, Search, Git operations
  ...
```

### Demo:
```
============================================================
PSnapBOT - Local Persistent Development Agent
============================================================
FEATURES:
[OK] Memory System (SQLite database)
[OK] File Operations (read/write/search)
...
```

## 🔍 Kiểm tra AgentRouterAnywhere:
```cmd
# Kiểm tra port 6969
netstat -an | findstr 6969

# Phải thấy:
# TCP    127.0.0.1:6969         0.0.0.0:0              LISTENING
```

Chúc bạn thành công! 🎉