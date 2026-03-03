# Hướng dẫn cấu hình AgentRouterAnywhere cho PSnapBOT

## Bước 1: Mở AgentRouterAnywhere
1. Khởi động AgentRouterAnywhere
2. Đảm bảo nó đang chạy ở port 6969 (kiểm tra với `netstat -an | findstr 6969`)

## Bước 2: Cấu hình Provider
1. Trong giao diện AgentRouterAnywhere, đi đến **Settings**
2. Chọn **Add Provider** > **OpenAI**
3. Điền thông tin sau:
   - **Provider Name**: PSnapBOT Provider (hoặc tên tùy chọn)
   - **API URL**: `http://127.0.0.1:6969/v1`
   - **API Key**: `sk-7AUvBXEXQSoq6X13lyKREfCamXU7jYEDWsynfU52fXe5H52g`
   - **Model Name**: `glm-4.6`
4. Nhấn **Save** để lưu cấu hình

## Bước 3: Kiểm tra kết nối
1. Sau khi lưu, provider sẽ xuất hiện trong danh sách
2. Chạy test script để kiểm tra:
   ```
   python test_simple_final.py
   ```

## Bước 4: Sử dụng PSnapBOT
1. Sau khi cấu hình thành công, chạy PSnapBOT:
   ```
   python main.py --project . "Analyze the test.py file and run it"
   ```
2. Hoặc chạy ở chế độ tương tác:
   ```
   python main.py --project .
   ```

## Lỗi thường gặp và giải pháp

### Lỗi 403 "unauthorized client detected"
- **Nguyên nhân**: Chưa cấu hình provider trong AgentRouterAnywhere
- **Giải pháp**: Làm theo Bước 2 để thêm provider

### Lỗi "Connection refused"
- **Nguyên nhân**: AgentRouterAnywhere chưa chạy
- **Giải pháp**: Khởi động AgentRouterAnywhere trước

### Lỗi "Model not found"
- **Nguyên nhân**: Sai tên model trong cấu hình
- **Giải pháp**: Kiểm tra lại tên model trong provider settings

## Cấu hình PSnapBOT
File `config_user.py` đã được cấu hình với:
- API Base URL: `http://127.0.0.1:6969/v1`
- API Key: `sk-7AUvBXEXQSoq6X13lyKREfCamXU7jYEDWsynfU52fXe5H52g`
- Model: `glm-4.6`

## Chức năng PSnapBOT
PSnapBOT có thể hoạt động ngay cả khi API chưa được cấu hình:
- ✅ Quản lý bộ nhớ (SQLite)
- ✅ Đọc/ghi file
- ✅ Tìm kiếm mã nguồn
- ✅ Phân tích dự án
- ✅ Thực thi lệnh shell an toàn
- ⚠️ Tính năng AI cần API được cấu hình đúng