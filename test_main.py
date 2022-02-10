from unittest import TestCase

import levels.scape
import main as SUT


class Test(TestCase):
    header_text = ""
    row_text_1 = ""

    def setUp(self) -> None:
        self.header_text = 'Company\nLocation | Date\nLevel Name\nTag\nYears of Experience\nAt Company / Total\nTotal Compensation\nBase | Stock (/yr) | Bonus'
        self.row_text_1 = 'Hudson River Trading\nNew York, NY | 1/3/2022\nSWE\nCore\n1 / 5\n$1,000,000\n150k | N/A | 850k'
        self.row_text_2 = 'Hudson River Trading\nNew York, NY | 1/3/2022\nSWE\nCore\n1 / 5\n$1,000,000\n150k | N/A | 850k'
        super().setUp()

    def test_get_table_data(self):
        rows = levels.scape.get_table_data([self.row_text_1, self.row_text_2])
        self.assertIsNotNone(rows, "result should not be None")
        self.assertIsNotNone(rows[0], "first row should not be None")
        for i in range(2):
            row = rows[i]
            self.assertEquals("Hudson River Trading", row[0])
            self.assertEquals("New York, NY", row[1])
            self.assertEquals("1/3/2022", row[2])
            self.assertEquals("SWE", row[3])
            self.assertEquals("Core", row[4])
            self.assertEquals("1", row[5])
            self.assertEquals("5", row[6])
            self.assertEquals("$1,000,000", row[7])
            self.assertEquals("150k", row[8])
            self.assertEquals("N/A", row[9])
            self.assertEquals("850k", row[10])

    def test_get_table_data_some_bad_rows(self):
        self.row_text_1 = 'Hudson River Trading\nNew York, NY | 1/3/2022\nSWE\nCore\n1 / 5\n$1,000,000\n150k | N/A | 850k'
        self.row_text_2 = 'Hudson River Trading\nNew York, NY\nSWE\nCore\n$1,000,000\n150k | N/A | 850k'
        self.row_text_3 = 'Hudson River Trading\nSWE\nCore\n$1,000,000\n150k | N/A | 850k'
        self.row_text_4 = 'Hudson River Trading\nNew York, NY | 1/3/2022\nSWE\nCore\n1 / 5\n$1,000,000\n150k | N/A | 850k'
        rows = levels.scape.get_table_data([self.row_text_1, self.row_text_2, self.row_text_3, self.row_text_4])
        self.assertEquals(len(rows), 2)
        for i in range(2):
            row = rows[i]
            self.assertEquals("Hudson River Trading", row[0])
            self.assertEquals("New York, NY", row[1])
            self.assertEquals("1/3/2022", row[2])
            self.assertEquals("SWE", row[3])
            self.assertEquals("Core", row[4])
            self.assertEquals("1", row[5])
            self.assertEquals("5", row[6])
            self.assertEquals("$1,000,000", row[7])
            self.assertEquals("150k", row[8])
            self.assertEquals("N/A", row[9])
            self.assertEquals("850k", row[10])

    def test_get_table_data_all_bad_rows(self):
        self.row_text_1 = 'Hudson River Trading\nNew York, NY | 1/3/2022\nSWE\nCore\n1 / 5\n150k | N/A | 850k'
        self.row_text_2 = 'Hudson River Trading\nNew York, NY\nSWE\nCore\n$1,000,000\n150k | N/A | 850k'
        rows = levels.scape.get_table_data([self.row_text_1, self.row_text_2])
        self.assertEqual(len(rows), 0)

    def test_get_table_headers(self):
        headers = levels.scape.get_table_headers(self.header_text)
        self.assertIsNotNone(headers, "results should not be None")
        self.assertEqual(11, len(headers))

    def test_method(self):
        arrs = [["hello", "world"], ["goodbye", "world"]]

        def genexpr(a):
            yield a[0]
            yield a[1]

        # it = lambda x: genexpr(x)

        print([list(genexpr(arr)) for arr in arrs])
