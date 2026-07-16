# raw/ — Tài liệu nạp vào

Nơi lưu file tài liệu thô để phân tích bằng skill **doc-analyzer**.

## Định dạng hỗ trợ
`.pdf` · `.docx` · `.xlsx` · `.csv` · `.md` · `.txt` · `.html`

## Cách dùng
1. Bỏ file vào thư mục này
2. Gọi `/doc-analyzer raw/<tên-file>` (hoặc nhờ Claude phân tích)
3. doc-analyzer trích xuất tri thức → xuất khối `@extracted_knowledge` YAML trong context (không sinh file)
4. Claude dừng lại, hỏi bước tiếp theo
