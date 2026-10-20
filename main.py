"""
main.py - 系统主入口（支持控制台交互，方便演示与验收）
"""
import sys
from database import Database
from statistics_service import StatisticsService
from self_service import SelfServicePortal

def manager_menu(stats_service: StatisticsService):
    while True:
        print("\n================== 管理层统计看板 (FR12/FR14) ==================")
        print("1. 查看总体指标统计 (总人数/平均时薪/部门数)")
        print("2. 查看部门人员分布统计")
        print("3. 查看排班与工时统计")
        print("0. 返回主菜单")
        choice = input("请选择操作: ").strip()

        if choice == "1":
            overview = stats_service.get_overview_statistics()
            print("\n--- 总体指标 ---")
            print(f"在职员工总数: {overview['total_employees']} 人")
            print(f"平均每小时薪资: ¥{overview['avg_hourly_rate']}")
            print(f"涵盖部门数量: {overview['total_departments']}")
            print(f"部门列表: {', '.join(overview['department_list'])}")
        elif choice == "2":
            dist = stats_service.get_department_distribution()
            print("\n--- 部门人员分布 ---")
            for dept, count in dist.items():
                print(f" • {dept}: {count} 人")
        elif choice == "3":
            shift_stats = stats_service.get_shift_statistics()
            print("\n--- 排班与班次分布 ---")
            print(f"计划总班次: {shift_stats['total_shifts']} 次")
            print(f"累计工时: {shift_stats['total_scheduled_hours']} 小时")
            for period, count in shift_stats["period_breakdown"].items():
                print(f" • {period}班次: {count} 次")
        elif choice == "0":
            break
        else:
            print("输入无效，请重新选择。")

def employee_menu(portal: SelfServicePortal, emp_id: str):
    while True:
        emp = portal.db.get_employee_by_id(emp_id)
        print(f"\n================ 员工自助服务中心 (FR15) - {emp.name} ================")
        print("1. 查看个人资料与排班")
        print("2. 修改绑定邮箱")
        print("0. 退出登录")
        choice = input("请选择操作: ").strip()

        if choice == "1":
            print("\n--- 个人资料 ---")
            print(f"工号: {emp.emp_id}")
            print(f"姓名: {emp.name}")
            print(f"部门: {emp.department}")
            print(f"当前邮箱: {emp.email}")
            print(f"时薪: ¥{emp.hourly_rate}")
            print("\n--- 我的排班记录 ---")
            my_shifts = [s for s in portal.db.shifts if s.emp_id == emp.emp_id]
            if my_shifts:
                for s in my_shifts:
                    print(f" • 日期: {s.date} | 班次: {s.period} | 工时: {s.hours}h")
            else:
                print("暂无已安排的班次。")
        elif choice == "2":
            new_email = input("请输入新的邮箱地址: ").strip()
            success, msg = portal.update_own_email(emp.emp_id, new_email)
            print(f"\n[{'成功' if success else '失败'}] {msg}")
        elif choice == "0":
            break
        else:
            print("输入无效，请重新选择。")

def main():
    db = Database()
    stats_service = StatisticsService(db)
    portal = SelfServicePortal(db)

    while True:
        print("\n================== 美体商城 (Meítǐ Shāngchéng) 系统 ==================")
        print("1. 管理端登录 (查看统计 - FR12/FR14)")
        print("2. 员工端登录 (员工自助 - FR15)")
        print("0. 退出系统")
        top_choice = input("请选择登录身份: ").strip()

        if top_choice == "1":
            manager_menu(stats_service)
        elif top_choice == "2":
            emp_id = input("请输入工号 (如 E001, E002): ").strip()
            pwd = input("请输入密码 (默认 123456): ").strip()
            emp = portal.authenticate(emp_id, pwd)
            if emp:
                employee_menu(portal, emp.emp_id)
            else:
                print("工号或密码错误！")
        elif top_choice == "0":
            print("系统已退出。")
            sys.exit(0)
        else:
            print("输入无效，请重新输入。")

if __name__ == "__main__":
    main()