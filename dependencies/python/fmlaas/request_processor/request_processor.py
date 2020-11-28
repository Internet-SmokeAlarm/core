class RequestProcessor:

    ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")

    def _is_string_name_valid(self, string: str) -> bool:
        return string and isinstance(string, str)

    def _is_int_name_valid(self, int_name: int) -> bool:
        return int_name is not None and isinstance(int_name, int)

    def _is_float_valid(self, val: float) -> bool:
        return val is not None and isinstance(val, type(0.0))

    def _valid_chars(self, string: str) -> bool:
        return len(set(string) - RequestProcessor.ALLOWED_CHARS) == 0