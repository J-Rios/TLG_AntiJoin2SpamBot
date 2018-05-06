# -*- coding: utf-8 -*-
'''
Script:
    Constants.py
Description:
    Constants values for Anti_Join2Spam_Bot.py.
Author:
    Jose Rios Rubio
Creation date:
    04/04/2018
Last modified date:
    06/05/2018
Version:
    1.5.0
'''

####################################################################################################

### Constants ###
CONST = {
    'TOKEN' : 'XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', # Bot Token (get it from @BotFather)
    'DATA_DIR' : './data', # Data directory path
    'F_USERS' : 'users.json', # Chat JSON files name
    'F_MSG' : 'msgs.json', # Messages JSON files name
    'F_CONF' : 'configs.json', # Chat configurations JSON files name
    'INIT_LANG' : 'EN', # Initial language at Bot start
    'INIT_ENABLE' : True, # Initial enable/disable status at Bot start
    'INIT_TIME_ALLOW_URLS' : 24, # Initial hours until allow a user to publish URLs in messages
    'INIT_MIN_MSG_ALLOW_URLS' : 10, # Initial number of users messages until allow publish URLs
    'INIT_CALL_ADMINS_WHEN_SPAM' : False, # Initial notify admins value when spam is detected
    'INIT_ALLOW_USERS_ADD_BOTS' : True, # Initial allow users to invite and add Bots to the group
    'T_DEL_MSG' : 5, # Time (in mins) to remove self-destruct sent messages from the Bot
    'DEVELOPER' : '@JoseTLG', # Bot developer
    'REPOSITORY' : 'https://github.com/J-Rios/TLG_AntiJoin2SpamBot', # Bot code repository
    'VERSION' : '1.5.0', # Bot version

    'REGEX_URLS' : r'((?<=[^a-zA-Z0-9])*(?:https\:\/\/|[a-zA-Z0-9]{1,}\.{1}|\b)(?:\w{1,}\.{1}){1,5}(?:aaa|aarp|abarth|abb|abbott|abbvie|abc|able|abogado|abudhabi|ac|academy|accenture|accountant|accountants|aco|active|actor|ad|adac|ads|adult|ae|aeg|aero|aetna|af|afamilycompany|afl|africa|ag|agakhan|agency|ai|aig|aigo|airbus|airforce|airtel|akdn|al|alfaromeo|alibaba|alipay|allfinanz|allstate|ally|alsace|alstom|am|americanexpress|americanfamily|amex|amfam|amica|amsterdam|analytics|android|anquan|anz|ao|aol|apartments|app|apple|aq|aquarelle|ar|arab|aramco|archi|army|arpa|art|arte|as|asda|asia|associates|at|athleta|attorney|au|auction|audi|audible|audio|auspost|author|auto|autos|avianca|aw|aws|ax|axa|az|azure|ba|baby|baidu|banamex|bananarepublic|band|bank|bar|barcelona|barclaycard|barclays|barefoot|bargains|baseball|basketball|bauhaus|bayern|bb|bbc|bbt|bbva|bcg|bcn|bd|be|beats|beauty|beer|bentley|berlin|best|bestbuy|bet|bf|bg|bh|bharti|bi|bible|bid|bike|bing|bingo|bio|biz|bj|black|blackfriday|blanco|blockbuster|blog|bloomberg|blue|bm|bms|bmw|bn|bnl|bnpparibas|bo|boats|boehringer|bofa|bom|bond|boo|book|booking|boots|bosch|bostik|boston|bot|boutique|box|br|bradesco|bridgestone|broadway|broker|brother|brussels|bs|bt|budapest|bugatti|build|builders|business|buy|buzz|bv|bw|by|bz|bzh|ca|cab|cafe|cal|call|calvinklein|cam|camera|camp|cancerresearch|canon|capetown|capital|capitalone|car|caravan|cards|care|career|careers|cars|cartier|casa|case|caseih|cash|casino|cat|catering|catholic|cba|cbn|cbre|cbs|cc|cd|ceb|center|ceo|cern|cf|cfa|cfd|cg|ch|chanel|channel|chase|chat|cheap|chintai|christmas|chrome|chrysler|church|ci|cipriani|circle|cisco|citadel|citi|citic|city|cityeats|ck|cl|claims|cleaning|click|clinic|clinique|clothing|cloud|club|clubmed|cm|cn|co|coach|codes|coffee|college|cologne|com|comcast|commbank|community|company|compare|computer|comsec|condos|construction|consulting|contact|contractors|cooking|cookingchannel|cool|coop|corsica|country|coupon|coupons|courses|cr|credit|creditcard|creditunion|cricket|crown|crs|cruise|cruises|csc|cu|cuisinella|cv|cw|cx|cy|cymru|cyou|cz|dabur|dad|dance|data|date|dating|datsun|day|dclk|dds|de|deal|dealer|deals|degree|delivery|dell|deloitte|delta|democrat|dental|dentist|desi|design|dev|dhl|diamonds|diet|digital|direct|directory|discount|discover|dish|diy|dj|dk|dm|dnp|do|docs|doctor|dodge|dog|doha|domains|dot|download|drive|dtv|dubai|duck|dunlop|duns|dupont|durban|dvag|dvr|dz|earth|eat|ec|eco|edeka|edu|education|ee|eg|email|emerck|energy|engineer|engineering|enterprises|epost|epson|equipment|er|ericsson|erni|es|esq|estate|esurance|et|etisalat|eu|eurovision|eus|events|everbank|exchange|expert|exposed|express|extraspace|fage|fail|fairwinds|faith|family|fan|fans|farm|farmers|fashion|fast|fedex|feedback|ferrari|ferrero|fi|fiat|fidelity|fido|film|final|finance|financial|fire|firestone|firmdale|fish|fishing|fit|fitness|fj|fk|flickr|flights|flir|florist|flowers|fly|fm|fo|foo|food|foodnetwork|football|ford|forex|forsale|forum|foundation|fox|fr|free|fresenius|frl|frogans|frontdoor|frontier|ftr|fujitsu|fujixerox|fun|fund|furniture|futbol|fyi|ga|gal|gallery|gallo|gallup|game|games|gap|garden|gb|gbiz|gd|gdn|ge|gea|gent|genting|george|gf|gg|ggee|gh|gi|gift|gifts|gives|giving|gl|glade|glass|gle|global|globo|gm|gmail|gmbh|gmo|gmx|gn|godaddy|gold|goldpoint|golf|goo|goodhands|goodyear|goog|google|gop|got|gov|gp|gq|gr|grainger|graphics|gratis|green|gripe|grocery|group|gs|gt|gu|guardian|gucci|guge|guide|guitars|guru|gw|gy|hair|hamburg|hangout|haus|hbo|hdfc|hdfcbank|health|healthcare|help|helsinki|here|hermes|hgtv|hiphop|hisamitsu|hitachi|hiv|hk|hkt|hm|hn|hockey|holdings|holiday|homedepot|homegoods|homes|homesense|honda|honeywell|horse|hospital|host|hosting|hot|hoteles|hotels|hotmail|house|how|hr|hsbc|ht|hu|hughes|hyatt|hyundai|ibm|icbc|ice|icu|id|ie|ieee|ifm|ikano|il|im|imamat|imdb|immo|immobilien|in|industries|infiniti|info|ing|ink|institute|insurance|insure|int|intel|international|intuit|investments|io|ipiranga|iq|ir|irish|is|iselect|ismaili|ist|istanbul|it|itau|itv|iveco|iwc|jaguar|java|jcb|jcp|je|jeep|jetzt|jewelry|jio|jlc|jll|jm|jmp|jnj|jo|jobs|joburg|jot|joy|jp|jpmorgan|jprs|juegos|juniper|kaufen|kddi|ke|kerryhotels|kerrylogistics|kerryproperties|kfh|kg|kh|ki|kia|kim|kinder|kindle|kitchen|kiwi|km|kn|koeln|komatsu|kosher|kp|kpmg|kpn|kr|krd|kred|kuokgroup|kw|ky|kyoto|kz|la|lacaixa|ladbrokes|lamborghini|lamer|lancaster|lancia|lancome|land|landrover|lanxess|lasalle|lat|latino|latrobe|law|lawyer|lb|lc|lds|lease|leclerc|lefrak|legal|lego|lexus|lgbt|li|liaison|lidl|life|lifeinsurance|lifestyle|lighting|like|lilly|limited|limo|lincoln|linde|link|lipsy|live|living|lixil|lk|llc|loan|loans|locker|locus|loft|lol|london|lotte|lotto|love|lpl|lplfinancial|lr|ls|lt|ltd|ltda|lu|lundbeck|lupin|luxe|luxury|lv|ly|ma|macys|madrid|maif|maison|makeup|man|management|mango|map|market|marketing|markets|marriott|marshalls|maserati|mattel|mba|mc|mckinsey|md|me|med|media|meet|melbourne|meme|memorial|men|menu|meo|merckmsd|metlife|mg|mh|miami|microsoft|mil|mini|mint|mit|mitsubishi|mk|ml|mlb|mls|mm|mma|mn|mo|mobi|mobile|mobily|moda|moe|moi|mom|monash|money|monster|mopar|mormon|mortgage|moscow|moto|motorcycles|mov|movie|movistar|mp|mq|mr|ms|msd|mt|mtn|mtr|mu|museum|mutual|mv|mw|mx|my|mz|na|nab|nadex|nagoya|name|nationwide|natura|navy|nba|nc|ne|nec|net|netbank|netflix|network|neustar|new|newholland|news|next|nextdirect|nexus|nf|nfl|ng|ngo|nhk|ni|nico|nike|nikon|ninja|nissan|nissay|nl|no|nokia|northwesternmutual|norton|now|nowruz|nowtv|np|nr|nra|nrw|ntt|nu|nyc|nz|obi|observer|off|office|okinawa|olayan|olayangroup|oldnavy|ollo|om|omega|one|ong|onl|online|onyourside|ooo|open|oracle|orange|org|organic|origins|osaka|otsuka|ott|ovh|pa|page|panasonic|panerai|paris|pars|partners|parts|party|passagens|pay|pccw|pe|pet|pf|pfizer|pg|ph|pharmacy|phd|philips|phone|photo|photography|photos|physio|piaget|pics|pictet|pictures|pid|pin|ping|pink|pioneer|pizza|pk|pl|place|play|playstation|plumbing|plus|pm|pn|pnc|pohl|poker|politie|porn|post|pr|pramerica|praxi|press|prime|pro|prod|productions|prof|progressive|promo|properties|property|protection|pru|prudential|ps|pt|pub|pw|pwc|py|qa|qpon|quebec|quest|qvc|racing|radio|raid|re|read|realestate|realtor|realty|recipes|red|redstone|redumbrella|rehab|reise|reisen|reit|reliance|ren|rent|rentals|repair|report|republican|rest|restaurant|review|reviews|rexroth|rich|richardli|ricoh|rightathome|ril|rio|rip|rmit|ro|rocher|rocks|rodeo|rogers|room|rs|rsvp|ru|rugby|ruhr|run|rw|rwe|ryukyu|sa|saarland|safe|safety|sakura|sale|salon|samsclub|samsung|sandvik|sandvikcoromant|sanofi|sap|sapo|sarl|sas|save|saxo|sb|sbi|sbs|sc|sca|scb|schaeffler|schmidt|scholarships|school|schule|schwarz|science|scjohnson|scor|scot|sd|se|search|seat|secure|security|seek|select|sener|services|ses|seven|sew|sex|sexy|sfr|sg|sh|shangrila|sharp|shaw|shell|shia|shiksha|shoes|shop|shopping|shouji|show|showtime|shriram|si|silk|sina|singles|site|sj|sk|ski|skin|sky|skype|sl|sling|sm|smart|smile|sn|sncf|so|soccer|social|softbank|software|sohu|solar|solutions|song|sony|soy|space|spiegel|sport|spot|spreadbetting|sr|srl|srt|st|stada|staples|star|starhub|statebank|statefarm|statoil|stc|stcgroup|stockholm|storage|store|stream|studio|study|style|su|sucks|supplies|supply|support|surf|surgery|suzuki|sv|swatch|swiftcover|swiss|sx|sy|sydney|symantec|systems|sz|tab|taipei|talk|taobao|target|tatamotors|tatar|tattoo|tax|taxi|tc|tci|td|tdk|team|tech|technology|tel|telecity|telefonica|temasek|tennis|teva|tf|tg|th|thd|theater|theatre|tiaa|tickets|tienda|tiffany|tips|tires|tirol|tj|tjmaxx|tjx|tk|tkmaxx|tl|tm|tmall|tn|to|today|tokyo|tools|top|toray|toshiba|total|tours|town|toyota|toys|tr|trade|trading|training|travel|travelchannel|travelers|travelersinsurance|trust|trv|tt|tube|tui|tunes|tushu|tv|tvs|tw|tz|ua|ubank|ubs|uconnect|ug|uk|unicom|university|uno|uol|ups|us|uy|uz|va|vacations|vana|vanguard|vc|ve|vegas|ventures|verisign|versicherung|vet|vg|vi|viajes|video|vig|viking|villas|vin|vip|virgin|visa|vision|vista|vistaprint|viva|vivo|vlaanderen|vn|vodka|volkswagen|volvo|vote|voting|voto|voyage|vu|vuelos|wales|walmart|walter|wang|wanggou|warman|watch|watches|weather|weatherchannel|webcam|weber|website|wed|wedding|weibo|weir|wf|whoswho|wien|wiki|williamhill|win|windows|wine|winners|wme|wolterskluwer|woodside|work|works|world|wow|ws|wtc|wtf|xbox|xerox|xfinity|xihuan|xin|xn--11b4c3d|xn--1ck2e1b|xn--1qqw23a|xn--2scrj9c|xn--30rr7y|xn--3bst00m|xn--3ds443g|xn--3e0b707e|xn--3hcrj9c|xn--3oq18vl8pn36a|xn--3pxu8k|xn--42c2d9a|xn--45br5cyl|xn--45brj9c|xn--45q11c|xn--4gbrim|xn--54b7fta0cc|xn--55qw42g|xn--55qx5d|xn--5su34j936bgsg|xn--5tzm5g|xn--6frz82g|xn--6qq986b3xl|xn--80adxhks|xn--80ao21a|xn--80aqecdr1a|xn--80asehdb|xn--80aswg|xn--8y0a063a|xn--90a3ac|xn--90ae|xn--90ais|xn--9dbq2a|xn--9et52u|xn--9krt00a|xn--b4w605ferd|xn--bck1b9a5dre4c|xn--c1avg|xn--c2br7g|xn--cck2b3b|xn--cg4bki|xn--clchc0ea0b2g2a9gcd|xn--czr694b|xn--czrs0t|xn--czru2d|xn--d1acj3b|xn--d1alf|xn--e1a4c|xn--eckvdtc9d|xn--efvy88h|xn--estv75g|xn--fct429k|xn--fhbei|xn--fiq228c5hs|xn--fiq64b|xn--fiqs8s|xn--fiqz9s|xn--fjq720a|xn--flw351e|xn--fpcrj9c3d|xn--fzc2c9e2c|xn--fzys8d69uvgm|xn--g2xx48c|xn--gckr3f0f|xn--gecrj9c|xn--gk3at1e|xn--h2breg3eve|xn--h2brj9c|xn--h2brj9c8c|xn--hxt814e|xn--i1b6b1a6a2e|xn--imr513n|xn--io0a7i|xn--j1aef|xn--j1amh|xn--j6w193g|xn--jlq61u9w7b|xn--jvr189m|xn--kcrx77d1x4a|xn--kprw13d|xn--kpry57d|xn--kpu716f|xn--kput3i|xn--l1acc|xn--lgbbat1ad8j|xn--mgb9awbf|xn--mgba3a3ejt|xn--mgba3a4f16a|xn--mgba7c0bbn0a|xn--mgbaakc7dvf|xn--mgbaam7a8h|xn--mgbab2bd|xn--mgbai9azgqp6j|xn--mgbayh7gpa|xn--mgbb9fbpob|xn--mgbbh1a|xn--mgbbh1a71e|xn--mgbc0a9azcg|xn--mgbca7dzdo|xn--mgberp4a5d4ar|xn--mgbgu82a|xn--mgbi4ecexp|xn--mgbpl2fh|xn--mgbt3dhd|xn--mgbtx2b|xn--mgbx4cd0ab|xn--mix891f|xn--mk1bu44c|xn--mxtq1m|xn--ngbc5azd|xn--ngbe9e0a|xn--ngbrx|xn--node|xn--nqv7f|xn--nqv7fs00ema|xn--nyqy26a|xn--o3cw4h|xn--ogbpf8fl|xn--otu796d|xn--p1acf|xn--p1ai|xn--pbt977c|xn--pgbs0dh|xn--pssy2u|xn--q9jyb4c|xn--qcka1pmc|xn--qxam|xn--rhqv96g|xn--rovu88b|xn--rvc1e0am3e|xn--s9brj9c|xn--ses554g|xn--t60b56a|xn--tckwe|xn--tiq49xqyj|xn--unup4y|xn--vermgensberater-ctb|xn--vermgensberatung-pwb|xn--vhquv|xn--vuq861b|xn--w4r85el8fhu5dnra|xn--w4rs40l|xn--wgbh1c|xn--wgbl6a|xn--xhq521b|xn--xkc2al3hye2a|xn--xkc2dl3a5ee0h|xn--y9a3aq|xn--yfro4i67o|xn--ygbi2ammx|xn--zfr164b|xperia|xxx|xyz|yachts|yahoo|yamaxun|yandex|ye|yodobashi|yoga|yokohama|you|youtube|yt|yun|za|zappos|zara|zero|zip|zippo|zm|zone|zuerich|zw){1}(?:\/[a-zA-Z0-9]{1,})*)'
}

