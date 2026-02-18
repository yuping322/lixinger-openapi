#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量技能执行器：支持批量关键词调用技能，结果自动保存到文件夹
"""
import json
import os
import time
from pathlib import Path
from typing import List, Dict
from skill_bridge import run_skill

class BatchSkillExecutor:
    def __init__(self, output_dir: str = "skill_outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.failed_tasks = []
        self.successful_tasks = []

    def _get_output_path(self, task: Dict) -> Path:
        """生成任务输出路径"""
        skill_name = task["skill"]
        params_str = "_".join([f"{k}_{v}" for k, v in task["params"].items()])
        filename = f"{skill_name}_{params_str}_{int(time.time())}.json"
        return self.output_dir / filename

    def _save_result(self, task: Dict, result: Dict):
        """保存结果到文件"""
        output_path = self._get_output_path(task)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                "task": task,
                "result": result,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }, f, ensure_ascii=False, indent=2)

    def execute_tasks(self, tasks: List[Dict], skip_existing: bool = True, delay: float = 1.0):
        """
        批量执行任务
        :param tasks: 任务列表，每个任务格式：{"skill": "技能名称", "params": {参数字典}}
        :param skip_existing: 是否跳过已存在的结果
        :param delay: 任务之间的延迟（秒），避免API限流
        """
        total = len(tasks)
        print(f"🚀 开始批量执行 {total} 个任务")
        print("=" * 80)

        for i, task in enumerate(tasks, 1):
            print(f"\n📋 任务 {i}/{total}: {task['skill']} - {task['params']}")

            # 检查是否已存在结果
            output_path = self._get_output_path(task)
            if skip_existing and output_path.exists():
                print(f"⏭️  跳过已存在的结果: {output_path}")
                self.successful_tasks.append(task)
                continue

            try:
                # 执行技能
                result = run_skill(task["skill"], task["params"])

                if "error" in result:
                    print(f"❌ 执行失败: {result['error']}")
                    self.failed_tasks.append({
                        "task": task,
                        "error": result["error"]
                    })
                else:
                    print(f"✅ 执行成功，结果保存到: {output_path}")
                    self._save_result(task, result)
                    self.successful_tasks.append(task)

                # 延迟避免限流
                time.sleep(delay)

            except Exception as e:
                print(f"💥 执行异常: {str(e)}")
                self.failed_tasks.append({
                    "task": task,
                    "error": str(e)
                })

        # 输出执行报告
        print("\n" + "=" * 80)
        print("📊 批量执行完成报告")
        print("=" * 80)
        print(f"总任务数: {total}")
        print(f"成功: {len(self.successful_tasks)} | 失败: {len(self.failed_tasks)} | 成功率: {len(self.successful_tasks)/total*100:.1f}%")

        if self.failed_tasks:
            print("\n❌ 失败任务列表:")
            for fail in self.failed_tasks:
                print(f"  - {fail['task']['skill']} {fail['task']['params']}: {fail['error'][:50]}...")

        # 保存失败任务列表
        if self.failed_tasks:
            failed_path = self.output_dir / "failed_tasks.json"
            with open(failed_path, 'w', encoding='utf-8') as f:
                json.dump(self.failed_tasks, f, ensure_ascii=False, indent=2)
            print(f"\n💾 失败任务列表已保存到: {failed_path}")

        return self.successful_tasks, self.failed_tasks

def create_stock_analysis_tasks(stock_codes: List[str], years: int = 5) -> List[Dict]:
    """创建批量个股财报分析任务"""
    return [
        {
            "skill": "财报分析",
            "params": {"stock_code": code, "years": years}
        } for code in stock_codes
    ]

def create_market_analysis_tasks(markets: List[str] = ["cn", "hk", "us"]) -> List[Dict]:
    """创建批量市场概览任务"""
    return [
        {
            "skill": "市场概览",
            "params": {"market": market}
        } for market in markets
    ]

if __name__ == "__main__":
    # 示例使用：批量分析贵州茅台、腾讯控股、苹果公司财报
    executor = BatchSkillExecutor()

    # 示例1：批量分析多个股票财报
    stock_tasks = create_stock_analysis_tasks(["600519", "00700", "AAPL"], years=5)
    executor.execute_tasks(stock_tasks)

    # 示例2：批量获取多市场概览
    # market_tasks = create_market_analysis_tasks(["cn", "hk", "us"])
    # executor.execute_tasks(market_tasks)

    # 示例3：自定义任务列表
    # custom_tasks = [
    #     {"skill": "高股息选股", "params": {}},
    #     {"skill": "行业轮动分析", "params": {}},
    #     {"skill": "北向资金分析", "params": {}},
    # ]
    # executor.execute_tasks(custom_tasks)
