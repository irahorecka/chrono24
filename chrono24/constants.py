"""
chrono24/constants
~~~~~~~~~~~~~~~~~~
"""

case_filters = {
    # Case Material
    "aluminum": "caseMaterials=6",
    "brass": "caseMaterials=19",
    "bronze": "caseMaterials=18",
    "carbon": "caseMaterials=17",
    "ceramic": "caseMaterials=13",
    "gold_steel": "caseMaterials=9",
    "gold_plated": "caseMaterials=20",
    "palladium": "caseMaterials=14",
    "plastic": "caseMaterials=12",
    "platinum": "caseMaterials=7",
    "red_gold": "caseMaterials=2",
    "rose_gold": "caseMaterials=1",
    "sapphire_crystal": "caseMaterials=21",
    "silver": "caseMaterials=10",
    "steel": "caseMaterials=4",
    "tantalum": "caseMaterials=16",
    "titanium": "caseMaterials=5",
    "tungsten": "caseMaterials=15",
    "white_gold": "caseMaterials=8",
    "yellow_gold": "caseMaterials=3",
    "no_details_case_material": "caseMaterials=0",
    # Bezel Material
    "aluminum_bezel": "bezelMaterial=1601",
    "brass_bezel": "bezelMaterial=1619",
    "bronze_bezel": "bezelMaterial=1617",
    "carbon_bezel": "bezelMaterial=1602",
    "ceramic_bezel": "bezelMaterial=1603",
    "gem_set_bezel": "bezelMaterial=1618",
    "gold_steel_bezel": "bezelMaterial=1604",
    "gold_plated_bezel": "bezelMaterial=1620",
    "palladium_bezel": "bezelMaterial=1605",
    "plastic_bezel": "bezelMaterial=1607",
    "platinum_bezel": "bezelMaterial=1608",
    "red_gold_bezel": "bezelMaterial=1609",
    "rose_gold_bezel": "bezelMaterial=1606",
    "rubber_bezel": "bezelMaterial=1621",
    "silver_bezel": "bezelMaterial=1610",
    "steel_bezel": "bezelMaterial=1611",
    "tantalum_bezel": "bezelMaterial=1612",
    "titanium_bezel": "bezelMaterial=1613",
    "tungsten_bezel": "bezelMaterial=1614",
    "white_gold_bezel": "bezelMaterial=1615",
    "yellow_gold_bezel": "bezelMaterial=1616",
    "no_details_bezel": "bezelMaterial=0",
    # Crystal Type
    "glass_crystal": "glass=203",
    "mineral_glass_crystal": "glass=204",
    "plastic_crystal": "glass=201",
    "plexiglass_crystal": "glass=202",
    "sapphire_crystal_glass": "glass=205",
    "no_details_crystal": "glass=0",
    # Water Resistance
    "not_water_resistant": "waterproof=901",
    "one_atm": "waterproof=902",
    "two_atm": "waterproof=903",
    "two_point_five_atm": "waterproof=1350",
    "three_atm": "waterproof=904",
    "four_atm": "waterproof=905",
    "five_atm": "waterproof=906",
    "six_atm": "waterproof=907",
    "seven_atm": "waterproof=908",
    "eight_atm": "waterproof=909",
    "nine_atm": "waterproof=910",
    "ten_atm": "waterproof=911",
    "fifteen_atm": "waterproof=1351",
    "twenty_atm": "waterproof=912",
    "thirty_atm": "waterproof=913",
    "forty_atm": "waterproof=914",
    "fifty_atm": "waterproof=915",
    "sixty_atm": "waterproof=916",
    "seventy_atm": "waterproof=917",
    "eighty_atm": "waterproof=918",
    "ninety_atm": "waterproof=919",
    "hundred_atm": "waterproof=920",
    "one_hundred_ten_atm": "waterproof=921",
    "one_hundred_twenty_atm": "waterproof=922",
    "over_one_hundred_twenty_atm": "waterproof=923",
    "no_details_water_resistance": "waterproof=0",
}

