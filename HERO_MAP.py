hero_names_default = {'Anti-Mage': 1, 'Axe': 2, 'Bane': 3, 'Bloodseeker': 4, 'Crystal Maiden': 5, 'Drow Ranger': 6,
                      'Earthshaker': 7, 'Juggernaut': 8, 'Mirana': 9, 'Morphling': 10, 'Shadow Fiend': 11,
                      'Phantom Lancer': 12,
                      'Puck': 13, 'Pudge': 14, 'Razor': 15, 'Sand King': 16, 'Storm Spirit': 17, 'Sven': 18, 'Tiny': 19,
                      'Vengeful Spirit': 20, 'Windranger': 21, 'Zeus': 22, 'Kunkka': 23, 'Lina': 25, 'Lion': 26,
                      'Shadow Shaman': 27, 'Slardar': 28, 'Tidehunter': 29, 'Witch Doctor': 30, 'Lich': 31, 'Riki': 32,
                      'Enigma': 33, 'Tinker': 34, 'Sniper': 35, 'Necrophos': 36, 'Warlock': 37, 'Beastmaster': 38,
                      'Queen of Pain': 39, 'Venomancer': 40, 'Faceless Void': 41, 'Wraith King': 42,
                      'Death Prophet': 43,
                      'Phantom Assassin': 44, 'Pugna': 45, 'Templar Assassin': 46, 'Viper': 47, 'Luna': 48,
                      'Dragon Knight': 49,
                      'Dazzle': 50, 'Clockwerk': 51, 'Leshrac': 52, "Nature's Prophet": 53, 'Lifestealer': 54,
                      'Dark Seer': 55,
                      'Clinkz': 56, 'Omniknight': 57, 'Enchantress': 58, 'Huskar': 59, 'Night Stalker': 60,
                      'Broodmother': 61,
                      'Bounty Hunter': 62, 'Weaver': 63, 'Jakiro': 64, 'Batrider': 65, 'Chen': 66, 'Spectre': 67,
                      'Ancient Apparition': 68, 'Doom': 69, 'Ursa': 70, 'Spirit Breaker': 71, 'Gyrocopter': 72,
                      'Alchemist': 73,
                      'Invoker': 74, 'Silencer': 75, 'Outworld Destroyer': 76, 'Lycan': 77, 'Brewmaster': 78,
                      'Shadow Demon': 79, 'Lone Druid': 80, 'Chaos Knight': 81, 'Meepo': 82, 'Treant Protector': 83,
                      'Ogre Magi': 84, 'Undying': 85, 'Rubick': 86, 'Disruptor': 87, 'Nyx Assassin': 88,
                      'Naga Siren': 89,
                      'Keeper of the Light': 90, 'Io': 91, 'Visage': 92, 'Slark': 93, 'Medusa': 94,
                      'Troll Warlord': 95, 'Centaur Warrunner': 96, 'Magnus': 97, 'Timbersaw': 98, 'Bristleback': 99,
                      'Tusk': 100, 'Skywrath Mage': 101, 'Abaddon': 102, 'Elder Titan': 103, 'Legion Commander': 104,
                      'Techies': 105, 'Ember Spirit': 106, 'Earth Spirit': 107, 'Underlord': 108, 'Terrorblade': 109,
                      'Phoenix': 110, 'Oracle': 111, 'Winter Wyvern': 112, 'Arc Warden': 113, 'Monkey King': 114,
                      'Dark Willow': 119, 'Pangolier': 120, 'Grimstroke': 121, 'Hoodwink': 123, 'Void Spirit': 126,
                      'Snapfire': 128, 'Mars': 129, 'Dawnbreaker': 135, 'Marci': 136, 'Primal Beast': 137,
                      'Muerta': 138}

hero_names = {}
for i in hero_names_default.keys():
    hero_names[i.lower()] = hero_names_default[i]

