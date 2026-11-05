from datetime import datetime, timezone, timedelta

def get_sample_transcript() -> list:
    """Returns a full timestamped transcript of a 16-minute long-form motovlog video."""
    return [
        {"start_sec": 0, "end_sec": 18, "text": "If you are planning to ride to Ladakh in 2026, here is the harsh truth about the Himalayan 450 that nobody tells you in showroom reviews."},
        {"start_sec": 18, "end_sec": 42, "text": "We just crossed Baralacha La at minus four degrees. The EFI map on this bike adjusted decently, but our handlebar vibration caused our phone camera optical stabilization to literally fry."},
        {"start_sec": 42, "end_sec": 75, "text": "Welcome back to the channel. Today we're breaking down the complete Ladakh touring setup: luggage racks, tire pressure choices, action camera batteries, and the crucial altitude tools you cannot skip."},
        {"start_sec": 75, "end_sec": 135, "text": "First, let's talk about luggage mounting. Soft panniers versus aluminum hard boxes. On rocky water crossings like Pagal Nala, hard boxes act as leg-breakers if you tip over. Soft bags with quick-release straps saved our ride twice."},
        {"start_sec": 135, "end_sec": 185, "text": "Tip number one for extreme cold: Action camera batteries die in eight minutes if exposed. Keep two spares inside your inner jacket pocket right against your chest heat, and run an external USB power lead directly from your bike's auxiliary port into the camera housing."},
        {"start_sec": 185, "end_sec": 240, "text": "Here is the exact vertical camera framing rig I use. A chin mount on a full-face helmet gives the viewer the authentic rider eye-level perspective, while keeping audio clean using a deadcat foam mic stuffed inside the cheek pad."},
        {"start_sec": 240, "end_sec": 310, "text": "Look at this water crossing ahead. Rule of thumb: never ride through the center of a glacial stream in the afternoon. Early morning water is ankle-deep; by 3 PM, melting snow turns it into a waist-high raging torrent."},
        {"start_sec": 310, "end_sec": 365, "text": "Watch this line. Stand up on the footpegs, keep constant throttle in first gear, and never look down at the rocks. Look where you want to exit, not where you're afraid to slip."},
        {"start_sec": 365, "end_sec": 420, "text": "We made it across cleanly! Notice how the rear tire slipped slightly on the shale rock. That's why dropping tire pressure to 22 PSI in the rear gives you 40% more contact patch on loose mountain trails."},
        {"start_sec": 420, "end_sec": 480, "text": "Now let's talk about emergency gadgets. Many riders carry puncture kits, but if you have tubed spoked wheels, a plug kit is completely useless. You need two tire levers, a spare 21-inch tube, and an electric air inflator."},
        {"start_sec": 480, "end_sec": 540, "text": "Here is a secret tool: carry a three-meter clear vinyl tube for siphoning fuel. In remote Zanskar stretches, fuel bunks run dry for days. Friendly local truck drivers will gladly sell you five liters if you can siphon it yourself."},
        {"start_sec": 540, "end_sec": 600, "text": "Checking in at the homestay in Padum. For 800 rupees, you get hot butter tea, home-cooked dal chawal, and safe parking for your motorcycle. Supporting local village homestays keeps this valley thriving."},
        {"start_sec": 600, "end_sec": 660, "text": "Summary of today's 280-kilometer stint: 14 hours saddle time, zero mechanical breakdowns, and memories that will last a lifetime. Drop your questions below on permits and gear list, and make sure you're subscribed for Part 2 tackling Shinku La pass."}
    ]

