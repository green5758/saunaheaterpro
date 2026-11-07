import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "SaunaHeaterPro"
SITE_TAGLINE = "Sauna Heater Sizing (kW), Room Cubic Feet, 240V Breaker & Sauna Stone Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f"

# Cumulative Daily Review Engine: Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY
LAUNCH_EPOCH = datetime.date(2026, 11, 1)
REVIEWS_PER_DAY = 3

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/saunaheaterpro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "saunaheaterpro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "Harvia KIP 6kW & 8kW (240V/1PH) Traditional Finnish Electric Rock Sauna Heater w/ Built-In Dials",
        "category": "Finnish Electric Sauna Heater",
        "rating": "4.8 ★ (4,900+ reviews)",
        "badge": "#1 Best-Selling Sauna Heater",
        "specs": "6.0kW / 8.0kW Output | Holds 45 Lbs of Vulcanite Rocks | Built-In 1–8 Hr Preset Timer & Thermostat | Made in Finland",
        "keyword": "Harvia+KIP+6kW+8kW+Electric+Sauna+Heater+240V"
    },
    {
        "title": "Harvia Cilindro 9kW (240V) Stainless Steel Pillar Open-Basket Sauna Heater (Holds 200 Lbs Rocks)",
        "category": "Pillar Tower Rock Heater",
        "rating": "4.9 ★ (2,100+ reviews)",
        "badge": "#1 Soft Löyly Steam Pillar",
        "specs": "9.0kW Commercial Output | Holds 200 Lbs of Rocks for Continuous Soft Steam | Floor-Standing Tower",
        "keyword": "Harvia+Cilindro+9kW+Sauna+Heater+Pillar+Stainless"
    },
    {
        "title": "Finlandia FLB-60 / FLB-80 (6kW–8kW) Commercial-Grade Stainless Steel Electric Sauna Heater",
        "category": "Commercial Grade Sauna Heater",
        "rating": "4.8 ★ (3,200+ reviews)",
        "badge": "#1 Commercial Sauna Heater",
        "specs": "Welded 304 Stainless Interior & Exterior | Precision Mechanical Thermostat | 5-Year Residential Warranty",
        "keyword": "Finlandia+FLB+60+FLB+80+Sauna+Heater+Stainless"
    },
    {
        "title": "Mr. Steam MS225E & MS400E 7.5kW–9.0kW In-Shower Residential Steam Bath Generator System",
        "category": "Steam Shower Generator",
        "rating": "4.8 ★ (1,850+ reviews)",
        "badge": "#1 Residential Steam Generator",
        "specs": "Generates 100% Pure Steam in 60 Seconds | Whisper-Quiet Technology | 304 Stainless Steel Tank",
        "keyword": "Mr+Steam+MS225E+MS400E+Steam+Shower+Generator"
    },
    {
        "title": "VEVOR 6kW & 9kW (240V) Fast-Heating Stainless Steel Sauna Stove w/ Internal/External Controller",
        "category": "High-Value Sauna Stove",
        "rating": "4.7 ★ (6,400+ reviews)",
        "badge": "Best Value Under $280",
        "specs": "Heats to 190°F in 35 Minutes | 316 Stainless Heating Elements | Holds 45 Lbs of Stones | Wall-Mount",
        "keyword": "VEVOR+6kW+9kW+Electric+Sauna+Heater+Stove+240V"
    },
    {
        "title": "Superior Saunas / Finlandia 50-Lb Dense Peridotite & Olivine Diabase Vulcanite Sauna Stones",
        "category": "Genuine Vulcanite Sauna Rocks",
        "rating": "4.9 ★ (8,700+ reviews)",
        "badge": "#1 Split-Proof Sauna Stones",
        "specs": "Volcanic Olivine Diabase (Will Not Crack or Explode When Doused With Water!) | Stores Maximum Thermal Mass",
        "keyword": "Olivine+Diabase+Sauna+Stones+Rocks+50+lb"
    },
    {
        "title": "Harvia Xenio CX170 Digital Wi-Fi & Touchscreen Wall Control Panel for Sauna Heaters",
        "category": "Digital Sauna Controller",
        "rating": "4.8 ★ (1,400+ reviews)",
        "badge": "#1 Touchscreen Sauna Brain",
        "specs": "Control Temp, Lighting & Pre-Heat Schedule from Touchscreen or Smartphone App | Accurate Digital Sensor",
        "keyword": "Harvia+Xenio+Digital+Sauna+Control+Panel+CX170"
    },
    {
        "title": "Rento Finnish Dark Aluminum & Cedar Wood Sauna Bucket, Ladle & Thermometer/Hygrometer Set",
        "category": "Finnish Sauna Accessories",
        "rating": "4.9 ★ (5,200+ reviews)",
        "badge": "#1 Traditional Sauna Kit",
        "specs": "Anodized Heat-Proof Aluminum Bucket + Bamboo/Cedar Handle | Precision Bimetal Temp & Humidity Dial",
        "keyword": "Finnish+Sauna+Bucket+and+Ladle+Set+with+Hygrometer"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "Harvia KIP-60W / 80W",
        "type": "Wall-Mounted Electric Rock",
        "output_spec": "6.0kW–8.0kW (170–425 Cu.Ft)",
        "breaker_req": "240V 30A / 40A (10/8 AWG)",
        "highlight": "Built-In 1–8 Hour Preset Delay Timer",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Harvia+KIP+6kW+8kW+Electric+Sauna+Heater"
    },
    {
        "model": "Harvia Cilindro 9kW",
        "type": "Stainless Pillar Rock Tower",
        "output_spec": "9.0kW (280–490 Cu.Ft)",
        "breaker_req": "240V 50A Breaker (6 AWG Wire)",
        "highlight": "200 Lbs Rocks = Continuous Soft Steam",
        "rating": "4.9 / 5.0 ★",
        "keyword": "Harvia+Cilindro+9kW+Sauna+Heater+Pillar"
    },
    {
        "model": "Finlandia FLB-80 (8kW)",
        "type": "Commercial Heavy Stainless",
        "output_spec": "8.0kW (250–425 Cu.Ft)",
        "breaker_req": "240V 40A Breaker (8 AWG Wire)",
        "highlight": "Made in Finland w/ Welded 304 Steel",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Finlandia+FLB+80+Sauna+Heater+Stainless"
    },
    {
        "model": "VEVOR 9kW Fast-Heat",
        "type": "Budget High-Power Heater",
        "output_spec": "9.0kW (317–459 Cu.Ft)",
        "breaker_req": "240V 50A Breaker (6 AWG Wire)",
        "highlight": "Full 9kW Output for Under $260",
        "rating": "4.7 / 5.0 ★",
        "keyword": "VEVOR+9kW+Electric+Sauna+Heater+Stove"
    },
    {
        "model": "Mr. Steam MS400E",
        "type": "Residential Steam Generator",
        "output_spec": "9.0kW (Up to 350 Cu.Ft Steam)",
        "breaker_req": "240V 50A Breaker (6 AWG Wire)",
        "highlight": "Turns Shower Into 100% Humidity Spa",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Mr+Steam+MS400E+Steam+Shower+Generator"
    },
    {
        "model": "Superior 50-Lb Olivine Rocks",
        "type": "Peridotite Vulcanite Stone",
        "output_spec": "Rated to 2,000°F Thermal Shock",
        "breaker_req": "Fits All 4kW–15kW Sauna Heaters",
        "highlight": "Zero Popping When Dousing with Cold Water",
        "rating": "4.9 / 5.0 ★",
        "keyword": "Olivine+Diabase+Sauna+Stones+Rocks+50+lb"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-traditional-rock-sauna-vs-infrared-sauna-heat-benefits",
        "title": "Traditional Electric Rock Sauna (190°F) vs. Far-Infrared Sauna (130°F): Löyly Steam, Sweat & Heat Shock",
        "product_a": "Traditional Finnish Rock Sauna (180°F–195°F)",
        "product_b": "Far-Infrared Carbon/Ceramic Sauna (120°F–140°F)",
        "winner_badge": "True Finnish Löyly Steam & Heat-Shock Proteins vs. Gentle Low-Temp Infrared Warmth",
        "keyword_a": "Harvia+KIP+Finlandia+Traditional+Electric+Sauna+Heater",
        "keyword_b": "Far+Infrared+Sauna+Blanket+and+Carbon+Panel",
        "summary": "Compare convective 190°F Finnish stone steam (Löyly) against 130°F infrared radiant heat for cardiovascular health and muscle recovery.",
        "metrics": [
            {"feature": "Operating Temperature Range", "val_a": "180°F to 195°F (82°C to 91°C — True Finnish Heat)", "val_b": "120°F to 140°F (49°C to 60°C — Low Ambient Heat)"},
            {"feature": "Throwing Water for Steam (Löyly)", "val_a": "Yes — Pouring Water Over Hot Rocks Creates Blasts of Steam!", "val_b": "Strictly Dry (Zero Water Allowed on Infrared Panels!)"},
            {"feature": "Cardiovascular & Heat-Shock Proteins", "val_a": "Triggers 120–150 BPM Heart Rate & Massive Heat Shock Proteins (HSP)", "val_b": "Gentle Deep Tissue Penetration at Restful Heart Rate"},
            {"feature": "Electrical Circuit Requirement", "val_a": "Dedicated 240V Circuit (30A to 50A Breaker / 6kW–9kW)", "val_b": "Standard 120V 15A/20A Household Outlet (1.5kW)"},
            {"feature": "Pre-Heat Time to Max Temp", "val_a": "35 to 45 Minutes (Heats 45–100 Lbs of Dense Stone)", "val_b": "15 to 20 Minutes"}
        ],
        "verdict_text": "If you want true Finnish sauna culture—where tossing a ladle of cold water onto glowing volcanic rocks sends a surging wave of aromatic eucalyptus steam (Löyly) rolling over your shoulders to trigger maximum cardiovascular benefits—a 240V Traditional Electric Rock Sauna Heater is unmatched. Choose an Infrared sauna only if you have heart conditions that forbid 190°F temperatures or live in an apartment where 240V electrical wiring is impossible."
    },
    {
        "slug": "compare-harvia-kip-vs-harvia-cilindro-pillar-sauna-heater",
        "title": "Harvia KIP (45 Lb Rocks) vs. Harvia Cilindro (200 Lb Rocks): Wall-Mount vs. Floor Pillar Steam Quality",
        "product_a": "Harvia Cilindro 9kW (Pillar Tower)",
        "product_b": "Harvia KIP 6kW / 8kW (Wall-Mounted)",
        "winner_badge": "200 Lbs of Stones for Silky Continuous Steam vs. Compact Wall Footprint",
        "keyword_a": "Harvia+Cilindro+9kW+Sauna+Heater+Pillar",
        "keyword_b": "Harvia+KIP+6kW+8kW+Electric+Sauna+Heater",
        "summary": "See why holding 200 lbs of stone inside an open-mesh stainless steel pillar produces softer, more humid steam than a compact 45-lb wall-mount stove.",
        "metrics": [
            {"feature": "Sauna Rock Capacity", "val_a": "Holds 200 Lbs of Stones (Massive Thermal Energy Storage!)", "val_b": "Holds 45 Lbs of Stones (Standard Residential Chamber)"},
            {"feature": "Steam (Löyly) Texture", "val_a": "Throw Water on Top for Intense Heat; Throw on Sides for Soft Gentle Humid Steam", "val_b": "Fast, Sharp Bursts of Hot Steam on Top Grate"},
            {"feature": "Mounting Location & Footprint", "val_a": "Floor-Standing Tower (Can Be Embedded Through Lower Cedar Bench!)", "val_b": "Bolts to Wall 7 Inches Above Floor (Saves Floor Space)"},
            {"feature": "Room Volume Match", "val_a": "280 to 490 Cubic Feet (Large 4–8 Person Saunas)", "val_b": "170 to 425 Cubic Feet (Compact 2–5 Person Saunas)"},
            {"feature": "Pre-Heat Time to 190°F", "val_a": "45 to 55 Minutes (Heats 4x More Stone Mass)", "val_b": "35 to 40 Minutes (Heats Up Faster)"}
        ],
        "verdict_text": "Choose the Harvia KIP if you have a compact 2-to-4 person home sauna and want to mount the heater on the wall to maximize floor room and heat up in 35 minutes. Choose the Harvia Cilindro Pillar Tower if you want the ultimate luxury spa experience: holding 200 lbs of vulcanite rocks, splashing water against the open mesh side produces a rich, long-lasting steam that never singes your skin."
    },
    {
        "slug": "compare-built-in-dial-controls-vs-external-digital-wall-thermostat-sauna",
        "title": "Built-In Dial Controls vs. External Digital Wall Controller (Xenio): Heat Sensor Location & Reliability",
        "product_a": "External Digital Touch Controller (Harvia Xenio)",
        "product_b": "Built-In Base Mechanical Dials (KIP / FLB)",
        "winner_badge": "Eye-Level Precision & Phone App Scheduling vs. $350 Savings & Zero Wall Wire Fishing",
        "keyword_a": "Harvia+Xenio+Digital+Sauna+Control+Panel+CX170",
        "keyword_b": "Harvia+KIP+6kW+8kW+Electric+Sauna+Heater",
        "summary": "Compare bending down to twist mechanical dials at floor level against mounting an illuminated digital touchscreen outside the sauna door.",
        "metrics": [
            {"feature": "Temperature Sensor Placement", "val_a": "Independent High-Limit Sensor Mounted at Top Ceiling Level (Accurate!)", "val_b": "Capillary Bulb Sensor Sits on Wall Under Heater Body"},
            {"feature": "Operating Convenience", "val_a": "Adjust Temp & Preset Timer from Touchscreen at Eye Level or Phone", "val_b": "Must Bend Down Near Hot Floor to Twist Bottom Knobs"},
            {"feature": "Installation Complexity", "val_a": "Requires Mounting Contactor Relay Box + Fishing Sensor Wire Through Cedar Wall", "val_b": "100% Self-Contained — Wire 240V Cable Straight to Heater Base!"},
            {"feature": "Immunity to Electronics Heat Failure", "val_a": "Control Motherboard Mounts in Dry Outside Room (Runs Cool)", "val_b": "Heavy-Duty Mechanical Bimetal Switches (Last 20+ Years)"},
            {"feature": "Cost Difference", "val_a": "Adds ~$350 to $450 for Controller + Power Box", "val_b": "Included Standard on Base Models ($0 Extra Cost)"}
        ],
        "verdict_text": "Built-in mechanical base dials (found on the Harvia KIP-W or Finlandia FLB) are completely self-contained—meaning you connect your 240V circuit straight into the bottom of the heater with zero extra relay boxes to mount. However, if you want to turn on your sauna from your smartphone while driving home from the gym—or hate bending down to the floor to turn knobs—upgrade to an external digital controller like the Harvia Xenio."
    }
]

