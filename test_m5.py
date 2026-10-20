"""
test_m5.py - 单元测试，确保 FR12/FR14 统计与 FR15 自助改邮箱功能正常
"""
import unittest
import os
import shutil
from database import Database, DATA_DIR
from statistics_service import StatisticsService
from self_service import SelfServicePortal

class TestM5Milestone(unittest.TestCase):
    def setUp(self):
        if os.path.exists(DATA_DIR):
            shutil.rmtree(DATA_DIR)
        self.db = Database()
        self.stats = StatisticsService(self.db)
        self.portal = SelfServicePortal(self.db)

    def test_statistics_overview_fr12_fr14(self):
        overview = self.stats.get_overview_statistics()
        self.assertEqual(overview["total_employees"], 4)
        self.assertGreater(overview["avg_hourly_rate"], 0)

        dist = self.stats.get_department_distribution()
        self.assertIn("Hardware", dist)
        self.assertEqual(dist["Hardware"], 2)

    def test_update_email_success_fr15(self):
        success, msg = self.portal.update_own_email("E001", "new_zhangsan@test.com")
        self.assertTrue(success)
        emp = self.db.get_employee_by_id("E001")
        self.assertEqual(emp.email, "new_zhangsan@test.com")

    def test_update_email_invalid_format(self):
        success, msg = self.portal.update_own_email("E001", "invalid_email_format")
        self.assertFalse(success)

    def test_update_email_duplicate(self):
        # 尝试将 E001 改成 E002 已有的邮箱
        success, msg = self.portal.update_own_email("E001", "lisi@meiti.com")
        self.assertFalse(success)

if __name__ == "__main__":
    unittest.main()