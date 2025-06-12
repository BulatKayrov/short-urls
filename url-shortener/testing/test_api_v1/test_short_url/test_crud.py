import unittest


# if getenv("TESTING") != "1":
#     raise EnvironmentError("Must be run in testing mode")


def total(a: int, b: int) -> int:
    return a + b


class TotalTestCase(unittest.TestCase):

    def test_total(self) -> None:
        a = 1
        b = 9
        result = total(a, b)
        expected = 10
        self.assertEqual(
            first=result,
            second=expected,
            msg="Сообщение об ошибке если тест не пройден",
        )