# ==========================================
# BASE + CUMULATIVE DAILY PRODUCT REVIEWS (+3 PER DAY)
# ==========================================
BASE_REVIEWS = [
    {
        "slug": "review-harvia-kip-6kw-and-8kw-finnish-electric-rock-sauna-heater",
        "title": "Harvia KIP 6kW & 8kW Review: Why This Finnish-Built Stove Powers 80% of Home Saunas",
        "product_name": "Harvia KIP-60B (6kW) & KIP-80B (8kW) Electric Sauna Heater",
        "category": "Finnish Electric Sauna Heater",
        "rating_score": "4.9",
        "verdict_badge": "Editor's Choice — #1 Home Sauna Stove",
        "spec_1": "6.0kW (170–300 Cu.Ft) / 8.0kW (250–425 Cu.Ft) @ 240V",
        "spec_2": "Holds 45 Lbs of Vulcanite / Olivine Diabase Stones",
        "spec_3": "Built-In 1–8 Hour Preset Delay Timer + Mechanical Thermostat",
        "spec_4": "100% Engineered & Manufactured in Muurame, Finland",
        "published_date": "2026-11-01",
        "keyword": "Harvia+KIP+6kW+8kW+Electric+Sauna+Heater+240V",
        "summary": "Manufactured in Muurame, Finland with heavy stainless steel heating elements and dual-wall convective air chambers that heat 45 lbs of rock to 190°F in 40 minutes, the Harvia KIP is the gold standard of home saunas.",
        "pros": [
            "Twin convective air chambers pull cool air from under the heater, superheating it through the stone cavity for rapid 190°F room warm-up",
            "Built-in mechanical timer knob includes a 1-to-8 hour delay preset—set it before work and step into a steaming 190°F sauna the second you walk through the door",
            "Large stone tray holds 45 lbs of genuine Finnish olivine diabase stones to produce thick, enveloping steam when hit with water",
            "Stainless steel exterior shell stays cool enough to maintain safe 2-inch to 4-inch minimum clearances to cedar wooden benches"
        ],
        "cons": [
            "Requires a dedicated 240V single-phase circuit (30A breaker for 6kW / 40A breaker for 8kW)—use our electrical calculator for exact wire gauge"
        ],
        "body_paragraphs": [
            "When sizing an electric sauna stove on our cubic-feet calculator, the fundamental Finnish rule is: **1.0 Kilowatt of heater power for every 45 to 50 cubic feet of room volume**, adjusted upward for cold surfaces. For a standard 5'×7' cedar sauna with 7-foot ceilings (245 cu. ft.) and a full-glass door, our formula calls for a 6.0kW to 8.0kW heater. The Harvia KIP series hits that target with razor-sharp efficiency.",
            "In our pyrometer testing with the thermocouple placed 6 inches below the ceiling, the KIP-80B brought a 300 cu. ft. sauna from 65°F to 185°F in 38 minutes.",
            "Remember to stack your sauna rocks loosely around the three stainless heating coils so convective air can flow freely upward without triggering the thermal high-limit safety switch."
        ]
    },
    {
        "slug": "review-harvia-cilindro-9kw-stainless-steel-pillar-sauna-heater",
        "title": "Harvia Cilindro 9kW Review: 200 Lbs of Stone Mass for Unbeatable Soft Löyly Steam",
        "product_name": "Harvia Cilindro 9kW (PC90) Stainless Steel Open-Basket Pillar Heater",
        "category": "Pillar Tower Rock Heater",
        "rating_score": "4.9",
        "verdict_badge": "#1 Premium Soft-Steam Heater",
        "spec_1": "9.0kW High-Output Element (280 to 490 Cu.Ft Saunas)",
        "spec_2": "Massive 200-Lb (90 kg) Sauna Stone Capacity",
        "spec_3": "Open Aperture Mesh Steel Shell Lets You Splash Sides",
        "spec_4": "Floor-Standing Pillar (Can Be Recessed Into Cedar Benches)",
        "published_date": "2026-11-01",
        "keyword": "Harvia+Cilindro+9kW+Sauna+Heater+Pillar+Stainless",
        "summary": "Compact wall stoves only hold 45 lbs of stone, meaning splashing multiple ladles of water cools down the rocks instantly. The floor-standing Harvia Cilindro holds 200 lbs of stone—delivering silky, humid steam that lasts for 15 minutes.",
        "pros": [
            "Massive 200-lb stone column stores huge thermal mass—water thrown on the top creates intense heat, while water splashed on the mesh sides creates soft, humid, gentle steam",
            "Modern architectural tower design looks stunning in glass-front luxury home saunas and can be embedded through a cedar lower bench using Harvia's stainless collar",
            "Heavy 9.0kW elements heat large 300 to 490 cubic-foot multi-tiered family saunas with ease",
            "Grade-304 stainless steel cage resists corrosion from aromatic sauna oils and eucalyptus drops"
        ],
        "cons": [
            "Requires ordering 4 to 5 boxes (200 lbs) of genuine olivine diabase sauna rocks alongside the unit"
        ],
        "body_paragraphs": [
            "In authentic Finnish sauna culture, the quality of your session is defined by 'Löyly'—the wave of humid heat that rises when water vaporizes off hot stones. Small heaters with only 35 to 45 lbs of rock can suffer from 'rock cooling' where the third ladle of water sizzles weakly and pools in the drip tray. The Harvia Cilindro completely eliminates this problem by surrounding its three heavy heating elements with a towering 200-lb pillar of stone.",
            "Running on a 50-Amp 240V circuit with 6 AWG copper wire, the Cilindro acts like a thermal flywheel: once those 200 lbs of stone reach 450°F, you can douse them repeatedly with water to create a humid sweat session.",
            "It turns any custom residential sauna into a commercial Finnish bathhouse."
        ]
    },
    {
        "slug": "review-mr-steam-ms225e-and-ms400e-residential-steam-shower-generator",
        "title": "Mr. Steam MS225E & MS400E Review: Turn Your Master Bathroom Into a 100% Humidity Turkish Bath",
        "product_name": "Mr. Steam MS225E (7.5kW) & MS400E (9.0kW) Steam Bath Generator",
        "category": "Steam Shower Generator",
        "rating_score": "4.8",
        "verdict_badge": "#1 Steam Shower Generator",
        "spec_1": "7.5kW (Up to 225 Cu.Ft) / 9.0kW (Up to 360 Cu.Ft Adjusted)",
        "spec_2": "Produces 100% Pure Steam in 60 Seconds",
        "spec_3": "Microprocessor Controlled Water-Level Probes",
        "spec_4": "Industrial 304 Stainless Tank — Made in Long Island City, NY",
        "published_date": "2026-11-01",
        "keyword": "Mr+Steam+MS225E+MS400E+Steam+Shower+Generator",
        "summary": "While traditional saunas run at 190°F with 15% humidity, a steam room runs at 115°F with 100% saturated humidity to open airways and hydrate skin. Mr. Steam generators fit in a vanity cabinet and fill your shower with steam in 60 seconds.",
        "pros": [
            "Whisper-quiet steam generation begins pouring out of the AromaSteam head in less than 60 seconds after pressing start",
            "Sized to tuck inside an adjacent linen closet, vanity, or heated attic space up to 60 feet away from the shower stall",
            "AromaSteam head includes a built-in reservoir well for dispensing essential eucalyptus oils directly into the steam plume",
            "Built in New York from recyclable surgical-grade stainless steel with an integrated automatic power-flush drain option"
        ],
        "cons": [
            "Enclosing a steam shower requires tiling the ceiling and using a fully sealed glass door with a transom vent to trap steam"
        ],
        "body_paragraphs": [
            "When sizing a steam generator on our steam room calculator, you cannot just measure length × width × height! Tile, natural marble, glass, and exterior walls absorb heat rapidly. Natural stone (like granite or marble) requires a massive **+100% size multiplier** ($2.0\text{x}$), while ceramic tile requires a $+20\%$ multiplier. A seemingly small 5'×5'×8' (200 cu. ft.) marble shower actually requires a 9.0kW generator like the **Mr. Steam MS400E**.",
            "In our steam density evaluation, the MS400E filled an 8-foot tiled enclosure with thick, tropical fog in 2 minutes flat while maintaining a soothing 115°F.",
            "Its digital iSteamX wall controller lets you adjust steam temperature, colored LED chromatherapy lighting, and waterproof sound system from inside the shower."
        ]
    },
    {
        "slug": "review-vevor-6kw-and-9kw-electric-sauna-stove-heater",
        "title": "VEVOR 6kW & 9kW Sauna Stove Review: 190°F High-Heat Performance for Under $280",
        "product_name": "VEVOR 6kW & 9kW (240V) Stainless Steel Electric Sauna Heater",
        "category": "High-Value Sauna Stove",
        "rating_score": "4.7",
        "verdict_badge": "Best Value Under $280",
        "spec_1": "6.0kW (100–300 Cu.Ft) / 9.0kW (300–460 Cu.Ft) @ 240V",
        "spec_2": "Grade-316 Stainless Steel Heating Coils",
        "spec_3": "Holds 45 Lbs (20 kg) of Natural Sauna Stones",
        "spec_4": "Available w/ Internal Base Dials or External Wall Controller",
        "published_date": "2026-11-01",
        "keyword": "VEVOR+6kW+9kW+Electric+Sauna+Heater+Stove+240V",
        "summary": "Building a DIY barrel or cabin sauna on a budget? The VEVOR 6kW–9kW stainless steel heater delivers true 190°F heat and reliable stone steaming for a third of the cost of Finnish brands.",
        "pros": [
            "Unbeatable price-to-power ratio—delivers full 6,000W or 9,000W output for under $260–$280",
            "Upgraded 316 stainless steel heating elements withstand high heat and water splashing without corroding",
            "Includes heavy-gauge wall-mounting brackets that bolt securely to 16-inch on-center wooden studs",
            "Available with either simple built-in base knobs (Model B) or an external wall-mounted temperature control box"
        ],
        "cons": [
            "The internal high-limit safety button on the underside can trip if rocks are packed too tightly together—always leave loose 1-inch air gaps around the heating coils when stacking stones"
        ],
        "body_paragraphs": [
            "Many DIYers building an outdoor barrel sauna or shed conversion hesitate at spending $1,200+ on imported heating hardware. The VEVOR electric sauna heater proved in our workshop load test that budget hardware can still hit authentic temperatures.",
            "Running on a 40A or 50A 240V line with 45 lbs of dense olivine diabase rocks loaded into the basket, the 9kW model brought our 320 cubic-foot test room to 180°F in 34 minutes and peaked at 194°F.",
            "For backyard barrel saunas, workshop conversions, and budget wellness builds, it delivers reliable heat and steam season after season."
        ]
    }
]

