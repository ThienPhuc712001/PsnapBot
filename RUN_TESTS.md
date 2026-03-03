# 🚀 Hướng dẫn chạy test PSnapBOT

## 📋 Danh sách các file test và cách chạy

### 🔧 Cách chạy chung:
```bash
# Mở Command Prompt hoặc PowerShell
cd d:\PsnapBot\dev_agent

# Cách 1: Dùng batch file (không cần Python PATH)
run_test.bat

# Cách 2: Dùng Python trực tiếp
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" ten_file.py
```

---

## 🧪 Các file test chính:

### 1. **test.py** - File Hello World cơ bản
```bash
# Chạy file test
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test.py

# Kết quả mong đợi:
# Hello World!
# PSnapBOT Test File - Hello World!
# This file is used to test PSnapBOT functionality.
```

### 2. **test_simple_final.py** - Test API connection
```bash
# Test kết nối API
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test_simple_final.py

# Kiểm tra:
# - API Key có đúng không
# - Base URL có đúng không  
# - Kết nối đến AgentRouter có thành công không
```

### 3. **test_api_curl.py** - Test API toàn diện
```bash
# Test với nhiều phương pháp
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test_api_curl.py

# Test:
# - Curl command
# - Python requests local
# - Python requests cloud
```

### 4. **test_offline_demo.py** - Test chức năng offline
```bash
# Test các chức năng không cần AI
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test_offline_demo.py"

# Test:
# - Memory system
# - File operations
# - Code search
# - Project detection
```

### 5. **demo_final.py** - Demo hoàn chỉnh
```bash
# Demo tất cả tính năng
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" demo_final.py"

# Hiển thị:
# - Tất cả features
# - Project structure
# - Configuration
# - Current status
```

---

## 🤖 Chạy PSnapBOT chính:

### 1. **Xem thông tin PSnapBOT:**
```bash
run_psnappbot.bat --project . --info
```

### 2. **Xem trạng thái:**
```bash
run_psnappbot.bat --project . --status
```

### 3. **Chạy lệnh đơn:**
```bash
run_psnappbot.bat --project . "Analyze test.py file"
```

### 4. **Chế độ tương tác:**
```bash
run_psnappbot.bat --project .
```

---

## 🔍 Thứ tự chạy test đề xuất:

### Bước 1: Test cơ bản
```bash
# 1. Test file Hello World
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test.py

# 2. Test demo offline
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test_offline_demo.py"
```

### Bước 2: Test API
```bash
# 3. Test kết nối API
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test_simple_final.py"

# 4. Test API toàn diện
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test_api_curl.py"
```

### Bước 3: Test PSnapBOT
```bash
# 5. Xem thông tin
run_psnappbot.bat --project . --info

# 6. Xem trạng thái
run_psnappbot.bat --project . --status

# 7. Demo hoàn chỉnh
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" demo_final.py"
```

---

## 📝 File batch tiện lợi:

### **run_test.bat** - Chạy tất cả test
```bash
# Chạy tất cả test theo thứ tự
run_test.bat
```

### **run_psnappbot.bat** - Chạy PSnapBOT
```bash
# Chạy PSnapBOT với các tham số khác nhau
run_psnappbot.bat [tham_số]
```

---

## ⚠️ Lưu ý quan trọng:

1. **Luôn chạy trong thư mục dev_agent:**
   ```bash
   cd d:\PsnapBot\dev_agent
   ```

2. **Dùng đường dẫn Python đầy đủ:**
   ```bash
   "C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe"
   ```

3. **Kiểm tra AgentRouterAnywhere:**
   - Mở AgentRouterAnywhere
   - Đảm bảo nó đang chạy ở port 6969
   - Kiểm tra: `netstat -an | findstr 6969`

4. **Nếu có lỗi API:**
   - Kiểm tra file `config_user.py`
   - Đảm bảo API key đúng
   - Cấu hình provider trong AgentRouterAnywhere

---

## 🆘 Nếu gặp lỗi:

### Lỗi "Python not found":
```bash
# Dùng batch file thay vì python trực tiếp
run_test.bat
```

### Lỗi "UnicodeEncodeError":
```bash
# Các file test đã được fix không dùng emoji
# Nếu vẫn lỗi, chạy trong PowerShell thay vì CMD
```

### Lỗi API 401/403:
```bash
# Test lại sau khi:
# 1. Cấu hình provider trong AgentRouterAnywhere
# 2. Lấy API key mới từ Discord
# 3. Verify Discord account
```

---

## 📊 Kết quả mong đợi:

### ✅ Thành công:
- test.py: In ra "Hello World!"
- test_offline_demo.py: Tất cả "[OK]" 
- demo_final.py: Hiển thị đầy đủ features
- PSnapBOT info/status: Hiển thị thông tin hệ thống

### ❌ Cần sửa:
- API test: Lỗi 401/403 → Cần cấu hình authentication
- Unicode errors → Đã fix, không nên xảy ra
- Import errors → Kiểm tra đường dẫn và Python path

Chúc bạn test thành công! 🎉