hero_ids_default = {1: 'Anti-Mage', 2: 'Axe', 3: 'Bane', 4: 'Bloodseeker', 5: 'Crystal Maiden', 6: 'Drow Ranger',
                    7: 'Earthshaker',
                    8: 'Juggernaut', 9: 'Mirana', 10: 'Morphling', 11: 'Shadow Fiend', 12: 'Phantom Lancer', 13: 'Puck',
                    14: 'Pudge',
                    15: 'Razor', 16: 'Sand King', 17: 'Storm Spirit', 18: 'Sven', 19: 'Tiny', 20: 'Vengeful Spirit',
                    21: 'Windranger',
                    22: 'Zeus', 23: 'Kunkka', 25: 'Lina', 26: 'Lion', 27: 'Shadow Shaman', 28: 'Slardar',
                    29: 'Tidehunter',
                    30: 'Witch Doctor', 31: 'Lich', 32: 'Riki', 33: 'Enigma', 34: 'Tinker', 35: 'Sniper',
                    36: 'Necrophos',
                    37: 'Warlock', 38: 'Beastmaster', 39: 'Queen of Pain', 40: 'Venomancer', 41: 'Faceless Void',
                    42: 'Wraith King',
                    43: 'Death Prophet', 44: 'Phantom Assassin', 45: 'Pugna', 46: 'Templar Assassin', 47: 'Viper',
                    48: 'Luna',
                    49: 'Dragon Knight', 50: 'Dazzle', 51: 'Clockwerk', 52: 'Leshrac', 53: "Nature's Prophet",
                    54: 'Lifestealer',
                    55: 'Dark Seer', 56: 'Clinkz', 57: 'Omniknight', 58: 'Enchantress', 59: 'Huskar',
                    60: 'Night Stalker',
                    61: 'Broodmother', 62: 'Bounty Hunter', 63: 'Weaver', 64: 'Jakiro', 65: 'Batrider', 66: 'Chen',
                    67: 'Spectre',
                    68: 'Ancient Apparition', 69: 'Doom', 70: 'Ursa', 71: 'Spirit Breaker', 72: 'Gyrocopter',
                    73: 'Alchemist',
                    74: 'Invoker', 75: 'Silencer', 76: 'Outworld Destroyer', 77: 'Lycan', 78: 'Brewmaster',
                    79: 'Shadow Demon',
                    80: 'Lone Druid', 81: 'Chaos Knight', 82: 'Meepo', 83: 'Treant Protector', 84: 'Ogre Magi',
                    85: 'Undying',
                    86: 'Rubick', 87: 'Disruptor', 88: 'Nyx Assassin', 89: 'Naga Siren', 90: 'Keeper of the Light',
                    91: 'Io',
                    92: 'Visage', 93: 'Slark', 94: 'Medusa', 95: 'Troll Warlord', 96: 'Centaur Warrunner', 97: 'Magnus',
                    98: 'Timbersaw', 99: 'Bristleback', 100: 'Tusk', 101: 'Skywrath Mage', 102: 'Abaddon',
                    103: 'Elder Titan',
                    104: 'Legion Commander', 105: 'Techies', 106: 'Ember Spirit', 107: 'Earth Spirit', 108: 'Underlord',
                    109: 'Terrorblade', 110: 'Phoenix', 111: 'Oracle', 112: 'Winter Wyvern', 113: 'Arc Warden',
                    114: 'Monkey King',
                    119: 'Dark Willow', 120: 'Pangolier', 121: 'Grimstroke', 123: 'Hoodwink', 126: 'Void Spirit',
                    128: 'Snapfire',
                    129: 'Mars', 135: 'Dawnbreaker', 136: 'Marci', 137: 'Primal Beast', 138: 'Muerta'}

hero_ids = {}
for i in hero_ids_default.keys():
    hero_ids[i] = hero_ids_default[i].lower()

brackets = {'рекрут': 'HERALD', 'страж': 'GUARDIAN', 'рыцарь': 'CRUSADER', 'герой': 'ARCHON', 'легенда': 'LEGEND',
            'властелин': 'ANCIENT', 'божество': 'DIVINE', 'титан': 'IMMORTAL'}