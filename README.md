# 🎮 Trò Chơi Cờ Caro

Dự án trò chơi Cờ Caro kích thước $9 \times 9$ (bản 4 nước thắng) được phát triển hoàn toàn bằng **Python** và **Tkinter** với cấu trúc mã nguồn chia module hóa rõ ràng, dễ bảo trì, phục vụ cho việc nghiên cứu và đối sánh hiệu năng thuật toán giữa Minimax và Alpha-Beta Pruning.

---

## ✨ Tính năng nổi bật

- **Hai thuật toán AI nâng cao**: Hỗ trợ chuyển đổi linh hoạt giữa thuật toán **Minimax** truyền thống và thuật toán **Cắt tỉa Alpha-Beta** nhằm tăng tốc độ tìm kiếm.
- **Tính năng So sánh hiệu năng**: Chức năng độc đáo giúp thống kê số lượng nút (Nodes) đã duyệt và thời gian tính toán của cả hai thuật toán qua từng độ sâu khác nhau ($1 \to 4$).
- **Chặn nước đi cấp bách**: AI tự động phát hiện để chặn đối thủ hoặc kết thúc ván đấu ngay lập tức nếu có thời cơ thắng mà không cần chờ duyệt sâu.

---

## 🧠 Cơ chế hoạt động của AI (Core AI Layer)

- **Hàm lượng định thế cờ (Heuristic Evaluation)**: AI tự động quét bàn cờ theo 4 hướng (Ngang, Dọc, Chéo xuôi, Chéo ngược) để chấm điểm trạng thái dựa trên số lượng quân cờ liên tiếp và trạng thái bị chặn (Bị chặn 1 đầu hoặc cả 2 đầu).
- **Phát hiện nước đi cấp bách (Urgent Move Detection)**: Tách riêng một lớp xử lý chiến thuật ưu tiên tốc độ $0.00s$. AI sẽ ngay lập tức đi nước quyết định nếu phát hiện cơ hội thắng 4 quân hoặc phải chặn đối thủ chuẩn bị thắng, không cần tốn tài nguyên duyệt cây thuật toán.
- **Sắp xếp nước đi tối ưu (Move Ordering Hint)**: Các nước đi tiềm năng được ưu tiên tìm kiếm từ tâm bàn cờ ra ngoài (tính theo khoảng cách Manhattan) giúp thuật toán Cắt tỉa Alpha-Beta đạt hiệu suất cắt nhánh tối đa.

---

## ⏳ Quản lý quỹ thời gian (Time Budget Control)

- **Cơ chế Timeout Protection**: Hệ thống cấu hình cứng giới hạn thời gian tính toán tối đa cho mỗi nước đi thông qua hằng số `TIME_LIMIT = 5.0s`. 
- **Ngắt toán an sau**: Nếu độ sâu tìm kiếm quá lớn dẫn đến bùng nổ tổ hợp nút, thuật toán sẽ tự động kích hoạt ngoại lệ `Timeout`, lập tức dừng duyệt cây để giữ ứng dụng không bị đóng băng (Not Responding) và trả về nước đi tốt nhất tìm được tính đến thời điểm ngắt.

---

## 📊 Chế độ thực nghiệm & Đối sánh (Benchmark Mode)

Chương trình tích hợp sẵn bộ công cụ thực nghiệm trực quan thông qua nút **"So sánh"** trên giao diện:
- Hệ thống sẽ chạy thử nghiệm động cả 2 thuật toán **Minimax** và **Alpha-Beta Pruning** trên cùng một trạng thái bàn cờ hiện tại.
- Kiểm thử tự động tăng dần qua các cấp độ sâu (Depth từ $1 \to 4$).
- Xuất báo cáo dạng bảng (Structured ASCII Table) ngay tại vùng Logs của ứng dụng bao gồm các chỉ số: Độ sâu (D), Thuật toán, Nước đi khuyến nghị (Hàng, Cột), Điểm số lượng định (Score), Tổng số nút đã duyệt (Nodes Visited), và Thời gian thực thi chi tiết (Time).

---

## 📁 Cấu trúc dự án (Project Layout)

| Đường dẫn (Path) | Vai trò trong đồ án (Role) |
| :--- | :--- |
| `src/` | Thư mục chứa toàn bộ các module mã nguồn chính của trò chơi. |
| `__init__.py` | File rỗng để cấu trúc hệ thống nhận diện `src` là một gói package. |
| `config.py` | Quản lý cấu hình tập trung (Kích thước bàn cờ, điều kiện thắng, thời gian AI nghĩ). |
| `engine.py` | Lõi tư duy AI: Hàm lượng định thế cờ (`evaluate_board`), thuật toán tìm kiếm (`minimax`, `alpha_beta`) và chặn nước đi cấp bách (`find_urgent_move`). |
| `gui.py` | Quản lý toàn bộ giao diện đồ họa Tkinter (`CaroGUI`) và tương tác click chuột của người chơi. |
| `.gitignore` | File cấu hình tự động loại bỏ các tệp bộ nhớ đệm thừa (`__pycache__`) khi đồng bộ lên GitHub. |
| `main.py` | **Entry Point**: File chạy chính của chương trình. Người dùng chỉ cần khởi chạy file này để mở game. |
| `requirement.txt` | File danh sách công bố môi trường thực thi và các thư viện phụ thuộc tiêu chuẩn. |
| `report.docx` | Báo cáo chi tiết đồ án (Cơ sở lý thuyết, sơ đồ khối thuật toán và đánh giá kết quả thực nghiệm). |

---

## 🛠️ Hướng dẫn khởi chạy nhanh

### 1. Yêu cầu hệ thống
- Ngôn ngữ lập trình Python phiên bản 3.10 trở lên.
- Thư viện đồ họa: `tkinter` (Thư viện tiêu chuẩn, mặc định đi kèm sẵn khi cài đặt Python).

### 2. Cách thực thi chương trình
- **Bước 1**: Tải  thư mục mã nguồn này về máy tính của bạn và giải nén
- **Bước 2**: Click chuột vào khoảng trống trên thanh hiển thị đường dẫn (Address Bar) của thư mục vừa giải nén, xóa toàn bộ và gõ chữ `cmd` rồi nhấn phím **Enter** .
- **Bước 3**: Gõ câu lệnh sau để khởi chạy trò chơi:
  ```bash
  python main.py
