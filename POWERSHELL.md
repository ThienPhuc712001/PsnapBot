# 🔧 PowerShell Commands for PSnapBOT

## ⚠️ PowerShell khác CMD!

PowerShell không chạy batch file trực tiếp. Cần dùng cú pháp:

## 🚀 Cách chạy đúng trong PowerShell:

### Method 1: Dùng .\ (Khuyến nghị)
```powershell
cd dev_agent
.\WORK
.\CHAT
.\FIX "build error"
.\ADD "user login"
```

### Method 2: Dùng cmd /c
```powershell
cd dev_agent
cmd /c WORK
cmd /c CHAT
cmd /c FIX "build error"
```

### Method 3: Dùng Call
```powershell
cd dev_agent
call .\WORK
call .\CHAT
call .\FIX "build error"
```

## 📋 Lệnh PowerShell chính xác:

```powershell
# Chuyển thư mục
cd D:\PsnapBot\dev_agent

# Menu làm việc
.\WORK

# Chat mode
.\CHAT

# Sửa lỗi
.\FIX "build error"

# Thêm feature
.\ADD "user authentication"

# Menu đầy đủ
.\PSnapBOT

# Test nhanh
.\GO
```

## 🎯 Workflow PowerShell:

### **Bắt đầu làm việc:**
```powershell
cd D:\PsnapBot\dev_agent
.\WORK
```

### **Sửa lỗi nhanh:**
```powershell
.\FIX "import error"
```

### **Chat với AI:**
```powershell
.\CHAT
```

## 🔧 Nếu vẫn lỗi:

### **Kiểm tra execution policy:**
```powershell
Get-ExecutionPolicy
```

### **Cho phép chạy script:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Hoặc dùng Bypass:**
```powershell
PowerShell -ExecutionPolicy Bypass -File .\WORK.bat
```

## 🆘 Lỗi thường gặp:

### **"not recognized" → Thêm .\ phía trước**
```powershell
# Sai:
WORK

# Đúng:
.\WORK
```

### **"cannot be loaded" → Set ExecutionPolicy**
```powershell
Set-ExecutionPolicy RemoteSigned
```

## 🎉 Quick Start PowerShell:

```powershell
cd D:\PsnapBot\dev_agent
.\WORK
```

Chỉ cần nhớ thêm `.\` trước mỗi lệnh!