clasp_filters = {
    # Clasp Material
    "aluminum_clasp": "claspMaterial=1109",
    "bronze_clasp": "claspMaterial=1112",
    "gold_steel_clasp": "claspMaterial=1105",
    "plastic_clasp": "claspMaterial=1101",
    "platinum_clasp": "claspMaterial=1110",
    "red_gold_clasp": "claspMaterial=1107",
    "rose_gold_clasp": "claspMaterial=1106",
    "silver_clasp": "claspMaterial=1103",
    "steel_clasp": "claspMaterial=1102",
    "titanium_clasp": "claspMaterial=1104",
    "white_gold_clasp": "claspMaterial=1111",
    "yellow_gold_clasp": "claspMaterial=1108",
    "no_details_clasp_material": "claspMaterial=0",
    # Clasp Type
    "buckle_clasp": "clasp=504",
    "double_fold_clasp": "clasp=503",
    "fold_clasp": "clasp=501",
    "fold_clasp_hidden": "clasp=502",
    "jewelry_clasp": "clasp=505",
    "no_clasp": "clasp=506",
    "no_details_clasp_type": "clasp=0",
}

condition_and_delivery_contents_filters = {
    # Delivery Contents
    "original_box_and_papers": "specials=102",
    "original_papers": "specials=104",
    "original_box": "specials=103",
    # Availability
    "in_stock": "stockInfo=InStock",
    "on_order": "stockInfo=OnOrder",
    "on_request": "stockInfo=OnRequest",
    # New/Used
    "new_unworn": "usedOrNew=new",
    "used": "usedOrNew=used",
    "no_details_new_unused": "usedOrNew=NODATA",
    # Condition
    "new": "condition=101",
    "like_new_unworn": "condition=1301",
    "very_good": "condition=1302",
    "good": "condition=1306",
    "fair": "condition=1303",
    "incomplete": "condition=1305",
    "no_details_condition": "condition=0",
}

dial_filters = {
    # Dial Style
    "arabic_numerals": "dialNumbers=801",
    "gemstones": "dialNumbers=804",
    "lines": "dialNumbers=805",
    "no_numerals": "dialNumbers=803",
    "roman_numerals": "dialNumbers=802",
    "no_details_style": "dialNumbers=0",
    # Dial Color
    "black_dial": "dialColor=702",
    "blue_dial": "dialColor=710",
    "bordeaux_dial": "dialColor=711",
    "bronze_dial": "dialColor=712",
    "brown_dial": "dialColor=723",
    "champagne_dial": "dialColor=709",
    "gold_dial": "dialColor=714",
    "gold_solid_dial": "dialColor=705",
    "green_dial": "dialColor=716",
    "grey_dial": "dialColor=715",
    "meteorite_dial": "dialColor=725",
    "mother_of_pearl_dial": "dialColor=707",
    "orange_dial": "dialColor=719",
    "pink_dial": "dialColor=722",
    "purple_dial": "dialColor=721",
    "red_dial": "dialColor=720",
    "silver_dial": "dialColor=708",
    "silver_solid_dial": "dialColor=706",
    "skeletonized_dial": "dialColor=726",
    "skeletonized_duplicate_dial": "dialColor=704",
    "turquoise_dial": "dialColor=724",
    "white_dial": "dialColor=701",
    "yellow_dial": "dialColor=713",
    "no_details_color_dial": "dialColor=0",
}