def get_mock_database_seed(my_channel_id: str = "UCu2EoFcaIV7rqAXvG9rcUiQ") -> dict:
    now = datetime.now(timezone.utc)
    
    channels = [
        {
            "channel_id": my_channel_id,
            "title": "MotoTech Explorer",
            "custom_url": "@MotoTechExplorer",
            "subscriber_count": 420,
            "view_count": 82400,
            "video_count": 18,
            "is_my_channel": True
        },
        {
            "channel_id": "UC_swati_rojha_mock_id",
            "title": "Swati Rojha",
            "custom_url": "@SwatiRojha",
            "subscriber_count": 340000,
            "view_count": 48200000,
            "video_count": 142,
            "is_my_channel": False
        },
        {
            "channel_id": "UC_deepranjan_sachan_mock_id",
            "title": "Deep Ranjan Sachan",
            "custom_url": "@deepranjansachan",
            "subscriber_count": 620000,
            "view_count": 89400000,
            "video_count": 280,
            "is_my_channel": False
        },
        {
            "channel_id": "UC_deeptesh_loves_tech_mock_id",
            "title": "Deeptesh Loves TECH",
            "custom_url": "@DeepteshLovesTECH",
            "subscriber_count": 185000,
            "view_count": 24100000,
            "video_count": 195,
            "is_my_channel": False
        },
        {
            "channel_id": "UC_dreamwalk_mock_id",
            "title": "dReamwAlk",
            "custom_url": "@dReamwAlk",
            "subscriber_count": 410000,
            "view_count": 62000000,
            "video_count": 160,
            "is_my_channel": False
        },
        {
            "channel_id": "UC_throttleyourlife_mock_id",
            "title": "Throttle Your Life",
            "custom_url": "@throttleyourlife",
            "subscriber_count": 290000,
            "view_count": 38700000,
            "video_count": 210,
            "is_my_channel": False
        }
    ]

    videos = [
        # --- MY CHANNEL VIDEOS ---
        {
            "video_id": "my_vid_01",
            "channel_id": my_channel_id,
            "title": "Ladakh Solo Ride on Himalayan 450: The Ultimate Touring Gear & Spiti Route",
            "description": "Planning a Ladakh or Spiti bike trip? Here is my tested motorcycle touring packing list and route advice.\n\nSubscribe for more adventure motorcycle travel tips!",
            "tags": ["motovlog", "himalayan 450", "ladakh bike trip", "motorcycle touring", "spiti valley", "touring gear"],
            "published_at": (now - timedelta(days=6, hours=4)).isoformat(),
            "duration_sec": 660,
            "views": 4850,
            "likes": 340,
            "comments": 42,
            "ctr": 7.4,
            "avg_view_duration_sec": 285.0,
            "retention_pct": 43.2,
            "traffic_sources": {"YouTube search": 52.0, "Suggested videos": 31.0, "Browse features": 12.0, "Direct": 5.0},
            "sub_change": 38,
            "view_velocity": 808.3,
            "is_my_channel": True,
            "transcript": get_sample_transcript()
        },
        {
            "video_id": "my_vid_02",
            "channel_id": my_channel_id,
            "title": "Best Action Camera Chin Mount Setup for Motovlogging (Under ₹1,500)",
            "description": "How to get smooth eye-level motovlog footage with zero audio wind noise using budget helmet mounts.\n\nGear links in description.",
            "tags": ["action camera", "motovlog setup", "helmet chin mount", "budget motovlog", "gadgets", "gopro audio"],
            "published_at": (now - timedelta(days=18, hours=10)).isoformat(),
            "duration_sec": 480,
            "views": 8920,
            "likes": 610,
            "comments": 78,
            "ctr": 8.8,
            "avg_view_duration_sec": 240.0,
            "retention_pct": 50.0,
            "traffic_sources": {"YouTube search": 68.0, "Suggested videos": 20.0, "Browse features": 8.0, "Direct": 4.0},
            "sub_change": 72,
            "view_velocity": 495.5,
            "is_my_channel": True,
            "transcript": []
        },
        {
            "video_id": "my_vid_03",
            "channel_id": my_channel_id,
            "title": "Weekend Bike Trip from Delhi to Lansdowne: 500KM Rain Ride Test",
            "description": "Monsoon touring guide: essential waterproof saddlebags and riding gear tips for Delhi riders.\n\nWatch till end for route condition updates.",
            "tags": ["bike trip", "delhi to lansdowne", "rain riding", "waterproof riding gear", "weekend ride", "motovlog"],
            "published_at": (now - timedelta(days=38, hours=2)).isoformat(),
            "duration_sec": 540,
            "views": 3200,
            "likes": 210,
            "comments": 19,
            "ctr": 5.2,
            "avg_view_duration_sec": 190.0,
            "retention_pct": 35.1,
            "traffic_sources": {"Browse features": 44.0, "Suggested videos": 32.0, "YouTube search": 18.0, "Other": 6.0},
            "sub_change": 14,
            "view_velocity": 84.2,
            "is_my_channel": True,
            "transcript": []
        },
        {
            "video_id": "my_vid_04",
            "channel_id": my_channel_id,
            "title": "5 Motorcycle Maintenance Checks Before Any 1,000KM Highway Tour",
            "description": "Never start a long motorcycle tour without checking these 5 crucial safety items. Chain slack, brake fluid, coolant levels explained.",
            "tags": ["motorcycle maintenance", "touring tips", "bike servicing", "diy motorcycle", "automotive"],
            "published_at": (now - timedelta(days=62, hours=6)).isoformat(),
            "duration_sec": 420,
            "views": 5100,
            "likes": 380,
            "comments": 45,
            "ctr": 6.9,
            "avg_view_duration_sec": 210.0,
            "retention_pct": 50.0,
            "traffic_sources": {"YouTube search": 61.0, "Suggested videos": 25.0, "Browse features": 10.0, "Other": 4.0},
            "sub_change": 41,
            "view_velocity": 82.2,
            "is_my_channel": True,
            "transcript": []
        },

        # --- COMPETITOR VIDEOS (Last 90 Days) ---
        # 1. Swati Rojha
        {
            "video_id": "swati_vid_01",
            "channel_id": "UC_swati_rojha_mock_id",
            "title": "Solo Female Winter Ride to Spiti: -15°C Extreme Challenge | Kaza Road Trip",
            "description": "Riding into frozen Spiti Valley in winter. Road closures, black ice, and local homestays.",
            "tags": ["spiti valley", "solo female rider", "motovlog", "extreme winter ride", "kaza", "bike trip"],
            "published_at": (now - timedelta(days=8, hours=1)).isoformat(),
            "duration_sec": 840,
            "views": 184000,
            "likes": 14200,
            "comments": 1280,
            "ctr": 11.2,
            "avg_view_duration_sec": 420.0,
            "retention_pct": 50.0,
            "traffic_sources": {"Browse features": 58.0, "Suggested videos": 32.0, "Search": 8.0, "Other": 2.0},
            "sub_change": 3200,
            "view_velocity": 23000.0,
            "is_my_channel": False,
            "transcript": []
        },
        {
            "video_id": "swati_vid_02",
            "channel_id": "UC_swati_rojha_mock_id",
            "title": "I Rode 1,200 KM Non-Stop on National Highway 44! What Happened to My Bike?",
            "description": "Testing endurance and motorcycle highway cruising speeds on NH44.",
            "tags": ["highway touring", "endurance ride", "nh44", "motorcycle touring", "motovlog"],
            "published_at": (now - timedelta(days=26, hours=5)).isoformat(),
            "duration_sec": 710,
            "views": 98000,
            "likes": 7600,
            "comments": 590,
            "ctr": 8.9,
            "avg_view_duration_sec": 310.0,
            "retention_pct": 43.6,
            "traffic_sources": {"Browse features": 50.0, "Suggested": 38.0, "Search": 10.0, "Other": 2.0},
            "sub_change": 1400,
            "view_velocity": 3769.2,
            "is_my_channel": False,
            "transcript": []
        },

        # 2. Deep Ranjan Sachan
        {
            "video_id": "deep_vid_01",
            "channel_id": "UC_deepranjan_sachan_mock_id",
            "title": "Don't Buy Himalayan 450 Before Watching This: 10,000KM Long Term Ownership Truth",
            "description": "Detailed mechanical review of Himalayan 450 after 10,000KM of brutal touring and city commuting.",
            "tags": ["himalayan 450 review", "ownership review", "long term review", "automotive", "motorcycle touring"],
            "published_at": (now - timedelta(days=12, hours=3)).isoformat(),
            "duration_sec": 1020,
            "views": 310000,
            "likes": 21500,
            "comments": 2450,
            "ctr": 12.8,
            "avg_view_duration_sec": 560.0,
            "retention_pct": 54.9,
            "traffic_sources": {"YouTube search": 45.0, "Suggested videos": 39.0, "Browse": 14.0, "Other": 2.0},
            "sub_change": 5800,
            "view_velocity": 25833.3,
            "is_my_channel": False,
            "transcript": []
        },
        {
            "video_id": "deep_vid_02",
            "channel_id": "UC_deepranjan_sachan_mock_id",
            "title": "KTM 390 Adventure vs Himalayan 450: The Definitive Highway & Offroad Comparison",
            "description": "Head-to-head dyno, weight, suspension travel, and touring comfort comparison.",
            "tags": ["ktm 390 adventure", "himalayan 450", "bike comparison", "automotive", "motorcycle touring"],
            "published_at": (now - timedelta(days=42, hours=4)).isoformat(),
            "duration_sec": 980,
            "views": 240000,
            "likes": 16800,
            "comments": 1950,
            "ctr": 10.4,
            "avg_view_duration_sec": 510.0,
            "retention_pct": 52.0,
            "traffic_sources": {"YouTube search": 50.0, "Suggested videos": 35.0, "Browse": 12.0, "Other": 3.0},
            "sub_change": 3900,
            "view_velocity": 5714.3,
            "is_my_channel": False,
            "transcript": []
        },

        # 3. Deeptesh Loves TECH
        {
            "video_id": "deeptesh_vid_01",
            "channel_id": "UC_deeptesh_loves_tech_mock_id",
            "title": "Insta360 X4 vs GoPro Hero 12 for Motovlogging: Watch Before You Waste Money!",
            "description": "Full side-by-side riding test in low light, highway speeds, and wind noise isolation.",
            "tags": ["insta360 x4", "gopro hero 12", "motovlog camera", "gadgets", "technology", "action camera"],
            "published_at": (now - timedelta(days=14, hours=2)).isoformat(),
            "duration_sec": 760,
            "views": 145000,
            "likes": 9800,
            "comments": 890,
            "ctr": 11.5,
            "avg_view_duration_sec": 390.0,
            "retention_pct": 51.3,
            "traffic_sources": {"YouTube search": 62.0, "Suggested": 26.0, "Browse": 10.0, "Other": 2.0},
            "sub_change": 2600,
            "view_velocity": 10357.1,
            "is_my_channel": False,
            "transcript": []
        },
        {
            "video_id": "deeptesh_vid_02",
            "channel_id": "UC_deeptesh_loves_tech_mock_id",
            "title": "Top 5 Must-Have Motorcycle Gadgets in 2026 That Are Actually Useful",
            "description": "Wireless Apple CarPlay for bikes, smart tire pressure monitors, and compact GPS trackers.",
            "tags": ["motorcycle gadgets", "bike technology", "apple carplay motorcycle", "gadgets", "technology"],
            "published_at": (now - timedelta(days=32, hours=8)).isoformat(),
            "duration_sec": 620,
            "views": 88000,
            "likes": 5900,
            "comments": 460,
            "ctr": 9.1,
            "avg_view_duration_sec": 300.0,
            "retention_pct": 48.3,
            "traffic_sources": {"Suggested": 44.0, "Search": 40.0, "Browse": 14.0, "Other": 2.0},
            "sub_change": 1300,
            "view_velocity": 2750.0,
            "is_my_channel": False,
            "transcript": []
        },

        # 4. dReamwAlk
        {
            "video_id": "dream_vid_01",
            "channel_id": "UC_dreamwalk_mock_id",
            "title": "Riding Into the Clouds: Sach Pass Deadly Waterfalls & High Mountain Trails [4K HDR]",
            "description": "Cinematic visual tour across Sach Pass in Himachal Pradesh on dual-sport motorcycles.",
            "tags": ["sach pass", "cinematic motovlog", "bike trip", "motorcycle touring", "himachal pradesh"],
            "published_at": (now - timedelta(days=19, hours=6)).isoformat(),
            "duration_sec": 920,
            "views": 162000,
            "likes": 13400,
            "comments": 820,
            "ctr": 10.1,
            "avg_view_duration_sec": 480.0,
            "retention_pct": 52.1,
            "traffic_sources": {"Browse features": 64.0, "Suggested": 28.0, "Search": 6.0, "Other": 2.0},
            "sub_change": 2400,
            "view_velocity": 8526.3,
            "is_my_channel": False,
            "transcript": []
        },

        # 5. Throttle Your Life
        {
            "video_id": "throttle_vid_01",
            "channel_id": "UC_throttleyourlife_mock_id",
            "title": "Complete Zanskar Valley Route Guide 2026: Shinku La Tunnel, Fuel & Permits",
            "description": "Everything you need to know about the new Darcha-Padum road and offroad conditions.",
            "tags": ["zanskar valley", "shinku la", "route guide", "motorcycle touring", "motovlog", "bike trips"],
            "published_at": (now - timedelta(days=22, hours=7)).isoformat(),
            "duration_sec": 810,
            "views": 118000,
            "likes": 8400,
            "comments": 740,
            "ctr": 8.7,
            "avg_view_duration_sec": 380.0,
            "retention_pct": 46.9,
            "traffic_sources": {"YouTube search": 54.0, "Suggested": 32.0, "Browse": 12.0, "Other": 2.0},
            "sub_change": 1700,
            "view_velocity": 5363.6,
            "is_my_channel": False,
            "transcript": []
        }
    ]

    return {"channels": channels, "videos": videos}
