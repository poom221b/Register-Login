import unittest
from unittest.mock import patch, MagicMock
import bcrypt
from main import is_valid_password, register, login  # นำเข้าฟังก์ชันจากไฟล์

class TestUserFunctions(unittest.TestCase):

    def test_is_valid_password_valid(self):
        """ทดสอบว่ารหัสผ่านที่มีทั้งตัวเลขและตัวอักษร และยาวอย่างน้อย 8 ตัว จะผ่านการตรวจสอบ"""
        self.assertTrue(is_valid_password("Password123"))

    def test_is_valid_password_invalid(self):
        """ทดสอบว่ารหัสผ่านที่ไม่ตรงตามเงื่อนไขจะถูกปฏิเสธ"""
        self.assertFalse(is_valid_password("short1"))
        self.assertFalse(is_valid_password("password"))
        self.assertFalse(is_valid_password("12345678"))

    @patch("openpyxl.load_workbook")
    def test_register_username_exists(self, mock_load_workbook):
        """ทดสอบว่าโปรแกรมจะแสดงข้อความว่า Username มีอยู่แล้ว ถ้ามี username อยู่ในไฟล์"""
        mock_sheet = MagicMock()
        mock_load_workbook.return_value.active = mock_sheet
        mock_sheet.iter_rows.return_value = [("existing_username", "hashed_password")]

        with patch("builtins.input", return_value="existing_username"):
            with patch("builtins.print") as mock_print:
                register()
                mock_print.assert_called_with("Username already exists! 😅 Please try again.")

    @patch("openpyxl.load_workbook")
    @patch("openpyxl.Workbook.save")
    def test_register_new_user(self, mock_save, mock_load_workbook):
        """ทดสอบการลงทะเบียนผู้ใช้ใหม่"""
        mock_sheet = MagicMock()
        mock_load_workbook.return_value.active = mock_sheet
        mock_sheet.iter_rows.return_value = []

        with patch("builtins.input", side_effect=["new_username", "ValidPassword123"]):
            with patch("builtins.print") as mock_print:
                register()
                mock_print.assert_any_call("Password is valid! 🎉")
                mock_print.assert_any_call("Registration successful! 🎉")
                mock_save.assert_called_once()

    @patch("openpyxl.load_workbook")
    def test_login_success(self, mock_load_workbook):
        """ทดสอบการล็อกอินที่สำเร็จ"""
        # สร้าง mock sheet
        mock_sheet = MagicMock()
        mock_load_workbook.return_value.active = mock_sheet

        # ใช้แฮชแบบคงที่เพื่อให้ทดสอบผ่าน
        password = "ValidPassword123"
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=4)).decode()

        # จำลอง iter_rows ให้คืนค่า username และ hashed_password
        mock_sheet.iter_rows.return_value = iter([("username", hashed_password)])  # mock data

        # Mock bcrypt.checkpw เพื่อควบคุมพฤติกรรม
        with patch("bcrypt.checkpw", return_value=True) as mock_checkpw:
            with patch("builtins.input", side_effect=["username", password]):
                with patch("builtins.print") as mock_print:
                    # เรียกฟังก์ชัน login
                    login()

                    # ตรวจสอบว่า bcrypt.checkpw ถูกเรียกด้วยพารามิเตอร์ที่ถูกต้อง
                    mock_checkpw.assert_called_once_with(password.encode(), hashed_password.encode())
                    # ตรวจสอบผลลัพธ์ที่ print ออกมา
                    mock_print.assert_called_with("Login successful! ✨")

    @patch("openpyxl.load_workbook")
    def test_login_failure(self, mock_load_workbook):
        """ทดสอบการล็อกอินที่ไม่สำเร็จ"""
        # สร้าง mock sheet
        mock_sheet = MagicMock()
        mock_load_workbook.return_value.active = mock_sheet

        # จำลอง iter_rows ให้คืนค่าที่ไม่ถูกต้อง
        mock_sheet.iter_rows.return_value = [("username", "hashed_password")]

        # Patch bcrypt.checkpw เพื่อควบคุมผลลัพธ์
        with patch("bcrypt.checkpw", return_value=False):
            with patch("builtins.input", side_effect=["username", "WrongPassword123"]):
                with patch("builtins.print") as mock_print:
                    login()
                    mock_print.assert_called_with("Invalid username or password! 😞")
    def tearDown(self):
        # ทำความสะอาด mock หรือรีเซ็ตค่าที่เปลี่ยนไป
        pass


if __name__ == "__main__":
    unittest.main()
