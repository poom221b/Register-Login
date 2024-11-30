import unittest
from unittest.mock import patch, MagicMock
from main import register, is_valid_password, login, load_workbook, Workbook
import bcrypt


class TestUserFunctions(unittest.TestCase):

    @patch('main.load_workbook')
    @patch('main.Workbook')
    @patch('bcrypt.hashpw')
    @patch('bcrypt.gensalt')
    @patch('bcrypt.checkpw')
    def test_register_new_user(self, mock_checkpw, mock_gensalt, mock_hashpw, mock_Workbook, mock_load_workbook):
        # Mock the workbook and sheet
        mock_workbook_instance = MagicMock()
        mock_sheet = MagicMock()
        mock_workbook_instance.active = mock_sheet
        mock_load_workbook.return_value = mock_workbook_instance

        # Mock bcrypt functions
        mock_gensalt.return_value = b"mocked_salt"
        mock_hashpw.return_value = b"mocked_hashed_password"
        mock_checkpw.return_value = True

        # Call the register function
        with patch('builtins.input', side_effect=["new_user", "validPass123"]):
            register()

        # Check if save was called once after appending a new user
        mock_workbook_instance.save.assert_called_once_with("users.xlsx")
        mock_sheet.append.assert_called_once()

    @patch('main.load_workbook')
    @patch('bcrypt.checkpw')
    def test_login_success(self, mock_checkpw, mock_load_workbook):
        mock_workbook_instance = MagicMock()
        mock_sheet = MagicMock()
        mock_workbook_instance.active = mock_sheet
        mock_load_workbook.return_value = mock_workbook_instance

        # Simulating database data
        mock_sheet.iter_rows.return_value = [("existing_user", b"mocked_hashed_password")]
        mock_checkpw.return_value = True  # Assuming the password check will pass

        with patch('builtins.input', side_effect=["existing_user", "validPass123"]):
            login()

        mock_sheet.iter_rows.assert_called_once()
        print("Login successful!")

    @patch('main.load_workbook')
    @patch('bcrypt.checkpw')
    def test_login_failure(self, mock_checkpw, mock_load_workbook):
        mock_workbook_instance = MagicMock()
        mock_sheet = MagicMock()
        mock_workbook_instance.active = mock_sheet
        mock_load_workbook.return_value = mock_workbook_instance

        mock_sheet.iter_rows.return_value = [("existing_user", b"mocked_hashed_password")]
        mock_checkpw.return_value = False  # Simulating password mismatch

        with patch('builtins.input', side_effect=["existing_user", "wrong_password"]):
            login()

        mock_sheet.iter_rows.assert_called_once()
        print("Invalid username or password.")

    def test_is_valid_password(self):
        self.assertTrue(is_valid_password("validPass123"))
        self.assertFalse(is_valid_password("short"))
        self.assertFalse(is_valid_password("NoNumber"))
        self.assertFalse(is_valid_password("12345678"))


if __name__ == "__main__":
    unittest.main()