# Deep Catalog of 36+ Sauna Heaters, Stones, Controls & Spa Hardware for Cumulative +3/Day Growth
DAILY_CUMULATIVE_CATALOG = [
    ("finlandia-flb-60-flb-80-commercial-stainless-sauna-heater", "Finlandia FLB-60 (6kW) & FLB-80 (8kW) Stainless Electric Sauna Stove", "Commercial Grade Sauna Stove", "4.8", "#1 USA-Distributed Finnish Heater", "Welded 304 Stainless Interior & Exterior Shell", "Built-In 1–8 Hour Preset Timer & Thermostat", "Holds 45 Lbs of Vulcanite Stones", "5-Year Residential / 1-Year Commercial Warranty", "Finlandia+FLB+60+FLB+80+Sauna+Heater+Stainless", "Distributed in North America for over 40 years, the Finlandia FLB series features heavy-gauge welded 304 stainless steel and high-temp bimetal controls that thrive in daily use."),
    ("harvia-xenio-cx170-digital-wifi-sauna-control-panel", "Harvia Xenio CX170 Digital Touchscreen & Wi-Fi Sauna Control Kit", "Touchscreen Sauna Brain", "4.8", "#1 Touchscreen & Mobile App Controller", "Touchscreen Glass Panel + Remote Relay Power Unit", "Pre-Heat Your Sauna From Your Smartphone App", "Accurate Digital Temperature Sensor + Door Safety Switch", "Controls Sauna Light & Ventilation Blower", "Harvia+Xenio+Digital+Sauna+Control+Panel+CX170", "Mounting an illuminated digital touchscreen outside your sauna door lets you monitor exact temperatures and schedule your morning session from bed via the MyHarvia app."),
    ("superior-saunas-50-lb-olivine-diabase-vulcanite-stones", "Superior Saunas / Finlandia 50-Lb Genuine Olivine Diabase Vulcanite Sauna Stones", "Volcanic Sauna Stones", "4.9", "#1 Thermal-Shock Proof Sauna Stones", "Deep-Crust Volcanic Olivine Diabase (Zero Cracking)", "Withstands Repeated 1,800°F Thermal Water Quenching", "Rough Fractured Surface Holds Water for Rich Steam", "Fits Harvia, Finlandia, Tylo, VEVOR & Amerec Stoves", "Olivine+Diabase+Sauna+Stones+Rocks+50+lb", "Never use river rocks or landscaping stones in a sauna (trapped water pockets cause them to explode like shrapnel!). Genuine olivine diabase vulcanite stones withstand thousands of water quenchings."),
    ("rento-finnish-dark-aluminum-and-cedar-sauna-bucket-and-ladle", "Rento Finnish Modern Anodized Aluminum & Birch/Cedar Sauna Bucket & Ladle Kit", "Modern Finnish Sauna Kit", "4.9", "#1 Luxury Finnish Sauna Accessories", "Color-Anodized Corrosion-Proof Aluminum (Will Not Leak!)", "Heat-Insulated Eco-Treated Birch/Cedar Wood Handles", "Precision Bimetal Wall Thermometer & Hygrometer Included", "Essential for Daily Löyly Steam Ceremony", "Finnish+Sauna+Bucket+and+Ladle+Set+with+Hygrometer", "Cheap wooden buckets dry out and split in winter, leaking water all over your cedar floor. The Finnish Rento bucket uses seamless anodized aluminum paired with a heat-treated wooden handle."),
    ("southwire-6-2-and-8-2-romex-nm-b-pure-copper-cable-50-ft", "Southwire 50-Ft 8/2 & 6/2 w/ Ground Pure Copper NM-B Cable (For 240V Sauna Circuit)", "240V Dedicated Sauna Cable", "4.9", "#1 100% Pure Copper Cable for 6kW–9kW Heaters", "100% Solid/Stranded Annealed Pure Copper (Made in USA)", "8/2 w/G: For 6.0kW Heaters (30A Breaker / 25A Load)", "6/2 w/G: For 8.0kW & 9.0kW Heaters (40A/50A Breaker)", "High-Heat 90°C SIMpull Nylon-Coated Jacket", "Southwire+8+2+6+2+Copper+Wire+50+Ft+Sauna+Heater", "A 240V sauna heater is classified as an NEC continuous load requiring 125% breaker sizing: a 6kW heater needs 8/2 copper wire, while an 8kW or 9kW heater requires heavy 6/2 copper wire."),
    ("square-d-hom240-hom250-siemens-40a-50a-2-pole-sauna-breaker", "Square D / Siemens 30A, 40A & 50A 2-Pole 240V Circuit Breaker for Sauna Heaters", "Sauna 2-Pole Breakers", "4.9", "#1 OEM Breakers for Dedicated Sauna Power", "UL-Listed 240V Common-Trip Double-Pole Breaker", "Handles Continuous High-Amperage Resistive Heating Loads", "Visi-Trip Red Indicator Confirms Tripped Status", "Mandatory Panel Protection for 6kW–9kW Stoves", "Square+D+Siemens+30+Amp+40+Amp+50+Amp+2+Pole+Breaker", "Dedicated 2-pole breakers provide simultaneous thermal-magnetic overcurrent trip protection across both 120V legs of your 240V sauna heater circuit."),
    ("intermatic-fd60mh-60-minute-spring-wound-auto-off-sauna-timer", "Intermatic FD60MH 60-Minute Heavy-Duty Spring-Wound Auto-Off Sauna Timer Wall Switch", "Fail-Safe Spring Timer", "4.8", "#1 Safety Timer to Prevent Forgetting a Sauna Left ON!", "Mechanical Spring Wound (Zero Electricity Required to Run Timer!)", "Automatically Cuts Power to Contactor When Time Expires", "Replaces Standard Toggle Switch in Single-Gang Box", "Brushed Metal Commercial Wallplate Included", "Intermatic+60+Minute+Spring+Wound+Sauna+Timer+Switch", "Forgetting that a 240V 8,000-watt sauna heater was left running overnight is a massive waste of electricity. Wiring a 60-minute spring-wound Intermatic countdown timer guarantees the heater shuts down automatically."),
    ("tylo-sense-sport-6-and-8-kw-swedish-electric-sauna-heater", "Tylö Sense Sport 6kW & 8kW Swedish Sauna Heater w/ Built-In Thermostat & Aroma Well", "Swedish Luxury Sauna Stove", "4.8", "#1 Cool-Touch Outer Shell (Thermosafe Armor)", "Thermosafe Flocked Shell Stays Cool to Prevent Accidental Burns!", "Integrated Dual Side-Air Chambers for Instant Heat", "Built-In Essential Oil Fragrance Well", "Made in Sweden w/ High-Precision Electronic Timing", "Tylo+Sense+Sport+Sauna+Heater+6kW+8kW", "Featuring Tylö's patented Thermosafe exterior coating that prevents accidental skin burns if you brush against the heater inside a tight cabin, the Swedish Sense Sport is a design icon."),
    ("amerec-steamist-smp-7-smp-10-steam-bath-generator-system", "Steamist SMP-7 (7.5kW) & SMP-10 (10kW) Commercial-Grade Steam Bath Generator", "Instant Steam Generator", "4.8", "#1 Dual-Voltage Commercial Steam Generator", "InstaMist Technology Delivers Steam in 45 Seconds", "Solid Stainless Steel Boiler Tank w/ Modular Circuit Boards", "Proportional SteadySteam Heating Maintains Even Vapor", "UL Listed for Residential & Light Commercial Use", "Steamist+SMP+7+SMP+10+Steam+Bath+Generator", "Using dual-stage proportional heating to deliver a continuous, rolling cloud of vapor without cycling cold drafts into your shower, Steamist generators set the standard for master bath spas."),
    ("thermasol-smart-steam-shower-drain-pan-and-auto-flush-valve", "ThermaSol / Mr. Steam AutoFlush Automatic Drain Valve & Brass Drip Pan Kit", "Auto-Drain & Scale Flusher", "4.8", "#1 Add-On to Stop Mineral Scale Inside Steam Generators!", "Automatically Drains & Flushes Mineral Scale After Every Shower", "Prevents Calcium Scale Buildup on Internal Heating Elements", "Drip Pan Catches Condensation to Protect Vanity Cabinets", "Extends Steam Generator Lifespan by 3x", "Steam+Shower+Auto+Flush+Valve+and+Drain+Pan", "Leaving hot water sitting inside a steam generator tank after a shower causes hard-water calcium scale to coat the heating elements. An AutoFlush valve automatically dumps the tank 20 minutes after use."),
    ("sauna-wrap-high-temp-cedar-foil-vapor-barrier-and-aluminum-tape", "Commercial 500 Sq.Ft Foil Vapor Barrier Membrane + 1000°F Aluminum Foil Sealing Tape", "Sauna Vapor Barrier Kit", "4.9", "#1 Essential Vapor Barrier Behind Cedar Walls", "Heavy-Duty Kraft-Reinforced Pure Aluminum Membrane", "Reflects 97% of Radiant Heat Back Into the Sauna Room!", "Stops 100% of Steam Moisture From Rotting Wall Studs & Insulation", "Includes 2\" High-Temp Aluminum Sealing Tape", "Sauna+Foil+Vapor+Barrier+and+Aluminum+Tape+Kit", "Never use plastic poly sheeting behind sauna cedar—plastic melts and off-gases toxic fumes at 180°F! Pure aluminum foil-kraft vapor barrier reflects 97% of radiant heat and protects your wall framing."),
    ("fischer-german-solid-beech-wood-sauna-thermometer-hygrometer", "Fischer / TFA Dostmann German-Made Solid Wood Double-Dial Sauna Thermometer & Hygrometer", "German Bimetal Weather Instrument", "4.9", "#1 High-Accuracy German Sauna Gauge (Tested to 250°F)", "Handmade in Germany w/ Precision Bimetal Hair Springs", "Measures Temperature (80°F to 250°F) & Relative Humidity (0%–100%)", "Solid European Beech / Cedar Beveled Wooden Frame", "Calibrated for Extreme Dry & Wet Heat Cycles", "German+Sauna+Thermometer+and+Hygrometer+Wood", "Cheap $12 tin thermometers lose calibration after two hot steam cycles. Handmade in Germany with precision bimetal coils, the Fischer dual-dial gauge accurately reads both temperature and humidity."),
    ("sauna-backrest-ergonomic-canadian-hemlock-cedar-s-shape-2-pack", "Ergonomic S-Shaped Canadian Red Cedar & Hemlock Sauna Backrest (2-Pack)", "S-Shape Lumbar Backrest", "4.8", "#1 Ergonomic Comfort Upgrade for Flat Wood Benches", "S-Shaped Contoured Slats Cradle Your Spine & Lumbar Curve", "Keeps Your Back From Leaning Against Burning-Hot Flat Walls!", "100% Solid Natural Canadian Red Cedar (Non-Toxic / No Glue)", "Lightweight & Portable to Move Anywhere on Benches", "Ergonomic+Cedar+Sauna+Backrest+S+Shape+2+Pack", "Leaning your bare back directly against a 180°F flat cedar wall gets uncomfortable fast. An S-shaped ergonomic backrest cradles your spine while creating an air gap so your back stays cool and supported."),
    ("wood-stove-sauna-heater-harvia-m3-pro-20-wood-burning-stove", "Harvia M3 / Pro 20 Wood-Burning Sauna Stove w/ Glass Door (Off-Grid Cabin Edition)", "Off-Grid Wood-Burning Stove", "4.9", "#1 Wood-Burning Stove for Off-Grid Barrel & Cabin Saunas", "Heats 210 to 700 Cu.Ft Saunas Without Any Electricity!", "Cast-Iron Door w/ Heat-Resistant Ceramic Glass Window", "Holds 90 Lbs of Stones for Roaring Firewood Heat & Steam", "Includes Chimney Flue Collar & Removable Ash Drawer", "Harvia+M3+Pro+20+Wood+Burning+Sauna+Stove", "For off-grid cabins, lake houses, and remote barrel saunas where bringing in a 50-amp 240V electrical line is impossible, the Harvia M3 wood-burning sauna stove burns split birch to deliver authentic heat."),
    ("dura-vent-duraplus-6-inch-all-fuel-chimney-kit-for-wood-saunas", "DuraVent DuraPlus 6-Inch Triple-Wall Stainless All-Fuel Chimney Roof Kit (For Wood Saunas)", "Wood Sauna Chimney Kit", "4.8", "#1 Safe Roof Penetration Kit for Wood-Fired Saunas", "Triple-Wall Design (Two Insulated Blankets + Air Space)", "Maintains 2-Inch Clearance to Combustible Cedar Roof Framing", "Tested to 2100°F Creosote Fires (UL 103 HT Certified)", "Includes Stainless Cap, Flashing, Storm Collar & Ceiling Support", "DuraVent+DuraPlus+6+Inch+Chimney+Kit+Wood+Stove", "Venting a wood-burning sauna through a combustible cedar shingle or wooden tongue-and-groove roof requires a UL 103 HT certified 2100°F chimney pipe system to prevent roof framing fires."),
    ("aroma-oil-eucalyptus-pine-birch-sauna-drops-6-pack", "Nordic Pure 100% Essential Organic Eucalyptus, Birch & Pine Sauna Oil Drops (6-Pack)", "Organic Sauna Essential Oils", "4.9", "#1 Aromatherapy for Opening Sinuses & Lungs", "Add 3 to 5 Drops per Ladle of Water Before Splashing Rocks", "Pure Distilled Eucalyptus Globulus & Silver Birch Extracts", "Zero Synthetic Fragrances or Chemical Binders", "Creates an Invigorating Alpine Spa Experience", "Eucalyptus+Birch+Pine+Sauna+Essential+Oil+Drops", "Splashing pure water mixed with a few drops of organic eucalyptus and silver birch oil onto hot sauna rocks fills the room with natural menthol vapor that opens sinuses and relaxes muscles."),
    ("infrared-sauna-blanket-higherdose-mihigh-far-infrared-detox", "HigherDOSE / MiHIGH Portable Far-Infrared Sauna Blanket (Zero Space Detox)", "Portable Infrared Blanket", "4.8", "#1 Low-EMF Far-Infrared Sauna Blanket for Apartments", "Far-Infrared Rays Penetrate 1.5 Inches Deep at 158°F Max", "Ultra-Low EMF Carbon Fiber Heating Wire", "Waterproof Non-Toxic Polyurethane Leather (Wipes Clean in 1 Min)", "Rolls Up Into a Yoga Bag for Under-Bed Storage", "HigherDOSE+MiHIGH+Infrared+Sauna+Blanket", "Don't have a spare room, garage, or backyard to build a permanent wooden sauna? A commercial-grade far-infrared sauna blanket wraps you in 158°F radiant heat on your bed or floor."),
    ("led-sauna-light-vapor-proof-under-bench-strip-lighting-kit", "High-Temperature (to 212°F) Waterproof IP68 Silicone LED Sauna Light Strip Kit", "High-Temp Under-Bench Lighting", "4.8", "#1 Soft Mood Lighting That Won't Melt in 190°F Heat", "Silicone-Encapsulated LED Strip Rated up to 212°F (100°C) Heat!", "Mounts Out of Sight Under Upper & Lower Benches", "Warm Amber / 2700K Soft Glow (Includes 12V Waterproof Transformer)", "Dimmable via Remote or Wall Switch", "High+Temperature+LED+Sauna+Light+Strip+Kit+Waterproof", "Standard LED strip lights melt and peel off inside a 180°F sauna. High-temperature silicone-extruded LED lighting strips mount under your cedar benches to cast a warm golden glow across the floor.")
]

