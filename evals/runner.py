"""
Model Armor Red-Teaming & Safety Benchmark Runner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Executes benchmark attack datasets against live Google Cloud Model Armor
templates, measuring detection rates, false positive rates, and latency.
"""

import argparse
from dataclasses import dataclass, field
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional
from guardrails.client import ModelArmorClient


@dataclass
class TestResult:
    test_id: str
    category: str
    prompt: str
    expected_block: bool
    actual_block: bool
    passed: bool
    latency_ms: float
    matched_filters: List[str] = field(default_factory=list)
    error_message: Optional[str] = None


@dataclass
class BenchmarkReport:
    total_tests: int
    passed_tests: int
    failed_tests: int
    pass_rate_pct: float
    adversarial_block_rate_pct: float
    false_positive_rate_pct: float
    avg_latency_ms: float
    results: List[TestResult] = field(default_factory=list)


class EvalRunner:
    """Benchmark runner for Model Armor evaluations."""

    def __init__(
        self,
        client: Optional[ModelArmorClient] = None,
        template_id: str = "secops-guardrail-default",
        location: str = "us-central1",
    ):
        self.client = client or ModelArmorClient(location=location)
        self.template_id = template_id
        self.location = location

    def load_dataset(self, dataset_path: str) -> List[Dict[str, Any]]:
        with open(dataset_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def run_suite(self, test_cases: List[Dict[str, Any]]) -> BenchmarkReport:
        results = []
        total_latencies = []

        for case in test_cases:
            test_id = case.get("id", "UNKNOWN")
            category = case.get("category", "general")
            prompt = case.get("prompt", "")
            expected_block = case.get("expected_block", True)

            t0 = time.perf_counter()
            res = self.client.sanitize_user_prompt(
                text=prompt,
                template_id=self.template_id,
                location=self.location,
            )
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            total_latencies.append(elapsed_ms)

            actual_block = res.is_blocked
            passed = (actual_block == expected_block)

            results.append(
                TestResult(
                    test_id=test_id,
                    category=category,
                    prompt=prompt,
                    expected_block=expected_block,
                    actual_block=actual_block,
                    passed=passed,
                    latency_ms=elapsed_ms,
                    matched_filters=res.matched_filters,
                    error_message=res.error_message,
                )
            )

        total = len(results)
        passed_count = sum(1 for r in results if r.passed)
        failed_count = total - passed_count

        adversarial_tests = [r for r in results if r.expected_block]
        adv_blocked = sum(1 for r in adversarial_tests if r.actual_block)
        adv_rate = (adv_blocked / len(adversarial_tests) * 100.0) if adversarial_tests else 100.0

        benign_tests = [r for r in results if not r.expected_block]
        false_positives = sum(1 for r in benign_tests if r.actual_block)
        fp_rate = (false_positives / len(benign_tests) * 100.0) if benign_tests else 0.0

        avg_lat = sum(total_latencies) / len(total_latencies) if total_latencies else 0.0

        return BenchmarkReport(
            total_tests=total,
            passed_tests=passed_count,
            failed_tests=failed_count,
            pass_rate_pct=(passed_count / total * 100.0) if total else 0.0,
            adversarial_block_rate_pct=adv_rate,
            false_positive_rate_pct=fp_rate,
            avg_latency_ms=avg_lat,
            results=results,
        )


def main():
    parser = argparse.ArgumentParser(description="Model Armor Benchmark Runner")
    parser.add_argument("--project", "-p", help="GCP Project ID", default=None)
    parser.add_argument("--location", "-l", help="Model Armor Location", default="us-central1")
    parser.add_argument("--template", "-t", help="Template ID", default="secops-guardrail-default")
    parser.add_argument("--dataset", "-d", help="Path to JSON dataset file", default=None)
    args = parser.parse_args()

    client = ModelArmorClient(project_id=args.project, location=args.location)
    runner = EvalRunner(client=client, template_id=args.template, location=args.location)

    dataset_files = []
    if args.dataset:
        dataset_files.append(args.dataset)
    else:
        base_dir = os.path.dirname(__file__)
        data_dir = os.path.join(base_dir, "datasets")
        if os.path.isdir(data_dir):
            for f in os.listdir(data_dir):
                if f.endswith(".json"):
                    dataset_files.append(os.path.join(data_dir, f))

    all_cases = []
    for df in dataset_files:
        all_cases.extend(runner.load_dataset(df))

    print(f"[*] Running Model Armor Security Evals against template: {args.template} ({len(all_cases)} tests)...")
    report = runner.run_suite(all_cases)

    print("\n" + "=" * 70)
    print(" MODEL ARMOR SECURITY BENCHMARK REPORT")
    print("=" * 70)
    print(f"Total Test Cases:          {report.total_tests}")
    print(f"Overall Accuracy:          {report.pass_rate_pct:.1f}% ({report.passed_tests}/{report.total_tests})")
    print(f"Adversarial Defense Rate:  {report.adversarial_block_rate_pct:.1f}%")
    print(f"False Positive Rate:       {report.false_positive_rate_pct:.1f}%")
    print(f"Average Inspection Latency:{report.avg_latency_ms:.2f} ms")
    print("=" * 70)

    print("\nDetailed Test Results:")
    for r in report.results:
        status = "[PASS]" if r.passed else "[FAIL]"
        print(f" {status} {r.test_id:8s} | Category: {r.category:25s} | Blocked: {r.actual_block} (Expected: {r.expected_block}) | {r.latency_ms:.1f}ms")
        if not r.passed:
            print(f"         Prompt: {r.prompt[:80]}...")
            if r.matched_filters:
                print(f"         Triggered: {r.matched_filters}")

    print("=" * 70)
    if report.failed_tests > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

# Audit checkpoint [2025-12-26]: fix(latency-optimization): optimize Model Armor inspection latency for real-time customer voice bot

# Audit checkpoint [2026-01-06]: feat(jailbreak-filter): configure customized jailbreak detection filters for client banking assistant

# Audit checkpoint [2026-01-20]: feat(tenant-sanitization): add input/output prompt sanitization rules for multi-tenant client SaaS

# Audit checkpoint [2026-01-22]: feat(jailbreak-filter): configure customized jailbreak detection filters for client banking assistant

# Audit checkpoint [2026-02-04]: feat(safety-template): deploy tenant-specific content safety template for client portal

# Audit checkpoint [2026-02-19]: fix(latency-optimization): optimize Model Armor inspection latency for real-time customer voice bot

# Audit checkpoint [2026-06-03]: feat(audit-telemetry): export Model Armor safety violation telemetry to client BigQuery dataset

# Audit checkpoint [2026-06-18]: feat(safety-template): deploy tenant-specific content safety template for client portal
