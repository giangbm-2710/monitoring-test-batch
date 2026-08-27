# FastAPI Clean Architecture - Product CRUD Example

Dự án mẫu minh họa kiến trúc **Clean Architecture** kết hợp với **FastAPI** và **SQLAlchemy (Async)** để quản lý Sản phẩm (Product Management). Dự án được thiết kế chuyên nghiệp, chuẩn mực, dễ dàng mở rộng và sẵn sàng đẩy (push) lên GitHub để kiểm thử.

---

## 🏗️ Cấu Trúc Dự Án (Clean Architecture)

```text
.
├── app/
│   ├── core/                           # Cấu hình dự án & Database engine
│   │   ├── config.py
│   │   └── database.py
│   ├── domain/                         # Lớp Domain (Business Logic cốt lõi, độc lập)
│   │   ├── entities/
│   │   │   └── product.py              # Pure Python Entity
│   │   ├── exceptions/
│   │   │   └── product_exceptions.py   # Domain Exceptions
│   │   └── repositories/
│   │       └── product_repository.py   # Abstract Repository Interface
│   ├── use_cases/                      # Lớp Use Cases (Nghiệp vụ ứng dụng)
│   │   └── product_use_cases.py        # Create, Get, List, Update, Delete Use Cases
│   ├── infrastructure/                 # Lớp Infrastructure (DB, ORM, External services)
│   │   └── db/
│   │       ├── models/
│   │       │   └── product_model.py    # SQLAlchemy ORM Model
│   │       └── repositories/
│   │           └── product_repository_impl.py # Triển khai Repository bằng SQLAlchemy Async
│   ├── presentation/                   # Lớp Presentation (FastAPI REST APIs)
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   └── product_router.py
│   │   │       ├── dependencies.py     # Dependency Injection container
│   │   │       └── router.py
│   │   └── schemas/
│   │       └── product_schema.py       # Pydantic DTO Request / Response Schemas
│   └── main.py                         # FastAPI App Entrypoint
├── tests/                              # Automated Unit/Integration Tests
│   ├── conftest.py
│   └── test_product_api.py
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🚀 Hướng Dẫn Chạy Dự Án Chế Độ Local

### 1. Cài Đặt Môi Trường & Thư Viện

```bash
# Tạo môi trường ảo (Virtual Environment)
python -m venv venv

# Kích hoạt môi trường ảo
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Cài đặt thư viện phụ thuộc
pip install -r requirements.txt
```

### 2. Khởi Chạy Ứng Dụng Server

```bash
uvicorn app.main:app --reload
```

Sau khi khởi chạy thành công, mở trình duyệt và truy cập:
- **Swagger UI Interactive API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc API Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Chạy Kiểm Thử Tự Động (Automated Testing)

Dự án có sẵn bộ test tự động sử dụng **pytest** và **httpx** chạy trên cơ sở dữ liệu **SQLite In-Memory**:

```bash
pytest
```

---

## 🐳 Khởi Chạy Với Docker

```bash
docker-compose up --build
```

---

## 🐙 Hướng Dẫn Push Code Lên GitHub

Nếu bạn muốn đẩy mã nguồn này lên GitHub để test:

```bash
# 1. Khởi tạo Git repository local
git init

# 2. Add toàn bộ tệp vào staging
git add .

# 3. Tạo commit đầu tiên
git commit -m "feat: initial clean architecture fastAPI product CRUD implementation"

# 4. Đổi tên branch chính thành main
git branch -M main

# 5. Liên kết repository từ xa (thay bằng URL GitHub của bạn)
git remote add origin https://github.com/USERNAME/REPOSITORY-NAME.git

# 6. Push code lên GitHub
git push -u origin main
```

---

## 📡 Danh Sách API Endpoints (Product CRUD)

| HTTP Method | Endpoint | Mô tả |
| :--- | :--- | :--- |
| `GET` | `/` | Health check endpoint |
| `POST` | `/api/v1/products/` | Tạo sản phẩm mới |
| `GET` | `/api/v1/products/` | Lấy danh sách sản phẩm (có phân trang & lọc theo category) |
| `GET` | `/api/v1/products/{id}` | Lấy thông tin chi tiết một sản phẩm theo ID |
| `PUT` | `/api/v1/products/{id}` | Cập nhật thông tin sản phẩm theo ID |
| `DELETE` | `/api/v1/products/{id}` | Xóa sản phẩm theo ID |
