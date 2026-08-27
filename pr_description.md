# PR Title
`feat(user): Thêm API danh sách và chi tiết User (List & Get User API)`

---

# PR Description (Mô tả Pull Request)

## 📌 Summary
PR này bổ sung tính năng quản lý người dùng (User Management) theo kiến trúc Clean Architecture cho ứng dụng FastAPI, bao gồm các API lấy danh sách người dùng (`GET /api/v1/users`) và lấy chi tiết người dùng theo ID (`GET /api/v1/users/{user_id}`).

---

## 🛠️ Key Changes
### 1. Domain Layer
- `app/domain/entities/user.py`: Định nghĩa entity `User`.
- `app/domain/exceptions/user_exceptions.py`: Định nghĩa các ngoại lệ `UserNotFoundException` và `UserAlreadyExistsException`.
- `app/domain/repositories/user_repository.py`: Interface `UserRepository` trừu tượng.

### 2. Infrastructure Layer
- `app/infrastructure/db/models/user_model.py`: Mẫu bảng `UserModel` với SQLAlchemy.
- `app/infrastructure/db/repositories/user_repository_impl.py`: Cài đặt `SQLAlchemyUserRepository` thực thi các truy vấn DB.

### 3. Use Cases Layer
- `app/use_cases/user_use_cases.py`: Lớp xử lý logic nghiệp vụ `ListUsersUseCase` và `GetUserUseCase`.

### 4. Presentation & API Layer
- `app/presentation/schemas/user_schema.py`: Định nghĩa Pydantic models `UserBase`, `UserCreate`, `UserResponse`.
- `app/presentation/api/v1/endpoints/user_router.py`: Đăng ký các endpoints `GET /users` và `GET /users/{user_id}`.
- `app/presentation/api/v1/dependencies.py`: Cấu hình Dependency Injection cho UserRepository & UseCases.
- `app/presentation/api/v1/router.py`: Thêm `user_router` vào `api_router` chính của `/v1`.

### 5. Testing
- `tests/test_user_api.py`: Thêm các test case cho API người dùng với `pytest` và `httpx`.

---

## 🧪 Testing Plan
- [x] Đã chạy unit test cho API User (`tests/test_user_api.py`).
- [x] Kiểm tra thành công các trường hợp:
  - `GET /api/v1/users` trả về danh sách rỗng ban đầu (Status 200).
  - `GET /api/v1/users/999` khi không tồn tại ID (Status 404).

---

## ✅ Checklist
- [x] Code tuân thủ kiến trúc Clean Architecture của dự án.
- [x] Đã bao gồm Unit Tests.
- [x] Không còn file tạm hoặc log dư thừa.