location_filters = {
    # Individual countries
    "afghanistan": "countryIds=AF",
    "albania": "countryIds=AL",
    "algeria": "countryIds=DZ",
    "andorra": "countryIds=AD",
    "angola": "countryIds=AO",
    "argentina": "countryIds=AR",
    "armenia": "countryIds=AM",
    "aruba": "countryIds=AW",
    "australia": "countryIds=AU",
    "austria": "countryIds=AT",
    "azerbaijan": "countryIds=AZ",
    "bahrain": "countryIds=BH",
    "barbados": "countryIds=BB",
    "belarus": "countryIds=BY",
    "belgium": "countryIds=BE",
    "bermuda": "countryIds=BM",
    "bhutan": "countryIds=BT",
    "bolivia": "countryIds=BO",
    "bosnia_and_herzegovina": "countryIds=BA",
    "botswana": "countryIds=BW",
    "brazil": "countryIds=BR",
    "brunei": "countryIds=BN",
    "bulgaria": "countryIds=BG",
    "canada": "countryIds=CA",
    "central_african_republic": "countryIds=CF",
    "chile": "countryIds=CL",
    "china": "countryIds=CN",
    "colombia": "countryIds=CO",
    "costa_rica": "countryIds=CR",
    "croatia": "countryIds=HR",
    "cyprus": "countryIds=CY",
    "czech_republic": "countryIds=CZ",
    "denmark": "countryIds=DK",
    "dominican_republic": "countryIds=DO",
    "ecuador": "countryIds=EC",
    "egypt": "countryIds=EG",
    "estonia": "countryIds=EE",
    "ethiopia": "countryIds=ET",
    "finland": "countryIds=FI",
    "france": "countryIds=FR",
    "georgia": "countryIds=GE",
    "germany": "countryIds=DE",
    "gibraltar": "countryIds=GI",
    "greece": "countryIds=GR",
    "guadeloupe": "countryIds=GP",
    "guam": "countryIds=GU",
    "haiti": "countryIds=HT",
    "hong_kong": "countryIds=HK",
    "hungary": "countryIds=HU",
    "iceland": "countryIds=IS",
    "india": "countryIds=IN",
    "indonesia": "countryIds=ID",
    "iraq": "countryIds=IQ",
    "ireland": "countryIds=IE",
    "israel": "countryIds=IL",
    "italy": "countryIds=IT",
    "jamaica": "countryIds=JM",
    "japan": "countryIds=JP",
    "jordan": "countryIds=JO",
    "kazakhstan": "countryIds=KZ",
    "kuwait": "countryIds=KW",
    "kyrgyzstan": "countryIds=KG",
    "latvia": "countryIds=LV",
    "lebanon": "countryIds=LB",
    "liechtenstein": "countryIds=LI",
    "lithuania": "countryIds=LT",
    "luxembourg": "countryIds=LU",
    "macao": "countryIds=MO",
    "macedonia": "countryIds=MK",
    "madagascar": "countryIds=MG",
    "malaysia": "countryIds=MY",
    "maldives": "countryIds=MV",
    "malta": "countryIds=MT",
    "mauritius": "countryIds=MU",
    "mexico": "countryIds=MX",
    "moldova": "countryIds=MD",
    "monaco": "countryIds=MC",
    "montenegro": "countryIds=ME",
    "morocco": "countryIds=MA",
    "nepal": "countryIds=NP",
    "netherlands_antilles": "countryIds=AN",
    "new_caledonia": "countryIds=NC",
    "new_zealand": "countryIds=NZ",
    "norway": "countryIds=NO",
    "oman": "countryIds=OM",
    "pakistan": "countryIds=PK",
    "panama": "countryIds=PA",
    "paraguay": "countryIds=PY",
    "peru": "countryIds=PE",
    "pitcairn_islands": "countryIds=PN",
    "poland": "countryIds=PL",
    "portugal": "countryIds=PT",
    "puerto_rico": "countryIds=PR",
    "qatar": "countryIds=QA",
    "réunion": "countryIds=RE",
    "romania": "countryIds=RO",
    "russia": "countryIds=RU",
    "rwanda": "countryIds=RW",
    "saint_barthélemy": "countryIds=BL",
    "saint_vincent_and_the_grenadines": "countryIds=VC",
    "san_marino": "countryIds=SM",
    "saudi_arabia": "countryIds=SA",
    "serbia": "countryIds=RS",
    "singapore": "countryIds=SG",
    "slovakia": "countryIds=SK",
    "slovenia": "countryIds=SI",
    "south_africa": "countryIds=ZA",
    "south_korea": "countryIds=KR",
    "spain": "countryIds=ES",
    "sri_lanka": "countryIds=LK",
    "st_kitts_and_nevis": "countryIds=KN",
    "swaziland": "countryIds=SZ",
    "sweden": "countryIds=SE",
    "switzerland": "countryIds=CH",
    "taiwan": "countryIds=TW",
    "tanzania": "countryIds=TZ",
    "thailand": "countryIds=TH",
    "the_netherlands": "countryIds=NL",
    "the_philippines": "countryIds=PH",
    "togo": "countryIds=TG",
    "turkey": "countryIds=TR",
    "uae": "countryIds=AE",
    "ukraine": "countryIds=UA",
    "united_kingdom": "countryIds=UK",
    "united_states_minor_outlying_islands": "countryIds=UM",
    "united_states_of_america": "countryIds=US",
    "uruguay": "countryIds=UY",
    "uzbekistan": "countryIds=UZ",
    "venezuela": "countryIds=VE",
    "vietnam": "countryIds=VN",
}