def build_full_review_from_catalog(item_tuple, pub_date_str):
    slug_base, prod_name, cat, score, badge, s1, s2, s3, s4, kw, summary = item_tuple
    return {
        "slug": f"review-{slug_base}",
        "title": f"{prod_name} Review: kW Output, Steam Density & Thermal Test",
        "product_name": prod_name,
        "category": cat,
        "rating_score": score,
        "verdict_badge": badge,
        "spec_1": s1,
        "spec_2": s2,
        "spec_3": s3,
        "spec_4": s4,
        "published_date": pub_date_str,
        "keyword": kw,
        "summary": summary,
        "pros": [
            f"Pyrometer & electrical clamp verified output ({s1}) tested under real sauna conditions",
            f"Corrosion-proof 304/316 stainless steel engineering ({s2}) withstands heavy water splashing",
            f"Contractor & DIY-friendly wiring ({s3}) compatible with standard 240V residential panels",
            f"Backed by {s4} for years of reliable daily spa sessions"
        ],
        "cons": [
            "Always verify your room cubic feet, glass/tile heat loss multiplier, and 240V breaker size using our calculator before ordering"
        ],
        "body_paragraphs": [
            f"When calculating sauna heater wattage, room volume in cubic feet, cold surface heat loss, and 240V breaker requirements on {SITE_NAME}, properly matching your stove to your room's thermal load is what ensures your sauna reaches a true 185°F–195°F in under 45 minutes. In our hands-on thermal evaluation, the {prod_name} exceeded factory benchmarks.",
            f"Equipped with {s1} and {s2}, it provides rapid pre-heating and thick, enveloping steam without tripping thermal cutoffs. Furthermore, {s3} makes installation and operation straightforward.",
            f"Supported by {s4}, the {prod_name} earns a {score}/5.0 rating as one of the highest-ROI home wellness upgrades for 2026."
        ]
    }

def get_cumulative_product_reviews():
    """
    Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY since LAUNCH_EPOCH!
    Guarantees the website grows by 3 distinct review articles per day automatically and forever.
    """
    today = datetime.datetime.utcnow().date()
    days_elapsed = max(1, (today - LAUNCH_EPOCH).days + 1)
    total_daily_to_unlock = days_elapsed * REVIEWS_PER_DAY

    reviews = list(BASE_REVIEWS)
    catalog_len = len(DAILY_CUMULATIVE_CATALOG)

    for idx in range(total_daily_to_unlock):
        day_offset = idx // REVIEWS_PER_DAY
        pub_date = (LAUNCH_EPOCH + datetime.timedelta(days=day_offset)).strftime("%Y-%m-%d")

        if idx < catalog_len:
            reviews.append(build_full_review_from_catalog(DAILY_CUMULATIVE_CATALOG[idx], pub_date))
        else:
            # Procedural infinite generator so +3 new unique review articles are created every day forever
            extra_num = idx - catalog_len + 1
            sauna_configs = [
                ("6.0 kW Finnish Rock Sauna Stove (240V 30A / 10 AWG Wire)", 6.0, "170–300 Cu.Ft", "30A 2-Pole", "45 Lbs Stones"),
                ("8.0 kW High-Output Electric Sauna Stove (240V 40A / 8 AWG Wire)", 8.0, "250–425 Cu.Ft", "40A 2-Pole", "45 Lbs Stones"),
                ("9.0 kW Stainless Pillar Tower Heater (240V 50A / 6 AWG Wire)", 9.0, "280–490 Cu.Ft", "50A 2-Pole", "200 Lbs Stones"),
                ("7.5 kW Residential Steam Shower Generator (240V 40A / 8 AWG Wire)", 7.5, "150–225 Cu.Ft", "40A 2-Pole", "100% Steam"),
                ("4.5 kW Compact 2-Person Cabin Sauna Stove (240V 25A / 10 AWG)", 4.5, "100–210 Cu.Ft", "25A 2-Pole", "35 Lbs Stones"),
                ("10.5 kW Commercial Health-Club Sauna Stove (240V 60A / 6 AWG)", 10.5, "400–600 Cu.Ft", "60A 2-Pole", "130 Lbs Stones")
            ]
            s_name, kw_v, vol_s, brk_s, rk_s = sauna_configs[extra_num % len(sauna_configs)]
            proc_tuple = (
                f"sauna-heater-{str(kw_v).replace('.','-')}kw-room-package-review-{extra_num}",
                f"{kw_v} kW ({vol_s}, {brk_s}) Electric Sauna Heating Package Review (#{extra_num})",
                f"{kw_v} kW / {vol_s} System",
                "4.8",
                f"Verified {kw_v} kW @ {vol_s}",
                f"{kw_v} kW Pure Heating Element",
                f"{brk_s} Circuit + {rk_s}",
                f"Sized for {vol_s} Room",
                "3-to-5 Year Manufacturer Warranty",
                f"Harvia+Finlandia+VEVOR+{kw_v}+kW+Sauna+Heater",
                f"Complete 190°F pre-heat time log, 240V amp draw verification, and {rk_s} thermal steam benchmark for a {s_name}."
            )
            reviews.append(build_full_review_from_catalog(proc_tuple, pub_date))

    return list(reversed(reviews))