TEXT = {
    'EN' : {
        'START' : \
            'I am a Bot that fight against spammers users that join groups to spam their ' \
            'annoying and unwanted info. Check /help command for more information about my usage.',

        'HELP' : \
            'Bot help:\n' \
            '————————————————\n' \
            '- To get working the Anti-spam, you must add me to a group ang give me ' \
            'Administration privileges to let me delete spam messages.\n' \
            '\n' \
            '- Once I got Admin privileges, I\'ll watch for all new users that join the group ' \
            'and don\'t let them to publish messages that contains URLs until they have been in ' \
            'the group long as an specific time, and they have written an enough number of ' \
            'messages.\n' \
            '\n' \
            '- The time that new users need to wait and the number of messages that they need to ' \
            'write before they can publish messages with URLs are, by default, {} hours and {} ' \
            'messages, but this values can be modified and configured by using the commands ' \
            '/set_messages and /set_hours.\n' \
            '\n' \
            '- To preserve a clean group, I auto-remove messages related to me, after {} minutes ' \
            '(except Spam detection messages and Admins calls).\n' \
            '\n' \
            '- Configuration and enable/disable commands just can be used by the group ' \
            'Administrators.\n' \
            '\n' \
            '- You can change the language that I speak, using the command /language.\n' \
            '\n' \
            '- Check /commands for get a list of all avaliable commands, and a short ' \
            'description of all of them.',

        'CMD_NOT_ALLOW' : \
            'Just an Admin can use this command',

        'LANG_CHANGE' : \
            'Language changed to english.',

        'LANG_SAME' : \
            'I am already in english.\n\nMay you want to say:\n/language es',

        'LANG_BAD_LANG' : \
            'Invalid language provided. The actual languages supported are english and spanish, ' \
            'change any of them using "en" or "es".\n' \
            '\n' \
            'Example:\n' \
            '/language en\n' \
            '/language es',

        'LANG_NOT_ARG' : \
            'The command needs a language to set (en - english, es - spanish).\n' \
            '\n' \
            'Example:\n' \
            '/language en\n' \
            '/language es',

        'STATUS' : \
            'Actual configuration:\n' \
            '————————————————\n' \
            'Number of messages to allow URLs:\n' \
            '    {}\n' \
            '\n' \
            'Hours until allow URLs:\n' \
            '    {}\n' \
            '\n' \
            'Admins call when spam detected:\n' \
            '    {}\n' \
            '\n' \
            'Allow users to add Bots:\n' \
            '    {}\n' \
            '\n' \
            'Anti-spam:\n' \
            '    {}\n',

        'SET_HOURS_CHANGED' : \
            'Time successfully changed.\n\nNew users need to wait {} hours to get allowed to ' \
            'publish URLs in messages.',

        'SET_HOURS_NEGATIVE_HOUR' : \
            'Invalid time provided. The hours need to be positives.',

        'SET_HOURS_BAD_ARG' : \
            'Invalid time provided. You need to specify how many hours want to set for a new ' \
            'user to wait, until get allowed to publish URLs in messages.\n' \
            '\n' \
            'Example (5h or 24h):\n' \
            '/set_hours 5\n' \
            '/set_hours 24',

        'SET_HOURS_NOT_ARG' : \
            'No time provided. You need to specify how many hours want to set for a new ' \
            'user to wait, until get allowed to publish URLs in messages.\n' \
            '\n' \
            'Example (5h or 24h):\n' \
            '/set_hours 5\n' \
            '/set_hours 24',

        'SET_MSG_CHANGED' : \
            'Number of messages successfully changed.\n\nNew users need to send {} messages ' \
            'to get allowed to publish URLs in messages.',

        'SET_MSG_NEGATIVE' : \
            'Invalid number of messages provided. The number of messages needs to be positive.',

        'SET_MSG_BAD_ARG' : \
            'Invalid number of messages provided. You need to specify how many messages want to ' \
            'to set for a new user to wait, until get allowed to publish URLs in messages.\n' \
            '\n' \
            'Example (5 or 20):\n' \
            '/set_messages 5\n' \
            '/set_messages 20',

        'SET_MSG_NOT_ARG' : \
            'No number of messages provided. You need to specify how many messages want to ' \
            'to set for a new user to wait, until get allowed to publish URLs in messages.\n' \
            '\n' \
            'Example (5 or 20):\n' \
            '/set_messages 5\n' \
            '/set_messages 20',

        'CMD_ALLOW_USR_OK' : \
            'User {} granted to publish URLs in messages.',

        'CMD_ALLOW_USR_ALREADY_ALLOWED' : \
            'User {} is already allowed to publish URLs in messages.',
        
        'CMD_ALLOW_USR_NOT_FOUND' : \
            'User not found in my data base.',

        'CMD_ALLOW_USR_NOT_ARG' : \
            'No user provided. You need to specify the user alias/name that we want to give ' \
            'permission to publish URLs in messages.\n' \
            '\n' \
            'Examples:\n' \
            '/allow_user @mr_doe\n' \
            '/allow_user Jhon Doe',

        'ENABLE' : \
            'Anti-Spam enabled. Stop it with /disable command.',

        'DISABLE' : \
            'Anti-Spam disabled. Start it with /enable command.',

        'ALREADY_ENABLE' : \
            'I am already enabled.',

        'ALREADY_DISABLE' : \
            'I am already disabled.',

        'MSG_SPAM_HEADER' : \
            'Anti-SPAM message:\n' \
            '————————————————\n',

        'MSG_SPAM_DETECTED_0' : \
            'Message from user {} removed for the sake of a free of spam Telegram.',

        'MSG_SPAM_DETECTED_1' : \
            '\n\nNew members need to write <b>{} messages</b> and wait <b>{} hours</b> to be ' \
            'allowed to publish URLs in messages.',

        'CALLING_ADMINS' : \
            '\n\nCalling to Admins:\n\n{}',

        'CALLING_ADMINS_NO_ADMINS': \
            'There is not Admins in this chat.',

        'CALL_WHEN_SPAM_ENABLE' : \
            'Automatic call Admins when spam is detected enabled.',

        'CALL_WHEN_SPAM_DISABLE' : \
            'Automatic call Admins when spam is detected disabled.',

        'CALL_WHEN_SPAM_ALREADY_ENABLE' : \
            'Call Admins when spam is detected is already enabled.',

        'CALL_WHEN_SPAM_ALREADY_DISABLE' : \
            'Call Admins when spam is detected is already disabled.',

        'CALL_WHEN_SPAM_NOT_ARG' : \
            'The command needs enable/disable keyword.\n' \
            '\n' \
            'Example:\n' \
            '/call_when_spam enable\n' \
            '/call_when_spam disable',

        'USERS_ADD_BOTS_ENABLE' : \
            'Allow users to add Bots enabled.',

        'USERS_ADD_BOTS_DISABLE' : \
            'Allow users to add Bots disabled.',
        
        'USERS_ADD_BOTS_ALREADY_ENABLE' : \
            'Allow users to add Bots is already enabled.',

        'USERS_ADD_BOTS_ALREADY_DISABLE' : \
            'Allow users to add Bots is already disabled.',

        'USERS_ADD_BOTS_NOT_ARG' : \
            'The command needs enable/disable keyword.\n' \
            '\n' \
            'Example:\n' \
            '/users_add_bots enable\n' \
            '/users_add_bots disable',
        
        'USER_CANT_ADD_BOT' : \
            'This group don\'t allow users to invite and add Bots.\n' \
            '\n' \
            'User {} try to add the Bot {}. The Bot has been kicked.',

        'CAN_NOT_GET_ADMINS' : \
            'Can\'t use this command in the current chat.',

        'VERSION' : \
            'Actual Bot version: {}',

        'ABOUT_MSG' : \
            'This is an open-source GNU-GPL licensed Bot developed by the telegram user {}. You ' \
            'can check the code here:\n{}',

        'LINE' : \
            '\n————————————————\n',

        'LINE_LONG' : \
            '\n————————————————————————————————————————————————\n',

        'COMMANDS' : \
            'List of commands:\n' \
            '————————————————\n' \
            '/start - Show the initial information about the bot.\n' \
            '\n' \
            '/help - Show the help information.\n' \
            '\n' \
            '/commands - Show the actual message. Information about all the available commands ' \
            'and their description.\n' \
            '\n' \
            '/language - Allow to change the language of the bot messages. Actual available ' \
            'languages: en (english) - es (spanish).\n' \
            '\n' \
            '/status - Check actual configured values of all properties.\n' \
            '\n' \
            '/set_messages - Set how many published messages are need for new users to be ' \
            'allowed to publish URLs in messages.\n' \
            '\n' \
            '/set_hours - Set how many hours for new users are need to wait to get allowed to ' \
            'publish URLs in messages.\n' \
            '\n' \
            '/call_admins - Call to all Admins of the group.\n' \
            '\n' \
            '/call_when_spam - Enable/disable Admins notify when a spam message is detected.\n' \
            '\n' \
            '/users_add_bots - Enable/disable allow users to invite and add Bots to the group.\n' \
            '\n' \
            '/allow_user - Allow an user to publish URLs in messages.\n' \
            '\n' \
            '/enable - Enable the Anti-Spam.\n' \
            '\n' \
            '/disable - Disable the Anti-Spam.\n' \
            '\n' \
            '/version - Show the version of the Bot.\n' \
            '\n' \
            '/about - Show about info.'
    },
    'ES' : {
        'START' : \
            'Soy un Bot que se enfrenta a aquellos usuarios spammers que se unen a un grupo para ' \
            'exclusivamente publicar sus molestos y no bienvenidos mensajes de spam. Echa un ' \
            'vistazo al comando /help para conocer más información sobre mi uso.',

        'HELP' : \
            'Ayuda sobre el Bot:\n' \
            '————————————————\n' \
            '- Para hacer funcionar el Anti-spam, es necesario añadirme a un grupo y otorgarme ' \
            'privilegios de administración para que pueda borrar los mensajes de spam.\n' \
            '\n' \
            '- Una vez con privilegios de administración, llevaré un control sobre los usuarios ' \
            'que se unan al grupo y evitaré que escriban mensajes que contengan URLs hasta que ' \
            'haya pasado un tiempo específico desde que se unieron, y hayan escrito el ' \
            'suficiente número de mensajes.\n' \
            '\n' \
            '- El tiempo que deben esperar los nuevos usuarios y el número de mensajes que deben ' \
            'de escribir antes de poder publicar mensajes con URLs son, por defecto, {} horas y ' \
            '{} mensajes, pero estos valores pueden modificarse y configurarse haciendo uso de ' \
            'los comandos /set_messages y /set_hours.\n' \
            '\n' \
            '- Para mantener limpio el grupo, elimino aquellos mensajes que tengan relación ' \
            'conmigo, pasados {} minutos (salvo mensajes relacionados con la detección de Spam y ' \
            'llamada a Administradores).\n' \
            '\n' \
            '- Los comandos de configuraciones y activación/desactivación solo pueden ser ' \
            'utilizados por los Administradores del grupo.\n' \
            '\n' \
            '- Puedes configurar el idioma en el que hablo mediante el comando /language.\n' \
            '\n' \
            '- Echa un vistazo al comando /commands para ver una lista con todos los comandos ' \
            'disponibles y una breve descripción de cada uno de ellos.\n',

        'CMD_NOT_ALLOW' : \
            'Solo un Admin puede utilizar este comando.',

        'LANG_CHANGE' : \
            'Idioma cambiado a español.',

        'LANG_SAME' : \
            'Ya estoy en español.\n\nQuizás querías decir:\n/language en',

        'LANG_BAD_LANG' : \
            'Idioma inválidado. Los idiomas actualmente soportados son el español y el inglés, ' \
            'cambia a uno de ellos mediante las etiquetas "es" o "en".\n' \
            '\n' \
            'Ejemplo:\n' \
            '/language es\n' \
            '/language en',

        'LANG_NOT_ARG' : \
            'El comando necesita un idioma que establecer (es - español, en - inglés).\n' \
            '\n' \
            'Ejemplo:\n' \
            '/language es\n' \
            '/language en',

        'STATUS' : \
            'Configuración actual:\n' \
            '————————————————\n' \
            'Número de mensajes hasta permitir URLs:\n' \
            '    {}\n' \
            '\n' \
            'Número de horas hasta permitir URLs:\n' \
            '    {}\n' \
            '\n' \
            'Llamada a los Admins cuando se detecta spam:\n' \
            '    {}\n' \
            '\n' \
            'Permitir que los usuarios puedan añadir Bots:\n' \
            '    {}\n' \
            '\n' \
            'Anti-spam:\n' \
            '    {}\n',

        'SET_HOURS_CHANGED' : \
            'Tiempo cambiado correctamente.\n\nLos usuarios nuevos tendrán que esperar {} horas ' \
            'antes de poder publicar mensajes que contengan URLs.',

        'SET_HOURS_NEGATIVE_HOUR' : \
            'Tiempo proporcionado inválido. Las horas deben ser positivas.',

        'SET_HOURS_BAD_ARG' : \
            'Tiempo proporcionado inválido. Tienes que especificar cuántas horas serán ' \
            'necesarias que pasen desde que un usuario se unió al grupo, antes de que se le ' \
            'permita publicar mensajes que contengan URLs.\n' \
            '\n' \
            'ejemplo (5h o 24h):\n' \
            '/set_hours 5\n' \
            '/set_hours 24',

        'SET_HOURS_NOT_ARG' : \
            'No se proporcionó ningún tiempo. Tienes que especificar cuántas horas quieres que ' \
            'un nuevo usuario deba esperar antes de poder publicar mensajes que contengan URLs.\n' \
            '\n' \
            'Ejemplo (5h o 24h):\n' \
            '/set_hours 5\n' \
            '/set_hours 24',

        'SET_MSG_CHANGED' : \
            'Número de mensajes cambiado correctamente.\n\nLos usuarios nuevos tendrán que ' \
            'escribir {} mensajes, antes de que se les permita publicar mensajes que contengan ' \
            'URLs.',

        'SET_MSG_NEGATIVE' : \
            'Número de mensajes inválido. El número de mensajes debe ser positivo.',

        'SET_MSG_BAD_ARG' : \
            'Número de mensajes inválido. Tienes que especificar cuántos mensajes ' \
            'deberán de escribir los nuevos usuarios antes de que se les permita publicar ' \
            'mensajes que contengan URLs.\n' \
            '\n' \
            'Ejemplo (5 o 20):\n' \
            '/set_messages 5\n' \
            '/set_messages 20',

        'SET_MSG_NOT_ARG' : \
            'No se proporcionó el número de mensajes. Tienes que especificar cuántos mensajes ' \
            'deberán de escribir los nuevos usuarios antes de que se les permita publicar ' \
            'mensajes que contengan URLs.\n' \
            '\n' \
            'Ejemplo (5 o 20):\n' \
            '/set_messages 5\n' \
            '/set_messages 20',

        'CMD_ALLOW_USR_OK' : \
            'Usuario {} habilitado para publicar URLs en sus mensajes.',

        'CMD_ALLOW_USR_ALREADY_ALLOWED' : \
            'El usuario {} ya tenía permiso para publicar URLs en sus mensajes.',

        'CMD_ALLOW_USR_NOT_FOUND' : \
            'Usuario no encontrado en la base de datos.',

        'CMD_ALLOW_USR_NOT_ARG' : \
            'No se proporcionó el usuario. Tienes que especificar el alias/nombre del usuario al ' \
            'que se le quiere dar permiso para publicar URLs en sus mensajes.\n' \
            '\n' \
            'Ejemplos:\n' \
            '/allow_user @mr_doe\n' \
            '/allow_user Jhon Doe',

        'ENABLE' : \
            'Anti-Spam activado. Desactívalo con el comando /disable.',

        'DISABLE' : \
            'Anti-Spam desactivado. Actívalo con el comando /enable.',

        'ALREADY_ENABLE' : \
            'Ya estoy activado.',

        'ALREADY_DISABLE' : \
            'Ya estoy desactivado.',

        'MSG_SPAM_HEADER' : \
            'Mensaje Anti-SPAM:\n' \
            '————————————————\n',

        'MSG_SPAM_DETECTED_0' : \
            'Mensaje del usuario {} eliminado en aras de un Telegram libre de Spam.',

        'MSG_SPAM_DETECTED_1' : \
            '\n\nLos nuevos usuarios necesitan escribir más de <b>{} mensajes</b> y esperar ' \
            '<b>{} horas</b> para poder publicar mensajes que contengan URLs.',

        'CALLING_ADMINS' : \
            '\n\nLlamando a los Admins:\n{}',

        'CALLING_ADMINS_NO_ADMINS': \
            'No hay Administradores en el chat actual.',

        'CALL_WHEN_SPAM_ENABLE' : \
            'Activada la llamada automática a los Admins cuando se detecta spam.',

        'CALL_WHEN_SPAM_DISABLE' : \
            'Desactivada la llamada automática a los Admins cuando se detecta spam.',

        'CALL_WHEN_SPAM_ALREADY_ENABLE' : \
            'La llamada a los Admins cuando se detecta spam ya está activada.',

        'CALL_WHEN_SPAM_ALREADY_DISABLE' : \
            'La llamada a los Admins cuando se detecta spam ya está desactivada.',

        'CALL_WHEN_SPAM_NOT_ARG' : \
            'El comando requiere el parámetro enable/disable.\n' \
            '\n' \
            'Ejemplo:\n' \
            '/call_when_spam enable\n' \
            '/call_when_spam disable',

        'USERS_ADD_BOTS_ENABLE' : \
            'Activado el permiso de los usuarios para añadir Bots al grupo.',

        'USERS_ADD_BOTS_DISABLE' : \
            'Desactivado el permiso de los usuarios para añadir Bots al grupo.',
        
        'USERS_ADD_BOTS_ALREADY_ENABLE' : \
            'El permiso de los usuarios para añadir Bots ya está activado.',

        'USERS_ADD_BOTS_ALREADY_DISABLE' : \
            'El permiso de los usuarios para añadir Bots ya está desactivado.',

        'USERS_ADD_BOTS_NOT_ARG' : \
            'El comando requiere el parámetro enable/disable.\n' \
            '\n' \
            'Ejemplo:\n' \
            '/users_add_bots enable\n' \
            '/users_add_bots disable',
        
        'USER_CANT_ADD_BOT' : \
            'Este grupo no permite que los usuarios inviten y añadan Bots.\n' \
            '\n' \
            'El usuario {} intento añadir al Bot {}. El Bot fue kickeado.',
        
        'CAN_NOT_GET_ADMINS' : \
            'No se puede usar este comando en el chat actual.',

        'VERSION' : \
            'Versión actual del Bot: {}',

        'ABOUT_MSG' : \
            'Este es un Bot open-source con licencia GNU-GPL, desarrollado por el usuario de ' \
            'telegram {}. Puedes consultar el código aquí:\n{}',

        'LINE' : \
            '\n————————————————\n',

        'LINE_LONG' : \
            '\n————————————————————————————————————————————————\n',

        'COMMANDS' : \
            'Lista de comandos:\n' \
            '————————————————\n' \
            '/start - Muestra la información inicial sobre el Bot.\n' \
            '\n' \
            '/help - Muestra la información de ayuda.\n' \
            '\n' \
            '/commands - Muestra el mensaje actual. Información sobre todos los comandos ' \
            'disponibles y su descripción.\n' \
            '\n' \
            '/language - Permite cambiar el idioma en el que habla el Bot. Idiomas actualmente ' \
            'disponibles: es (español) - en (inglés).\n' \
            '\n' \
            '/status - Muestra la configuración actual de todas las propiedades.\n' \
            '\n' \
            '/set_messages - Configura cuantos mensajes han de ser publicados por un usuario ' \
            'nuevo para permitirle publicar mensajes que contengan URLs.\n' \
            '\n' \
            '/set_hours - Configura cuántas horas son necesarias que hayan pasado desde que un ' \
            'usuario nuevo se unió al grupo para permitirle publicar mensajes que contengan ' \
            'URLs.\n' \
            '\n' \
            '/call_admins - Avisa a todos los Admins del grupo.\n' \
            '\n' \
            '/call_when_spam - Activa/desactiva el aviso a los Admins cuando se detecta spam.\n' \
            '\n' \
            '/users_add_bots - Activa/desactiva el permiso de que los usuarios puedan invitar y ' \
            'añadir Bots al grupo.\n' \
            '\n' \
            '/allow_user - Permite a un usuario publicar mensajes que contengan URLs.\n' \
            '\n' \
            '/enable - Activa el Anti-Spam.\n' \
            '\n' \
            '/disable - Desactiva el Anti-Spam.\n' \
            '\n' \
            '/version - Consulta la versión del Bot.\n' \
            '\n' \
            '/about - Muestra la información \"acerca de...\" del Bot.'
    }
}
