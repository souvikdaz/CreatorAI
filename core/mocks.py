from datetime import datetime, timezone, timedelta

def get_sample_transcript() -> list:
    """Returns a full timestamped transcript of a 16-minute long-form motovlog video."""
    return [
        {"start_sec": 0, "end_sec": 18, "text": "If you are planning to ride to Ladakh in 2026, here is the harsh truth about the Himalayan 450 that nobody tells you in showroom reviews."},
        {"start_sec": 18, "end_sec": 42, "text": "We just crossed Baralacha La at minus four degrees. The EFI map on this bike adjusted decently, but our handlebar vibration caused our phone mount stabilization to undergo severe stress."},
        {"start_sec": 42, "end_sec": 75, "text": "Welcome back to the channel. Today we're breaking down the complete Ladakh touring setup: luggage racks, tire pressure choices, action camera batteries on our DJI Osmo Action 3, and crucial altitude tools."},
        {"start_sec": 75, "end_sec": 135, "text": "First, let's talk about luggage mounting. Soft panniers versus aluminum hard boxes. On rocky water crossings like Pagal Nala, hard boxes act as leg-breakers if you tip over. Soft bags with quick-release straps saved our ride twice."},
        {"start_sec": 135, "end_sec": 185, "text": "Tip number one for extreme cold: Action camera batteries die in eight minutes if exposed. Keep two spares inside your inner jacket pocket right against your chest heat, and run an external USB power lead directly from your bike's auxiliary port into the camera housing."},
        {"start_sec": 185, "end_sec": 240, "text": "Here is the exact vertical camera framing rig I use with the DJI Osmo Action 3. A chin mount on a full-face helmet gives the viewer the authentic rider eye-level perspective, while keeping audio clean using a wired mic or Grenaro wireless transmitter stuffed inside the cheek pad."},
        {"start_sec": 240, "end_sec": 310, "text": "Look at this water crossing ahead. Rule of thumb: never ride through the center of a glacial stream in the afternoon. Early morning water is ankle-deep; by 3 PM, melting snow turns it into a waist-high raging torrent."},
        {"start_sec": 310, "end_sec": 365, "text": "Watch this line. Stand up on the footpegs, keep constant throttle in first gear, and never look down at the rocks. Look where you want to exit, not where you're afraid to slip."},
        {"start_sec": 365, "end_sec": 420, "text": "We made it across cleanly! Notice how the rear tire slipped slightly on the shale rock. That's why dropping tire pressure to 22 PSI in the rear gives you 40% more contact patch on loose mountain trails."},
        {"start_sec": 420, "end_sec": 480, "text": "Now let's talk about emergency gadgets. Many riders carry puncture kits, but if you have tubed spoked wheels, a plug kit is completely useless. You need two tire levers, a spare 21-inch tube, and an electric air inflator."},
        {"start_sec": 480, "end_sec": 540, "text": "Here is a secret tool: carry a three-meter clear vinyl tube for siphoning fuel. In remote Zanskar stretches, fuel bunks run dry for days. Friendly local truck drivers will gladly sell you five liters if you can siphon it yourself."},
        {"start_sec": 540, "end_sec": 600, "text": "Checking in at the homestay in Padum. For 800 rupees, you get hot butter tea, home-cooked dal chawal, and safe parking for your motorcycle. Supporting local village homestays keeps this valley thriving."},
        {"start_sec": 600, "end_sec": 660, "text": "Summary of today's 280-kilometer stint: 14 hours saddle time on the Himalayan 450, zero mechanical breakdowns, and memories that will last a lifetime. Drop your questions below on permits and gear list, and make sure you're subscribed for Part 2 tackling Shinku La pass."}
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
        # --- MY CHANNEL VIDEOS (Exact 5 Uploads for CTR/Retention Analytics) ---
        {
            "video_id": "my_vid_01",
            "channel_id": my_channel_id,
            "title": "Ladakh Solo Ride on Himalayan 450: The Ultimate Touring Gear & Spiti Route",
            "description": "Planning a Ladakh or Spiti bike trip? Here is my tested Himalayan 450 packing list and route advice.\n\nCut in Final Cut Pro on Mac Mini M4.",
            "tags": ["motovlog", "himalayan 450", "ladakh bike trip", "motorcycle touring", "spiti valley", "dji osmo action 3"],
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
            "title": "DJI Osmo Action 3 Chin Mount Setup: Budget Audio That Beats Wind Noise",
            "description": "How to get smooth eye-level motovlog footage on the Himalayan 450 with zero audio wind noise using wired mic.\n\nCover created with Canva Free.",
            "tags": ["action camera", "motovlog setup", "dji osmo action 3", "helmet chin mount", "himalayan 450"],
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
            "title": "Weekend Bike Trip on Himalayan 450: Delhi to Lansdowne 500KM Rain Ride Test",
            "description": "Monsoon touring guide: essential waterproof saddlebags and riding gear tips for Delhi riders on the Himalayan 450.",
            "tags": ["bike trip", "delhi to lansdowne", "himalayan 450", "rain riding", "waterproof riding gear", "motovlog"],
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
            "title": "5 Motorcycle Maintenance Checks Before Any 1,000KM Tour on Himalayan 450",
            "description": "Never start a long motorcycle tour without checking these 5 crucial safety items on your Himalayan 450.",
            "tags": ["motorcycle maintenance", "himalayan 450", "touring tips", "bike servicing", "automotive"],
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
        {
            "video_id": "my_vid_05",
            "channel_id": my_channel_id,
            "title": "Grenaro Wireless Microphone vs Wired Mic: High-Speed Himalayan 450 Audio Test",
            "description": "Real riding audio test on the Himalayan 450 comparing Grenaro wireless mic vs generic wired mic inside a full-face helmet.\n\nEdited in Final Cut Pro on Mac Mini M4.",
            "tags": ["grenaro wireless mic", "himalayan 450", "motovlog audio", "dji osmo action 3", "mototech explorer"],
            "published_at": (now - timedelta(days=78, hours=4)).isoformat(),
            "duration_sec": 490,
            "views": 6200,
            "likes": 440,
            "comments": 38,
            "ctr": 7.2,
            "avg_view_duration_sec": 245.0,
            "retention_pct": 50.0,
            "traffic_sources": {"YouTube search": 55.0, "Suggested videos": 30.0, "Browse features": 10.0, "Other": 5.0},
            "sub_change": 52,
            "view_velocity": 79.5,
            "is_my_channel": True,
            "transcript": []
        },

        # --- COMPETITOR VIDEOS ---
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
            "video_id": "deeptesh_vid_01",
            "channel_id": "UC_deeptesh_loves_tech_mock_id",
            "title": "Action Camera Audio Setup for Motovlogging: Watch Before You Waste Money!",
            "description": "Full side-by-side riding test in low light, highway speeds, and wind noise isolation.",
            "tags": ["action camera", "motovlog audio", "technology", "helmet audio"],
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
            "video_id": "dream_vid_01",
            "channel_id": "UC_dreamwalk_mock_id",
            "title": "Riding Into the Clouds: Sach Pass Deadly Waterfalls & High Mountain Trails [4K HDR]",
            "description": "Cinematic visual tour across Sach Pass in Himachal Pradesh on adventure motorcycles.",
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

    # --- INSTAGRAM MOCK DATA (Last 5 Posts & Reels) ---
    instagram_posts = [
        {
            "post_id": "ig_post_01",
            "caption": "Cold start at -4°C in Spiti on the Himalayan 450... DJI Osmo Action 3 battery survival trick 🥶 Keep spares inside your jacket! Full breakdown in bio link.\n.\n#himalayan450 #spiti #motovlog #djiosmoaction3 #motorcycletouring",
            "hashtags": ["himalayan450", "spiti", "motovlog", "djiosmoaction3", "motorcycletouring"],
            "format": "REEL",
            "duration_sec": 28,
            "plays": 18400,
            "reach": 14200,
            "likes": 1420,
            "saves": 420,
            "shares": 310,
            "comments": 48,
            "profile_visits": 380,
            "follows_gained": 64,
            "thumbnail_url": "https://images.unsplash.com/photo-1558981403-c5f9899a28bc?w=500&q=80",
            "permalink": "https://instagram.com/p/mock_ig_01",
            "published_at": (now - timedelta(days=3, hours=2)).isoformat(),
            "is_my_post": True
        },
        {
            "post_id": "ig_post_02",
            "caption": "5 Essential Emergency Tools for Himalayan 450 Highway Touring (Save for later!) 🔧🏍️ Never tour without tire levers and 21mm wrench. Slide 3 has the packing order.\n.\n#motorcycletouring #himalayan450 #biketrip #diybiker #packinglist",
            "hashtags": ["motorcycletouring", "himalayan450", "biketrip", "diybiker", "packinglist"],
            "format": "CAROUSEL",
            "duration_sec": 0,
            "plays": 0,
            "reach": 9800,
            "likes": 890,
            "saves": 680,
            "shares": 140,
            "comments": 62,
            "profile_visits": 210,
            "follows_gained": 42,
            "thumbnail_url": "https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?w=500&q=80",
            "permalink": "https://instagram.com/p/mock_ig_02",
            "published_at": (now - timedelta(days=9, hours=5)).isoformat(),
            "is_my_post": True
        },
        {
            "post_id": "ig_post_03",
            "caption": "Glacial river crossing on Himalayan 450! 🌊 Stand up, keep steady throttle in 1st gear. Audio recorded on Grenaro wireless microphone inside the helmet.\n.\n#offroad #himalayan450 #watercrossing #adventuremotorcycle #grenaro",
            "hashtags": ["offroad", "himalayan450", "watercrossing", "adventuremotorcycle", "grenaro"],
            "format": "REEL",
            "duration_sec": 42,
            "plays": 24500,
            "reach": 19100,
            "likes": 2150,
            "saves": 890,
            "shares": 620,
            "comments": 95,
            "profile_visits": 540,
            "follows_gained": 110,
            "thumbnail_url": "https://images.unsplash.com/photo-1571188654248-7a89213915f7?w=500&q=80",
            "permalink": "https://instagram.com/p/mock_ig_03",
            "published_at": (now - timedelta(days=16, hours=3)).isoformat(),
            "is_my_post": True
        },
        {
            "post_id": "ig_post_04",
            "caption": "Sunrise pitstop at 16,000 feet near Baralacha La. The Himalayan 450 taking a well-deserved breather amidst freezing wind. 🏔️✨ Drop a 🏍️ if you love high mountain rides.\n.\n#ladakh #baralachala #solorider #himalayas #himalayan450",
            "hashtags": ["ladakh", "baralachala", "solorider", "himalayas", "himalayan450"],
            "format": "SINGLE_IMAGE",
            "duration_sec": 0,
            "plays": 0,
            "reach": 6400,
            "likes": 620,
            "saves": 95,
            "shares": 35,
            "comments": 24,
            "profile_visits": 85,
            "follows_gained": 12,
            "thumbnail_url": "https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?w=500&q=80",
            "permalink": "https://instagram.com/p/mock_ig_04",
            "published_at": (now - timedelta(days=24, hours=6)).isoformat(),
            "is_my_post": True
        },
        {
            "post_id": "ig_post_05",
            "caption": "Motorola Edge 40 Neo quick take: checking rear tire pressure on Himalayan 450 before entering loose mountain trails. 22 PSI gives massive grip! 🏍️💨\n.\n#bikerlife #himalayan450 #motorcycletips #motorolaedge40neo",
            "hashtags": ["bikerlife", "himalayan450", "motorcycletips", "motorolaedge40neo"],
            "format": "REEL",
            "duration_sec": 35,
            "plays": 12300,
            "reach": 10500,
            "likes": 980,
            "saves": 310,
            "shares": 180,
            "comments": 41,
            "profile_visits": 190,
            "follows_gained": 32,
            "thumbnail_url": "https://images.unsplash.com/photo-1508974239320-0a029497e820?w=500&q=80",
            "permalink": "https://instagram.com/p/mock_ig_05",
            "published_at": (now - timedelta(days=32, hours=4)).isoformat(),
            "is_my_post": True
        }
    ]

    # --- INSTAGRAM COMPETITORS (12 Accounts in Niche) ---
    instagram_creators = [
        {
            "handle": "@swati_rojha",
            "name": "Swati Rojha | Solo Motovlogger",
            "followers_count": 285000,
            "posts_count": 420,
            "avg_reach": 85000,
            "avg_engagement_rate": 6.4,
            "top_formats": ["REEL", "CAROUSEL"],
            "sample_posts": [
                {"hook": "How I survived -15°C alone in Spiti", "format": "REEL", "plays": 240000, "saves": 8400, "caption_len": 180, "hashtags_count": 6},
                {"hook": "Top 4 emergency items every female rider carries", "format": "CAROUSEL", "plays": 0, "saves": 11200, "caption_len": 240, "hashtags_count": 8}
            ]
        },
        {
            "handle": "@deepranjansachan",
            "name": "Deep Ranjan Sachan",
            "followers_count": 410000,
            "posts_count": 680,
            "avg_reach": 140000,
            "avg_engagement_rate": 7.1,
            "top_formats": ["REEL", "CAROUSEL"],
            "sample_posts": [
                {"hook": "The biggest mechanical flaw on touring bikes", "format": "REEL", "plays": 480000, "saves": 14500, "caption_len": 190, "hashtags_count": 5},
                {"hook": "10,000 KM maintenance checklist", "format": "CAROUSEL", "plays": 0, "saves": 18400, "caption_len": 310, "hashtags_count": 7}
            ]
        },
        {
            "handle": "@deepteshlovestech",
            "name": "Deeptesh | Motovlog Tech & Gadgets",
            "followers_count": 125000,
            "posts_count": 310,
            "avg_reach": 52000,
            "avg_engagement_rate": 5.8,
            "top_formats": ["REEL"],
            "sample_posts": [
                {"hook": "Stop mounting your phone like this on handlebars", "format": "REEL", "plays": 180000, "saves": 9200, "caption_len": 140, "hashtags_count": 5}
            ]
        },
        {
            "handle": "@dreamwalk_official",
            "name": "dReamwAlk Travels",
            "followers_count": 320000,
            "posts_count": 490,
            "avg_reach": 98000,
            "avg_engagement_rate": 6.8,
            "top_formats": ["REEL", "SINGLE_IMAGE"],
            "sample_posts": [
                {"hook": "Waterfalls falling directly onto Sach Pass roads", "format": "REEL", "plays": 310000, "saves": 12800, "caption_len": 110, "hashtags_count": 4}
            ]
        },
        {
            "handle": "@throttleyourlife",
            "name": "Throttle Your Life",
            "followers_count": 195000,
            "posts_count": 380,
            "avg_reach": 64000,
            "avg_engagement_rate": 5.5,
            "top_formats": ["CAROUSEL", "REEL"],
            "sample_posts": [
                {"hook": "Zanskar fuel map & road update 2026", "format": "CAROUSEL", "plays": 0, "saves": 15600, "caption_len": 280, "hashtags_count": 8}
            ]
        },
        {
            "handle": "@nomadic_tourer_india",
            "name": "Nomadic Tourer India",
            "followers_count": 142000,
            "posts_count": 275,
            "avg_reach": 44000,
            "avg_engagement_rate": 4.9,
            "top_formats": ["REEL"],
            "sample_posts": []
        },
        {
            "handle": "@adv_himalayan_riders",
            "name": "Himalayan ADV Riders",
            "followers_count": 165000,
            "posts_count": 520,
            "avg_reach": 49000,
            "avg_engagement_rate": 5.2,
            "top_formats": ["REEL", "CAROUSEL"],
            "sample_posts": []
        },
        {
            "handle": "@rider_girl_vishakha",
            "name": "RiderGirl Vishakha",
            "followers_count": 890000,
            "posts_count": 910,
            "avg_reach": 280000,
            "avg_engagement_rate": 7.8,
            "top_formats": ["REEL"],
            "sample_posts": []
        },
        {
            "handle": "@strell_moto",
            "name": "Strell Moto Reviews",
            "followers_count": 230000,
            "posts_count": 410,
            "avg_reach": 72000,
            "avg_engagement_rate": 5.9,
            "top_formats": ["CAROUSEL", "REEL"],
            "sample_posts": []
        },
        {
            "handle": "@bulu_biker",
            "name": "Bulu Biker Adventure",
            "followers_count": 115000,
            "posts_count": 340,
            "avg_reach": 38000,
            "avg_engagement_rate": 4.7,
            "top_formats": ["REEL"],
            "sample_posts": []
        },
        {
            "handle": "@biker_souls_india",
            "name": "Biker Souls Community",
            "followers_count": 178000,
            "posts_count": 620,
            "avg_reach": 45000,
            "avg_engagement_rate": 4.8,
            "top_formats": ["REEL", "SINGLE_IMAGE"],
            "sample_posts": []
        },
        {
            "handle": "@tech_gadget_rider",
            "name": "Moto Tech India",
            "followers_count": 94000,
            "posts_count": 210,
            "avg_reach": 31000,
            "avg_engagement_rate": 5.1,
            "top_formats": ["REEL", "CAROUSEL"],
            "sample_posts": []
        }
    ]

    # --- YOUTUBE RETENTION CURVES FOR LAST 5 UPLOADS ---
    youtube_retention_curves = [
        {
            "video_id": "my_vid_01",
            "title": "Ladakh Solo Ride on Himalayan 450: The Ultimate Touring Gear & Spiti Route",
            "ctr": 7.4,
            "avg_view_duration_sec": 285.0,
            "avg_percentage_viewed": 43.2,
            "retention_curve": [
                {"second": 0, "retention_pct": 100.0},
                {"second": 3, "retention_pct": 78.5},
                {"second": 15, "retention_pct": 68.0},
                {"second": 45, "retention_pct": 60.5},
                {"second": 105, "retention_pct": 49.0},
                {"second": 180, "retention_pct": 42.0},
                {"second": 300, "retention_pct": 38.0},
                {"second": 450, "retention_pct": 34.0},
                {"second": 660, "retention_pct": 28.0}
            ],
            "drop_off_points": [
                {"timestamp_sec": 3, "timestamp_formatted": "00:03", "drop_pct": 21.5, "cause": "Slow intro / talking head without immediate riding hook"},
                {"timestamp_sec": 105, "timestamp_formatted": "01:45", "drop_pct": 11.5, "cause": "Long B-roll with no angle change or dialogue progression"}
            ]
        },
        {
            "video_id": "my_vid_02",
            "title": "DJI Osmo Action 3 Chin Mount Setup: Budget Audio That Beats Wind Noise",
            "ctr": 8.8,
            "avg_view_duration_sec": 240.0,
            "avg_percentage_viewed": 50.0,
            "retention_curve": [
                {"second": 0, "retention_pct": 100.0},
                {"second": 5, "retention_pct": 82.0},
                {"second": 30, "retention_pct": 74.0},
                {"second": 90, "retention_pct": 66.0},
                {"second": 190, "retention_pct": 52.0},
                {"second": 320, "retention_pct": 44.0},
                {"second": 480, "retention_pct": 38.0}
            ],
            "drop_off_points": [
                {"timestamp_sec": 5, "timestamp_formatted": "00:05", "drop_pct": 18.0, "cause": "Lengthy channel intro animation delay before demonstrating mount"},
                {"timestamp_sec": 190, "timestamp_formatted": "03:10", "drop_pct": 14.0, "cause": "Complex technical mounting diagram with no audio commentary"}
            ]
        },
        {
            "video_id": "my_vid_03",
            "title": "Weekend Bike Trip on Himalayan 450: Delhi to Lansdowne 500KM Rain Ride Test",
            "ctr": 5.2,
            "avg_view_duration_sec": 190.0,
            "avg_percentage_viewed": 35.1,
            "retention_curve": [
                {"second": 0, "retention_pct": 100.0},
                {"second": 4, "retention_pct": 72.0},
                {"second": 30, "retention_pct": 58.0},
                {"second": 135, "retention_pct": 44.0},
                {"second": 270, "retention_pct": 32.0},
                {"second": 420, "retention_pct": 25.0},
                {"second": 540, "retention_pct": 21.0}
            ],
            "drop_off_points": [
                {"timestamp_sec": 4, "timestamp_formatted": "00:04", "drop_pct": 28.0, "cause": "Mismatched title expectation: opens with static garage dialogue instead of rain riding action"},
                {"timestamp_sec": 135, "timestamp_formatted": "02:15", "drop_pct": 14.0, "cause": "Protracted highway cruising clip exceeding 40 seconds with static Osmo Action 3 angle"}
            ]
        },
        {
            "video_id": "my_vid_04",
            "title": "5 Motorcycle Maintenance Checks Before Any 1,000KM Tour on Himalayan 450",
            "ctr": 6.9,
            "avg_view_duration_sec": 210.0,
            "avg_percentage_viewed": 50.0,
            "retention_curve": [
                {"second": 0, "retention_pct": 100.0},
                {"second": 8, "retention_pct": 84.0},
                {"second": 60, "retention_pct": 72.0},
                {"second": 150, "retention_pct": 59.0},
                {"second": 270, "retention_pct": 46.0},
                {"second": 420, "retention_pct": 39.0}
            ],
            "drop_off_points": [
                {"timestamp_sec": 8, "timestamp_formatted": "00:08", "drop_pct": 16.0, "cause": "Unnecessary personal backstory before jumping into tip #1 (chain slack)"},
                {"timestamp_sec": 270, "timestamp_formatted": "04:30", "drop_pct": 13.0, "cause": "Abstract electrical relay check without close-up Macro framing"}
            ]
        },
        {
            "video_id": "my_vid_05",
            "title": "Grenaro Wireless Microphone vs Wired Mic: High-Speed Himalayan 450 Audio Test",
            "ctr": 7.2,
            "avg_view_duration_sec": 245.0,
            "avg_percentage_viewed": 50.0,
            "retention_curve": [
                {"second": 0, "retention_pct": 100.0},
                {"second": 2, "retention_pct": 81.0},
                {"second": 45, "retention_pct": 71.0},
                {"second": 160, "retention_pct": 58.0},
                {"second": 310, "retention_pct": 47.0},
                {"second": 490, "retention_pct": 40.0}
            ],
            "drop_off_points": [
                {"timestamp_sec": 2, "timestamp_formatted": "00:02", "drop_pct": 19.0, "cause": "Silent title card at 0:01 rather than immediate A/B audio comparison playback"},
                {"timestamp_sec": 160, "timestamp_formatted": "02:40", "drop_pct": 13.0, "cause": "Excessively long repetitive wind noise segment without visual graphic telemetry"}
            ]
        }
    ]

    return {
        "channels": channels,
        "videos": videos,
        "instagram_posts": instagram_posts,
        "instagram_creators": instagram_creators,
        "youtube_retention_curves": youtube_retention_curves
    }
