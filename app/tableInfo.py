"""
For inserting the information into the database
Those information should be stored in this file
"""

#
user_list = [
    ['Customer1@163.com', 'Customer1', '123', 1],
    ['Retailer1@163.com', 'Retailer1', '123', 2],
    ['Retailer2@163.com', 'Retailer2', '123', 2],
    ['Retailer3@163.com', 'Retailer3', '123', 2],
    ['Retailer4@163.com', 'Retailer4', '123', 2],
    ['Retailer5@163.com', 'Retailer5', '123', 2],
    ['Retailer6@163.com', 'Retailer6', '123', 2],
    ['Retailer7@163.com', 'Retailer7', '123', 2],
    ['Retailer8@163.com', 'Retailer8', '123', 2],
    ['Retailer9@163.com', 'Retailer9', '123', 2],
    ['Retailer10@163.com', 'Retailer10', '123', 2],
]

category_list = [
    'sports',
    'foods',
    'clothes',
    'digital',
    'books',
    'makeup',
    'luxury',
    'daily',
    'art',
    'home',
    'instruments',
    'others'
]

#
product_picture_list = [
    # [name1, name2, ...] (at least 2, at most 5)
    # all in png, without spacing
    ['91u24xvKpxL._AC_SX679_.jpg', '914XpdnqSrL._AC_SL1500_.jpg'],  # pic of product 0
    ['81vPJY1agyL._SL1500_.jpg', '81jZWKisi+L._SL1500_.jpg', '71n54nZiDuL._SL1500_.jpg'],  # pic of product 1
    ['6166TvCN33S._AC_SL1500_.jpg', '51W9Zo0aHxS._AC_SL1500_.jpg', '61G-xklXq-S._AC_SL1500_.jpg'],
    ['91TKOKJe2zL._SL1500_.jpg', '91XslFohKxL._SL1500_.jpg'],
    ['9150Gx-BrKS._AC_SL1500_.jpg', '915zTdcqILS._AC_SL1500_.jpg'],
    ['61-ggLv1AuL._AC_UX466_.jpg', '61GL637HSNL._AC_UX466_.jpg', '61eQ776sLuL._AC_UX342_.jpg'],
    ['finishes_1_sierra_blue__2bovafkl4yaa_large.jpg', 'iphone-13-pro-blue-select.png'],
    ['MW65G1_Angle_800x800_6ef52f0d-fd79-4dc3-8ffc-915eb00699d4_800x800.png',
     'MH65G1_Stand_800x800_StandNotIncluded_800x800.png',
     'MW65G1_Angle_800x800_6ef52f0d-fd79-4dc3-8ffc-915eb00699d4_800x800.png',
     'MW65G1_Straight_800x800_b1d350f7-d86f-4c60-ab99-7f09531de16f_800x800.png'],
    ['MH40S2-W_Angle_800x800_04655dea-1957-41e8-96fb-a186f2d696b5_800x800.png',
     'MH40S2-W_Earcup_800x800_aa42e89f-cb35-496a-9488-3fe6f9d4c4fe_800x800.png',
     'MH40S2-W_Stand_800x800_StandNotIncluded_800x800.png',
     'MH40S2-W_Straight_800x800_d83e49ea-8f51-4c78-8ce2-1da9e2ba6365_800x800.png',
     'MH40-W-S2_Engraving_800x800._73fc6af4-a1e8-40da-a8b9-66659569f295_800x800.png'],
    ['MW08SportWH_Inside-ChargingCase_800x800_89ec877d-63e7-49e7-97ce-b03b847ea32f_800x800.png',
     'MW08SportWH_Angle_Right_800x800_a426ea6b-e9d2-4de8-a24f-f7050b1a6b37_800x800.png',
     'MW08SportWH_Fit_800x800_4f8eff59-dcbf-4831-bbf3-87c765fdf0c4_800x800.png',
     'MW08SportWH_Inside-ChargingCase_800x800_89ec877d-63e7-49e7-97ce-b03b847ea32f_800x800.png'],
    ['MW65-LAM1_Angle_800x800_c122fed7-32a8-463e-8a52-58d6c0f96601_800x800.png',
     'MW65-LAM1_Stand_800x800_ef4bbfff-922b-4ef0-a5c9-4674d6f1c532_800x800.png',
     'MW65-LAM1_Straight_800x800_30cbe41e-fa34-40e7-ae01-dff7867e705b_800x800.png'],
    ['MW07-PSG_ChargingCase-Open_800x800_a48a6f8e-ff1e-4881-a59c-152805a52be4_800x800.png',
     'MW07-PSG_iPhone_800x800_6134afe1-6479-4f67-a1c5-7b6c312ae49e_800x800.jpg',
     'MW07-PSG_Angle_Right_800x800_eef693ef-ce8b-4910-aa92-b76dee59c8e3_800x800.png',
     'MW07-PSG_FitWing_800x800_b2371c78-7f51-42e5-b4c8-25e4bcc1766e_800x800.png'],
    ['MH40-W-PSG_Angle_800x800_e282edb5-d29d-4291-8c22-cdcfbe1919b0_800x800.png',
     'MH40-W-PSG_Stand_800x800._800x800.png',
     'MH40-W-PSG_Straight_800x800_e45e9b10-92d6-4c0f-ac85-7f9405df779a_800x800.png'],
    ['6476246_sd.jpg', '6476246cv12d.jpg', '6476246cv11d.jpg'],
    ['6415568_sd.jpg', '6415568cv1d.jpg', '6415568cv2d.jpg', '6415568cv11d.jpg'],
    ['6215932_sd.jpg', '6215932cv11d.jpg', '6215932cv12d.jpg'],
    ['front-300_600.png', 'hardware-500_500.png', 'neck-side-500_500.png'],
    ['BAT400EBCH1_1.jpg', 'hardware-500_500 (1).png', 'neck-side-500_500 (1).png'],
    ['0113942750_fen_ins_frt_1_rr.jpg', '0113942750_fen_ins_bck_1_rl.jpg', '0113942750_fen_ins_fbd_1_nr.jpg'],
    ['0378553505_sqr_ins_frt_1_rr.jpg', '0378553505_sqr_ins_bck_1_rl.jpg', '0378553505_sqr_ins_fbd_1_nr.jpg'],
    ['NY_Model_D_with_Polyester_Finish_PS_fma_scale.jpg', 'model_d_overhead_rotated_fma.jpg',
     'model_d_overhead_fma.jpg'],
    ['model_b_room_landscape.jpg', 'Fluegel_B_Ivory_White_03.jpg', 'Fluegel_B_Black_03.jpg'],
    ['csm_C_227_black_polished_HH_xl_rectangle_4375299f00.jpg', 'Fluegel_C_White_03.jpg', 'Fluegel_C_Black_03.jpg'],
    ['28000153_fr.jpg', '28000153_b.jpg', '28000153_lm.jpg'],
    ['5905_1A_001_8.jpg', '5905_1A_001_1.jpg', '5905_1A_001_1 (1).jpg'],
    ['6119G_001_8.jpg', '6119G_001_9.jpg', '6119G_001_10.jpg'],
    ['giro-ratio-mips-snow-helmet-matte-midnight-side.jpg', 'giro-ratio-mips-snow-helmet-matte-ox-red-side.jpg'],
    ['848556-004_Team-TLS_White-Black_Product-1_0.jpg', '848556-004_Team-TLS_White-Black_Product-3_0.jpg'],
['eternal-n-5-necklace-white-white-gold-diamond-packshot-default-j11991-8845375995934.jpg', 'eternal-n-5-necklace-white-white-gold-diamond-packshot-motif-j11991-8845518077982.jpg', 'eternal-n-5-necklace-white-white-gold-diamond-packshot-fermoir-j11991-8845539934238.jpg'],
['giro-contour-goggle-black-phased-vivid-jet-black-hero.jpg', 'giro-contour-goggle-black-phased-vivid-jet-black-left.jpg'],
    ['21-machine-carbon-grey-p1.png.png', '21-machine-carbon-grey-p2.png.png', '21-machine-carbon-grey-p3.png.png'],
['ultra-bracelet-white-diamond-white-gold-white-ceramic-packshot-default-j2931-8834193948702.jpg', 'ultra-bracelet-white-diamond-white-gold-white-ceramic-packshot-arriere-j2931-8834194800670.jpg', 'ultra-bracelet-white-diamond-white-gold-white-ceramic-packshot-motif-j2931-8834195292190.jpg'],
['mini-flap-bag-black-white-velvet-gold-tone-metal-velvet-gold-tone-metal-packshot-artistique-vue1-as2597b06780c0229-8845484851230.jpg', 'mini-flap-bag-black-white-velvet-gold-tone-metal-velvet-gold-tone-metal-packshot-artistique-vue2-as2597b06780c0229-8845484916766.jpg', 'mini-flap-bag-black-white-velvet-gold-tone-metal-velvet-gold-tone-metal-packshot-artistique-vue4-as2597b06780c0229-8845484785694.jpg'],


]