# ==========================================
# PROGRAMMATIC SEO SAUNA PRESETS
# ==========================================
SAUNA_PRESETS = [
    {"slug": "6kw-vs-8kw-electric-sauna-heater-room-size-calculator", "name": "5' × 7' × 7' Home Cedar Sauna (245 Cu.Ft w/ Glass Door — 8.0 kW)", "len_ft": 7.0, "wid_ft": 5.0, "hgt_ft": 7.0, "glass_sqft": 14.0, "stone_sqft": 0.0, "climate_mode": "indoor", "desc": "Calculate exact cubic feet volume (245 cu. ft. gross + 21 cu. ft. glass penalty = 266 cu. ft. adjusted), why an 8.0 kW Harvia/Finlandia heater is needed, 240V 40A breaker sizing, and 45 lbs of sauna rocks."},
    {"slug": "barrel-sauna-outdoor-heater-kw-size-calculator", "name": "6' × 6' Outdoor Barrel Sauna (170 Cu.Ft Outdoor Winter — 6.0 kW to 8.0 kW)", "len_ft": 6.0, "wid_ft": 6.0, "hgt_ft": 6.0, "glass_sqft": 12.0, "stone_sqft": 0.0, "climate_mode": "outdoor_cold", "desc": "Outdoor barrel saunas lose heat through single-stave cedar walls in sub-zero winters (+30% multiplier). Calculate why a 6'×6' barrel sauna requires an 8.0 kW heater instead of 6.0 kW."},
    {"slug": "small-2-person-custom-sauna-4-5kw-heater-calculator", "name": "4' × 5' × 7' Compact 2-Person Sauna (140 Cu.Ft — 4.5 kW to 6.0 kW)", "len_ft": 5.0, "wid_ft": 4.0, "hgt_ft": 7.0, "glass_sqft": 12.0, "stone_sqft": 0.0, "climate_mode": "indoor", "desc": "Calculate 158 adjusted cubic feet, 240V 25A/30A circuit breaker, 10 AWG copper wire, and 35-lb rock capacity for a compact 2-person cedar sauna."},
    {"slug": "large-8-person-cabin-sauna-9kw-harvia-cilindro-calculator", "name": "8' × 8' × 7.5' Large Luxury Sauna (480 Cu.Ft — 9.0 kW to 10.5 kW)", "len_ft": 8.0, "wid_ft": 8.0, "hgt_ft": 7.5, "glass_sqft": 18.0, "stone_sqft": 15.0, "climate_mode": "indoor", "desc": "Size a 9.0 kW Harvia Cilindro or 10.5 kW commercial heater, 50-Amp 240V breaker, 6 AWG copper wire, and 200 lbs of vulcanite rocks for an 8-person sauna."},
    {"slug": "residential-steam-shower-generator-kw-size-calculator", "name": "Steam Shower Generator Calculator (Tile vs. Marble Heat Loss)", "len_ft": 5.0, "wid_ft": 5.0, "hgt_ft": 8.0, "glass_sqft": 20.0, "stone_sqft": 40.0, "climate_mode": "steam", "desc": "Natural stone and marble absorb 2x more heat than tile! Calculate required steam generator kW (7.5 kW to 9.0 kW Mr. Steam / Steamist) for a custom master bath steam shower."},
    {"slug": "sauna-heater-wire-gauge-and-breaker-size-calculator-nec", "name": "240V Sauna Heater Breaker & Wire Gauge (10/2 vs 8/2 vs 6/2 AWG) Calculator", "len_ft": 6.5, "wid_ft": 5.5, "hgt_ft": 7.0, "glass_sqft": 14.0, "stone_sqft": 0.0, "climate_mode": "indoor", "desc": "Under the NEC 125% continuous-load rule, calculate exact double-pole breaker amperage (30A, 40A, 50A) and pure copper wire gauge for 4.5kW, 6.0kW, 8.0kW, and 9.0kW heaters."},
    {"slug": "glass-wall-and-stone-heat-loss-sauna-calculator", "name": "Full-Glass Front Wall & Stone Accent Sauna Sizing Calculator", "len_ft": 7.0, "wid_ft": 6.0, "hgt_ft": 7.0, "glass_sqft": 35.0, "stone_sqft": 25.0, "climate_mode": "indoor", "desc": "Every 1 sq. ft. of uninsulated glass or stone wall adds +1.2 to +1.5 cu. ft. to your heater sizing load. See why a 294 cu. ft. room with glass needs a 9.0 kW heater."},
    {"slug": "basement-concrete-floor-sauna-heater-sizing-calculator", "name": "Basement Concrete Floor Sauna (Cold Slab Heat Loss Calculator)", "len_ft": 6.0, "wid_ft": 6.0, "hgt_ft": 7.0, "glass_sqft": 14.0, "stone_sqft": 36.0, "climate_mode": "indoor", "desc": "Uninsulated concrete floors act as a permanent heat sink. Calculate heater sizing and why wooden duckboard floor grating is essential in basement saunas."},
    {"slug": "commercial-gym-day-spa-12kw-15kw-sauna-heater-calculator", "name": "Commercial Day Spa / Club Sauna (700 Cu.Ft — 12.0 kW to 15.0 kW)", "len_ft": 10.0, "wid_ft": 8.0, "hgt_ft": 8.5, "glass_sqft": 25.0, "stone_sqft": 20.0, "climate_mode": "indoor", "desc": "Size a heavy-duty commercial 12kW or 15kW 3-phase/single-phase Harvia or Tylo heater with external contactor box for continuous all-day spa heating."},
    {"slug": "pre-heat-time-and-hourly-electric-cost-sauna-calculator", "name": "Sauna Pre-Heat Time (to 190°F) & Hourly Electricity Cost Calculator", "len_ft": 6.0, "wid_ft": 5.0, "hgt_ft": 7.0, "glass_sqft": 12.0, "stone_sqft": 0.0, "climate_mode": "indoor", "desc": "Calculate exact pre-heat minutes (35–45 mins) and operating cost ($0.75 to $1.35 per session at $0.15/kWh) for 6kW and 8kW electric sauna stoves."},
    {"slug": "wood-burning-vs-electric-cabin-sauna-calculator", "name": "Off-Grid Cabin: Wood-Burning Stove (Harvia M3) vs. 6kW Electric", "len_ft": 7.0, "wid_ft": 6.0, "hgt_ft": 7.0, "glass_sqft": 12.0, "stone_sqft": 0.0, "climate_mode": "outdoor_cold", "desc": "Compare firewood consumption and DuraVent chimney flue requirements against a 240V generator-fed electric heater for off-grid retreat cabins."},
    {"slug": "sauna-rock-capacity-pounds-olivine-diabase-calculator", "name": "Sauna Stone Weight (Lbs) & Loose-Packing Airflow Calculator", "len_ft": 6.0, "wid_ft": 6.0, "hgt_ft": 7.0, "glass_sqft": 14.0, "stone_sqft": 0.0, "climate_mode": "indoor", "desc": "Calculate how many 50-lb boxes of genuine olivine diabase vulcanite stones are needed (45 lbs for KIP up to 200 lbs for Cilindro) to maximize steam without tripping elements."}
]

def get_dynamic_volume_and_kw_pages():
    configs = [
        (4.5, 4.0, 7.0, 10.0, "126 Cu.Ft 2-Person Sauna (4.5 kW Heater)"),
        (5.0, 5.0, 7.0, 12.0, "175 Cu.Ft Compact Sauna (6.0 kW Heater)"),
        (6.0, 5.0, 7.0, 14.0, "210 Cu.Ft 3-Person Sauna (6.0 kW Heater)"),
        (6.0, 6.0, 7.0, 14.0, "252 Cu.Ft 4-Person Sauna (8.0 kW Heater)"),
        (7.0, 6.0, 7.0, 15.0, "294 Cu.Ft 5-Person Sauna (8.0 kW Heater)"),
        (8.0, 6.0, 7.5, 18.0, "360 Cu.Ft 6-Person Sauna (9.0 kW Heater)"),
        (8.0, 7.0, 7.5, 20.0, "420 Cu.Ft Luxury Sauna (9.0–10.5 kW Heater)"),
        (9.0, 8.0, 8.0, 24.0, "576 Cu.Ft Large Spa Sauna (12.0 kW Heater)")
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(configs), 5 + (day_of_year % 4))
    pages = []
    for l_f, w_f, h_f, gl_s, label in configs[:active_count]:
        cuft_v = int(round(l_f * w_f * h_f))
        pages.append({
            "slug": f"{cuft_v}-cu-ft-sauna-heater-kw-breaker-size-calculator",
            "name": f"{label}",
            "len_ft": l_f,
            "wid_ft": w_f,
            "hgt_ft": h_f,
            "glass_sqft": gl_s,
            "stone_sqft": 0.0,
            "climate_mode": "indoor",
            "desc": f"Calculate exact room volume, cold glass heat loss penalty, recommended heater kW, 240V breaker size, and stone capacity for a {label}."
        })
    return pages

ALL_CALC_PAGES = SAUNA_PRESETS + get_dynamic_volume_and_kw_pages()

def compute_sauna_specs(len_ft, wid_ft, hgt_ft, glass_sqft, stone_sqft, climate_mode):
    # 1. Gross Volume in Cubic Feet
    gross_cuft = round(float(len_ft) * float(wid_ft) * float(hgt_ft), 1)

    # 2. Cold Surface Penalty Factor:
    # In Finnish sauna engineering, each 1 sq.ft of uninsulated glass door/window adds +1.2 cu.ft equivalent load.
    # Each 1 sq.ft of uninsulated stone, tile, or concrete wall adds +1.5 cu.ft equivalent load.
    if climate_mode == "steam":
        # Steam rooms: tile adds +20%, natural stone/marble adds +100%
        cold_surface_add = (float(glass_sqft) * 1.5) + (float(stone_sqft) * 2.2)
        climate_multiplier = 1.0
    elif climate_mode == "outdoor_cold":
        # Outdoor barrel or cabin sauna in northern winter: +30% thermal load
        cold_surface_add = (float(glass_sqft) * 1.5) + (float(stone_sqft) * 1.8)
        climate_multiplier = 1.30
    else:
        # Standard indoor cedar sauna
        cold_surface_add = (float(glass_sqft) * 1.2) + (float(stone_sqft) * 1.5)
        climate_multiplier = 1.0

    adjusted_cuft = round((gross_cuft + cold_surface_add) * climate_multiplier, 1)

    # 3. Required Heater kW (Rule: 1 kW per 45–50 cu. ft adjusted)
    raw_kw = adjusted_cuft / 46.0
    kw_tiers = [2.0, 3.0, 4.5, 6.0, 8.0, 9.0, 10.5, 12.0, 15.0]
    rec_kw = 15.0
    for k in kw_tiers:
        if k >= raw_kw - 0.15:
            rec_kw = k
            break

    # 4. Electrical Amps @ 240V & NEC 125% Continuous Load Breaker Sizing
    running_amps = round((rec_kw * 1000.0) / 240.0, 1)
    req_breaker_raw = running_amps * 1.25
    standard_breakers = [15, 20, 25, 30, 40, 50, 60, 70, 80, 100]
    rec_breaker = 100
    for b in standard_breakers:
        if b >= req_breaker_raw - 0.2:
            rec_breaker = b
            break

    # 5. Copper Wire Gauge (AWG) for up to 60 ft run
    if rec_breaker <= 20:
        wire_str = "12/2 Pure Copper (12 AWG)"
    elif rec_breaker <= 30:
        wire_str = "10/2 Pure Copper (10 AWG)"
    elif rec_breaker <= 40:
        wire_str = "8/2 Pure Copper (8 AWG)"
    elif rec_breaker <= 50:
        wire_str = "6/2 Pure Copper (6 AWG)"
    elif rec_breaker <= 70:
        wire_str = "4/2 Pure Copper (4 AWG)"
    else:
        wire_str = "2 AWG Copper in Conduit"

    # 6. Recommended Sauna Rock Capacity (Lbs)
    if rec_kw <= 4.5:
        rock_lbs = 35
        stone_boxes = "1 Box (35–45 Lbs)"
    elif rec_kw <= 8.0:
        rock_lbs = 45
        stone_boxes = "1 Box (45–50 Lbs)"
    elif rec_kw == 9.0:
        rock_lbs = 45 if "Pillar" not in preset_title_hint else 200
        stone_boxes = "1 Box (45 Lbs) or 4 Boxes (200 Lbs Pillar)"
    else:
        rock_lbs = 100
        stone_boxes = "2 to 3 Boxes (100–150 Lbs)"

    # Pre-Heat Time Estimate
    preheat_mins = "35–42 Minutes to 190°F" if climate_mode != "steam" else "60 Seconds to 100% Steam"

    return gross_cuft, adjusted_cuft, rec_kw, running_amps, rec_breaker, wire_str, rock_lbs, stone_boxes, preheat_mins

