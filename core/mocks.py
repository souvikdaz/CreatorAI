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

def get_mock_database_seed(my_channel_id: str = "UCu2EoFcaIV7rqAXvG9rcUiQ", my_channel_handle: str = "@SouvikSays", my_channel_title: str = "Souvik Says", my_channel_subscribers: int = 887) -> dict:
    now = datetime.now(timezone.utc)

    channels = [
        {
            "channel_id": my_channel_id,
            "title": my_channel_title,
            "custom_url": my_channel_handle,
            "subscriber_count": my_channel_subscribers,
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
        # --- MY CHANNEL VIDEOS (Real Kolkata to Ladakh Series on Himalayan 450) ---
        {
            "video_id": "bW5s1DNjK8I",
            "channel_id": my_channel_id,
            "title": "The Hardest Route to Umling La: Surviving Nurbu La on the Himalayan 450 | Kolkata to Ladakh Ep. 6",
            "description": "At 18,000 feet, you stop talking. Every ounce of oxygen is needed just to keep the motorcycle upright.\n\nIn Episode 6, we tackle the infamous Nurbu La route to Umling La on the Royal Enfield Himalayan 450.\n\nCut in Final Cut Pro on Mac Mini M4.",
            "tags": ["himalayan 450", "umling la", "nurbu la", "kolkata to ladakh", "motovlog", "dji osmo action 3", "grenaro wireless mic", "souvik says"],
            "published_at": "2026-10-26T03:35:38+00:00",
            "duration_sec": 1299,
            "views": 248,
            "likes": 32,
            "comments": 14,
            "ctr": 7.8,
            "avg_view_duration_sec": 485.0,
            "retention_pct": 37.3,
            "traffic_sources": {"YouTube search": 56.0, "Suggested videos": 28.0, "Browse features": 11.0, "Direct": 5.0},
            "sub_change": 18,
            "view_velocity": 24.8,
            "is_my_channel": True,
            "transcript": get_sample_transcript()
        },
        {
            "video_id": "mxK3KPN1FMk",
            "channel_id": my_channel_id,
            "title": "Riding the Silent Frontier | Pangong Tso to Hanle via Rezang La | Kolkata to Ladakh Ep. 5",
            "description": "Leaving the turquoise calm of Pangong Tso behind, Episode 5 takes us into some of the most emotional and desolate border regions: Rezang La war memorial and on to the dark-sky sanctuary of Hanle.\n\nEdited in Final Cut Pro on Mac Mini M4.",
            "tags": ["pangong tso", "hanle", "rezang la", "himalayan 450", "ladakh bike trip", "dji osmo action 3"],
            "published_at": "2026-10-23T03:35:14+00:00",
            "duration_sec": 602,
            "views": 186,
            "likes": 24,
            "comments": 8,
            "ctr": 6.9,
            "avg_view_duration_sec": 290.0,
            "retention_pct": 48.2,
            "traffic_sources": {"YouTube search": 48.0, "Suggested videos": 34.0, "Browse features": 14.0, "Direct": 4.0},
            "sub_change": 12,
            "view_velocity": 13.3,
            "is_my_channel": True,
            "transcript": []
        },
        {
            "video_id": "uiPuFqgcWCo",
            "channel_id": my_channel_id,
            "title": "Auto-Rickshaw at Khardung La?! | Leh to Khardung La & Pangong | Kolkata to Ladakh Ep. 4",
            "description": "Just when you think you’ve seen it all in Ladakh, the mountains surprise you. In Episode 4, we climb the mighty Khardung La on the Himalayan 450 and descend into Nubra and Pangong.\n\nCover created with Canva Free.",
            "tags": ["khardung la", "leh ladakh", "pangong", "himalayan 450", "motovlog", "autorickshaw"],
            "published_at": "2026-10-19T03:35:09+00:00",
            "duration_sec": 1640,
            "views": 430,
            "likes": 48,
            "comments": 21,
            "ctr": 8.4,
            "avg_view_duration_sec": 580.0,
            "retention_pct": 35.4,
            "traffic_sources": {"YouTube search": 62.0, "Suggested videos": 24.0, "Browse features": 10.0, "Other": 4.0},
            "sub_change": 26,
            "view_velocity": 23.9,
            "is_my_channel": True,
            "transcript": []
        },
        {
            "video_id": "0BorTN7XpKM",
            "channel_id": my_channel_id,
            "title": "The Road to Leh That Doesn't Exist on Google Maps! | Kolkata to Ladakh Ep. 3",
            "description": "What happens when Google Maps says 'No Route Found,' but you turn your motorcycle onto the dirt anyway? Episode 3 takes us off the beaten path into high-altitude mountain passes.",
            "tags": ["road to leh", "offroad ladakh", "google maps", "himalayan 450", "biketrip"],
            "published_at": "2026-10-16T03:35:14+00:00",
            "duration_sec": 1011,
            "views": 381,
            "likes": 40,
            "comments": 18,
            "ctr": 7.6,
            "avg_view_duration_sec": 440.0,
            "retention_pct": 43.5,
            "traffic_sources": {"Browse features": 42.0, "Suggested videos": 36.0, "YouTube search": 18.0, "Other": 4.0},
            "sub_change": 21,
            "view_velocity": 18.1,
            "is_my_channel": True,
            "transcript": []
        },
        {
            "video_id": "JLEuioDpubM",
            "channel_id": my_channel_id,
            "title": "Jispa to Zanskar Through Hell's Weather | Kolkata to Ladakh Ep.2",
            "description": "Jispa to Gombo Rangjan, Zanskar. Crossed Baralacha La straight into a wall of freezing rain, sleet, and slush on the Himalayan 450.",
            "tags": ["zanskar", "jispa", "gombo rangjan", "baralacha la", "himalayan 450", "rain riding"],
            "published_at": "2026-10-12T03:35:18+00:00",
            "duration_sec": 1051,
            "views": 158,
            "likes": 22,
            "comments": 10,
            "ctr": 5.8,
            "avg_view_duration_sec": 410.0,
            "retention_pct": 39.0,
            "traffic_sources": {"YouTube search": 50.0, "Suggested videos": 32.0, "Browse features": 12.0, "Other": 6.0},
            "sub_change": 9,
            "view_velocity": 6.3,
            "is_my_channel": True,
            "transcript": []
        },
        {
            "video_id": "Cl0_RMreWMc",
            "channel_id": my_channel_id,
            "title": "1700km - Kolkata to the Himalayas | Kolkata to Ladakh Ep. 1",
            "description": "The journey begins. 1,700 kilometers from the humid plains of Kolkata up into the majestic foothills of the Himalayas on the Royal Enfield Himalayan 450.",
            "tags": ["kolkata to ladakh", "himalayan 450", "highway touring", "solorider", "dji osmo action 3"],
            "published_at": "2026-10-09T03:35:00+00:00",
            "duration_sec": 982,
            "views": 343,
            "likes": 36,
            "comments": 16,
            "ctr": 7.1,
            "avg_view_duration_sec": 380.0,
            "retention_pct": 38.7,
            "traffic_sources": {"YouTube search": 55.0, "Suggested videos": 30.0, "Browse features": 10.0, "Other": 5.0},
            "sub_change": 19,
            "view_velocity": 12.3,
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

    # --- INSTAGRAM MOCK DATA (Calibrated to Real 282-Follower Scale & Kolkata to Ladakh Series) ---
    instagram_posts = [
        {
            "post_id": "ig_post_01",
            "caption": "At 18,000 feet near Nurbu La, every breath is hard work. Himalayan 450 climbing to Umling La... drop a 🏔️ if you want the full route breakdown! Ep. 6 is live on YouTube.\n.\n#umlingla #himalayan450 #nurbula #ladakhtrip #solorider #souvik_says",
            "hashtags": ["umlingla", "himalayan450", "nurbula", "ladakhtrip", "solorider", "souvik_says"],
            "format": "REEL",
            "duration_sec": 28,
            "plays": 1240,
            "reach": 890,
            "likes": 78,
            "saves": 24,
            "shares": 16,
            "comments": 9,
            "profile_visits": 34,
            "follows_gained": 6,
            "thumbnail_url": "https://i.ytimg.com/vi/bW5s1DNjK8I/hqdefault.jpg",
            "permalink": "https://instagram.com/p/souvik_says_ep6",
            "published_at": (now - timedelta(days=3, hours=2)).isoformat(),
            "is_my_post": True
        },
        {
            "post_id": "ig_post_02",
            "caption": "Rezang La to Hanle: 5 things nobody warns you about the silent border roads. (Save this guide for your 2026 Ladakh ride!) 🇮🇳🏍️ Slide 4 has fuel calculation.\n.\n#hanle #rezangla #ladakhtour #himalayan450 #motorcycletouring #souvik_says",
            "hashtags": ["hanle", "rezangla", "ladakhtour", "himalayan450", "motorcycletouring", "souvik_says"],
            "format": "CAROUSEL",
            "duration_sec": 0,
            "plays": 0,
            "reach": 640,
            "likes": 62,
            "saves": 38,
            "shares": 12,
            "comments": 8,
            "profile_visits": 22,
            "follows_gained": 4,
            "thumbnail_url": "https://i.ytimg.com/vi/mxK3KPN1FMk/hqdefault.jpg",
            "permalink": "https://instagram.com/p/souvik_says_ep5",
            "published_at": (now - timedelta(days=9, hours=5)).isoformat(),
            "is_my_post": True
        },
        {
            "post_id": "ig_post_03",
            "caption": "An auto-rickshaw at 17,982 ft on Khardung La?! 🛺🤯 Just when you think Ladakh can't surprise you anymore. Himalayan 450 in freezing sleet! Full story in Ep. 4.\n.\n#khardungla #autorickshaw #lehladakh #himalayan450 #biketrip #souvik_says",
            "hashtags": ["khardungla", "autorickshaw", "lehladakh", "himalayan450", "biketrip", "souvik_says"],
            "format": "REEL",
            "duration_sec": 42,
            "plays": 2180,
            "reach": 1540,
            "likes": 142,
            "saves": 45,
            "shares": 38,
            "comments": 19,
            "profile_visits": 52,
            "follows_gained": 11,
            "thumbnail_url": "https://i.ytimg.com/vi/uiPuFqgcWCo/hqdefault.jpg",
            "permalink": "https://instagram.com/p/souvik_says_ep4",
            "published_at": (now - timedelta(days=16, hours=3)).isoformat(),
            "is_my_post": True
        },
        {
            "post_id": "ig_post_04",
            "caption": "The road to Leh that Google Maps said did not exist! Turning off the highway onto unmarked mountain dirt. 🏍️💨 Who else loves getting lost in the mountains?\n.\n#offroadladakh #himalayan450 #googlemaps #adventuremotorcycle #bikerlife #souvik_says",
            "hashtags": ["offroadladakh", "himalayan450", "googlemaps", "adventuremotorcycle", "bikerlife", "souvik_says"],
            "format": "SINGLE_IMAGE",
            "duration_sec": 0,
            "plays": 0,
            "reach": 490,
            "likes": 54,
            "saves": 14,
            "shares": 6,
            "comments": 7,
            "profile_visits": 18,
            "follows_gained": 2,
            "thumbnail_url": "https://i.ytimg.com/vi/0BorTN7XpKM/hqdefault.jpg",
            "permalink": "https://instagram.com/p/souvik_says_ep3",
            "published_at": (now - timedelta(days=24, hours=6)).isoformat(),
            "is_my_post": True
        },
        {
            "post_id": "ig_post_05",
            "caption": "Freezing rain across Baralacha La into Zanskar. When the weather turns into hell, the Himalayan 450 just keeps chugging through mud and slush. 🌧️🏔️\n.\n#zanskar #baralachala #monsoonride #himalayan450 #rainriding #souvik_says",
            "hashtags": ["zanskar", "baralachala", "monsoonride", "himalayan450", "rainriding", "souvik_says"],
            "format": "REEL",
            "duration_sec": 35,
            "plays": 980,
            "reach": 710,
            "likes": 64,
            "saves": 19,
            "shares": 10,
            "comments": 6,
            "profile_visits": 28,
            "follows_gained": 5,
            "thumbnail_url": "https://i.ytimg.com/vi/JLEuioDpubM/hqdefault.jpg",
            "permalink": "https://instagram.com/p/souvik_says_ep2",
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

    # --- YOUTUBE RETENTION CURVES FOR LAST 5 REAL UPLOADS (KOLKATA TO LADAKH) ---
    youtube_retention_curves = [
        {
            "video_id": "bW5s1DNjK8I",
            "title": "The Hardest Route to Umling La: Surviving Nurbu La on the Himalayan 450 | Kolkata to Ladakh Ep. 6",
            "ctr": 7.8,
            "avg_view_duration_sec": 485.0,
            "avg_percentage_viewed": 37.3,
            "retention_curve": [
                {"second": 0, "retention_pct": 100.0},
                {"second": 3, "retention_pct": 78.5},
                {"second": 15, "retention_pct": 68.0},
                {"second": 45, "retention_pct": 60.5},
                {"second": 105, "retention_pct": 49.0},
                {"second": 240, "retention_pct": 42.0},
                {"second": 500, "retention_pct": 38.0},
                {"second": 850, "retention_pct": 34.0},
                {"second": 1299, "retention_pct": 28.0}
            ],
            "drop_off_points": [
                {"timestamp_sec": 3, "timestamp_formatted": "00:03", "drop_pct": 21.5, "cause": "Slow intro talking head at high altitude without immediate riding hook"},
                {"timestamp_sec": 105, "timestamp_formatted": "01:45", "drop_pct": 11.5, "cause": "Protracted scenic B-roll with no throttle change or dialogue progression"}
            ]
        },
        {
            "video_id": "mxK3KPN1FMk",
            "title": "Riding the Silent Frontier | Pangong Tso to Hanle via Rezang La | Kolkata to Ladakh Ep. 5",
            "ctr": 6.9,
            "avg_view_duration_sec": 290.0,
            "avg_percentage_viewed": 48.2,
            "retention_curve": [
                {"second": 0, "retention_pct": 100.0},
                {"second": 5, "retention_pct": 82.0},
                {"second": 30, "retention_pct": 74.0},
                {"second": 90, "retention_pct": 66.0},
                {"second": 190, "retention_pct": 52.0},
                {"second": 380, "retention_pct": 44.0},
                {"second": 602, "retention_pct": 38.0}
            ],
            "drop_off_points": [
                {"timestamp_sec": 5, "timestamp_formatted": "00:05", "drop_pct": 18.0, "cause": "Lengthy scenic pan before introducing the emotional significance of Rezang La"},
                {"timestamp_sec": 190, "timestamp_formatted": "03:10", "drop_pct": 14.0, "cause": "Silent straight-road riding clip exceeding 35s with no mic narration"}
            ]
        },
        {
            "video_id": "uiPuFqgcWCo",
            "title": "Auto-Rickshaw at Khardung La?! | Leh to Khardung La & Pangong | Kolkata to Ladakh Ep. 4",
            "ctr": 8.4,
            "avg_view_duration_sec": 580.0,
            "avg_percentage_viewed": 35.4,
            "retention_curve": [
                {"second": 0, "retention_pct": 100.0},
                {"second": 4, "retention_pct": 72.0},
                {"second": 45, "retention_pct": 58.0},
                {"second": 150, "retention_pct": 44.0},
                {"second": 400, "retention_pct": 32.0},
                {"second": 900, "retention_pct": 25.0},
                {"second": 1640, "retention_pct": 21.0}
            ],
            "drop_off_points": [
                {"timestamp_sec": 4, "timestamp_formatted": "00:04", "drop_pct": 28.0, "cause": "Mismatched title payoff delay: talking in Leh room rather than teasing the auto-rickshaw encounter"},
                {"timestamp_sec": 150, "timestamp_formatted": "02:30", "drop_pct": 14.0, "cause": "Prolonged mountain pass traffic wait with static helmet cam view"}
            ]
        },
        {
            "video_id": "0BorTN7XpKM",
            "title": "The Road to Leh That Doesn't Exist on Google Maps! | Kolkata to Ladakh Ep. 3",
            "ctr": 7.6,
            "avg_view_duration_sec": 440.0,
            "avg_percentage_viewed": 43.5,
            "retention_curve": [
                {"second": 0, "retention_pct": 100.0},
                {"second": 8, "retention_pct": 84.0},
                {"second": 60, "retention_pct": 72.0},
                {"second": 180, "retention_pct": 59.0},
                {"second": 450, "retention_pct": 46.0},
                {"second": 1011, "retention_pct": 39.0}
            ],
            "drop_off_points": [
                {"timestamp_sec": 8, "timestamp_formatted": "00:08", "drop_pct": 16.0, "cause": "Unnecessary GPS phone interface demonstration before showing the dramatic dirt trail"},
                {"timestamp_sec": 180, "timestamp_formatted": "03:00", "drop_pct": 13.0, "cause": "Continuous dirt track riding without showing route satellite perspective"}
            ]
        },
        {
            "video_id": "JLEuioDpubM",
            "title": "Jispa to Zanskar Through Hell's Weather | Kolkata to Ladakh Ep.2",
            "ctr": 5.8,
            "avg_view_duration_sec": 410.0,
            "avg_percentage_viewed": 39.0,
            "retention_curve": [
                {"second": 0, "retention_pct": 100.0},
                {"second": 2, "retention_pct": 81.0},
                {"second": 45, "retention_pct": 71.0},
                {"second": 160, "retention_pct": 58.0},
                {"second": 450, "retention_pct": 47.0},
                {"second": 1051, "retention_pct": 38.0}
            ],
            "drop_off_points": [
                {"timestamp_sec": 2, "timestamp_formatted": "00:02", "drop_pct": 19.0, "cause": "Starting in dry tent before showing the extreme weather storm outside"},
                {"timestamp_sec": 160, "timestamp_formatted": "02:40", "drop_pct": 13.0, "cause": "Heavy rain lens drops obscuring Osmo Action 3 without wiping cut"}
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
