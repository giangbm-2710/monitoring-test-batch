# PR Title
`feat(category,product): Thêm module quản lý Danh mục (Category) và tích hợp liên kết Sản phẩm (Product)`

---

# PR Description (Mô tả Pull Request)

## 📌 Summary
PR này thực hiện 2 nhiệm vụ chính:
1. **Thêm mới module Quản lý Danh mục (Category Management)** bao gồm đầy đủ CRUD (Create, Read, Update, Delete) theo kiến trúc Clean Architecture.
2. **Cập nhật module Sản phẩm (Product Management)**: Chuyển đổi thuộc tính `category` (dạng string) sang khóa ngoại `category_id` liên kết trực tiếp với bảng `Category`, đồng thời hỗ trợ nạp thông tin danh mục tương ứng khi lấy chi tiết sản phẩm.

---

## 🛠️ Key Changes

### 1. New Feature: Category Management Module
- **Domain Layer**:
  - [`app/domain/entities/category.py`](file:///d:/monitoring-tool/monitoring-test-batch/app/domain/entities/category.py): Định nghĩa entity `Category` với các quy tắc kiểm tra tính hợp lệ (`validate`).
  - [`app/domain/exceptions/category_exceptions.py`](file:///d:/monitoring-tool/monitoring-test-batch/app/domain/exceptions/category_exceptions.py): Định nghĩa các ngoại lệ `CategoryNotFoundException` và `CategoryAlreadyExistsException`.
  - [`app/domain/repositories/category_repository.py`](file:///d:/monitoring-tool/monitoring-test-batch/app/domain/repositories/category_repository.py): Interface `CategoryRepository` trừu tượng cho thao tác lưu trữ danh mục.
- **Infrastructure Layer**:
  - [`app/infrastructure/db/models/category_model.py`](file:///d:/monitoring-tool/monitoring-test-batch/app/infrastructure/db/models/category_model.py): Model SQLAlchemy `CategoryModel` cho bảng `categories`.
  - [`app/infrastructure/db/repositories/category_repository_impl.py`](file:///d:/monitoring-tool/monitoring-test-batch/app/infrastructure/db/repositories/category_repository_impl.py): Cài đặt `SQLAlchemyCategoryRepository` thực thi CRUD dữ liệu với SQLAlchemy Async Session.
- **Use Cases Layer**:
  - [`app/use_cases/category_use_cases.py`](file:///d:/monitoring-tool/monitoring-test-batch/app/use_cases/category_use_cases.py): Triển khai các Use Cases `CreateCategoryUseCase`, `GetCategoryUseCase`, `ListCategoriesUseCase`, `UpdateCategoryUseCase`, `DeleteCategoryUseCase`.
- **Presentation & API Layer**:
  - [`app/presentation/schemas/category_schema.py`](file:///d:/monitoring-tool/monitoring-test-batch/app/presentation/schemas/category_schema.py): Pydantic models `CategoryCreate`, `CategoryUpdate`, `CategoryResponse`, `CategoryListResponse`.
  - [`app/presentation/api/v1/endpoints/category_router.py`](file:///d:/monitoring-tool/monitoring-test-batch/app/presentation/api/v1/endpoints/category_router.py): Khai báo 5 endpoints chính cho danh mục (`GET`, `POST`, `PUT`, `DELETE`).
  - [`app/presentation/api/v1/dependencies.py`](file:///d:/monitoring-tool/monitoring-test-batch/app/presentation/api/v1/dependencies.py): Bổ sung Dependency Injection cho Category Repository và Use Cases.
  - [`app/presentation/api/v1/router.py`](file:///d:/monitoring-tool/monitoring-test-batch/app/presentation/api/v1/router.py): Tích hợp `category_router` vào router chính `/v1`.

---

### 2. Refactoring & Enhancements: Product Module Integration
- **Relational Mapping**:
  - Thay thế trường `category: str` bằng `category_id: Optional[int]` trong Entity, Model SQLAlchemy, Use Cases, và Schemas.
  - Tạo quan hệ Foreign Key (`category_id` -> `categories.id`) và SQLAlchemy `relationship("CategoryModel")` để tự động load thông tin danh mục.
- **Pagination & Response Updates**:
  - Cập nhật `ListProductsUseCase` và `ProductRepository` trả về tuple `(items, total)` hỗ trợ phân trang chuẩn.
  - Cập nhật `ProductResponse` schema hỗ trợ nhúng thông tin đối tượng `category` chi tiết.

---

### 3. Automated Tests
- [`tests/test_category_api.py`](file:///d:/monitoring-tool/monitoring-test-batch/tests/test_category_api.py): Bổ sung toàn bộ unit/integration test cases cho các API danh mục (Tạo mới, trùng tên, Lấy chi tiết, Cập nhật, Xóa, Phân trang).
- [`tests/test_product_api.py`](file:///d:/monitoring-tool/monitoring-test-batch/tests/test_product_api.py): Cập nhật lại các test suite sản phẩm phù hợp với cấu trúc `category_id`.

---

## 🧪 Testing Plan
- [x] Đã chạy toàn bộ test suite bằng `pytest`. Tất cả test cases trong `test_category_api.py` và `test_product_api.py` đều PASS.
- [x] Kiểm tra thành công các trường hợp:
  - `POST /api/v1/categories`: Tạo danh mục mới thành công & trả về 409 nếu trùng tên.
  - `GET /api/v1/categories`: Phân trang danh mục chính xác (`items`, `total`).
  - `POST /api/v1/products`: Tạo sản phẩm gắn với `category_id`.
  - `GET /api/v1/products/{id}`: Trả về thông tin sản phẩm cùng đối tượng danh mục lồng nhau (`category`).

---

## ✅ Checklist
- [x] Tuân thủ kiến trúc Clean Architecture của dự án.
- [x] Đã bao gồm Unit & Integration Tests.
- [x] Đã cập nhật và tương thích ngược/sửa đổi toàn bộ API cũ liên quan đến Product.