"""
Categories:
sports
foods
clothes
digital
books
makeup
luxury
daily
art
home
instruments
others
"""

#
product_category_list = [
    # [cate1, cate2, cate3, ...] (must have at least 1 single category tag)
    ['sports'],
    ['foods'],
    ['sports'],
    ['foods'],
    ['clothes'],
    ['clothes'],
    ['digital'],
    ['digital'],
    ['digital'],
    ['digital'],
    ['digital'],
    ['digital'],
    ['digital'],
    ['digital'],
    ['digital'],
    ['digital'],
    ['instruments'],
    ['instruments'],
    ['instruments'],
    ['instruments'],
    ['instruments'],
    ['instruments'],
    ['instruments'],
    ['luxury'],
['luxury'],
['luxury'],
['sports'],
['sports'],
['luxury'],
['sports'],
['sports'],
['luxury'],
['luxury'],

]

#
product_list = [
    # name, description, price,
    ['Spalding basketball', 'Youth size and weight: size 5, 27.5 Performance composite cover\
Deep channel design for superior control\
Butyl rubber bladder for air retention\
Designed for indoor play only', 290.84],
    ['Lindt Gourmet Chocolate Truffle Gift Box', 'Share the passion of delectable chocolate or have a moment of indulgence alone\
Perfect for indulging with at home or as a surprise gift\
Made by Lindt Master Chocolatiers with premium ingredients from world-renowned regions\
The 14.7 oz. Box of gourmet truffles is an ideal gift for any occasion', 178.7],
    ['BURTON Custom Flying V Snowboard', "Directional Shape is the classic snowboard shape, designed to be ridden with a slightly longer nose than tail to concentrate pop in the tail while providing plenty of float, flow, and control to rip any terrain or condition\
Flying V Bend features rocker zones between and outside your feet for enhanced playfulness, and float and camber zones underneath your feet that focus edge control for crisp snap, added pop, and powerful turns\
Twin Flex is perfectly symmetrical from tip to tail for a balanced ride that's equally versatile regular or switch\
Super Fly II 700G Core uses stronger and lighter wood to provide pop and strength while reducing overall weight\
Dualzone EGD engineered wood grain is positioned along the toe and heel edges on two continuous zones perpendicular to the core for more edge-hold, response, and strength",
     4021.54],
    ["Lay's Potato Chip Variety Pack", "Variety pack of Lay's potato chips favorites with classic flavors in one convenient package\
With 4 different varieties, there's sure to be something everyone will love\
40 count pack featuring 10 of each of these Lay's potato chips favorites in 1 oz bags - Classic, Barbecue, Sour Cream and Onion, and Salt and Vinegar\
These much loved treats are fun to enjoy at lunch, as an after-school snack, or party refreshment\
Easy to carry, easy to store, and easy to pack\
Our snacks have a short shelf life (60-90 days) so most of our packages only show the month & day of expiration. For optimum flavor and freshness, we recommend the snack be consumed by the date on the package.",
     57.39],
    ["Legendary Whitetails Men's Buck Camp Flannel Shirt", "100% Cotton PERFECT WEIGHT: Weighing in at 5.1 ounces, the Buck Camp Flannel Shirt is the perfect weight to be worn alone or layered, indoors or outside; you're gonna love this comfortable brushed cotton flannel shirt\
DURABLE QUALITY: Our signature corduroy lined collar and cuffs not only look cool, but add stablility. which means they will hold their shape so you don't have to iron",
     190.88],
    ['Bbonlinedress Women Short 1950s Retro Vintage Cocktail Party Swing Dresses', '98% Cotton, 2% Spandex, Zipper closure, Machine Wash\
Size: Please use Size Chart Image Left / Size Info in Product Description (XS-5XL) to choose a suitable size. Our size is different from standard size, thanks.\
Features: Vintage Black Dress, A-line Style, Sweetheart Neckline, Cap Sleeves, Back Zipper Closure, Classic Vintage Party Dress.\
Material: 98% Cotton & 2% Spandex.\
Great for Wedding Party, Bridesmaid, Cocktail Party, Birthday, Work, Holiday, Tea Party, Dinner, Anniversary, Theme Party and Daily Casual.\
Garment Care: Hand wash cold hang dry recommended, machine washable. Do not wring or twist, low iron to remove wrinkles if necessary.',
     245.89],
    ['iPhone 13 Pro',
     'A dramatically more powerful camera system. A display so responsive, every interaction feels new again. The world’s fastest smartphone chip. Exceptional durability. And a huge leap in battery life.',
     5999],
    ['MW65 Active Noise-Cancelling Wireless Headphones',
     "Our Most Technically Sophisticated Noise-Cancelling Wireless Headphones Built for Life On-the-Go: The ultimate companion for your daily listening or travels, the MW65's are our lightest over-ear noise-cancelling wireless headphones and feature custom 40mm Beryllium drivers and Active Noise-Cancelling technology to produce an exceptional acoustic experience. These active noise-cancelling wireless headphones are the perfect match for audiophiles everywhere.",
     3499],
    ['MH40 WIRELESS Over-Ear Headphones',
     "An Icon, Now Wireless MH40 Wireless Over-Ear Headphones are an evolution of our very first headphones--the MH40--in celebration of our five year anniversary. Staying true to the original vintage aviator-inspired design and signature rich, warm sound, our new cordless headphones with dual mics feature Bluetooth 5.0 with a 100ft/30m connectivity range and 18 hours of playtime. Lightweight yet durable, the MH40 Wireless Over-Ear Headphones are crafted from coated canvas with lambskin leather details.",
     2099],
    ['MW08 Sport Active Noise-Cancelling True Wireless Earphones',
     "Inspire Movement Designed with shatter-resistant sapphire glass and a custom Kevlar® fiber charging case case compatible with our MC100 WIRELESS CHARGE PAD, MW08 Sport is built to endure. Power through with Hybrid Active Noise-Cancellation, two Ambient Listening modes for improved outdoor awareness, and memory foam ear tips for an enhanced and comfortable fit. Hear your workout playlist in a whole new way",
     2227.98],
    ['MW65 AUTOMOBILI LAMBORGHINI Active Noise-Cancelling Wireless Headphones',
     "MASTER & DYNAMIC FOR Automobili Lamborghini Master & Dynamic has partnered with Automobili Lamborghini on a collection of high-performance sound tools inspired by the design and materials of the iconic Italian super sports cars.",
     3499],
    ['MW07 PLUS PARIS SAINT-GERMAIN True Wireless Earphones',
     "MASTER & DYNAMIC FOR Paris Saint-Germain Master & Dynamic has partnered with the iconic football club to create a limited-edition collection of MH40 Wireless Over-Ear Headphones and MW07 PLUS True Wireless Earphones. The collaboration features the design from the club's fourth kits, which are inspired by the Milky Way and represent the new dimension in which the team is evolving.",
     1589.59],
    ['MH40 WIRELESS PARIS SAINT-GERMAIN Over-Ear Headphones',
     "MASTER & DYNAMIC FOR Paris Saint-Germain Master & Dynamic has partnered with the iconic football club to create a limited-edition collection of MH40 Wireless Over-Ear Headphones and MW07 PLUS True Wireless Earphones. The collaboration features the design from the club's fourth kits, which are inspired by the Milky Way and represent the new dimension in which the team is evolving.",
     1908.79],
    ["Samsung - 70” Class TU6985 4K Crystal UHD Smart Tizen TV",
     "Get enhanced smart capabilities with the TU6985. Crystal Processor 4K automatically upscales your favorite movies, TV shows and sports events to 4K. Smart TV powered by Tizen lets you find content and navigate streaming services easily. PurColor fine tunes colors while HDR steps up to millions of shades of color that go beyond what HDTV can offer.",
     4199],
    ['Canon - EOS R Mirrorless 4K Video Camera with RF 24-105mm f/4-7.1 IS STM Lens - Black',
     "For outstanding quality and convenience, all in one package, turn to the EOS R + RF24-105mm F4-7.1 IS STM Lens Kit. Designed to deliver optical excellence, the EOS R features a 30.3 MP CMOS sensor, DIGIC 8 image processor and a maximum of 5,655 manually selectable AF point positions ― providing incredible detail and clarity, even in low-light situations. Shoot stunning 4K video up to 30 frames per second (fps) or Full HD 1080p video up to 60 fps. Plus, when paired with the compact RF24-105mm F4-7.1 IS STM lens, which boasts smooth and quiet autofocusing in both still and video shooting, thanks to its leadscrew-type STM motor, and optical image stabilization with up to 5 stops of shake correction, you’ll have the versatility at your fingertips to capture everything from portraits and landscapes, to everyday snapshots and more.",
     12129.35],
    ['Apple Watch Series 7 (GPS) 41mm Midnight Aluminum Case with Midnight Sport Band - Midnight',
     "The largest, most advanced Always-on Retina display yet makes everything you do with your Apple Watch Series 7 bigger and better. Series 7 is the most durable Apple Watch ever built, with an even more crack-resistant front crystal. Advanced features let you measure your blood oxygen level,¹ take an ECG anytime,² and access mindfulness and sleep tracking apps. You can also track dozens of workouts, including new tai chi and pilates.",
     2799],
    ['Gibson 1957 Les Paul Custom Reissue - Ebony 2-Pickup',
     "The Original Black Beauty Gibson Custom Shop is the pinnacle of craftsmanship, quality, and sound excellence. Each instrument celebrates Gibson's legacy through accuracy, authenticity and attention to detail. With its elegant lines and Ebony/Pearl/Gold aesthetic, the 1957 Les Paul Custom is easily one of the most iconic and beautiful guitars ever made. It features a body carved out of a single large piece of solid mahogany, unique among Les Paul models. The resulting dark mid-range tone from the body pairs perfectly with its bright-sounding solid Ebony fingerboard. All together, it's the pinnacle of guitar craftsmanship, design and tone. Gibson Custom Shop is proud to revive every last detail of the original 'Black Beauty' for this '57 Les Paul Custom Reissue, from the dimensions and contours to the precise inlay patterns to the entire ownership experience.",
     44042.53],
    ['Gibson Thunderbird Bass - Ebony',
     "Hard Rock Low End The Gibson Thunderbird has the classic reverse body and headstock design as originally introduced in 1963 as Gibson's first neck-through-body bass design. The traditional 9-ply mahogany/walnut neck through body construction provides a thundering low end response and a piano like sustain. The narrow nut width and rounded neck profile neck feels both fast and intuitive. The Thunderbird high output, ceramic magnet loaded humbucking pickups (neck and bridge) deliver the sonic and iconic low end voice for which the Thunderbird is known. Available in 2 classic finishes: Tobacco Burst and Ebony.",
     14676.59],
    ['Fender AMERICAN PROFESSIONAL II TELECASTER',
     "The American Professional II Telecaster® draws from more than seventy years of innovation, inspiration and evolution to meet the demands of today’s working player. Our popular Deep 'C' neck now sports smooth rolled fingerboard edges, a 'Super-Natural' satin finish and a newly sculpted neck heel for a supremely comfortable feel and easy access to the upper register. New V-Mod II Telecaster single-coil pickups are more articulate than ever while delivering the twang, snap and snarl that made the Tele famous. The new top-load/string-through bridge with compensated 'bullet' saddles is our most comfortable, flexible Tele bridge yet – retaining classic brass-saddle tone and providing excellent intonation and flexible setup options, allowing you to tailor the tension and tone of each string to your liking. The American Pro II Telecaster delivers instant familiarity and sonic versatility you’ll feel and hear right away, with broad ranging improvements that add up to nothing less than a new standard for professional instruments.",
     14198],
    ['Fender AFFINITY SERIES™ PRECISION BASS',
     "A superb gateway into the time-honored Fender® family, the Squier® Affinity Series™ Precision Bass® PJ delivers legendary design and quintessential tone for today’s aspiring bassist. This P Bass® features several player-friendly refinements such as a thin and lightweight body, a slim and comfortable “C”-shaped neck profile and vintage-style open-gear tuning machines for smooth, accurate tuning. Loaded with a Squier split single-coil P Bass neck pickup and a single-coil J Bass® bridge pickup for a wide variety of tones, this model is ready to help lay the foundation for any player at any stage.",
     18900],
    ['Steinway D-274',
     'At 274 cm in length, this majestic musical instrument is the overwhelming choice of the world’s greatest pianists. This concert grand will completely satisfy those who desire the highest possible level of musical expression.',
     1080000],
    ['Steinway B-211',
     'This magnificent 211 cm grand piano is often referred to as “the perfect piano”. And available with Spirio also. It’s a wonderfully balanced and versatile piano that does extremely well in intimate settings, teaching studios, and mid-sized venues.',
     700000],
    ['Steinway C-227',
     'Measuring 227 cm in length, this concert grand offers a large variety of sound and touch from soft piano to strong forte, from clear treble to deep bass.',
     800000],
    ['MVMT RAPTOR HONEY SMOKE', "Dressed to kill. The Raptor Honey Smoke watch brings a double threat design that’s both radical and refined. Its sport chronograph dial commands attention with bold geometric hands, a lifted, bolted bezel, and crown with knurling grip. Featuring a gunmetal and gold colorway with blue dial accents.", 8999],
    ['Patek Philippe 5905/1A - COMPLICATIONS', "Available for the first time in steel, the Reference 5905 self-winding flyback chronograph with Annual Calendar radiates a resolutely sporty look. The rhythmic dial features an elegant and casual 'sunburst' olive green color. The integrated bracelet is enhanced by contrasting polished and satin finishes. Thanks to the vertical disk-type clutch, the central chronograph seconds hand can be used as a permanent (running) seconds display. The patented Annual Calendar automatically takes account of 30- and 31-day months, requiring only one correction per year, on March 1st.", 120000],
    ['Patek Philippe 6119G - CALATRAVA', 'Patek Philippe gives fresh momentum to the emblematic Calatrava model featuring a guilloched hobnail pattern also known as Clous de Paris by treating it to a slightly larger diameter and a design reinterpreted in a contemporary spirit. The faceted applied white gold hour-markers, combined with dauphine-style hours/minutes hands, create a sleek and timeless dial aesthetic. The elegantly refined white gold case houses the new manually wound movement 30-255 PS with a 65-hour power reserve.', 98000],
['Giro RATIO MIPS HELMET', 'THE RATIO™ MIPS® HELMET HAS THE PERFECT RATIO OF EVERYTHING YOU NEED TO ACCOMPANY YOU ON THE MOUNTAIN, FROM ITS THERMOSTAT CONTROL ADJUSTABLE VENTING TO ITS MIPS® TECHNOLOGY TO ITS LAID-BACK STYLE.', 699],
    ['Nitro TEAM TLS', "Delivering team-tested and snowboarder-proven performance year after year, the Nitro Team is considered by snowboarders everywhere to be the most versatile snowboard boot on the market with a proper fit that never quits.", 2999],
['Chanel ETERNAL N°5 NECKLACE', 'The different adjustment rings on the chain enable the necklace to be worn either in the long or short version.', 24800],
['Giro CONTOUR GOGGLE', "HEAD DOWN THE MOUNTAIN IN STYLE WITH THE CONTOUR GOGGLE. WITH A NEW TORIC LENS SHAPE AND VIVID LENSES WITH OPTICS BY ZEISS®, YOU'LL BE ABLE TO SEE AS GREAT AS YOU LOOK.", 780],
    [' Nitro Machine binding', "The Nitro Machine binding has become a staple within the Nitro Binding line over the years for its unmatched customizable fits and unparalleled responsive performance. The Machine is the binding where the Nitro binding engineers can put their attention to detail to the test continue to create the lightest, strongest, and most responsive binding on the market, without sacrificing anything when it comes to fit. Designed for precision!", 1800],
['Chanel ULTRA BRACELET', 'The radically stunning combination of black and white gives unique rhythm to Ultra jewellery creations.', 89000],
    ['Chanel MINI FLAP BAG', "Velvet & Gold-Tone Metal Black & White Ref.  AS2597 B06780 C0229 dimensions 5.9 × 7.8 × 2.9 in ( cm )", 59000],

]