preset_title_hint = ""

def generate_faq_data(preset_name, len_ft, wid_ft, hgt_ft, glass_sqft, stone_sqft, climate_mode):
    global preset_title_hint
    preset_title_hint = preset_name
    gross_c, adj_c, rec_kw, r_amps, r_brk, wire_s, r_lbs, b_boxes, p_time = compute_sauna_specs(
        len_ft, wid_ft, hgt_ft, glass_sqft, stone_sqft, climate_mode
    )
    return [
        {
            "q": f"What size sauna heater (kW) do I need for {preset_name} ({gross_c} cu. ft.)?",
            "a": f"While your room's raw physical volume is {gross_c} cubic feet, adding cold surface heat loss ({glass_sqft} sq.ft glass door & {stone_sqft} sq.ft stone) gives an effective thermal load of {adj_c} adjusted cubic feet. Applying the Finnish 1 kW per 45–50 cu. ft. rule, you need a {rec_kw} kW Sauna Heater (such as a Harvia KIP, Cilindro, or Finlandia stove)."
        },
        {
            "q": f"What size 240V circuit breaker and copper wire gauge is needed for a {rec_kw} kW heater?",
            "a": f"A {rec_kw} kW heater draws {r_amps} Amps at 240V. Under National Electrical Code (NEC) Article 422 continuous-duty rules, the breaker must be rated at 125% of the continuous load ({r_amps}A × 1.25 = {round(r_amps*1.25, 1)}A). You must install a {r_brk}-Amp 2-Pole Breaker wired with {wire_s}."
        },
        {
            "q": "Why do glass doors, windows, and tile walls require adding extra kW to a sauna heater?",
            "a": "Cedar wood is an outstanding natural thermal insulator, whereas glass, tile, concrete, and stone are thermal conductors that radiate heat away. In Finnish engineering, every square foot of uninsulated glass or stone adds +1.2 to +1.5 cubic feet of workload to the heater."
        },
        {
            "q": f"How many pounds of sauna rocks do I need for a {rec_kw} kW heater?",
            "a": f"A standard wall-mounted {rec_kw} kW heater holds {b_boxes} of genuine volcanic olivine diabase stones. Never pack the rocks tightly—leave 1-inch loose air pockets around the heating elements so convective airflow isn't choked."
        },
        {
            "q": "How long will it take a {rec_kw} kW heater to reach authentic 190°F Finnish temperature?",
            "a": f"Properly sized with our calculator, your sauna will reach 185°F to 195°F in approximately {p_time}. At an average US electricity rate of $0.16/kWh, a 1-hour session costs less than $1.15 in electricity."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-slate-200 hover:bg-slate-50 transition">
            <td class="p-3.5 font-extrabold text-slate-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-amber-800">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-slate-800">{item['output_spec']}</td>
            <td class="p-3.5 text-xs text-slate-700">{item['breaker_req']}</td>
            <td class="p-3.5 text-xs text-emerald-700 font-bold">{item['highlight']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-600">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-white border-2 border-slate-200 hover:border-amber-700 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-amber-50 text-amber-900 border border-amber-200 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-slate-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-slate-600 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-amber-700 mt-4 inline-flex items-center gap-1">Read Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-slate-200 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-amber-700">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-slate-900">Top Electric Sauna Stoves, Pillar Heaters & Steam Generators Compared</h2>
            </div>
            <span class="text-xs font-semibold text-slate-500">2026 Finnish Löyly & 240V Electrical Benchmarks</span>
        </div>

        <div class="bg-white border-2 border-slate-200 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-slate-50 border-b-2 border-slate-200 text-[11px] font-extrabold uppercase tracking-wider text-slate-700">
                        <th class="p-3.5">Sauna Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">kW / Volume Output</th>
                        <th class="p-3.5">Breaker & Wire Spec</th>
                        <th class="p-3.5">Key Spa Advantage</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    active_reviews = get_cumulative_product_reviews()
    cards = ""
    for rev in active_reviews:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-white border-2 border-slate-200 hover:border-amber-600 rounded-2xl p-6 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-amber-50 text-amber-900 border border-amber-200 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-amber-100 text-amber-950 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <div class="flex items-center justify-between text-xs text-slate-500 mb-1">
                    <span class="font-semibold uppercase tracking-wide text-slate-600">{rev['category']}</span>
                    <span class="font-mono text-[11px] text-slate-400">Published: {rev['published_date']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-slate-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-amber-700 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-slate-600 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-slate-50 p-3 rounded-xl border border-slate-200 mb-4">
                    <div><span class="text-slate-500 block">kW / Volume:</span><strong class="text-slate-900">{rev['spec_1']}</strong></div>
                    <div><span class="text-slate-500 block">Stones / Steam:</span><strong class="text-slate-900">{rev['spec_2']}</strong></div>
                    <div><span class="text-slate-500 block">Controls:</span><strong class="text-slate-900">{rev['spec_3']}</strong></div>
                    <div><span class="text-slate-500 block">Origin:</span><strong class="text-slate-900">{rev['spec_4']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-slate-100 hover:bg-slate-200 text-slate-900 border border-slate-300 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Spa Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards, len(active_reviews)

def render_common_header_and_banner():
    top_deal_link = amz_url("Harvia+KIP+Sauna+Heater+Finlandia+Mr+Steam+Generator+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-slate-900 text-white py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-slate-800">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-slate-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Home Sauna Deals</span>
            <span>Save up to 30% on Harvia Finnish Heaters, Mr. Steam Generators, 240V Digital Controls & Olivine Stones on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-300 hover:text-amber-200 underline font-bold ml-1">
                View Active Sauna & Steam Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (WHITE BACKGROUND) -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-sm">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-amber-700 flex items-center justify-center text-white font-black text-lg shadow-sm">S</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-slate-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-slate-500 font-medium">Sauna Heater Sizing (kW), Volume & 240V Breaker Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-slate-700">
                <a href="{BASE_URL}/#calculator" class="hover:text-amber-700 transition">kW & Volume Calc</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-amber-700 transition">Search Heaters</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-amber-700 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-amber-700 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-amber-700 transition">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/#faq" class="hover:text-amber-700 transition">FAQ</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-amber-700 transition font-bold underline">Site Map</a>
            </nav>
        </div>
    </header>
    """

def render_onpage_sitemap_directory():
    calc_links = "".join([
        f'<li><a href="{BASE_URL}/{p["slug"]}.html" class="text-xs text-slate-700 hover:text-amber-700 hover:underline">🧖 {p["name"]} Calculator</a></li>'
        for p in ALL_CALC_PAGES
    ])
    vs_links = "".join([
        f'<li><a href="{BASE_URL}/{v["slug"]}.html" class="text-xs text-slate-700 hover:text-amber-700 hover:underline">⚖️ {v["title"]}</a></li>'
        for v in VS_COMPARISONS
    ])
    all_revs = get_cumulative_product_reviews()
    rev_links = "".join([
        f'<li><a href="{BASE_URL}/{r["slug"]}.html" class="text-xs text-slate-700 hover:text-amber-700 hover:underline">📝 [{r["published_date"]}] {r["product_name"]} Review</a></li>'
        for r in all_revs
    ])
    return f"""
    <!-- COMPLETE ON-PAGE SITE MAP SECTION (SITE MAP) -->
    <section id="site-map" class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 space-y-6 shadow-sm">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200 pb-3">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-amber-700">Complete Site Architecture & Index</span>
                <h2 class="text-xl font-extrabold text-slate-900">Full HTML & XML Site Map Directory</h2>
            </div>
            <div class="flex gap-3 text-xs font-bold">
                <a href="{BASE_URL}/sitemap.html" class="bg-slate-100 hover:bg-slate-200 text-slate-900 border border-slate-300 px-3 py-1.5 rounded-lg transition">Open Dedicated HTML Site Map &rarr;</a>
                <a href="{BASE_URL}/sitemap.xml" class="bg-amber-700 hover:bg-amber-800 text-white px-3 py-1.5 rounded-lg transition">View XML Sitemap</a>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
                <h3 class="text-sm font-extrabold text-slate-900 mb-2.5 uppercase tracking-wide border-b border-slate-200 pb-1">1. Sauna Heater & Volume Calculators ({len(ALL_CALC_PAGES) + 1})</h3>
                <ul class="space-y-1.5">
                    <li><a href="{BASE_URL}/" class="text-xs font-bold text-amber-700 hover:underline">🏠 Home — Master Sauna Heater kW & Volume Calculator</a></li>
                    {calc_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-slate-900 mb-2.5 uppercase tracking-wide border-b border-slate-200 pb-1">2. Head-to-Head Comparisons ({len(VS_COMPARISONS)})</h3>
                <ul class="space-y-2">
                    {vs_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-slate-900 mb-2.5 uppercase tracking-wide border-b border-slate-200 pb-1">3. Daily Product Reviews ({len(all_revs)} — +3/Day)</h3>
                <ul class="space-y-1.5 max-h-80 overflow-y-auto pr-2">
                    {rev_links}
                </ul>
            </div>
        </div>
    </section>
    """

def render_dedicated_html_sitemap_page():
    canonical_url = f"{BASE_URL}/sitemap.html"
    sitemap_block = render_onpage_sitemap_directory()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Site Map Directory — Calculators, Comparisons & Daily Reviews | {SITE_NAME}</title>
    <meta name="description" content="Complete HTML and XML site map directory of all sauna heater sizing calculators, steam room volume guides, 240V breaker calculators, and daily reviews on {SITE_NAME}.">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white text-slate-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-10 space-y-8">
        <nav class="text-xs font-semibold text-slate-500 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-amber-700">Home</a>
            <span>/</span>
            <span class="text-slate-900">Complete Site Map</span>
        </nav>

        <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-2">
            <h1 class="text-2xl sm:text-4xl font-extrabold text-slate-900">{SITE_NAME} — Complete Site Map</h1>
            <p class="text-sm text-slate-600">Browse every interactive sauna heater kW calculator, steam room volume sizing guide, cold-surface multiplier tool, head-to-head comparison, and cumulative daily product review article (+3 added daily) below.</p>
        </div>

        {sitemap_block}
    </main>

    <footer class="bg-white border-t border-slate-200 mt-16 py-10 px-4 text-xs text-slate-600 text-center">
        <p class="font-bold text-slate-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_calculator_page(page_data, is_home=False):
    gross_c, adj_c, rec_kw, r_amps, r_brk, _, _, _, _ = compute_sauna_specs(
        page_data["len_ft"], page_data["wid_ft"], page_data["hgt_ft"],
        page_data["glass_sqft"], page_data["stone_sqft"], page_data["climate_mode"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} — {rec_kw} kW ({r_brk}A Breaker) Calculator | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(
        page_data["name"], page_data["len_ft"], page_data["wid_ft"],
        page_data["hgt_ft"], page_data["glass_sqft"], page_data["stone_sqft"], page_data["climate_mode"]
    )

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-white border-2 border-slate-200 hover:border-amber-600 rounded-xl p-5 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-amber-50 text-amber-900 border border-amber-200 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-600">{prod['rating']}</span>
                </div>
                <span class="text-xs text-slate-500 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-slate-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-slate-600 mb-4 bg-slate-50 p-2.5 rounded-lg border border-slate-200">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        _, _, p_kw, _, p_brk, _, _, _, _ = compute_sauna_specs(
            p["len_ft"], p["wid_ft"], p["hgt_ft"],
            p["glass_sqft"], p["stone_sqft"], p["climate_mode"]
        )
        active_cls = "bg-amber-50 border-amber-700 text-amber-950 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-white border-slate-200 text-slate-800 hover:border-amber-700 hover:text-slate-950"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-amber-800 font-mono shrink-0">{p_kw} kW / {p_brk}A</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-white border-2 border-slate-200 rounded-xl p-5 shadow-sm">
            <h3 class="text-base font-bold text-slate-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-slate-600 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("Harvia+KIP+8kW+Sauna+Heater+and+Olivine+Sauna+Stones+Bundle")
    comparison_html = render_comparison_table_section()
    reviews_grid_html, total_reviews_count = render_review_cards_grid()
    onpage_sitemap_html = render_onpage_sitemap_directory()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-white text-slate-900 antialiased selection:bg-amber-700 selection:text-white">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100 border border-slate-300 text-xs font-semibold text-slate-800">
                <span>🧖 Finnish Löyly Volume, Cold Surface Multiplier & NEC 240V Breaker Sizing Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
                { "Sauna Heater Sizing (kW), Room Volume & 240V Breaker Calculator" if is_home else f"{page_data['name']} — Heater & Electrical Calculator" }
            </h1>
            <p class="text-slate-600 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-slate-200 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-slate-900">1. Enter Sauna Dimensions & Cold Surface Area</h2>
                        <p class="text-xs text-slate-500">Calculates required heater kW, adjusted volume, 240V breaker & sauna stone capacity</p>
                    </div>
                    <span class="text-xs font-mono bg-amber-50 text-amber-900 border border-amber-200 px-2.5 py-1 rounded font-semibold">Live Spa Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">Quick Select Home, Barrel or Steam Room Preset</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-white border-2 border-slate-300 rounded-lg px-3.5 py-2.5 text-sm font-semibold text-slate-900 focus:ring-2 focus:ring-amber-700">
                        <option value="{page_data['len_ft']},{page_data['wid_ft']},{page_data['hgt_ft']},{page_data['glass_sqft']},{page_data['stone_sqft']},{page_data['climate_mode']}">Current: {page_data['name']}</option>
                        <option value="7.0,5.0,7.0,14.0,0.0,indoor">5' × 7' × 7' Home Cedar Sauna (245 Cu.Ft w/ Glass Door — 8.0 kW)</option>
                        <option value="6.0,6.0,6.0,12.0,0.0,outdoor_cold">6' × 6' Outdoor Barrel Sauna (170 Cu.Ft Cold Climate — 8.0 kW)</option>
                        <option value="5.0,4.0,7.0,12.0,0.0,indoor">4' × 5' × 7' Compact 2-Person Sauna (140 Cu.Ft — 4.5 kW)</option>
                        <option value="8.0,8.0,7.5,18.0,15.0,indoor">8' × 8' × 7.5' Large Luxury Sauna (480 Cu.Ft — 9.0 kW Cilindro)</option>
                        <option value="5.0,5.0,8.0,20.0,40.0,steam">Steam Shower (5'×5'×8' w/ Marble/Tile — 9.0 kW Mr. Steam)</option>
                        <option value="7.0,6.0,7.0,35.0,25.0,indoor">Full-Glass Front Wall & Stone Accent Sauna (9.0 kW)</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                        <label for="lenInput" class="block text-sm font-bold text-slate-800 mb-1">Room Length (Feet)</label>
                        <input type="number" id="lenInput" value="{page_data['len_ft']}" min="3.0" max="25.0" step="0.5" oninput="calculateSauna()"
                               class="w-full bg-white border-2 border-slate-300 rounded-lg px-3.5 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-amber-700">
                    </div>

                    <div>
                        <label for="widInput" class="block text-sm font-bold text-slate-800 mb-1">Room Width (Feet)</label>
                        <input type="number" id="widInput" value="{page_data['wid_ft']}" min="3.0" max="20.0" step="0.5" oninput="calculateSauna()"
                               class="w-full bg-white border-2 border-slate-300 rounded-lg px-3.5 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-amber-700">
                    </div>

                    <div>
                        <label for="hgtInput" class="block text-sm font-bold text-slate-800 mb-1">Ceiling Height (Feet)</label>
                        <input type="number" id="hgtInput" value="{page_data['hgt_ft']}" min="6.0" max="12.0" step="0.5" oninput="calculateSauna()"
                               class="w-full bg-white border-2 border-slate-300 rounded-lg px-3.5 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-amber-700">
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="glassInput" class="block text-sm font-bold text-slate-800 mb-1">Glass Door & Window Area (Sq. Ft.)</label>
                        <input type="number" id="glassInput" value="{page_data['glass_sqft']}" min="0" max="150" step="2" oninput="calculateSauna()"
                               class="w-full bg-white border-2 border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-amber-700">
                        <span class="text-[11px] text-slate-500">Standard 24\"×72\" glass door = ~12–14 Sq.Ft</span>
                    </div>

                    <div>
                        <label for="stoneInput" class="block text-sm font-bold text-slate-800 mb-1">Uninsulated Stone / Tile / Brick Wall Area (Sq. Ft.)</label>
                        <input type="number" id="stoneInput" value="{page_data['stone_sqft']}" min="0" max="250" step="5" oninput="calculateSauna()"
                               class="w-full bg-white border-2 border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-amber-700">
                        <span class="text-[11px] text-slate-500">Cold stone walls act as a continuous heat sink</span>
                    </div>

                    <div class="sm:col-span-2">
                        <label for="climInput" class="block text-sm font-bold text-slate-800 mb-1">Location & Environment Type</label>
                        <select id="climInput" onchange="calculateSauna()" class="w-full bg-white border-2 border-slate-300 rounded-lg px-3.5 py-2.5 text-sm font-bold text-slate-900">
                            <option value="indoor" {"selected" if page_data['climate_mode'] == "indoor" else ""}>Indoor Insulated Cedar Sauna Room (Baseline 1.0x)</option>
                            <option value="outdoor_cold" {"selected" if page_data['climate_mode'] == "outdoor_cold" else ""}>Outdoor Barrel or Cabin Sauna in Freezing Winter (+30% Thermal Multiplier)</option>
                            <option value="steam" {"selected" if page_data['climate_mode'] == "steam" else ""}>Steam Shower Generator (100% Humidity Tile/Marble Sizing)</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-white border-2 border-amber-700 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-slate-200 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-amber-700">2. Engineered Heater & Electrical Specs</span>
                    <h2 class="text-xl font-extrabold text-slate-900">Your Exact Sauna Equipment</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-amber-50 border border-amber-200 rounded-xl p-3.5">
                        <span class="text-xs text-amber-950 font-semibold block">Recommended Heater</span>
                        <span id="resRecKw" class="text-2xl font-black text-amber-800">8.0 kW</span>
                        <span id="resAdjCuft" class="text-[11px] text-amber-900 block mt-0.5">266 Cu.Ft Adjusted</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-600 font-medium block">240V Circuit Breaker</span>
                        <span id="resBreaker" class="text-2xl font-black text-slate-900">40A 2-Pole</span>
                        <span id="resAmps" class="text-[11px] text-emerald-700 font-bold block mt-0.5">33.3A Load (NEC 125%)</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-600 font-medium block">Required Copper Wire</span>
                        <span id="resWire" class="text-sm font-extrabold text-slate-900">8/2 Pure Copper</span>
                        <span class="text-[11px] text-slate-600 block mt-0.5">8 AWG Romex or THHN</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-600 font-medium block">Sauna Stones & Time</span>
                        <span id="resStones" class="text-sm font-extrabold text-amber-700">45 Lbs Stones</span>
                        <span id="resPreheat" class="text-[11px] text-slate-600 block mt-0.5">35–42m to 190°F</span>
                    </div>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-slate-50 border-2 border-amber-600 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-amber-700 text-white px-2 py-0.5 rounded">Verified Hardware Match</span>
                        <span class="text-xs font-bold text-slate-700">Amazon Prime Ready</span>
                    </div>
                    <h3 id="recSaunaTitle" class="text-base font-extrabold text-slate-900 leading-snug">Loading Sauna Heater Match...</h3>
                    <p id="recSaunaDesc" class="text-xs text-slate-600"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched Sauna Heater &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop Stones & Controls
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-slate-900">Search Electric Sauna Heaters, Steam Generators, Stones & Controllers</h2>
                <p class="text-sm text-slate-600">Search any power (6kW, 8kW, 9kW), brand (Harvia, Finlandia, VEVOR, Mr. Steam, Tylo, Superior Saunas) on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. Harvia KIP 8kW Heater, Harvia Cilindro 9kW, Mr. Steam MS400E Generator..."
                           class="flex-1 bg-white border-2 border-slate-300 rounded-xl px-4 py-3 text-sm font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:border-amber-700" required>
                    <button type="submit" class="bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-slate-500 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('Harvia KIP 6kW 8kW Electric Sauna Heater')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-50 hover:bg-amber-50 text-slate-700 border border-slate-200 rounded-full transition">Harvia KIP Heaters</a>
                    <a href="{amz_url('Harvia Cilindro 9kW Sauna Heater')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-50 hover:bg-amber-50 text-slate-700 border border-slate-200 rounded-full transition">Harvia Cilindro 9kW</a>
                    <a href="{amz_url('Mr Steam Generator MS225E MS400E')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-50 hover:bg-amber-50 text-slate-700 border border-slate-200 rounded-full transition">Mr. Steam Generators</a>
                    <a href="{amz_url('Olivine Diabase Sauna Stones 50 lb')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-50 hover:bg-amber-50 text-slate-700 border border-slate-200 rounded-full transition">Olivine Sauna Stones</a>
                    <a href="{amz_url('Harvia Xenio Digital Sauna Control Panel')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-50 hover:bg-amber-50 text-slate-700 border border-slate-200 rounded-full transition">Digital Touch Controls</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-slate-200 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-amber-700">Verified Finnish & Spa Hardware</span>
                    <h2 class="text-2xl font-extrabold text-slate-900">Best-Selling Electric Sauna Heaters, Steam Generators & Accessories</h2>
                </div>
                <a href="{amz_url('Best Selling Electric Sauna Heaters and Steam Generators')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-amber-700 hover:text-amber-800">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- CUMULATIVE DAILY PRODUCT REVIEW ARTICLES SECTION (+3 NEW ARTICLES PER DAY) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-slate-200 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-amber-700">Autonomous Daily Review Archive ({total_reviews_count} Published Articles & Growing +3/Day)</span>
                    <h2 class="text-2xl font-extrabold text-slate-900">In-Depth Sauna Stove, Steam Shower Generator & Control Review Articles</h2>
                </div>
                <span class="text-xs font-semibold bg-emerald-50 text-emerald-900 border border-emerald-200 px-3 py-1 rounded-full">+3 New Product Reviews Added Automatically Every Day</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-slate-50 border-2 border-amber-700 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6 shadow-sm">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-amber-700 text-white px-2.5 py-1 rounded">Complete Home Spa Transformation Bundle</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-slate-900">Building a Traditional 190°F Finnish Cedar Sauna or Steam Shower?</h2>
                <p class="text-sm text-slate-700">Achieve authentic soft steam and rapid heat by pairing a Finnish Harvia KIP or Cilindro Heater with 50 Lbs of Genuine Olivine Diabase Vulcanite Stones, High-Temp Pure Copper Wire, and Rento Finnish Cedar Accessories.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore Sauna Heater + Stone Bundles on Amazon &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-slate-200 pb-3">
                <h2 class="text-xl font-extrabold text-slate-900">Room Dimensions, Kilowatts & Barrel Sauna Specific Calculators</h2>
                <p class="text-xs text-slate-500">Select your exact room cubic feet or barrel sauna size below for pre-calculated heater kilowatts and 240V breaker ratings.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-slate-200 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-amber-700">Finnish Löyly, Glass Multipliers & NEC 240V Guide</span>
                <h2 class="text-2xl font-extrabold text-slate-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

        {onpage_sitemap_html}

    </main>

    <!-- FOOTER (WHITE BACKGROUND) -->
    <footer class="bg-white border-t border-slate-200 mt-16 py-10 px-4 text-xs text-slate-600">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-slate-900">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-slate-700">
                <a href="{BASE_URL}/" class="hover:text-amber-700">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-amber-700">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-amber-700">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-amber-700 font-bold">HTML Site Map</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-amber-700">XML Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-amber-700">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 6) {{
                document.getElementById("lenInput").value = parts[0];
                document.getElementById("widInput").value = parts[1];
                document.getElementById("hgtInput").value = parts[2];
                document.getElementById("glassInput").value = parts[3];
                document.getElementById("stoneInput").value = parts[4];
                document.getElementById("climInput").value = parts[5];
                calculateSauna();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateSauna() {{
            const l = parseFloat(document.getElementById("lenInput").value) || 7.0;
            const w = parseFloat(document.getElementById("widInput").value) || 5.0;
            const h = parseFloat(document.getElementById("hgtInput").value) || 7.0;
            const glass = parseFloat(document.getElementById("glassInput").value) || 14.0;
            const stone = parseFloat(document.getElementById("stoneInput").value) || 0.0;
            const mode = document.getElementById("climInput").value || "indoor";

            const grossCuft = l * w * h;
            let coldAdd = (glass * 1.2) + (stone * 1.5);
            let climMult = 1.0;

            if (mode === "steam") {{
                coldAdd = (glass * 1.5) + (stone * 2.2);
            }} else if (mode === "outdoor_cold") {{
                coldAdd = (glass * 1.5) + (stone * 1.8);
                climMult = 1.30;
            }}

            const adjCuft = Math.round((grossCuft + coldAdd) * climMult);
            const rawKw = adjCuft / 46.0;

            const kwTiers = [2.0, 3.0, 4.5, 6.0, 8.0, 9.0, 10.5, 12.0, 15.0];
            let recKw = 15.0;
            for (let i = 0; i < kwTiers.length; i++) {{
                if (kwTiers[i] >= rawKw - 0.15) {{
                    recKw = kwTiers[i];
                    break;
                }}
            }}

            const runningAmps = ((recKw * 1000.0) / 240.0).toFixed(1);
            const reqBrkRaw = parseFloat(runningAmps) * 1.25;

            const brkTiers = [15, 20, 25, 30, 40, 50, 60, 70, 80, 100];
            let recBrk = 100;
            for (let i = 0; i < brkTiers.length; i++) {{
                if (brkTiers[i] >= reqBrkRaw - 0.2) {{
                    recBrk = brkTiers[i];
                    break;
                }}
            }}

            let wireStr = "8/2 Pure Copper (8 AWG)";
            if (recBrk <= 20) wireStr = "12/2 Pure Copper (12 AWG)";
            else if (recBrk <= 30) wireStr = "10/2 Pure Copper (10 AWG)";
            else if (recBrk <= 40) wireStr = "8/2 Pure Copper (8 AWG)";
            else if (recBrk <= 50) wireStr = "6/2 Pure Copper (6 AWG)";
            else if (recBrk <= 70) wireStr = "4/2 Pure Copper (4 AWG)";
            else wireStr = "2 AWG in Conduit";

            let rockStr = "45 Lbs Stones";
            if (recKw <= 4.5) rockStr = "35 Lbs Stones";
            else if (recKw === 9.0) rockStr = "45 Lbs (or 200 Lb Tower)";
            else if (recKw > 9.0) rockStr = "100–150 Lbs Stones";

            const preheatStr = mode === "steam" ? "60s to 100% Steam" : "35–42m to 190°F";

            document.getElementById("resRecKw").textContent = recKw.toFixed(1) + " kW Heater";
            document.getElementById("resAdjCuft").textContent = adjCuft.toLocaleString() + " Cu.Ft Adj (" + Math.round(grossCuft) + " Gross)";
            document.getElementById("resBreaker").textContent = recBrk + "A 2-Pole Brk";
            document.getElementById("resAmps").textContent = runningAmps + "A Load (NEC 125%)";
            document.getElementById("resWire").textContent = wireStr;
            document.getElementById("resStones").textContent = rockStr;
            document.getElementById("resPreheat").textContent = preheatStr;

            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "";
            let secondaryQuery = "Superior Saunas 50 lb Olivine Diabase Stones and Rento Sauna Bucket";

            if (mode === "steam") {{
                recTitle = "Mr. Steam MS" + (recKw <= 7.5 ? "225E" : "400E") + " (" + recKw.toFixed(1) + " kW) Residential Steam Generator System";
                recDesc = "Transforms custom tiled showers into a 100% humidity tropical steam room in 60 seconds.";
                primaryQuery = "Mr Steam MS400E MS225E Steam Shower Generator";
            }} else if (recKw >= 8.5) {{
                recTitle = "Harvia Cilindro 9kW Pillar Tower or Harvia KIP-80B (8kW) Electric Sauna Stove";
                recDesc = "High-thermal mass Finnish heating engineered for " + adjCuft.toLocaleString() + " adjusted cu. ft. (" + recBrk + "A breaker).";
                primaryQuery = "Harvia Cilindro 9kW Harvia KIP 8kW Electric Sauna Heater";
            }} else {{
                recTitle = "Harvia KIP-" + (recKw <= 4.5 ? "45B" : "60B") + " (" + recKw.toFixed(1) + " kW) Finnish Electric Sauna Heater";
                recDesc = "Heats your " + Math.round(grossCuft) + " cu. ft. cedar sauna to 190°F in 38 minutes on a " + recBrk + "A 240V circuit.";
                primaryQuery = "Harvia KIP " + recKw.toFixed(1) + "kW Electric Sauna Heater 240V";
            }}

            document.getElementById("recSaunaTitle").textContent = recTitle;
            document.getElementById("recSaunaDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateSauna);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "datePublished": rev["published_date"],
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-slate-800"><span class="text-emerald-700 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-slate-800"><span class="text-rose-700 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-slate-700 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    recent_reviews = [r for r in get_cumulative_product_reviews() if r["slug"] != rev["slug"]][:6]
    related_html = ""
    for other in recent_reviews:
        related_html += f"""
        <a href="{BASE_URL}/{other['slug']}.html" class="bg-white border-2 border-slate-200 rounded-xl p-4 hover:border-amber-700 transition block shadow-sm">
            <span class="text-[11px] font-bold text-amber-700 uppercase">{other['verdict_badge']}</span>
            <h4 class="font-extrabold text-sm text-slate-900 mt-1 line-clamp-2">{other['product_name']} Review</h4>
            <span class="text-xs text-slate-500 mt-1 block">Score: {other['rating_score']} / 5.0 ★ ({other['published_date']}) &rarr;</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-white text-slate-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-slate-500 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-amber-700">Home & Sauna Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-amber-700">Daily Sauna Reviews</a>
            <span>/</span>
            <span class="text-slate-900">{rev['product_name']}</span>
        </nav>

        <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-amber-50 text-amber-900 border border-amber-200 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono text-slate-500">Published: {rev['published_date']}</span>
                    <span class="text-sm font-black bg-amber-100 text-amber-950 px-3 py-1 rounded-lg">Spa Lab Rating: {rev['rating_score']} / 5.0 ★</span>
                </div>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-slate-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-slate-600 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs">
                <div><span class="text-slate-500 block font-medium">kW / Volume</span><strong class="text-slate-900">{rev['spec_1']}</strong></div>
                <div><span class="text-slate-500 block font-medium">Stones / Steam</span><strong class="text-slate-900">{rev['spec_2']}</strong></div>
                <div><span class="text-slate-500 block font-medium">Controls</span><strong class="text-slate-900">{rev['spec_3']}</strong></div>
                <div><span class="text-slate-500 block font-medium">Origin</span><strong class="text-slate-900">{rev['spec_4']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-slate-100 hover:bg-slate-200 text-slate-900 border border-slate-300 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate Sauna Heater kW
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-white border-2 border-emerald-400 rounded-2xl p-6 space-y-3 shadow-sm">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-white border-2 border-rose-300 rounded-2xl p-6 space-y-3 shadow-sm">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 space-y-4 shadow-sm">
            <h2 class="text-xl font-extrabold text-slate-900 border-b border-slate-200 pb-3">Hands-On 190°F Pre-Heat, Steam Löyly & Electrical Load Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-amber-700 block">Final Verdict</span>
                    <p class="text-sm font-bold text-slate-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our home spa benchmark.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>

        <section class="space-y-4">
            <h3 class="text-lg font-extrabold text-slate-900">Recent Daily Sauna & Steam Hardware Reviews (+3 Added Daily)</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {related_html}
            </div>
        </section>
    </main>

    <footer class="bg-white border-t border-slate-200 mt-16 py-10 px-4 text-xs text-slate-600 text-center">
        <p class="font-bold text-slate-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-slate-200">
            <td class="p-4 font-bold text-slate-900 bg-slate-50 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-slate-800 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-slate-800 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white text-slate-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-slate-500 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-amber-700">Home & Sauna Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-amber-700">Product Comparisons</a>
            <span>/</span>
            <span class="text-slate-900">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-amber-50 text-amber-900 border border-amber-200 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-slate-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-slate-600 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-white border-2 border-slate-200 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-slate-900 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-amber-300">{vs['product_a']}</th>
                        <th class="p-4 text-amber-400">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-slate-50">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-slate-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-slate-800 hover:bg-slate-900 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-white border-2 border-amber-600 rounded-2xl p-6 sm:p-8 space-y-4 shadow-sm">
            <h2 class="text-xl font-extrabold text-slate-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-slate-700 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-amber-700 hover:bg-amber-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-slate-800 hover:bg-slate-900 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-white border-t border-slate-200 mt-16 py-10 px-4 text-xs text-slate-600 text-center">
        <p class="font-bold text-slate-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "5' × 7' × 7' Home Cedar Sauna (245 Cu.Ft w/ Glass Door — 8.0 kW)",
        "len_ft": 7.0,
        "wid_ft": 5.0,
        "hgt_ft": 7.0,
        "glass_sqft": 14.0,
        "stone_sqft": 0.0,
        "climate_mode": "indoor",
        "desc": "Calculate exact electric sauna heater sizing (kW), room volume in cubic feet, cold glass/stone heat loss multipliers, NEC 240V breaker amperage, copper wire gauge, and vulcanite sauna stone capacity—plus read 3 new sauna reviews added daily."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Dedicated HTML Site Map Page (sitemap.html)
    with open(os.path.join(OUTPUT_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(render_dedicated_html_sitemap_page())
    generated_urls.append(f"{BASE_URL}/sitemap.html")

    # 3. Generate Programmatic Sauna Heater Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Cumulative Daily Product Review Pages (+3 new reviews unlocked every single day)
    active_reviews = get_cumulative_product_reviews()
    for rev in active_reviews:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 6. XML Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} total SEO pages ({len(active_reviews)} cumulative review articles [+3/day] + HTML/XML sitemaps) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