movement_and_functions = {
    # Movement Types
    "automatic": "movementTypes=1",
    "manual_winding": "movementTypes=2",
    "quartz": "movementTypes=3",
    "smartwatch": "movementTypes=5",
    "solar": "movementTypes=4",
    "no_details": "movementTypes=0",
    # Function Types
    "four_year_calendar": "functions=1016",
    "alarm": "functions=1018",
    "annual_calendar": "functions=1015",
    "chiming_clock": "functions=1019",
    "chronograph": "functions=1000",
    "date": "functions=1022",
    "double_chronograph": "functions=1010",
    "equation_of_time": "functions=1028",
    "flyback": "functions=1011",
    "gmt": "functions=1360",
    "jumping_hour": "functions=1027",
    "minute_repeater": "functions=1021",
    "month": "functions=1024",
    "moon_phase": "functions=1020",
    "panorama_date": "functions=1012",
    "perpetual_calendar": "functions=1017",
    "repeater": "functions=1013",
    "tachymeter": "functions=1026",
    "tourbillon": "functions=1014",
    "weekday": "functions=1023",
    "year": "functions=1025",
}

other_filters = {
    # Other Attributes
    "central_seconds": "otherAttributes=1201",
    "chronometer": "otherAttributes=1207",
    "crown_left": "otherAttributes=1210",
    "display_back": "otherAttributes=1215",
    "gemstones_or_diamonds": "otherAttributes=1204",
    "genevian_seal": "otherAttributes=1206",
    "guilloche_dial": "otherAttributes=1203",
    "guilloche_dial_handwork": "otherAttributes=1212",
    "helium_valve": "otherAttributes=1218",
    "limited_edition": "otherAttributes=1209",
    "luminous_hands": "otherAttributes=1214",
    "luminous_indices": "otherAttributes=1222",
    "luminous_numerals": "otherAttributes=1205",
    "master_chronometer": "otherAttributes=1225",
    "one_hand_watches": "otherAttributes=1228",
    "only_original_parts": "otherAttributes=1221",
    "power_reserve_display": "otherAttributes=1217",
    "pvd_dlc_coating": "otherAttributes=1223",
    "quick_set": "otherAttributes=1219",
    "rotating_bezel": "otherAttributes=1208",
    "screw_down_crown": "otherAttributes=1211",
    "screw_down_push_buttons": "otherAttributes=1220",
    "skeletonized": "otherAttributes=1216",
    "small_seconds": "otherAttributes=1202",
    "smartwatch": "otherAttributes=1226",
    "solar_watch": "otherAttributes=1227",
    "tempered_blue_hands": "otherAttributes=1213",
    "world_time_watch": "otherAttributes=1224",
}

seller_and_listing_type_filters = {
    # Seller
    "chrono24_direct": "sellerType=C24Direct",
    "private_seller": "sellerType=PrivateSeller",
    "professional_dealer": "sellerType=Dealer",
    # Listing Type
    "auction": "listingType=Auction",
    "buy_now": "listingType=BuyItNow",
    # Security
    "includes_buyer_protection": "checkoutAvailable=yes",
    # Dealer Badges
    "fast_shipper": "dealerPerformanceAttributes=FastShipper",
    "highly_rated": "dealerPerformanceAttributes=TopRating",
    "punctuality": "dealerPerformanceAttributes=Punctuality",
    "response_time": "dealerPerformanceAttributes=Reaction",
}

sort_by_filters = {
    "relevance": "sortorder=0",
    "price_asc": "sortorder=1",
    "price_desc": "sortorder=11",
    "newest": "sortorder=5",
    "popularity": "sortorder=15",
}

