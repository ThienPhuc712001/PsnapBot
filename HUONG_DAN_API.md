# 🔗 Hướng Dẫn Cấu Hình API cho PSnapBOT

## 📋 Bước 1: Mở file cấu hình
```
d:\PsnapBot\dev_agent\config_user.py
```

## 📝 Bước 2: Thay thế thông tin API

Tìm các dòng sau và thay thế:

```python
# Thay thế dòng này:


# Thành:
API_KEY = "sk-7AUvBXEXQSoq6X13lyKREfCamXU7jYEDWsynfU52fXe5H52g"

# Nếu dùng endpoint khác:
API_BASE_URL = "http://127.0.0.1:6969/v1"


```

## 🎯 Các nhà cung cấp API phổ biến:

### **1. OpenAI**
```python
API_KEY = "sk-your-openai-key-here"
API_BASE_URL = "https://api.openai.com/v1/chat/completions"
```

### **2. Anthropic Claude**
```python
API_KEY = "sk-ant-your-claude-key"
API_BASE_URL = "https://api.anthropic.com/v1/messages"
```

### **3. Google Gemini**
```python
API_KEY = "your-gemini-key"
API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
```

### **4. AgentRouter (GLM-4.6)**
```python
API_KEY = "sk-7AUvBXEXQSoq6X13lyKREfCamXU7jYEDWsynfU52fXe5H52g"
API_BASE_URL = "http://127.0.0.1:6969/v1"
```

## ⚙️ Sau khi cấu hình:

1. **Lưu file** (Ctrl + S)
2. **Chạy PSnapBOT:**
   ```bash
   cd d:\PsnapBot\dev_agent
   run_psnappbot.bat
   ```
3. **Kiểm tra kết nối:**
   ```bash
   "C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" config_user.py
   ```

## 🔍 Kiểm tra kết nối:

Sau khi cấu hình, chạy test để kiểm tra:
```bash
"C:\Users\cntt.tts13\AppData\Local\Programs\Python\Launcher\py.exe" test_simple_api.py
```

## ⚠️ Lưu ý:

- **Bảo mật API key** - Không chia sẻ với ai
- **Endpoint đúng** - Đảm bảo URL tương thích với API key
- **Internet** - Cần kết nối internet để sử dụng
- **Firewall** - Có thể cần mở port 443

## 🚀 Sau khi sẵn sàng:

PSnapBOT sẽ:
- Kết nối API của bạn
- Phân tích yêu cầu thông minh
- Học từ kinh nghiệm
- Tự động fix lỗi build
- Thực thi các tác vụ development

**Chúc bạn sử dụng PSnapBOT hiệu quả!** 🎉