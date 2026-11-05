#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from core.config import Config
from core.db import Database
from core.quota import QuotaManager
from core.youtube_client import YouTubeClient
from modules.ideas import VideoIdeasModule
from modules.metadata import MetadataModule
from modules.timing import TimingModule
from modules.competitors import CompetitorInsightsModule
from modules.repurpose import RepurposeModule
from modules.sponsors import SponsorshipModule
from modules.monetization import MonetizationAccelerationModule
from reports.daily_digest import DailyDigestGenerator
from reports.weekly_report import WeeklyReportGenerator

MODULE_MAP = {
    "ideas": VideoIdeasModule,
    "metadata": MetadataModule,
    "timing": TimingModule,
    "competitors": CompetitorInsightsModule,
    "repurpose": RepurposeModule,
    "sponsors": SponsorshipModule,
    "monetization": MonetizationAccelerationModule
}

def main():
    parser = argparse.ArgumentParser(
        description="YouTube Social Media Manager Agent (Data API v3 & Analytics API)",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--module",
        choices=["all", "ideas", "metadata", "timing", "competitors", "repurpose", "sponsors", "monetization"],
        default=None,
        help="Run a specific strategy module or 'all'"
    )
    parser.add_argument(
        "--daily-digest",
        action="store_true",
        help="Generate the high-priority daily action digest"
    )
    parser.add_argument(
        "--weekly-report",
        action="store_true",
        help="Generate the comprehensive 7-module weekly audit report"
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Force run using sample/mock dataset without consuming API quota"
    )
    parser.add_argument(
        "--script",
        type=str,
        default=None,
        help="Draft script or topic for metadata module title/tag scoring"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to YAML configuration file"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory to save JSON artifacts and Markdown reports"
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Force refresh channel and competitor cache"
    )

    args = parser.parse_args()

    # If no flags passed, show help or run all by default
    if not args.module and not args.daily_digest and not args.weekly_report:
        print("[Agent] No specific module selected. Running full suite (--module all)...")
        args.module = "all"

    # 1. Load Config & Resources
    config = Config(config_path=args.config)
    if args.mock:
        config.use_mock_data = True

    db = Database(config.sqlite_db_path)
    quota = QuotaManager(config.sqlite_db_path, daily_limit=config.quota_daily_limit)
    client = YouTubeClient(config, db, quota)

    print(f"\n=======================================================")
    print(f"🎬 YouTube Social Media Manager Agent")
    print(f"Channel: {config.my_channel_id} | Timezone: {config.timezone}")
    print(f"Mode: {'MOCK DATASET' if config.use_mock_data or not config.youtube_api_key else 'LIVE API v3'}")
    print(f"=======================================================\n")

    # Initialize data cache
    client.initialize_data(force_refresh=args.refresh)

    # 2. Run Module(s)
    if args.module:
        target_keys = list(MODULE_MAP.keys()) if args.module == "all" else [args.module]

        for mod_key in target_keys:
            mod_class = MODULE_MAP[mod_key]
            instance = mod_class(config, db, quota)
            print(f"[*] Running Module: {mod_key.upper()}...")

            run_kwargs = {}
            if mod_key == "metadata" and args.script:
                run_kwargs["draft_topic_or_script"] = args.script

            res, md_text = instance.execute_and_export(output_dir=args.output_dir, **run_kwargs)
            print(f"    -> Exported: {args.output_dir}/{mod_key}.json & {args.output_dir}/{mod_key}.md")

            # Print concise preview if single module
            if len(target_keys) == 1:
                print(f"\n--- Preview: {mod_key.upper()} ---\n")
                print(md_text[:1200])
                if len(md_text) > 1200:
                    print(f"\n... [Full output saved to {args.output_dir}/{mod_key}.md]")

    # 3. Generate Daily Digest
    if args.daily_digest:
        print("\n[*] Generating Daily Channel Action Digest...")
        digest_gen = DailyDigestGenerator(config, db, quota)
        digest_text = digest_gen.generate(output_dir=args.output_dir)
        print(f"    -> Exported: {args.output_dir}/daily_digest.md\n")
        print(digest_text)

    # 4. Generate Weekly Report
    if args.weekly_report or args.module == "all":
        print("\n[*] Generating Comprehensive Weekly Report (All 7 Modules)...")
        weekly_gen = WeeklyReportGenerator(config, db, quota)
        weekly_text = weekly_gen.generate(output_dir=args.output_dir)
        print(f"    -> Exported: {args.output_dir}/weekly_report.md")

    # 5. Print Quota Summary
    quota_info = quota.get_summary()
    print(f"\n[Quota Status] {quota_info['units_used_today']}/{quota_info['daily_limit']} units used today ({quota_info['percent_used']}%)")
    print(f"[Done] All requested reports and JSON artifacts are saved in '{args.output_dir}/'.\n")

if __name__ == "__main__":
    main()
