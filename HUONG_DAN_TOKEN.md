# Hướng dẫn lấy AgentRouter Token

## 🔄 AgentRouterAnywhere (Local)

Nếu bạn đang dùng AgentRouterAnywhere local như bạn đã cài:

### Cách 1: Không cần token (Free tier)
1. Mở AgentRouterAnywhere
2. Settings → Add Provider → OpenAI
3. Điền thông tin:
   - **Provider Name**: PSnapBOT Local
   - **API URL**: `http://127.0.0.1:6969/v1`
   - **API Key**: `sk-free` (hoặc để trống)
   - **Model Name**: `glm-4.6`
4. Save

### Cách 2: Dùng token có sẵn
Nếu bạn có token từ các nguồn khác, điền vào API Key.

## 🌐 AgentRouter Cloud (Online)

### Cách 1: Đăng ký miễn phí
1. Truy cập: https://agentrouter.org
2. Đăng ký tài khoản mới
3. Vào Dashboard → API Keys
4. Copy token (bắt đầu bằng `sk-`)

### Cách 2: Discord
1. Join Discord: https://discord.com/invite/V6kaP6Rg44
2. Vào channel #api-keys
3. Lấy free token từ bot

### Cách 3: GitHub Student Pack
1. Nếu bạn có GitHub Student Pack
2. Kiểm tra có ưu đãi AgentRouter không
3. Activate và lấy token

## 🔧 Cấu hình trong PSnapBOT

### Cấu hình cho AgentRouterAnywhere Local:
```python
# config_user.py
API_KEY = ""  # Để trống hoặc "sk-free"
API_BASE_URL = "http://127.0.0.1:6969/v1"
API_MODEL = "glm-4.6"
```

### Cấu hình cho AgentRouter Cloud:
```python
# config_user.py
API_KEY = "sk-your-token-here"
API_BASE_URL = "http://127.0.0.1:6969/v1"
API_MODEL = "glm-4.6"
```

## 🧪 Test Token

Sau khi có token, test với:
```bash
python test_simple_final.py
```

## 📝 Các loại token phổ biến:

### Free Tokens:
- `sk-free` - Token miễn phí cơ bản
- `sk-demo` - Token demo
- Token từ Discord bot

### Paid Tokens:
- `sk-pro-xxxxx` - Token pro
- `sk-enterprise-xxxxx` - Token enterprise

## ⚠️ Lưu ý quan trọng:

1. **Bảo mật token**: Không chia sẻ token với người khác
2. **Limitations**: Token miễn phí có giới hạn usage
3. **Expiration**: Một số token có thời hạn sử dụng
4. **Rate limits**: Token miễn phí có rate limit thấp hơn

## 🔍 Kiểm tra token hoạt động:

```python
# Test token
import requests

headers = {
    "Authorization": f"Bearer YOUR_TOKEN_HERE",
    "Content-Type": "application/json"
}

response = requests.get("http://127.0.0.1:6969/v1/models", headers=headers)
print(response.status_code)
print(response.json())
```

## 🆘 Hỗ trợ:

Nếu không lấy được token:
1. Join Discord: https://discord.com/invite/V6kaP6Rg44
2. Ask trong channel #help
3. Check documentation: https://docs.agentrouter.org

## 🎯 Khuyến nghị cho bạn:

Vì bạn đã cài AgentRouterAnywhere local, hãy thử:

1. **Đầu tiên**: Dùng không cần token (để trống API key)
2. **Nếu không được**: Dùng `sk-free`
3. **Cuối cùng**: Lấy token từ Discord

Chúc bạn thành công!