strap_bracelet_filters = {
    # Band Material
    "alligator_skin": "braceletMaterial=424",
    "aluminium_band": "braceletMaterial=414",
    "brass_band": "braceletMaterial=425",
    "calf_skin": "braceletMaterial=401",
    "ceramic_band": "braceletMaterial=421",
    "crocodile_skin": "braceletMaterial=403",
    "gold_steel_band": "braceletMaterial=410",
    "gold_plated_band": "braceletMaterial=426",
    "leather_band": "braceletMaterial=404",
    "lizard_skin": "braceletMaterial=422",
    "ostrich_skin": "braceletMaterial=402",
    "plastic_band": "braceletMaterial=406",
    "platinum_band": "braceletMaterial=415",
    "red_gold_band": "braceletMaterial=412",
    "rose_gold_band": "braceletMaterial=411",
    "rubber_band": "braceletMaterial=418",
    "satin_band": "braceletMaterial=420",
    "shark_skin": "braceletMaterial=419",
    "silicon_band": "braceletMaterial=423",
    "silver_band": "braceletMaterial=417",
    "snake_skin": "braceletMaterial=405",
    "steel_band": "braceletMaterial=407",
    "textile_band": "braceletMaterial=2017",
    "titanium_band": "braceletMaterial=409",
    "white_gold_band": "braceletMaterial=416",
    "yellow_gold_band": "braceletMaterial=413",
    "no_details_band_material": "braceletMaterial=0",
    # Band Color
    "beige_band": "braceletColor=606",
    "black_band": "braceletColor=601",
    "blue_band": "braceletColor=607",
    "bordeaux_band": "braceletColor=608",
    "bronze_band": "braceletColor=609",
    "brown_band": "braceletColor=602",
    "gold_band": "braceletColor=604",
    "gold_steel_color": "braceletColor=620",
    "green_band": "braceletColor=612",
    "grey_band": "braceletColor=611",
    "orange_band": "braceletColor=615",
    "pink_band": "braceletColor=619",
    "purple_band": "braceletColor=617",
    "red_band": "braceletColor=616",
    "silver_band_color": "braceletColor=603",
    "steel_band_color": "braceletColor=605",
    "white_band": "braceletColor=618",
    "yellow_band": "braceletColor=610",
    "no_details_band_color": "braceletColor=0",
}


watch_type_filters = {
    # Gender
    "mens_unisex_watch": "gender=1401",
    "womens_watch": "gender=1402",
    # Watch Type
    "automatic_watches": "styles=1811",
    "business_watches": "styles=1809",
    "calendar_watches": "styles=1821",
    "chronographs": "styles=1812",
    "chronometer": "styles=1813",
    "diving_watches": "styles=1804",
    "dress_watches": "styles=1805",
    "flyback_chronographs": "styles=1818",
    "large_xxl_watches": "styles=1819",
    "left_handed_watches": "styles=1823",
    "limited_edition_watches": "styles=1822",
    "manually_wound_watches": "styles=1841",
    "mechanical_watches": "styles=1824",
    "military_watches": "styles=1807",
    "minute_repeater": "styles=1825",
    "moon_phase_watches": "styles=1826",
    "one_hand_watches": "styles=1815",
    "perpetual_calendar_watches": "styles=1816",
    "pilots_watches": "styles=1803",
    "quartz_watches": "styles=1827",
    "racing_watches": "styles=1801",
    "rectangular_watches": "styles=1842",
    "russian_watches": "styles=1828",
    "sailing_watches": "styles=1802",
    "sapphire_glass_watches": "styles=1829",
    "skeleton_watches": "styles=1831",
    "smartwatches": "styles=1832",
    "solar_watches": "styles=1833",
    "sports_watches": "styles=1806",
    "swiss_watches": "styles=1830",
    "tachymeter_watches": "styles=1837",
    "thin_watches": "styles=1817",
    "tonneau_watches": "styles=1835",
    "tourbillon_watches": "styles=1836",
    "vintage_watches": "styles=1810",
    "watches_from_german_manufacturers": "styles=1838",
    "watches_with_geneva_seal": "styles=1839",
    "watches_with_see_through_case_back": "styles=1840",
    "world_time_watches": "styles=1843",
    # Style of Watch
    "wristwatch": "watchCategories=301",
    "pocket_watch": "watchCategories=302",
    "other_watch_clock": "watchCategories=303",
}

# Year will be either a single year or a range of years
