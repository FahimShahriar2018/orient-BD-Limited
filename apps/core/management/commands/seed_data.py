from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from apps.accounts.models import User
from apps.catalog.models import Category, Product, ProductImage, Review, Brand
from apps.orders.models import Coupon
from apps.service.models import Branch


class Command(BaseCommand):
    help = 'Seeds Orient Computers database with full official categories, partner brands, products, online images, coupons, and branches.'


    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting Orient Computers database seeding...'))

        # 1. Create Users
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@orientcomputers.com.bd',
                'first_name': 'Orient',
                'last_name': 'Administrator',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'phone': '+880 1711-000001',
                'address_division': 'Dhaka',
                'address_district': 'Dhaka',
                'address_street': 'Orient Corporate Tower, 32 Motijheel C/A',
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Admin user created (admin / admin123)'))

        demo_customer, created = User.objects.get_or_create(
            username='fahim',
            defaults={
                'email': 'fahim@orient.bd',
                'first_name': 'Fahim',
                'last_name': 'Shahriar',
                'role': 'customer',
                'phone': '+880 1711-123456',
                'address_division': 'Dhaka',
                'address_district': 'Dhaka',
                'address_street': 'House 14, Road 7, Dhanmondi',
                'address_postal': '1205',
            }
        )
        if created:
            demo_customer.set_password('customer123')
            demo_customer.save()
            self.stdout.write(self.style.SUCCESS('Demo customer created (fahim / customer123)'))

        # 2. Create Orient Categories
        categories_data = [
            {
                'name': 'PC Component', 'slug': 'pc-component', 'icon': 'bi-cpu',
                'desc': 'Processors, Motherboards, RAM, NVMe SSDs, Graphics Cards, PSUs and Gaming Casings.'
            },
            {
                'name': 'AVR (Voltage Regulator)', 'slug': 'avr', 'icon': 'bi-lightning-charge',
                'desc': 'Apollo, MaxGreen & Kstar Servo Motor and Relay Type Automatic Voltage Regulators.'
            },
            {
                'name': 'Renewable Energy', 'slug': 'renewable-energy', 'icon': 'bi-sun',
                'desc': 'Solar Hybrid Inverters, Monocrystalline Solar Panels, MPPT Charge Controllers & Solar Storage.'
            },
            {
                'name': 'UPS (Offline & Online)', 'slug': 'ups', 'icon': 'bi-battery-charging',
                'desc': 'APC, MaxGreen, Apollo, Santak & Vertiv Enterprise Online and Desktop Offline UPS systems.'
            },
            {
                'name': 'IPS (Instant Power Supply)', 'slug': 'ips', 'icon': 'bi-plug',
                'desc': 'Pure Sine Wave Home IPS, Commercial Inverters & Automatic Power Backup units from Luminous & Microtek.'
            },
            {
                'name': 'Battery', 'slug': 'battery', 'icon': 'bi-battery-full',
                'desc': 'Deep Cycle Tubular Batteries, SMF VRLA Batteries & Lithium LiFePO4 Battery Packs from Hamko, Eastern & Long.'
            },
            {
                'name': 'Telecom Power', 'slug': 'telecom', 'icon': 'bi-broadcast-pin',
                'desc': 'High-efficiency Telecom Rectifier Systems, DC-to-DC Converters & Industrial Power Distribution units.'
            },
            {
                'name': 'Audio-Visual', 'slug': 'audio-visual', 'icon': 'bi-camera-video',
                'desc': 'Interactive Flat Panels, Digital Smart Podiums, 4K Projectors & Enterprise Video Conference Systems.'
            },
            {
                'name': 'Office Equipment', 'slug': 'office-equipment', 'icon': 'bi-printer',
                'desc': 'Digital Heavy-Duty Photocopiers, Currency Counting Machines, Paper Shredders & Time Attendance.'
            },
        ]

        cat_map = {}
        for c in categories_data:
            cat_obj, _ = Category.objects.update_or_create(
                slug=c['slug'],
                defaults={'name': c['name'], 'icon': c['icon'], 'description': c['desc']}
            )
            cat_map[c['slug']] = cat_obj

        # Clean up legacy non-Orient categories and unreferenced SKUs
        legacy_skus = ['GPU-MSI-4070TIS-SLIM', 'CPU-INT-14900K-LGA1700', 'MB-ASUS-X670E-HERO', 'RAM-COR-DDR5-32GB-RGB', 'NET-MIK-CCR2004', 'LAP-ROG-SCAR16-2026']
        Product.objects.filter(sku__in=legacy_skus).delete()
        Category.objects.exclude(slug__in=[c['slug'] for c in categories_data]).delete()

        # 3. Create Hardware Products with online image URLs
        products_data = [
            # --- PC Components ---
            {
                'name': 'ASUS ROG Strix GeForce RTX 4080 Super OC Edition 16GB',
                'slug': 'asus-rog-strix-rtx-4080-super-16gb',
                'sku': 'GPU-ASUS-4080S-STRIX',
                'brand': 'ASUS',
                'category': cat_map['pc-component'],
                'price': Decimal('148000.00'),
                'discount_price': Decimal('142500.00'),
                'count_in_stock': 12,
                'description': 'The ROG Strix GeForce RTX 4080 SUPER brings immense compute headroom for 4K ray-traced gaming. Features axial-tech fans scaled up for 23% more airflow, patented vapor chamber with milled heatspreader, and 3.5-slot design.',
                'short_specs': [
                    '16GB GDDR6X 256-bit Memory',
                    '2670 MHz Boost Clock (OC Mode)',
                    '10,240 CUDA Cores with DLSS 3.5',
                    '3.5-Slot Axial-Tech Triple Fan Cooler',
                ],
                'technical_specs': {
                    'Graphic Engine': 'NVIDIA GeForce RTX 4080 SUPER',
                    'CUDA Cores': '10,240',
                    'Video Memory': '16GB GDDR6X',
                    'Memory Bus': '256-bit',
                    'Engine Clock (OC)': '2670 MHz',
                    'Display Outputs': '2x HDMI 2.1a, 3x DisplayPort 1.4a',
                    'Recommended PSU': '850W',
                },
                'is_featured': True,
                'is_deal_of_day': True,
                'warranty': '3 Years Official Brand Replacement Warranty',
                'rating': Decimal('4.9'),
                'num_reviews': 28,
                'images': [
                    'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=800&q=80',
                    'https://images.unsplash.com/photo-1591488320449-011701bb6704?auto=format&fit=crop&w=800&q=80',
                ]
            },
            {
                'name': 'AMD Ryzen 7 7800X3D Desktop Processor (8 Cores, 16 Threads)',
                'slug': 'amd-ryzen-7-7800x3d-processor',
                'sku': 'CPU-AMD-7800X3D-AM5',
                'brand': 'AMD',
                'category': cat_map['pc-component'],
                'price': Decimal('52000.00'),
                'discount_price': Decimal('48500.00'),
                'count_in_stock': 25,
                'description': 'The undisputed champion of gaming processors. Features revolutionary AMD 3D V-Cache technology with a massive 104MB total cache for unmatched frame rates in competitive Esports and open-world titles.',
                'short_specs': [
                    '8 Cores / 16 Threads (Zen 4)',
                    'Up to 5.0 GHz Max Boost Clock',
                    'Massive 104MB Cache (3D V-Cache)',
                    'Socket AM5 with DDR5 & PCIe 5.0 Support',
                ],
                'technical_specs': {
                    'Socket': 'AM5',
                    'Cores / Threads': '8 / 16',
                    'Base Clock': '4.2 GHz',
                    'Boost Clock': 'Up to 5.0 GHz',
                    'L3 Cache': '96MB 3D V-Cache',
                    'TDP': '120W',
                },
                'is_featured': True,
                'is_deal_of_day': True,
                'warranty': '3 Years Official AMD Warranty',
                'rating': Decimal('5.0'),
                'num_reviews': 42,
                'images': [
                    'https://images.unsplash.com/photo-1555680202-c86f0e12f086?auto=format&fit=crop&w=800&q=80',
                ]
            },
            {
                'name': 'Samsung 990 Pro 2TB PCIe Gen 4.0 x4 M.2 NVMe SSD (7450 MB/s)',
                'slug': 'samsung-990-pro-2tb-nvme-ssd',
                'sku': 'SSD-SAM-990PRO-2TB',
                'brand': 'Samsung',
                'category': cat_map['pc-component'],
                'price': Decimal('24000.00'),
                'discount_price': Decimal('22500.00'),
                'count_in_stock': 20,
                'description': 'Peak PCIe 4.0 performance with sequential read speeds up to 7450 MB/s and write speeds up to 6900 MB/s. Nickel-coated controller with Dynamic Thermal Guard.',
                'short_specs': [
                    '2TB NVMe M.2 (2280) Form Factor',
                    'Up to 7,450 MB/s Read & 6,900 MB/s Write',
                    'Samsung Pascal Controller & V-NAND TLC',
                    '1200 TBW Endurance Rating',
                ],
                'technical_specs': {
                    'Interface': 'PCIe 4.0 x4, NVMe 2.0',
                    'Sequential Read': '7,450 MB/s',
                    'Sequential Write': '6,900 MB/s',
                    'Form Factor': 'M.2 2280',
                },
                'is_featured': True,
                'warranty': '5 Years Official Brand Warranty',
                'rating': Decimal('4.9'),
                'num_reviews': 31,
                'images': [
                    'https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?auto=format&fit=crop&w=800&q=80',
                ]
            },

            # --- AVR (Automatic Voltage Regulators) ---
            {
                'name': 'Apollo 2000VA Servo Motor Automatic Voltage Regulator (AVR)',
                'slug': 'apollo-2000va-servo-avr',
                'sku': 'AVR-APOLLO-2000VA',
                'brand': 'Apollo',
                'category': cat_map['avr'],
                'price': Decimal('8500.00'),
                'discount_price': Decimal('7800.00'),
                'count_in_stock': 18,
                'description': 'Heavy-duty 2000VA Servo Motor Automatic Voltage Regulator designed specifically for Bangladesh grid conditions. Stabilizes unstable input voltage (140V-260V) to steady 220V +/- 3% pure output for precision electronics, servers, and medical gear.',
                'short_specs': [
                    '2000VA / 1600W Capacity',
                    'High Precision Servo Motor Stabilization (±3%)',
                    'Wide Input Range: 140V - 260V AC',
                    'Digital Dual Meter Voltage Display',
                ],
                'technical_specs': {
                    'Capacity': '2000VA / 1600W',
                    'Technology': 'Servo Motor Control',
                    'Input Voltage': '140V ~ 260V AC, 50/60Hz',
                    'Output Voltage': '220V AC ± 3%',
                    'Protection': 'Over-voltage, Under-voltage, Short-circuit, Thermal Overload',
                    'Efficiency': '> 95%',
                },
                'is_featured': True,
                'is_deal_of_day': True,
                'warranty': '1 Year Official Brand Warranty',
                'rating': Decimal('4.8'),
                'num_reviews': 19,
                'images': [
                    'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=800&q=80',
                ]
            },
            {
                'name': 'MaxGreen 5000VA Digital Relay Automatic Voltage Regulator',
                'slug': 'maxgreen-5000va-relay-avr',
                'sku': 'AVR-MG-5000VA',
                'brand': 'MaxGreen',
                'category': cat_map['avr'],
                'price': Decimal('16500.00'),
                'discount_price': Decimal('15200.00'),
                'count_in_stock': 10,
                'description': 'High-power 5kVA digital voltage stabilizer suitable for entire apartments, air conditioners, photocopiers, and heavy equipment. Zero cross switching ensures flicker-free voltage regulation.',
                'short_specs': [
                    '5000VA / 4000W Heavy Duty Load',
                    'MCU Digital Relay Controlled Step-Up/Step-Down',
                    'Input Voltage Range: 110V - 270V AC',
                    'Time Delay Protection Switch (6s / 180s)',
                ],
                'technical_specs': {
                    'Power Capacity': '5000VA / 4000W',
                    'Input Range': '110V - 270V',
                    'Output': '220V ± 8%',
                    'Display': 'Digital LED Input/Output Meter',
                },
                'is_featured': False,
                'warranty': '1 Year Full Replacement Warranty',
                'rating': Decimal('4.7'),
                'num_reviews': 14,
                'images': [
                    'https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?auto=format&fit=crop&w=800&q=80',
                ]
            },

            # --- Renewable Energy ---
            {
                'name': 'Luminous Solar Hybrid Inverter NXG 1800 (1500VA / 24V Pure Sine Wave)',
                'slug': 'luminous-solar-hybrid-inverter-nxg-1800',
                'sku': 'SOLAR-LUM-NXG1800',
                'brand': 'Luminous',
                'category': cat_map['renewable-energy'],
                'price': Decimal('28500.00'),
                'discount_price': Decimal('26800.00'),
                'count_in_stock': 8,
                'description': 'Next-generation Intelligent Solar Hybrid Inverter with built-in ISOT technology (Intelligent Solar Optimization Technique) saving up to 3-5 units of grid electricity daily. Pure sine wave output protects sensitive household appliances.',
                'short_specs': [
                    '1500VA / 24V Dual Battery Architecture',
                    'Supports up to 1200W Solar PV Module Panels',
                    'Intelligent Solar Optimization Technique (ISOT)',
                    'Pure Sine Wave Output for Sensitive Hardware',
                ],
                'technical_specs': {
                    'VA Rating': '1500 VA',
                    'System Voltage': '24V DC',
                    'Max Solar Panel Capacity': '1200 Wp',
                    'Solar Charge Controller': 'PWM with High Efficiency',
                    'Output Waveform': 'Pure Sine Wave',
                },
                'is_featured': True,
                'is_deal_of_day': True,
                'warranty': '2 Years Official Luminous Warranty',
                'rating': Decimal('4.9'),
                'num_reviews': 22,
                'images': [
                    'https://images.unsplash.com/photo-1509391365360-2e959784a276?auto=format&fit=crop&w=800&q=80',
                ]
            },
            {
                'name': 'Longi Solar Hi-MO 6 Explorer 580W Monocrystalline Half-Cell Solar Panel',
                'slug': 'longi-solar-himo6-580w-mono-panel',
                'sku': 'SOLAR-LONGI-580W',
                'brand': 'Longi',
                'category': cat_map['renewable-energy'],
                'price': Decimal('19800.00'),
                'discount_price': Decimal('18500.00'),
                'count_in_stock': 35,
                'description': 'High efficiency HPBC cell technology offering 22.5% module efficiency. Exceptional performance under low light and high ambient temperature climates.',
                'short_specs': [
                    '580W Peak Power Output',
                    '22.5% Maximum Module Efficiency',
                    'Monocrystalline Half-Cut Cell Design',
                    'Anti-PID and High Wind/Snow Load Tested',
                ],
                'technical_specs': {
                    'Peak Power (Pmax)': '580W',
                    'Efficiency': '22.5%',
                    'Cell Type': 'Monocrystalline HPBC',
                    'Dimensions': '2278 x 1134 x 35 mm',
                },
                'is_featured': False,
                'warranty': '12 Years Product / 25 Years Linear Power Warranty',
                'rating': Decimal('5.0'),
                'num_reviews': 17,
                'images': [
                    'https://images.unsplash.com/photo-1508873696983-2df5293cb32f?auto=format&fit=crop&w=800&q=80',
                ]
            },

            # --- UPS (Offline & Online) ---
            {
                'name': 'APC Smart-UPS 3000VA / 2700W LCD 230V Online UPS (SRT3000XLI)',
                'slug': 'apc-smart-ups-on-line-3000va-srt3000xli',
                'sku': 'UPS-APC-SRT3000XLI',
                'brand': 'APC',
                'category': cat_map['ups'],
                'price': Decimal('185000.00'),
                'discount_price': Decimal('178000.00'),
                'count_in_stock': 6,
                'description': 'High density, double-conversion on-line power protection with scalable runtime. Ideal for enterprise servers, voice/data networks, medical labs, and light industrial applications.',
                'short_specs': [
                    '3000VA / 2700W Double-Conversion Online Topology',
                    'Zero Millisecond Transfer Time (0ms)',
                    'Pure Sine Wave True Online Output',
                    'Interactive Multi-Function LCD Status Console',
                ],
                'technical_specs': {
                    'Output Power Capacity': '3000VA / 2700 Watts',
                    'Nominal Output Voltage': '230V',
                    'Topology': 'Double Conversion Online',
                    'Waveform Type': 'Sine wave',
                    'Transfer Time': '0 ms (Zero)',
                    'Communication': 'SmartSlot, USB, Serial',
                },
                'is_featured': True,
                'is_deal_of_day': False,
                'warranty': '2 Years Official APC Warranty including Battery',
                'rating': Decimal('5.0'),
                'num_reviews': 15,
                'images': [
                    'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=800&q=80',
                ]
            },
            {
                'name': 'Apollo 1200VA Offline UPS with Built-In AVR',
                'slug': 'apollo-1200va-offline-ups',
                'sku': 'UPS-APOLLO-1200VA',
                'brand': 'Apollo',
                'category': cat_map['ups'],
                'price': Decimal('6200.00'),
                'discount_price': Decimal('5800.00'),
                'count_in_stock': 40,
                'description': 'Reliable desktop power backup with dual internal 12V/7.2Ah batteries, wide input AVR range, and cold start function. Backs up desktop PCs, monitors, and Wi-Fi routers for 25-40 minutes.',
                'short_specs': [
                    '1200VA / 720W Output Capacity',
                    'Dual 12V 7.2Ah Heavy Duty Batteries Built-in',
                    'Automatic Voltage Regulation (AVR) Boost/Buck',
                    'Cold Start Function & Surge Protection',
                ],
                'technical_specs': {
                    'Capacity': '1200VA / 720W',
                    'Battery': '2x 12V / 7.2Ah Lead-Acid',
                    'Backup Time': '25 - 40 Mins (Standard Desktop Load)',
                    'Transfer Time': '2-6 ms typical',
                },
                'is_featured': True,
                'warranty': '1 Year Full Warranty with Battery',
                'rating': Decimal('4.7'),
                'num_reviews': 38,
                'images': [
                    'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=800&q=80',
                ]
            },

            # --- IPS (Instant Power Supply) ---
            {
                'name': 'Microtek Super Power 1100 Pure Sine Wave Home IPS Inverter',
                'slug': 'microtek-super-power-1100-pure-sine-wave-ips',
                'sku': 'IPS-MICRO-1100VA',
                'brand': 'Microtek',
                'category': cat_map['ips'],
                'price': Decimal('14500.00'),
                'discount_price': Decimal('13200.00'),
                'count_in_stock': 15,
                'description': 'Microcontroller based intelligent Pure Sine Wave IPS Inverter system designed with Dura-Retain technology for long battery life and completely noiseless operation for fans and lights during power outages.',
                'short_specs': [
                    '950VA / 760W Pure Sine Wave Output',
                    'Supports 1x 12V (100Ah - 220Ah) Battery',
                    'Smart Battery Charging with Multi-Stage Control',
                    'Powers 5 Fans, 8 LED Lights, 1 LED TV & Router',
                ],
                'technical_specs': {
                    'Capacity': '950VA / 760W',
                    'Input Voltage': '100V - 300V',
                    'Output Waveform': 'Pure Sine Wave',
                    'Battery Support': '12V Single Battery',
                    'Switching Time': '< 10 ms',
                },
                'is_featured': True,
                'is_deal_of_day': True,
                'warranty': '2 Years Replacement Warranty',
                'rating': Decimal('4.8'),
                'num_reviews': 27,
                'images': [
                    'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80',
                ]
            },
            {
                'name': 'Luminous Cruze 2kVA / 24V Pure Sine Wave Commercial IPS Inverter',
                'slug': 'luminous-cruze-2kva-24v-sine-wave-ips',
                'sku': 'IPS-LUM-CRUZE-2KVA',
                'brand': 'Luminous',
                'category': cat_map['ips'],
                'price': Decimal('32000.00'),
                'discount_price': Decimal('29800.00'),
                'count_in_stock': 9,
                'description': 'Heavy duty commercial inverter capable of running refrigerators, laser printers, computers, and medical equipment smoothly without interruption.',
                'short_specs': [
                    '2000VA / 1600W Heavy Load Capacity',
                    '24V System Architecture (2x Batteries)',
                    'Adaptive Battery Charging Management (ABCC)',
                    'Comprehensive LCD Display with Time Remaining',
                ],
                'technical_specs': {
                    'Capacity': '2000VA / 1600W',
                    'DC Voltage': '24V',
                    'Charging Current': '21A Fast Charging',
                },
                'is_featured': False,
                'warranty': '2 Years Official Warranty',
                'rating': Decimal('4.9'),
                'num_reviews': 16,
                'images': [
                    'https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80',
                ]
            },

            # --- Battery ---
            {
                'name': 'Hamko Combo 200Ah 12V Deep Cycle Tubular Solar & IPS Battery',
                'slug': 'hamko-combo-200ah-tubular-battery',
                'sku': 'BAT-HAMKO-200AH-TUB',
                'brand': 'Hamko',
                'category': cat_map['battery'],
                'price': Decimal('26500.00'),
                'discount_price': Decimal('24800.00'),
                'count_in_stock': 22,
                'description': 'Engineered with spine gauntlet technology for high cyclical life (over 1500 cycles at 80% DOD). Extremely resilient to deep discharges and prolonged power cuts in Bangladesh.',
                'short_specs': [
                    '200Ah Capacity @ C20 Rating',
                    'High Pressure Die-Cast Tubular Positive Plates',
                    'Extra Heavy Duty Thick Plates for Long Lifespan (5-7 Years)',
                    'Float Vent Plugs with Electrolyte Level Indicators',
                ],
                'technical_specs': {
                    'Nominal Voltage': '12V',
                    'Rated Capacity': '200Ah @ 20Hr',
                    'Technology': 'Flooded Tubular Lead-Acid',
                    'Weight (Filled)': '62 kg approx.',
                },
                'is_featured': True,
                'warranty': '30 Months Official Hamko Replacement Warranty',
                'rating': Decimal('4.9'),
                'num_reviews': 34,
                'images': [
                    'https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?auto=format&fit=crop&w=800&q=80',
                ]
            },
            {
                'name': 'Eastern 150Ah Tubular Deep Cycle IPS & Solar Battery',
                'slug': 'eastern-150ah-tubular-ips-battery',
                'sku': 'BAT-EASTERN-150AH',
                'brand': 'Eastern',
                'category': cat_map['battery'],
                'price': Decimal('21000.00'),
                'discount_price': Decimal('19500.00'),
                'count_in_stock': 16,
                'description': 'Superior quality tubular deep discharge battery built for home IPS, UPS, and solar applications with minimum maintenance.',
                'short_specs': [
                    '150Ah @ C20 Deep Cycle Battery',
                    'Tubular Positive Grid Design',
                    'Low Antimony Alloy for Low Self Discharge',
                ],
                'technical_specs': {
                    'Voltage': '12V',
                    'Capacity': '150Ah',
                    'Plate Type': 'Tubular',
                },
                'is_featured': False,
                'warranty': '24 Months Replacement Warranty',
                'rating': Decimal('4.8'),
                'num_reviews': 21,
                'images': [
                    'https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?auto=format&fit=crop&w=800&q=80',
                ]
            },

            # --- Telecom Power ---
            {
                'name': 'Vertiv NetSure 731 NQA High-Efficiency Telecom Power System (48V / 300A)',
                'slug': 'vertiv-netsure-731-telecom-power-system',
                'sku': 'TEL-VERTIV-731NQA',
                'brand': 'Vertiv',
                'category': cat_map['telecom'],
                'price': Decimal('450000.00'),
                'discount_price': Decimal('425000.00'),
                'count_in_stock': 3,
                'description': 'Modular DC power solution designed for wireless base stations, core telecom shelters, and edge data centers. Incorporates eSure high-efficiency 3000W rectifiers operating at up to 96.5% conversion efficiency.',
                'short_specs': [
                    '48V DC Nominal Output (Expandable to 300A)',
                    'Up to 96.5% Ultra-High Rectifier Efficiency',
                    'Modular Hot-Swappable Rectifier Slots',
                    'Advanced NCU Remote Network Controller (SNMP/HTTP)',
                ],
                'technical_specs': {
                    'Output Voltage': '-48V DC (-42V to -58V)',
                    'System Capacity': '300A (16 kW)',
                    'Rectifier Compatibility': 'eSure R48-3000e3 (3000W)',
                    'Input AC Range': '85V - 300V AC',
                    'Distribution': 'Integrated Battery and Load Circuit Breakers',
                },
                'is_featured': True,
                'warranty': '2 Years Enterprise Warranty & SLA Support',
                'rating': Decimal('5.0'),
                'num_reviews': 8,
                'images': [
                    'https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=800&q=80',
                ]
            },

            # --- Audio-Visual ---
            {
                'name': 'Maxhub 75" V6 Classic Interactive Flat Panel Display (4K UHD Smart Touch)',
                'slug': 'maxhub-75-v6-classic-interactive-panel',
                'sku': 'AV-MAXHUB-75V6',
                'brand': 'Maxhub',
                'category': cat_map['audio-visual'],
                'price': Decimal('345000.00'),
                'discount_price': Decimal('320000.00'),
                'count_in_stock': 5,
                'description': 'Next-level smart collaboration board featuring 4K UHD Anti-Glare glass, 48MP integrated AI camera with auto-framing, 8-array beamforming microphone with noise cancellation, and seamless wireless BYOD screen sharing.',
                'short_specs': [
                    '75" 4K UHD (3840 x 2160) Anti-Glare IPS Display',
                    '20-Point Multi-Touch Writing with 1mm Accuracy',
                    'Integrated 48MP AI Auto-Framing Conference Camera',
                    '8-Array Beamforming Microphones (8m Pickup Range)',
                ],
                'technical_specs': {
                    'Screen Size': '75 inches 4K UHD',
                    'Touch Points': '20 Points High Precision IR Touch',
                    'Camera': '48 Megapixels AI Framing',
                    'Audio': '2x 10W + 20W Subwoofer',
                    'Operating System': 'Android 11 & Optional Windows 11 OPS PC Slot',
                },
                'is_featured': True,
                'is_deal_of_day': True,
                'warranty': '3 Years Official Full Hardware Warranty',
                'rating': Decimal('5.0'),
                'num_reviews': 12,
                'images': [
                    'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=800&q=80',
                ]
            },
            {
                'name': 'ViewSonic PX701-4K 3200 ANSI Lumens High Refresh 4K Projector',
                'slug': 'viewsonic-px701-4k-projector',
                'sku': 'AV-VIEWSONIC-PX701-4K',
                'brand': 'ViewSonic',
                'category': cat_map['audio-visual'],
                'price': Decimal('125000.00'),
                'discount_price': Decimal('118000.00'),
                'count_in_stock': 8,
                'description': 'True 4K HDR entertainment and auditorium presentation projector with 3,200 ANSI Lumens brightness and ultra-fast 240Hz refresh rate / 4.2ms low input lag.',
                'short_specs': [
                    'True 4K UHD (3840x2160) Resolution with HDR/HLG',
                    '3,200 ANSI Lumens High Brightness',
                    'Ultra-Fast 240Hz Refresh Rate with 4.2ms Input Lag',
                    'SuperEco+ Mode with up to 20,000 Hours Lamp Life',
                ],
                'technical_specs': {
                    'Resolution': '3840 x 2160 (4K UHD)',
                    'Brightness': '3,200 ANSI Lumens',
                    'Contrast Ratio': '12000:1',
                    'Throw Ratio': '1.5 - 1.65',
                },
                'is_featured': False,
                'warranty': '2 Years Official Warranty (1 Year / 1000h Lamp)',
                'rating': Decimal('4.8'),
                'num_reviews': 19,
                'images': [
                    'https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=800&q=80',
                ]
            },

            # --- Office Equipment ---
            {
                'name': 'Canon imageRUNNER 2625i Multi-Function Digital Photocopier (A3 / Network / Duplex)',
                'slug': 'canon-imagerunner-2625i-photocopier',
                'sku': 'OFF-CANON-IR2625I',
                'brand': 'Canon',
                'category': cat_map['office-equipment'],
                'price': Decimal('285000.00'),
                'discount_price': Decimal('265000.00'),
                'count_in_stock': 4,
                'description': 'Robust, reliable, and high-speed A3 monochrome multi-function printer engineered to withstand demanding enterprise workloads. Offers print, copy, scan, and optional fax with advanced document security.',
                'short_specs': [
                    '25 Pages Per Minute (PPM) High-Speed A3/A4 Printing',
                    'Standard Automatic Duplex Printing & DADF Feeder',
                    '7-inch Color TFT LCD Touch Screen Interface',
                    'Gigabit Ethernet, Wi-Fi & Mobile Cloud Print Support',
                ],
                'technical_specs': {
                    'Print Speed': '25 ppm (A4), 15 ppm (A3)',
                    'Resolution': '1200 x 1200 dpi',
                    'Memory': '2.0 GB RAM',
                    'Paper Capacity': 'Standard 1,200 sheets (Max 2,300 sheets)',
                    'Duty Cycle': 'Up to 50,000 pages per month',
                },
                'is_featured': True,
                'is_deal_of_day': True,
                'warranty': '1 Year Service Warranty & Free Installation in Dhaka',
                'rating': Decimal('4.9'),
                'num_reviews': 18,
                'images': [
                    'https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?auto=format&fit=crop&w=800&q=80',
                ]
            },
            {
                'name': 'Kisan Newton A Heavy-Duty 2-Pocket Currency Counter & Fake Note Detector',
                'slug': 'kisan-newton-a-currency-counter',
                'sku': 'OFF-KISAN-NEWTON-A',
                'brand': 'Kisan',
                'category': cat_map['office-equipment'],
                'price': Decimal('165000.00'),
                'discount_price': Decimal('155000.00'),
                'count_in_stock': 7,
                'description': 'Bank-grade 2-pocket currency discriminator with full image CIS sensor, multi-currency detection (BDT, USD, EUR, GBP, SAR, INR), and counterfeit detection.',
                'short_specs': [
                    'Dual Pocket Architecture (Reject Pocket for Non-Stop Counting)',
                    'Full Dual-Color CIS Image Sensor Counterfeit Detection',
                    'Counts and Denominates Mixed Bangladeshi Taka (BDT) Bills',
                    '4.3" Full Color Touchscreen Interface',
                ],
                'technical_specs': {
                    'Speed': 'Up to 1500 notes/min',
                    'Hopper Capacity': '600 notes',
                    'Stacker Capacity': '200 notes',
                    'Reject Pocket': '100 notes',
                },
                'is_featured': False,
                'warranty': '1 Year Free Servicing & Replacement Warranty',
                'rating': Decimal('5.0'),
                'num_reviews': 14,
                'images': [
                    'https://images.unsplash.com/photo-1580519542036-c47de6196ba5?auto=format&fit=crop&w=800&q=80',
                ]
            },
            # --- Live Site Parity: Trendsonic, Patriot, ViewSonic, Sako, Mofii ---
            {
                'name': 'Trendsonic TS22IPS100B 21.45" 100Hz Borderless FHD IPS Monitor',
                'slug': 'trendsonic-ts22ips100b-21-45-inch-100hz-fhd-monitor',
                'sku': 'MON-TRENDSONIC-TS22IPS100B',
                'brand': 'TrendSonic',
                'category': cat_map['pc-component'],
                'price': Decimal('8900.00'),
                'discount_price': Decimal('8200.00'),
                'count_in_stock': 40,
                'description': 'Trendsonic TS22IPS100B features a 21.45-inch Full HD (1920x1080) IPS display with 100Hz refresh rate, 3-sided frameless design, Low Blue Light and Flicker-Free technology.',
                'short_specs': [
                    '21.45" Full HD (1920 x 1080) IPS Panel',
                    'Smooth 100Hz Refresh Rate (HDMI)',
                    '3-Side Borderless Ultra-Slim Bezel Design',
                    'Eye-Care Low Blue Light & Flicker-Free',
                ],
                'technical_specs': {
                    'Screen Size': '21.45 Inches',
                    'Panel Type': 'IPS Wide Viewing Angle',
                    'Resolution': '1920 x 1080 (FHD)',
                    'Refresh Rate': '100Hz',
                    'Response Time': '5ms (GTG)',
                    'Connectivity': '1x HDMI 1.4, 1x VGA',
                },
                'is_featured': True,
                'is_deal_of_day': True,
                'warranty': '3 Years Official Brand Warranty',
                'rating': Decimal('4.8'),
                'num_reviews': 31,
                'images': [
                    'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=800&q=80',
                ]
            },
            {
                'name': 'Patriot Viper Venom RGB 32GB (2x16GB) DDR5 6000MHz Desktop Gaming RAM',
                'slug': 'patriot-viper-venom-rgb-32gb-ddr5-6000mhz-ram',
                'sku': 'RAM-PATRIOT-VIPER-32GB-D5',
                'brand': 'Viper Gaming',
                'category': cat_map['pc-component'],
                'price': Decimal('16500.00'),
                'discount_price': Decimal('15200.00'),
                'count_in_stock': 35,
                'description': 'Patriot Viper Venom DDR5 features advanced aluminum heatshield with dynamic full-spectrum RGB lighting, on-die ECC error correction, and Intel XMP 3.0 / AMD EXPO profile support.',
                'short_specs': [
                    '32GB Dual Channel Kit (2x 16GB)',
                    'Blazing 6000MHz Speed (CL36)',
                    'Dynamic Full-Spectrum Addressable RGB',
                    'Intel XMP 3.0 & AMD EXPO Ready',
                ],
                'technical_specs': {
                    'Capacity': '32GB (2x 16GB)',
                    'Frequency': '6000MHz',
                    'CAS Latency': 'CL36-36-36-76',
                    'Voltage': '1.35V',
                    'Heatshield': 'Matte Black Aluminum',
                },
                'is_featured': True,
                'warranty': 'Lifetime Limited Official Warranty',
                'rating': Decimal('4.9'),
                'num_reviews': 24,
                'images': [
                    'https://images.unsplash.com/photo-1562976540-1502c2145186?auto=format&fit=crop&w=800&q=80',
                ]
            },
            {
                'name': 'Mofii Sweet 2.4G Wireless Retro Colorful Mixed Keyboard & Mouse Combo',
                'slug': 'mofii-sweet-wireless-retro-keyboard-mouse-combo',
                'sku': 'KB-MOFII-SWEET-WIRELESS',
                'brand': 'Mofii',
                'category': cat_map['pc-component'],
                'price': Decimal('3200.00'),
                'discount_price': Decimal('2850.00'),
                'count_in_stock': 50,
                'description': 'Vintage typewriter style round keys with aesthetic multi-color palette, 2.4GHz stable wireless connection up to 10 meters, and energy saving sleep mode.',
                'short_specs': [
                    'Typewriter-Inspired Round Keycaps',
                    '2.4GHz Wireless Nano Receiver (10m Range)',
                    'Ergonomic Optical Mouse with Adjustable DPI',
                    'Long Battery Life with Auto-Sleep Power Saving',
                ],
                'technical_specs': {
                    'Keys': '104 Full-Size Keys',
                    'Connectivity': '2.4GHz USB Dongle',
                    'Compatibility': 'Windows, MacOS, Android',
                },
                'is_featured': False,
                'warranty': '1 Year Replacement Warranty',
                'rating': Decimal('4.7'),
                'num_reviews': 18,
                'images': [
                    'https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=80',
                ]
            },
            # --- Call For Price High-Ticket Enterprise Hardware ---
            {
                'name': 'ViewSonic IFP8650-5 86" 4K UHD Interactive Flat Panel (EDLA Certified)',
                'slug': 'viewsonic-ifp8650-5-86-inch-4k-interactive-panel',
                'sku': 'AV-VIEWSONIC-IFP8650-86',
                'brand': 'ViewSonic',
                'category': cat_map['audio-visual'],
                'price': Decimal('520000.00'),
                'discount_price': Decimal('0.00'),
                'is_call_for_price': True,
                'count_in_stock': 6,
                'description': 'ViewSonic ViewBoard IFP8650-5 delivers revolutionary interactive education and enterprise collaboration. Built-in Android 13 EDLA Google certified, 40-point touch, front facing speakers with subwoofer.',
                'short_specs': [
                    '86" 4K Ultra HD (3840 x 2160) Anti-Glare Display',
                    '40-Point Ultra-Fine Touch (Dual Pen Support)',
                    'Official Android 13 EDLA with Google Play Services',
                    '2x 15W Speakers + 20W Built-in Subwoofer',
                ],
                'technical_specs': {
                    'Display': '86" IPS DLED Backlight',
                    'Brightness': '450 cd/m2',
                    'Contrast Ratio': '1200:1 (typ), 5000:1 (DCR)',
                    'CPU / RAM': 'Octa-Core Processor, 8GB RAM, 64GB ROM',
                    'Ports': '4x HDMI 2.0, 1x USB-C (65W PD), 4x USB 3.0, Gigabit LAN',
                },
                'is_featured': True,
                'warranty': '3 Years Official Comprehensive Commercial Warranty',
                'rating': Decimal('5.0'),
                'num_reviews': 9,
                'images': [
                    'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=800&q=80',
                ]
            },
            {
                'name': 'SAKO Sunpolo 15kW 3-Phase Commercial Solar Hybrid Inverter (Dual MPPT)',
                'slug': 'sako-sunpolo-15kw-3-phase-solar-hybrid-inverter',
                'sku': 'SOLAR-SAKO-SUNPOLO-15KW',
                'brand': 'SAKO',
                'category': cat_map['renewable-energy'],
                'price': Decimal('380000.00'),
                'discount_price': Decimal('0.00'),
                'is_call_for_price': True,
                'count_in_stock': 8,
                'description': 'High-power 3-Phase 15kW pure sine wave solar hybrid inverter with dual MPPT charge controller (18kW max PV input). Supports grid feeding, net metering, and lithium battery communication via RS485/CAN.',
                'short_specs': [
                    '15,000 Watts 3-Phase Pure Sine Wave AC Output',
                    'Dual MPPT Tracker with 18,000W Max PV Array Input',
                    'On-Grid Net Metering & Off-Grid Battery Operation',
                    'Built-in Wi-Fi Mobile App Remote Cloud Monitoring',
                ],
                'technical_specs': {
                    'Nominal Output Power': '15,000W (400V 3-Phase)',
                    'MPPT Voltage Range': '150V - 850V DC',
                    'Max PV Input Voltage': '1000V DC',
                    'Battery Voltage': '48V DC / High Voltage Battery Supported',
                    'Efficiency': 'Up to 98.2%',
                },
                'is_featured': True,
                'warranty': '5 Years Official Manufacturer Warranty',
                'rating': Decimal('5.0'),
                'num_reviews': 7,
                'images': [
                    'https://images.unsplash.com/photo-1509391365360-2e959784a276?auto=format&fit=crop&w=800&q=80',
                ]
            },
            # --- Upcoming Hardware Preview Line ---
            {
                'name': 'ViewSonic ColorPro VP2776 27" 4K OLED Professional Colorist Monitor',
                'slug': 'viewsonic-colorpro-vp2776-4k-oled-monitor',
                'sku': 'MON-VIEWSONIC-VP2776-OLED',
                'brand': 'ViewSonic',
                'category': cat_map['pc-component'],
                'price': Decimal('115000.00'),
                'discount_price': Decimal('0.00'),
                'is_upcoming': True,
                'count_in_stock': 0,
                'description': 'Upcoming 2026 flagship ColorPro monitor engineered for film colorists and creators. Features 4K True 10-bit OLED panel with 1,000,000:1 contrast, 99% DCI-P3, and integrated ColorPro Wheel calibration puck.',
                'short_specs': [
                    '27" True 4K OLED (3840 x 2160) Display',
                    '99% DCI-P3 & 100% sRGB Factory Calibrated (Delta E < 2)',
                    'Included ColorPro Wheel for Instant OSD & Calibration',
                    '90W USB-C Single Cable Video, Data & Fast Charging',
                ],
                'technical_specs': {
                    'Panel': '4K OLED',
                    'Refresh Rate': '120Hz',
                    'Color Depth': '1.07 Billion (True 10-bit)',
                    'Contrast': '1,000,000:1',
                },
                'is_featured': True,
                'warranty': '3 Years Zero Bright Dot Replacement Warranty',
                'rating': Decimal('0.0'),
                'num_reviews': 0,
                'images': [
                    'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=800&q=80',
                ]
            },
            {
                'name': 'Apollo Commander 20kVA Online Double Conversion Modular UPS (Rack/Tower)',
                'slug': 'apollo-commander-20kva-modular-online-ups',
                'sku': 'UPS-APOLLO-CMD-20KVA',
                'brand': 'Apollo',
                'category': cat_map['ups'],
                'price': Decimal('295000.00'),
                'discount_price': Decimal('0.00'),
                'is_upcoming': True,
                'count_in_stock': 0,
                'description': 'Upcoming enterprise 20kVA/20kW unity power factor online UPS with scalable hot-swappable battery cabinets, N+X parallel redundancy, and colored LCD monitoring.',
                'short_specs': [
                    '20kVA / 20kW Unity Power Factor (PF=1.0)',
                    'Zero Millisecond True Double Conversion Transfer',
                    'N+X Parallel Redundancy (Up to 4 Units)',
                    'Intelligent Battery Management (ABM) Technology',
                ],
                'technical_specs': {
                    'Capacity': '20,000VA / 20,000W',
                    'Input Voltage': '3-Phase 380/400/415V or 1-Phase 220/230/240V',
                    'Output Voltage': '220/230/240V AC',
                    'Overload Capacity': '125% for 10 minutes, 150% for 1 minute',
                },
                'is_featured': True,
                'warranty': '2 Years 24/7 SLA Support & Warranty',
                'rating': Decimal('0.0'),
                'num_reviews': 0,
                'images': [
                    'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=800&q=80',
                ]
            },
        ]

        # Insert / Update Products and their images
        for p_data in products_data:
            images_list = p_data.pop('images', [])
            rating = p_data.pop('rating', Decimal('0'))
            num_reviews = p_data.pop('num_reviews', 0)

            prod_obj, _ = Product.objects.update_or_create(
                sku=p_data['sku'],
                defaults=p_data
            )
            prod_obj.rating = rating
            prod_obj.num_reviews = num_reviews
            prod_obj.save()

            # Ensure ProductImage with online URL is attached
            ProductImage.objects.filter(product=prod_obj).delete()
            for idx, img_url in enumerate(images_list):
                ProductImage.objects.create(
                    product=prod_obj,
                    display_order=idx,
                    image_url=img_url,
                    alt_text=prod_obj.name
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {len(products_data)} hardware products with online images and technical specs.'))

        # 4. Create Promo Discount Coupons
        coupons_data = [
            {
                'code': 'ORIENT10',
                'discount_type': 'percent',
                'discount_value': Decimal('10.00'),
                'min_order_value': Decimal('1000.00'),
                'valid_from': timezone.now() - timedelta(days=1),
                'valid_to': timezone.now() + timedelta(days=365),
                'is_active': True,
            },
            {
                'code': 'ORIENT500',
                'discount_type': 'flat',
                'discount_value': Decimal('500.00'),
                'min_order_value': Decimal('5000.00'),
                'valid_from': timezone.now() - timedelta(days=1),
                'valid_to': timezone.now() + timedelta(days=365),
                'is_active': True,
            },
            {
                'code': 'POWER2026',
                'discount_type': 'percent',
                'discount_value': Decimal('15.00'),
                'min_order_value': Decimal('20000.00'),
                'valid_from': timezone.now() - timedelta(days=1),
                'valid_to': timezone.now() + timedelta(days=365),
                'is_active': True,
            },
        ]

        for coup in coupons_data:
            Coupon.objects.update_or_create(code=coup['code'], defaults=coup)
        self.stdout.write(self.style.SUCCESS('Seeded promo discount coupons (ORIENT10, ORIENT500, POWER2026).'))

        # 5. Create Authentic Authorized Partner Brands (25+ live brands from orientcomputers.com.bd)
        brands_data = [
            {'name': 'ViewSonic', 'slug': 'viewsonic', 'letter': 'V', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/viewsonic.png', 'description': 'Global leader in visual solutions, 4K interactive flat panels, commercial monitors, and smart projectors.'},
            {'name': 'SAKO', 'slug': 'sako', 'letter': 'S', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/sako.png', 'description': 'Premier manufacturer of solar hybrid inverters, AVR voltage stabilizers, and energy storage systems.'},
            {'name': 'Apollo', 'slug': 'apollo', 'letter': 'A', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/apollo.png', 'description': 'Trusted offline and online double conversion UPS systems, servo stabilizers, and backup power solutions.'},
            {'name': 'Patriot', 'slug': 'patriot', 'letter': 'P', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/patriot.png', 'description': 'High-performance memory modules, solid state drives, and enthusiast computer hardware.'},
            {'name': 'Viper Gaming', 'slug': 'viper-gaming', 'letter': 'V', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/viper.png', 'description': 'Flagship RGB DDR5 gaming DRAM, Gen4 NVMe SSDs, and gaming peripherals by Patriot.'},
            {'name': 'TrendSonic', 'slug': 'trendsonic', 'letter': 'T', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/trendsonic.png', 'description': 'High-airflow gaming chassis, tempered glass PC cases, and ergonomic accessories.'},
            {'name': 'Plustek', 'slug': 'plustek', 'letter': 'P', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/plustek.png', 'description': 'High-speed ADF document scanners, book scanners, and passport OCR readers.'},
            {'name': 'FirstPower', 'slug': 'firstpower', 'letter': 'F', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/firstpower.png', 'description': 'Maintenance-free valve regulated sealed lead acid (VRLA) AGM and GEL deep cycle batteries.'},
            {'name': 'Kstar', 'slug': 'kstar', 'letter': 'K', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/kstar.png', 'description': 'Data center critical infrastructure, modular online UPS, and smart PV power inverters.'},
            {'name': 'Long', 'slug': 'long', 'letter': 'L', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/long.png', 'description': 'Kung Long high-rate discharge sealed lead acid batteries for telecom, UPS, and emergency power.'},
            {'name': 'Mofii', 'slug': 'mofii', 'letter': 'M', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/mofii.png', 'description': 'Aesthetic wireless retro keyboards, mechanical gaming mice, and colorful desktop sets.'},
            {'name': 'Neata', 'slug': 'neata', 'letter': 'N', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/neata.png', 'description': 'Industrial deep cycle storage batteries and VRLA power cells for solar and UPS backup.'},
            {'name': 'Jinko Solar', 'slug': 'jinko-solar', 'letter': 'J', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/jinko.png', 'description': 'World-leading Tier-1 N-Type TOPCon monocrystalline high-efficiency solar photovoltaic panels.'},
            {'name': 'Megmeet', 'slug': 'megmeet', 'letter': 'M', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/megmeet.png', 'description': 'Custom industrial power supplies, medical grade power, and telecom rectifier units.'},
            {'name': 'Meki', 'slug': 'meki', 'letter': 'M', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/meki.png', 'description': 'Motorized and manual projection screens, audio-visual mounts, and presentation accessories.'},
            {'name': 'Inovtech', 'slug': 'inovtech', 'letter': 'I', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/inovtech.png', 'description': 'Commercial display stands, interactive kiosk enclosures, and audio-visual rigging hardware.'},
            {'name': 'Effekta', 'slug': 'effekta', 'letter': 'E', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/effekta.png', 'description': 'German engineered online UPS systems, DC rectifiers, and industrial solar backup converters.'},
            {'name': 'AEC', 'slug': 'aec', 'letter': 'A', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/aec.png', 'description': 'Allis Electric three-phase industrial UPS and high-capacity transformer-based voltage stabilizers.'},
            {'name': 'APC by Schneider', 'slug': 'apc', 'letter': 'A', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/apc.png', 'description': 'Global benchmark in Smart-UPS online power protection and server room surge suppression.'},
            {'name': 'Futek', 'slug': 'futek', 'letter': 'F', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/futek.png', 'description': 'Electronic money counting machines, currency discriminators, and counterfeit banknote detectors.'},
            {'name': 'Futronic', 'slug': 'futronic', 'letter': 'F', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/futronic.png', 'description': 'Optical USB fingerprint scanners and biometric identity verification hardware.'},
            {'name': 'Hinorms', 'slug': 'hinorms', 'letter': 'H', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/hinorms.png', 'description': 'Enterprise paper shredders, heavy-duty binding machines, and office automation gear.'},
            {'name': 'Siel Energy', 'slug': 'siel-energy', 'letter': 'S', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/siel.png', 'description': 'Industrial photovoltaic central inverters and utility-scale energy storage systems.'},
            {'name': 'Sineng', 'slug': 'sineng', 'letter': 'S', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/sineng.png', 'description': 'String inverters, central inverters, and utility solar power conversion solutions.'},
            {'name': 'TransWorld', 'slug': 'transworld', 'letter': 'T', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/transworld.png', 'description': 'Heavy-duty voltage stabilizers and industrial electrical distribution transformers.'},
            {'name': 'Volto', 'slug': 'volto', 'letter': 'V', 'logo_url': 'https://orientcomputers.com.bd/uploads/brand/volto.png', 'description': 'Smart mini DLP projectors and portable home theater projection systems.'},
        ]

        for b in brands_data:
            Brand.objects.update_or_create(
                slug=b['slug'],
                defaults={
                    'name': b['name'],
                    'logo_url': b['logo_url'],
                    'description': b['description'],
                    'is_featured': True,
                }
            )
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(brands_data)} authentic partner brands.'))

        # 6. Create 8 Authentic Physical Showroom Branches (Matching orientcomputers.com.bd/contact/branch)
        branches_data = [
            {
                'name': 'IDB Branch (BCS Computer City)',
                'address': 'BCS Computer City, Shop # 141 (Ground Floor), IDB Bhaban, E/8-A, Rokeya Sarani, Sher-e-Bangla Nagar, Dhaka-1207',
                'phone': '01811-486477, 01847-082721',
                'email': 'br.idb@orientcomputers.com',
                'maps_url': 'https://maps.google.com/?q=BCS+Computer+City+IDB+Bhaban+Dhaka',
                'hours': '10:00 AM – 8:00 PM',
                'off_day': 'Sunday',
                'is_flagship': True,
                'display_order': 1,
            },
            {
                'name': 'Multiplan Branch (Elephant Road)',
                'address': 'Multiplan Centre, Shop # 1408, Level # 14, 69-71 New Elephant Road, Dhaka-1205',
                'phone': '01814-655440, 01847-082723',
                'email': 'br.mtp@orientcomputers.com',
                'maps_url': 'https://maps.google.com/?q=Multiplan+Center+Dhaka',
                'hours': '10:30 AM – 8:30 PM',
                'off_day': 'Tuesday',
                'is_flagship': True,
                'display_order': 2,
            },
            {
                'name': 'Elephant Road Branch',
                'address': 'M A Ali Bhaban, 60 Elephant Road, Dhaka-1205',
                'phone': '01847-082718, 01847-082722',
                'email': 'br.erd@orientcomputers.com',
                'maps_url': 'https://maps.google.com/?q=60+Elephant+Road+Dhaka',
                'hours': '10:00 AM – 8:00 PM',
                'off_day': 'Friday',
                'is_flagship': False,
                'display_order': 3,
            },
            {
                'name': 'Motijheel Corporate Branch',
                'address': 'Rahmania International Complex, Shop # 17 & 18 (1st Floor), 28/1/C Toyenbee Circular Road, Motijheel C/A, Dhaka-1000',
                'phone': '01847-081771, 01847-082720',
                'email': 'br.mot@orientcomputers.com',
                'maps_url': 'https://maps.google.com/?q=Rahmania+Complex+Motijheel+Dhaka',
                'hours': '10:00 AM – 7:30 PM',
                'off_day': 'Friday',
                'is_flagship': True,
                'display_order': 4,
            },
            {
                'name': 'Power House Branch (Gulistan)',
                'address': 'Sundarban Square Market, Shop # 146 (Ground Floor), Nawabpur, Gulistan, Dhaka-1000',
                'phone': '01847-082714, 01847-082715',
                'email': 'br.ph@orientcomputers.com',
                'maps_url': 'https://maps.google.com/?q=Sundarban+Square+Market+Gulistan+Dhaka',
                'hours': '10:00 AM – 8:00 PM',
                'off_day': 'Friday',
                'is_flagship': False,
                'display_order': 5,
            },
            {
                'name': 'Uttara Branch',
                'address': 'SGC Computer City, Shop # 118, Level # 01, House # 07, Road # 07, Sector # 07, Jashimuddin Avenue, Uttara, Dhaka-1230',
                'phone': '01814-655437, 01847-082724',
                'email': 'br.utt@orientcomputers.com',
                'maps_url': 'https://maps.google.com/?q=SGC+Computer+City+Uttara+Dhaka',
                'hours': '10:30 AM – 8:30 PM',
                'off_day': 'Wednesday',
                'is_flagship': False,
                'display_order': 6,
            },
            {
                'name': 'Chattogram Branch',
                'address': 'R F Johora Tower, Shop # 506, Level # 05, Chowmuhani, Sheikh Mujib Road, Agrabad C/A, Chattogram',
                'phone': '01811-414262, 01847-082725',
                'email': 'br.ctg@orientcomputers.com',
                'maps_url': 'https://maps.google.com/?q=RF+Johora+Tower+Agrabad+Chattogram',
                'hours': '10:00 AM – 8:00 PM',
                'off_day': 'Friday',
                'is_flagship': False,
                'display_order': 7,
            },
            {
                'name': 'Sylhet Branch',
                'address': 'Karim Ullah Market, Shop # C-35, Level # 03, Bondor Bazar, Sylhet',
                'phone': '01847-213848, 01847-082726',
                'email': 'br.syl@orientcomputers.com',
                'maps_url': 'https://maps.google.com/?q=Karim+Ullah+Market+Bondor+Bazar+Sylhet',
                'hours': '10:00 AM – 8:00 PM',
                'off_day': 'Friday',
                'is_flagship': False,
                'display_order': 8,
            },
        ]

        for b in branches_data:
            Branch.objects.update_or_create(name=b['name'], defaults=b)
        self.stdout.write(self.style.SUCCESS('Created/Updated 8 official Orient showroom branches across Bangladesh.'))

        # 7. Sample Reviews
        sample_prod = Product.objects.filter(sku='AVR-APOLLO-2000VA').first()
        if sample_prod and demo_customer:
            Review.objects.update_or_create(
                product=sample_prod,
                user=demo_customer,
                defaults={
                    'rating': 5,
                    'title': 'Essential protection against Dhaka voltage fluctuations!',
                    'body': 'Connected this 2000VA servo stabilizer to our work server and dual workstation setup. Completely solved the low voltage tripping issues during peak hours. Rock solid 220V output.',
                }
            )

        self.stdout.write(self.style.SUCCESS('Orient Computers database successfully initialized and seeded!'))

