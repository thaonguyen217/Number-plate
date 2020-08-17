# NUMBER PLATE:

Nhận dạng biển số xe bằng cách quét qua ảnh (hoặc camera) có chứa hình ảnh xe hơi, ảnh biển số xe sẽ được lưu vào file Resource/Scanned theo thứ tự xuất hiện trong đoạn video/webcam hoặc trùng tên file ảnh được sử dụng trong Resource.

Phương pháp :
- Sử dụng Shaarcascade_russian_plate_number.xml để nhận diện biển số xe, đầu ra là ảnh vùng biển số của xe.
- Tìm contour trong ảnh thu được ở bước trên để khoanh vùng biển số xe, loại nền không cần thiết

Các file .py :
- usingImage : Sử dụng đầu vào là ảnh xe hơi
- usingCamera : Sử dụng đầu vào là ảnh từ webcam, nhấn 's' để lưu lại ảnh biển số xe
![p2](https://user-images.githubusercontent.com/49630112/90391216-f1958880-e0b6-11ea-82ef-2fd2575ebdc2.jpg)
![workflow](https://user-images.githubusercontent.com/49630112/90391322-1f7acd00-e0b7-11ea-94cd-850c5400ba9a.jpg)
