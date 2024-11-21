import unittest
from unittest.mock import patch, MagicMock
from main import is_valid_password, register


class TestRegistration(unittest.TestCase):

    # ทดสอบฟังก์ชันตรวจสอบพาสเวิด
    def test_is_valid_password(self):
        self.assertTrue(is_valid_password("password123"))  # ใช้พาสที่ถูกต้อง
        self.assertFalse(is_valid_password("pass"))  # ใช้พาสที่สั้นเกินไป
        self.assertFalse(is_valid_password("12345678"))  # ใช้พาสที่ไม่มีตัวอักษร

    # ทดสอบฟังก์ชัน register
    @patch("builtins.input", side_effect=["testuser", "password123"])  # mock input เพื่อไม่ต้องใส่ค่าจริง
    @patch("openpyxl.load_workbook")  # mock openpyxl load_workbook
    def test_register(self, mock_load_workbook, mock_input):
        # mock workbook
        mock_workbook = MagicMock()
        mock_sheet = MagicMock()
        mock_load_workbook.return_value = mock_workbook
        mock_workbook.active = mock_sheet
        mock_sheet.iter_rows.return_value = []  # ไม่มี user ในไฟล์

        # ทดสอบการลงทะเบียน
        register()  # เรียกฟังก์ชัน register

        mock_sheet.append.assert_called_once()  # เช็คว่าเรียก append ไปหนึ่งครั้ง
        mock_workbook.save.assert_called_once_with("users.xlsx")  # เช็คว่าเรียก save ด้วยชื่อไฟล์ที่ถูกต้อง


if __name__ == "__main__":
    unittest.main()
