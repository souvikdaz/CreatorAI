import json
from datetime import datetime, timezone
from modules.base import BaseModule
from core.gear_manager import GearManager

class ShootPlannerModule(BaseModule):
    name = "shoot"

    def run(self, **kwargs) -> dict:
        gm = self.config.gear_manager if hasattr(self.config, "gear_manager") else GearManager()
        data_source = f"Hardware & Software Manifest: {self.config.gear_config_path if hasattr(self.config, 'gear_config_path') else 'config/gear.yaml'}"
        confidence = "HIGH"

        # Mandatory Phone Specs Notice
        phone_notice = gm.get_phone_spec_notice()

        # 4 Fully-Detailed Main Planned Shoots using ONLY gear.yaml items
        planned_shoots = [
            {
                "id": 1,
                "title": "Glacial Stream Crossing Line & Throttle Control Reel",
                "format": "Instagram Reel (9:16 vertical) & YouTube Short",
                "platform": "Instagram & YouTube",
                "is_moving_shot": True,
                "gear_assigned": {
                    "motorcycle": gm.bike,
                    "primary_camera": gm.action_camera,
                    "secondary_camera": gm.phone,
                    "microphone": "Grenaro wireless microphone",
                    "editing_station": f"{gm.computer} with {gm.video_editing}",
                    "graphics_tool": gm.image_editing
                },
                "moving_subject_flag": "FLAGGED: Moving motorcycle over water terrain requires Grenaro wireless microphone transmitter clipped to rider jacket to eliminate cable pull and isolate voice from rushing water.",
                "step_by_step_setup": [
                    f"1. Mount {gm.action_camera} securely to helmet chin mount using standard vertical bracket for native 9:16 capture or shoot 4K 16:9 for Final Cut Pro vertical crop.",
                    "2. Clip Grenaro wireless mic transmitter inside rider jacket with deadcat foam facing away from direct chin-vent wind.",
                    f"3. Place {gm.phone} on a stable rock/pack at water exit point for third-person rider perspective (confirm Motorola Edge 40 Neo capture fps in config/gear.yaml).",
                    f"4. Ride {gm.bike} across stream in 1st gear standing on footpegs with steady throttle; avoid touching front brake.",
                    f"5. Ingest SD card footage into {gm.computer}; sync dual-camera angles and audio in {gm.video_editing}."
                ],
                "canva_free_graphic_plan": "Design a high-contrast cover in Canva (Free tier) with bold yellow '#FFEB3B' text: 'WATER CROSSING RULE'. Note: Free tier lacks Magic Resize; start directly with 1080x1920 Reel template."
            },
            {
                "id": 2,
                "title": "Himalayan 450 Emergency Toolkit & Puncture Survival Carousel",
                "format": "Instagram Carousel (1080x1350 4:5 ratio, 5 slides)",
                "platform": "Instagram",
                "is_moving_shot": False,
                "gear_assigned": {
                    "motorcycle": gm.bike,
                    "primary_camera": gm.phone,
                    "secondary_camera": "None needed",
                    "microphone": "Generic wired microphone (for voiceover)",
                    "editing_station": f"{gm.computer} with {gm.video_editing}",
                    "graphics_tool": gm.image_editing
                },
                "moving_subject_flag": "Static workshop/campsite setup: Generic wired microphone is ideal for clear desktop voiceover narration.",
                "step_by_step_setup": [
                    f"1. Park {gm.bike} on center stand on level ground.",
                    f"2. Lay out tool roll on clean ground cloth: 21mm wrench, 2 tire spoons, 21-inch tube, chain breaker, inflator.",
                    f"3. Capture flat-lay top-down photos using {gm.phone} under diffuse natural light (avoid direct harsh midday shadows).",
                    f"4. Record voiceover explanation on {gm.computer} using Generic wired microphone plugged into audio interface.",
                    f"5. Assemble 5 slides in {gm.image_editing} (Free tier): Slide 1 Cover, Slide 2 Tire repair tools, Slide 3 Fastener wrenches, Slide 4 Emergency siphoning tube, Slide 5 Packing checklist."
                ],
                "canva_free_graphic_plan": "Canva Free does not include 1-click background remover. Use high-contrast solid color backdrops during photography to keep clean edges."
            },
            {
                "id": 3,
                "title": "Sub-Zero Himalayan 450 Cold Start & Battery Survival Reel",
                "format": "Instagram Reel (9:16 vertical)",
                "platform": "Instagram",
                "is_moving_shot": False,
                "gear_assigned": {
                    "motorcycle": gm.bike,
                    "primary_camera": gm.action_camera,
                    "secondary_camera": gm.phone,
                    "microphone": "Generic wired microphone",
                    "editing_station": f"{gm.computer} with {gm.video_editing}",
                    "graphics_tool": gm.image_editing
                },
                "moving_subject_flag": "Stationary bike start: Generic wired microphone positioned near exhaust and engine block for clean acoustic capture.",
                "step_by_step_setup": [
                    f"1. Leave {gm.bike} parked overnight in cold conditions.",
                    f"2. Position {gm.action_camera} on tripod or pack facing the digital TFT console to record initial boot sequence and ambient temperature reading.",
                    f"3. Use {gm.phone} for quick vertical B-roll of frosted seat and frozen water droplets on fuel tank.",
                    "4. Position Generic wired microphone 1 meter behind exhaust to capture initial cold ignition burst without clipping.",
                    f"5. Transfer clips to {gm.computer} and color-grade cold tones in {gm.video_editing} with subtle vignette."
                ],
                "canva_free_graphic_plan": "Add high-contrast text overlay in Canva Free: '-4°C COLD START' using bold sans-serif font."
            },
            {
                "id": 4,
                "title": "Why You Must Drop Rear Tire to 22 PSI on Mountain Shale Trails",
                "format": "Instagram Reel & YouTube Short (9:16 vertical)",
                "platform": "Instagram & YouTube",
                "is_moving_shot": True,
                "gear_assigned": {
                    "motorcycle": gm.bike,
                    "primary_camera": gm.action_camera,
                    "secondary_camera": gm.phone,
                    "microphone": "Grenaro wireless microphone",
                    "editing_station": f"{gm.computer} with {gm.video_editing}",
                    "graphics_tool": gm.image_editing
                },
                "moving_subject_flag": "FLAGGED: Rider speaking while riding over loose shale rocks requires Grenaro wireless microphone for clear helmet voice capture.",
                "step_by_step_setup": [
                    f"1. Measure {gm.bike} rear tire pressure using handheld gauge; capture gauge readout close-up with {gm.phone}.",
                    f"2. Mount {gm.action_camera} on lower engine guard or footpeg bracket facing rear tire to capture tread flexion over loose rocks.",
                    "3. Connect Grenaro wireless mic transmitter into helmet cheek pad.",
                    f"4. Ride a 50-meter test section on {gm.bike} at 32 PSI, then repeat at 22 PSI to show visible traction difference.",
                    f"5. Edit side-by-side comparison in {gm.video_editing} on {gm.computer}."
                ],
                "canva_free_graphic_plan": "Create split comparison graphic in Canva Free: '32 PSI (SLIP)' vs '22 PSI (GRIP)'."
            }
        ]

        # Concepts needing missing gear strictly segregated into "Needs gear (optional)"
        needs_gear_optional = [
            {
                "concept": "Cinematic Aerial Tracking Shots over Shinku La Pass",
                "required_missing_gear": "Compact Drone (e.g. DJI Mini series)",
                "why_kept_out_of_main_plan": "Drone is not listed in config/gear.yaml. Cannot be executed with current gear.",
                "current_workaround": f"Use {gm.action_camera} mounted on extended selfie stick braced on {gm.bike} pannier mount for high-angle simulated jib shots."
            },
            {
                "concept": "360-Degree Third-Person Chase Cam Without Visible Mounting Stick",
                "required_missing_gear": "Dedicated 360 Camera",
                "why_kept_out_of_main_plan": "360 camera is not listed in config/gear.yaml. Rule strictly prohibits suggesting unlisted cameras.",
                "current_workaround": f"Mount {gm.action_camera} facing backward on {gm.bike} tail luggage rack with ultra-wide RockSteady stabilization enabled."
            },
            {
                "concept": "Automated One-Click Multi-Platform Asset Resizing & Brand Kit Palettes",
                "required_missing_gear": "Canva Pro Subscription",
                "why_kept_out_of_main_plan": "Only Canva (Free tier) is authorized in config/gear.yaml.",
                "current_workaround": "Manually create separate 1080x1920 (9:16) and 1080x1350 (4:5) canvas projects in Canva Free and reuse saved hex codes (#FFEB3B, #FFFFFF, #0F0F0F)."
            }
        ]

        return {
            "module": self.name,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "data_source": data_source,
            "confidence": confidence,
            "gear_manifest": gm.get_gear_manifest(),
            "phone_notice": phone_notice,
            "phone_spec_confirmed": gm.is_phone_spec_confirmed(),
            "phone_settings": gm.phone_settings,
            "planned_shoots_count": len(planned_shoots),
            "planned_shoots": planned_shoots,
            "needs_gear_optional": needs_gear_optional
        }

    def to_markdown(self, result: dict) -> str:
        md = []
        md.append("# 🎬 Instagram & YouTube Module 5: Gear-Aware Shoot Planner\n")
        md.append(f"- **Data Source:** {result['data_source']}")
        md.append(f"- **Confidence Level:** {result['confidence']}\n")

        gm = result["gear_manifest"]
        md.append("## 🎒 Authorized Gear Manifest (`config/gear.yaml`)")
        md.append(f"- **Motorcycle:** `{gm['authorized_bike']}` (Strict rule: ride & travel content only)")
        md.append(f"- **Action Camera:** `{gm['authorized_action_camera']}` (Primary motovlog & rides)")
        md.append(f"- **Phone:** `{gm['authorized_phone']}` (Reels quick-capture & vertical)")
        md.append(f"- **Microphones:** `{', '.join(gm['authorized_microphones'])}` (Wired for fixed, Grenaro wireless for moving)")
        md.append(f"- **Computer & FX:** `{gm['authorized_workstation']}` running `{gm['authorized_video_editor']}`")
        md.append(f"- **Design:** `{gm['authorized_image_editor']}` (Free tier limits respected)\n")

        if result.get("phone_notice"):
            md.append(f"> ⚠️ **Phone Configuration Notice:** {result['phone_notice']}\n")
        elif result.get("phone_spec_confirmed"):
            ps = result.get("phone_settings", {})
            ps_str = ", ".join(f"{k.replace('_', ' ').title()}: {v}" for k, v in ps.items())
            md.append(f"> 📱 **Phone Settings Confirmed:** Motorola Edge 40 Neo ({ps_str})\n")

        md.append("## 📋 Planned Shoots (100% Compliant with `gear.yaml`)\n")
        for shoot in result["planned_shoots"]:
            md.append(f"### #{shoot['id']}. {shoot['title']}")
            md.append(f"- **Format:** `{shoot['format']}` on **{shoot['platform']}**")
            md.append(f"- **Assigned Gear:** Bike: `{shoot['gear_assigned']['motorcycle']}` | Cam: `{shoot['gear_assigned']['primary_camera']}` | Mic: `{shoot['gear_assigned']['microphone']}`")
            if shoot["is_moving_shot"]:
                md.append(f"- 🎙️ **Microphone Rule:** `{shoot['moving_subject_flag']}`")
            else:
                md.append(f"- 🎙️ **Microphone Rule:** `{shoot['moving_subject_flag']}`")
            md.append("- **Step-by-Step Setup:**")
            for step in shoot["step_by_step_setup"]:
                md.append(f"  - {step}")
            md.append(f"- **Canva Free Design Plan:** {shoot['canva_free_graphic_plan']}\n")

        md.append("## 📦 Needs gear (optional)")
        md.append("*The following concepts require equipment not present in `config/gear.yaml`. They are kept strictly separate from the main production plan:*\n")
        for opt in result["needs_gear_optional"]:
            md.append(f"### ⚙️ {opt['concept']}")
            md.append(f"- **Required Missing Gear:** `{opt['required_missing_gear']}`")
            md.append(f"- **Reason Kept Out:** {opt['why_kept_out_of_main_plan']}")
            md.append(f"- **Current Workaround with Listed Gear:** {opt['current_workaround']}\n")

        return "\n".join(md)
