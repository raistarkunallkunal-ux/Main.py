import requests, json, os, time, random, threading, websocket, re, base64, queue

OWNER_ID = "1546451034392502323"

TOKENS = [
   "MTU1MDczOTE5Njg4NzU2ODQxNA.GF8y_S.eayEJ0n8NvhkVOsvGi2jk9_9g_mREAqNuZJnBw",
   "MTUyMzcxMzkxNzExMTc2Mjk4MQ.GwbAyN.NlYWqOvSZ91rpRZ4WE2moTcIwyMM-wU-5LnYps",
   "MTU1MDc1NDAwNDI1MzAxNjE3NQ.GPLAuu.7dDIRs6RDyuRsMib5Y7Zo658RI1xhr9NLJHtjo",
   "MTU0NjgxOTk3MjM1NjExMjQxOA.G7dCaD.yObI3Jw6DxWGjENQ7kXPJgw38ZukP",
   "MTU0NzYxMjM4NjE0NjM4NjAyMg.G5Xq6O.94PDXOVrmWGd4qJbXmhWhTIoO4",
   "MTU0Nzg4MTc3ODIzMDg2MTg5Nw.Gg_Du9.b9lxWuxnow-bogB_l3LYmZVP",
"MTU0Nzg4NDU4NTg1MjA4MDE3MQ.GZWp5t.8Ye9f476PFv5l2Cj4e1OeOSJQY",
"MTU0Nzg4NTY3NTQ5NDI1MjYzNA.GJeDo0.s4eCm2UQAA6YQSmZRWYuS-VcxZCF",
"MTU0Nzg4NjM4MDg5MjU2MTQ0OA.GaiK5_.U24z-1BVeRJb4A6-QZitL2whzbOupf",
"MTU0Nzg4NzYzNzEzNjgxMDAzNQ.GlrWuJ.GnHBhi4OtWFFc4jbgWmB3rX36X5Tg",
"MTU0Nzg5MDEyMTU5MDcxMDMxNQ.GmIP4G.bEcmy97v4XT11_xpqe_pyZmx5NmlZga"
]
TOKENS = [x for x in TOKENS if x.strip() and not x.startswith('.')]

SUDO_FILE = "sudo_users.json"
PREFIX = "$"

nc_on = {}; nc2_on = {}; cnc_on = {}; spam_on = {}; spam2_on = {}
spam3_on = {}; cspam_on = {}; pic_on = {}
autoreply = {}; autoreact = {}
start_time = time.time()
myid_cache = {}

GC_COOLDOWN = 3
_gc_lock = threading.Lock()
_gc_last = [0.0]


# ==================== ANTIBAN BACKOFF ====================
_rl_backoff_send = 1.0
_rl_backoff_edit = 1.0
_rl_backoff_create = 1.0

CHANNEL_PACE = 0.05   # min seconds between any 2 sends/renames in same channel (Discord limit)

nc2_stuff = [
    "𝗖ʜᴜᴅ 𝗠ᴄ 🩵⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🩶⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🩷⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🤍⃤","𝗖ʜᴜᴅ 𝗠ᴄ 💔⃤",
    "𝗖ʜᴜᴅ 𝗠ᴄ 🧡⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🖤⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🌖⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🌗⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🌒⃤",
    "𝗖ʜᴜᴅ 𝗠ᴄ 🌕⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🌘⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🌑⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🌓⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🌔⃤",
    "𝗖ʜᴜᴅ 𝗠ᴄ 🚄⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🚅⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🐂⃤","𝗖ʜᴜᴅ 𝗠ᴄ 📯⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🎧⃤",
    "𝗖ʜᴜᴅ 𝗠ᴄ 🌪️⃤","𝗖ʜᴜᴅ 𝗠ᴄ ❄️⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🌀⃤","𝗖ʜᴜᴅ 𝗠ᴄ ⚡⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🌈⃤"
]
nc2_i = {}


# ==================== CHUD MC NC2 (gcmaker auto-NC) ====================
CHUD_MC_NC2 = [
    "🩶⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🩷⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🤍⃤","𝗖ʜᴜᴅ 𝗠ᴄ 💔⃤",
    "𝗖ʜᴜᴅ 𝗠ᴄ 🧡⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🖤⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🌖⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🌗⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🌒⃤",
    "𝗖ʜᴜᴅ 𝗠ᴄ 🌕⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🌘⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🌑⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🌓⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🌔⃤",
    "𝗖ʜᴜᴅ 𝗠ᴄ 🚄⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🚅⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🐂⃤","𝗖ʜᴜᴅ 𝗠ᴄ 📯⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🎧⃤",
    "𝗖ʜᴜᴅ 𝗠ᴄ 🌪️⃤","𝗖ʜᴜᴅ 𝗠ᴄ ❄️⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🌀⃤","𝗖ʜᴜᴅ 𝗠ᴄ ⚡⃤","𝗖ʜᴜᴅ 𝗠ᴄ 🌈⃤"
]
# =====================================================================

nc_names = [
    "𝐇𝐀𝐓𝐄𝐑𝐒  𝑻𝑴𝑲𝑪 𝑴𝑬𝑰-->-ᥬ🌵᭄","𝐇𝐀𝐓𝐄𝐑𝐒  𝑻𝑴𝑲𝑪 𝑴𝑬𝑰-->-ᥬ🍈᭄",
    "𝐇𝐀𝐓𝐄𝐑𝐒  𝑻𝑴𝑲𝑪 𝑴𝑬𝑰-->-ᥬ🌶️᭄","𝐇𝐀𝐓𝐄𝐑𝐒  𝑻𝑴𝑲𝑪 𝑴𝑬𝑰-->-ᥬ🥭᭄",
    "𝐇𝐀𝐓𝐄𝐑𝐒  𝑻𝑴𝑲𝑪 𝑴𝑬𝑰-->-ᥬ🍆᭄","𝐇𝐀𝐓𝐄𝐑𝐒  𝑻𝑴𝑲𝑪 𝑴𝑬𝑰-->-ᥬ🍌᭄",
    "𝐇𝐀𝐓𝐄𝐑𝐒  𝑻𝑴𝑲𝑪 𝑴𝑬𝑰-->-ᥬ🥒᭄","𝐇𝐀𝐓𝐄𝐑𝐒  𝑻𝑴𝑲𝑪 𝑴𝑬𝑰-->-ᥬ🍇᭄",
    "𝐇𝐀𝐓𝐄𝐑𝐒  𝑻𝑴𝑲𝑪 𝑴𝑬𝑰-->-ᥬ🌽᭄","𝐇𝐀𝐓𝐄𝐑𝐒  𝑻𝑴𝑲𝑪 𝑴𝑬𝑰-->-ᥬ🍓᭄"
]

spam_base = [
    "# 𓆩 🔸𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩 🔸𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩 🔸𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩 🔸𓆪",
    "# 𓆩🈸𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈸𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩🈸𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈸𓆪",
    "# 𓆩🈷️𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈷️𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩🈷️𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈷️𓆪",
    "# 𓆩🈺𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈺𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩🈺𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈺𓆪",
    "# 𓆩🈸𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈸𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩🈸𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈸𓆪,",
    "# 𓆩🈚𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈚𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩🈚𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈚𓆪",
    "# 𓆩🈶𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈶𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩🈶𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈶𓆪",
    "# 𓆩🉑𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🉑𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩🉑𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🉑𓆪",
    "# 𓆩🈲𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈲𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩🈲𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈲𓆪",
    "# 𓆩🈹𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈹𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 𓆩🈹𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈹𓆪",
    "# 𓆩🈵𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈵𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩🈵𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈵𓆪",
    "# 𓆩🈴𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈴𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩🈴𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🈴𓆪",
    "# 𓆩㊗️𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩㊗️𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩㊗️𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩㊗️𓆪",
    "# 𓆩㊙️𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩㊙️𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩㊙️𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩㊙️𓆪",
    "# 𓆩🉐𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🉐𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩🉐𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🉐𓆪",
    "# 𓆩⛔𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩⛔𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩⛔𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩⛔𓆪",
    "# 𓆩🚫𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🚫𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩🚫𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🚫𓆪",
    "# 𓆩⭕𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩⭕𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩⭕𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩⭕𓆪",
    "# 𓆩⛎𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩⛎𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩⛎𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩⛎𓆪",
    "# 𓆩♓𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♓𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩♓𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♓𓆪",
    "# 𓆩♒𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔𝗺ᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♒𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩♒𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♒𓆪",
    "# 𓆩♑𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♑𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩♑𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♑𓆪",
    "# 𓆩♐𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♐𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩♐𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♐𓆪",
    "# 𓆩♏𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♏𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩♏𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♏𓆪",
    "# 𓆩♎𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♎𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩♎𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔𝗺ᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♎𓆪",
    "# 𓆩♍𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♍𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩♍𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♍𓆪",
    "# 𓆩♌𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♌𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩♌𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♌𓆪",
    "# 𓆩♋𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♋𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩♋𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♋𓆪",
    "# 𓆩♊𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♊𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩♊𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♊𓆪",
    "# 𓆩♉𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♉𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩♉𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♉𓆪",
    "# 𓆩♈𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♈𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩♈𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩♈𓆪",
    "# 𓆩🧭𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔𝗺ᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🧭𓆪~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~𓆩🧭𓆪##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞 #𝗥𝗻𝗗l⃠𝗖ᴇ #𝗟ᴀ𝗗ᴄ𝗘 #ɪ𝗦 #s𝗘 #𝗧ᴇ𝗭 #𝗧ᴏ #ᴋ𝗢 #𝗔ᴍᴍᴀ #𝗖𝗵ᴜᴅ𝗧ɪ #𝗛ᴀ𝗜I⃠ 𓆩🧭𓆪"
]

spam_msgs = [x * 6 for x in spam_base]

spam2_msgs = [
    "# 『𝐃ʀᴀᴋᴇ×𝐆ʜᴏsᴛ×𝐑ᴏɴɴʏ×𝐊ᴀᴢᴀᴋᴀ×𝐗ᴋᴇᴠɪɴ』 ɴᴇᴡ ɢᴇɴ ᴘɪʟʟᴀ ⃖‹🤍›⃗, " * 16,
    "# 『𝐃ʀᴀᴋᴇ×𝐆ʜᴏsᴛ×𝐑ᴏɴɴʏ×𝐊ᴀᴢᴀᴋᴀ×𝐗ᴋᴇᴠɪɴ』 ɴᴇᴡ ɢᴇɴ ᴘɪʟʟᴀ ⃖‹🖤›⃗, " * 16,
    "# 『𝐃ʀᴀᴋᴇ×𝐆ʜᴏsᴛ×𝐑ᴏɴɴʏ×𝐊ᴀᴢᴀᴋᴀ×𝐗ᴋᴇᴠɪɴ』 ɴᴇᴡ ɢᴇɴ ᴘɪʟʟᴀ ⃖‹💜›⃗, " * 16,
]

replies = [
    "𝐖ᴏ ʙʜɪ ᴋʏᴀ ᴅɪɴ ᴛʜᴇ ᴊᴀʙ ᴛʀʏ ᴍᴀᴀ ᴍᴜᴊʜᴇ 𝐀ᴘɴᴀ 𝐂ʜᴜᴛ 𝐃ᴇᴛɪ ᴛʜɪ ʏᴀᴀʀ 💔🥀👌🏻",
    "𝐀ᴡᴀᴢ 𝐍ɪᴄʜᴇ 𝐆ᴜʟᴀᴀᴍ 🤢👇🏻",
    "𝐓ʀʏ 𝐌ᴀᴀ ɴᴇ 𝐂ʜᴜᴅɴᴇ 𝐌ᴀɪ ɢᴏʟᴅ 𝐌ᴇᴅᴀʟ 𝐉ᴇᴇᴛᴀ ᴇʏ 𝐃ᴏꜱᴛ 🤩👑",
    "𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋɪ 𝐂ʜᴜᴛ 𝐌ᴇ 𝐌ᴇʀᴀ 𝐋ᴜɴᴅ 🖕🏻😈",
    "𝐁ʜᴏꜱᴀᴅɪᴋᴇ 𝐀ᴘɴɪ 𝐁ᴇʜᴇɴ 𝐂ʜᴜᴅᴀ 🖕🏻😈",
    "𝐑ᴀɴᴅɪ ᴋᴇ 𝐁ᴀᴄᴄʜᴇ 𝐀ᴜᴋᴀᴛ 𝐌ᴇ 𝐑ᴇʜ 🖕🏻😈",
    "𝐌ᴀᴅᴀʀᴄʜᴏᴅ 𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋɪ 𝐂ʜᴜᴛ 🖕🏻😈",
    "𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋᴀ 𝐁ʜᴏꜱᴅᴀ ᴋʜᴏʟ ᴅᴜɴɢᴀ 🔓😈",
    "𝐁ʜᴇɴᴄʜᴏᴅ 𝐀ᴘɴɪ 𝐀ᴜᴋᴀᴛ 𝐌ᴇ 𝐑ᴇʜ 🤡💩",
    "𝐓𝐌𝐊𝐂 ᴘᴇ 𝐂ʜᴀᴘᴘᴀʟ 𝐌ᴀᴀʀᴜɴɢᴀ 👟💥",
    "𝐁ʜᴏꜱᴅɪᴋᴇ 𝐓ᴇʀɪ 𝐊ʜᴀɴᴅᴀɴ ᴋɪ 𝐁𝐊𝐂 💀🖕🏻",
    "𝐑ᴀɴᴅɪ ᴋɪ 𝐀ᴜʟᴀᴅ ᴄʜᴜᴘ ʜᴏ ᴊᴀ 🔇😒",
    "𝐆ᴜʟᴀᴀᴍ ʜᴇɪ ᴛᴜ ᴍᴇʀᴀ ᴀʙ ᴀᴜʀ ʀᴀʜᴇɢᴀ ʙʜɪ 👑😎",
    "𝐓ᴇʀɪ 𝐁ᴇʜᴇɴ ᴋɪ 𝐂ʜᴜᴛ 𝐌ᴇ 𝐌ɪʀᴄʜɪ 🌶️🖕🏻",
    "𝐌ᴀᴅᴀʀᴄʜᴏᴅ 𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋɪ 𝐂ʜᴜᴛ 𝐌ᴇ 𝐏ᴀɪʀ 🦶🏻😈",
    "𝐁ʜᴏꜱᴀᴅɪᴋᴇ 𝐓ᴇʀɪ 𝐁ᴇʜᴇɴ ᴋᴀ 𝐁ʜᴏꜱᴅᴀ 🗑️😏",
    "𝐑ᴀɴᴅɪ ᴋᴀ 𝐏ɪʟʟᴀ ʜᴀɪ ᴛᴜ 🐕💩",
    "𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋᴏ 𝐁ᴀᴢᴀᴀʀ 𝐌ᴇ 𝐂ʜᴏᴅᴜɴɢᴀ 🌃😈",
    "𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋɪ 𝐂ʜᴜᴛ 𝐌ᴇ 𝐆ᴀʀᴀᴍ 𝐓ᴇʟ 🌡️🖕🏻",
    "𝐌ᴀᴅᴀʀᴄʜᴏᴅ 𝐓ᴇʀɪ 𝐁ᴇʜᴇɴ ᴍᴇʀɪ 𝐑ᴀɴᴅɪ 💋👿",
    "𝐑ᴀɴᴅɪ ᴋᴇ 𝐁ᴀᴄᴄʜᴇ 𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋɪ 𝐂ʜᴜᴛ 🖕🏻😈",
    "𝐓ᴇʀɪ 𝐁ᴇʜᴇɴ ᴋᴏ 𝐑ᴀᴀᴛ ʙʜᴀʀ 𝐂ʜᴏᴅᴜɴɢᴀ 🌙😈",
    "𝐑ᴀɴᴅɪ ᴋᴀ 𝐁ᴀᴄᴄʜᴀ ʜᴀɪ ᴛᴜ ꜱᴀᴀʟᴇ 🤡💀",
    "𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋɪ 𝐂ʜᴜᴛ 𝐌ᴇ 𝐌ᴇʀᴀ 𝐉ᴏᴏᴛᴀ 👞🖕🏻",
    "𝐀ᴍᴀɴ 𝐃ᴀᴅʏ ᴋᴀ 𝐆ᴜʟᴀᴀᴍ ʜᴀɪ ᴛᴜ 🥀😤",
    "ᴊɪꜱ ᴅɪɴ ᴛᴜ ᴘᴀɪᴅᴀ ʜᴜᴀ 𝐓ᴇʀɪ 𝐌ᴀᴀ ɴᴇ ꜱᴏᴄʜᴀ ᴛʜᴀ ᴋᴀꜱʜ ᴀʙᴏʀᴛ ᴋᴀʀ ᴅᴇᴛɪ 💀🥀",
    "𝐀ᴘɴɪ 𝐀ᴜᴋᴀᴛ ᴅᴇᴋʜ ᴋᴜᴛᴛᴇ 🐕😂",
    "𝐆ᴀʟɪ ᴋᴀ 𝐊ᴜᴛᴛᴀ ʜᴀɪ ᴛᴜ 🐕🗑️",
    "𝐓ᴇʀɪ 𝐌ᴀᴀ ɴᴇ ᴍᴜᴊʜᴇ ᴅᴇᴋʜ ᴋᴇ ꜱᴏᴄʜᴀ ᴋᴀꜱʜ ʏᴇ ᴍᴇʀᴀ ʙᴇᴛᴀ ʜᴏᴛᴀ 🫦😏",
    "𝐂ʜᴜᴘ ᴋᴀʀ 𝐌ᴀᴅᴀʀᴄʜᴏᴅ ᴛᴇʀɪ ᴀᴜᴋᴀᴛ ɴᴀʜɪ ᴍᴇʀᴇ ꜱᴀᴀᴍɴᴇ ʙᴏʟɴᴇ ᴋɪ 🤐💀",
    "𝐓ᴇʀɪ 𝐌ᴀᴀ ᴋɪ 𝐂ʜᴜᴅᴀɪ ᴍᴇ ᴊᴀʙ ᴍᴀɪ ᴛʜᴀ ᴛᴏ ᴛᴜ ᴘᴀɪᴅᴀ ʜᴜᴀ 💀😂",
    "𝐁ʜᴀɢ ʏᴀʜᴀɴ ꜱᴇ ᴋᴜᴛᴛᴇ ᴋᴇ ᴘɪʟʟᴇ 🐕💨",
    "𝐓ᴇʀɪ 𝐁ᴇʜᴇɴ ᴋɪ ꜱᴀᴅɪ 𝐌ᴇ ᴍᴇʀᴀ ʟᴜɴᴅ 💍😈",
    "𝐌ᴀᴅᴀʀᴄʜᴏᴅ ᴀᴘɴɪ 𝐌ᴀᴀ ᴍᴀᴛ ᴄʜᴜᴅᴀ 🖕🏻👹",
    "𝐁ʜᴇɴᴄʜᴏᴅ 𝐓ᴇʀɪ 𝐊ʜᴀɴᴅᴀɴ ᴋɪ 𝐁𝐊𝐂 💀🖕🏻",
    "𝐁𝐊𝐂 🦴🐕",
]

nc_speed = 0.05
spam_speed = 0.05
pic_speed = 0.05

_sessions = {}
def get_session(tok):
    s = _sessions.get(tok)
    if s is None:
        s = requests.Session()
        _sessions[tok] = s
    return s

def make_super():
    data = {
        "os": "Windows", "browser": "Chrome", "device": "",
        "system_locale": "en-US",
        "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "browser_version": "120.0.0.0", "os_version": "10",
        "referrer": "", "referring_domain": "",
        "referrer_current": "", "referring_domain_current": "",
        "release_channel": "stable", "client_build_number": 250000,
        "client_event_source": None
    }
    return base64.b64encode(json.dumps(data, separators=(',', ':')).encode()).decode()

SUPER = make_super()
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def hdr(tok, json_body=False):
    h = {
        "Authorization": tok, "User-Agent": UA,
        "X-Super-Properties": SUPER, "X-Discord-Locale": "en-US",
        "X-Debug-Options": "bugReporterEnabled",
        "Origin": "https://discord.com",
        "Referer": "https://discord.com/channels/@me",
    }
    if json_body: h["Content-Type"] = "application/json"
    return h

# ────────── PRIORITY SEND QUEUE ──────────
_queues = {}
_qlock = threading.Lock()
_counters = {}
_clock = threading.Lock()

def _next_id(key):
    with _clock:
        _counters[key] = _counters.get(key, 0) + 1
        return _counters[key]

def _worker(key):
    q = _queues[key]
    while True:
        pri, n, cid, fn = q.get()
        worked = False
        try:
            worked = fn()
        except Exception:
            pass
        if worked:
            time.sleep(CHANNEL_PACE)

def _get_queue(tok, cid):
    key = (tok[:10], cid)
    with _qlock:
        if key not in _queues:
            _queues[key] = queue.PriorityQueue()
            threading.Thread(target=_worker, args=(key,), daemon=True).start()
        return _queues[key], key

def _enqueue(tok, cid, fn, priority):
    q, key = _get_queue(tok, cid)
    q.put((priority, _next_id(key), cid, fn))

def _do_send_api(chan, text, reply, tok, max_retries=5):
    global _rl_backoff_send
    d = {"content": text}
    if reply:
        d["message_reference"] = {"channel_id": chan, "message_id": reply}
    for _ in range(max_retries):
        try:
            r = get_session(tok).post(
                f"https://discord.com/api/v9/channels/{chan}/messages",
                headers=hdr(tok, True), json=d, timeout=10)
            if r.status_code == 429:
                wait = (r.json().get("retry_after", 2.0) * _rl_backoff_send) + random.uniform(0.1, 0.5)
                _rl_backoff_send = min(3.0, _rl_backoff_send * 1.15)
                time.sleep(wait); continue
            elif r.status_code in (500, 502, 503, 504):
                time.sleep(1 + random.uniform(0.5, 2.0)); continue
            _rl_backoff_send = max(1.0, _rl_backoff_send * 0.9)
            return True
        except (requests.Timeout, requests.ConnectionError):
            time.sleep(0.5 + random.uniform(0, 0.5)); continue
        except Exception:
            time.sleep(0.5); continue
    return False

def _do_rename_api(chan, name, tok, max_retries=5):
    global _rl_backoff_edit
    for _ in range(max_retries):
        try:
            r = get_session(tok).patch(
                f"https://discord.com/api/v9/channels/{chan}",
                headers=hdr(tok, True), json={"name": name}, timeout=10)
            if r.status_code == 429:
                wait = (r.json().get("retry_after", 1.5) * _rl_backoff_edit) + random.uniform(0.05, 0.3)
                _rl_backoff_edit = min(3.0, _rl_backoff_edit * 1.15)
                time.sleep(wait); continue
            elif r.status_code in (500, 502, 503, 504):
                time.sleep(1 + random.uniform(0.3, 1.5)); continue
            _rl_backoff_edit = max(1.0, _rl_backoff_edit * 0.9)
            return True
        except (requests.Timeout, requests.ConnectionError):
            time.sleep(0.4 + random.uniform(0, 0.4)); continue
        except Exception:
            time.sleep(0.4); continue
    return False

def send(chan, text, reply=None, tok=None, priority=5, check=None):
    if not tok: return
    def task():
        if check and not check():
            return False
        return _do_send_api(chan, text, reply, tok)
    _enqueue(tok, chan, task, priority)

def rename(chan, name, tok=None, priority=8, check=None):
    if not tok: return
    def task():
        if check and not check():
            return False
        return _do_rename_api(chan, name, tok)
    _enqueue(tok, chan, task, priority)

# ────────── DIRECT (non-queued) helpers for gc progress ──────────
def _direct_send(chan, text, tok, max_retries=3):
    for _ in range(max_retries):
        try:
            r = get_session(tok).post(
                f"https://discord.com/api/v9/channels/{chan}/messages",
                headers=hdr(tok, True), json={"content": text}, timeout=10)
            if r.status_code in (200, 201):
                return r.json().get("id")
            if r.status_code == 429:
                time.sleep(r.json().get("retry_after", 2) + random.uniform(0.5, 1.5)); continue
            if r.status_code in (500, 502, 503, 504):
                time.sleep(1 + random.uniform(0.5, 1.5)); continue
            return None
        except:
            time.sleep(0.5); continue
    return None

def _direct_edit(chan, mid, text, tok):
    try:
        r = get_session(tok).patch(
            f"https://discord.com/api/v9/channels/{chan}/messages/{mid}",
            headers=hdr(tok, True), json={"content": text}, timeout=10)
        if r.status_code == 429:
            time.sleep(r.json().get("retry_after", 1))
            return False
        return r.status_code in (200, 201)
    except: return False

# ────────── REST ──────────
def send_pic(chan, path, tok=None, priority=8, check=None):
    if not tok or not os.path.exists(path): return
    def task():
        if check and not check(): return False
        try:
            with open(path, "rb") as f:
                r = get_session(tok).post(
                    f"https://discord.com/api/v9/channels/{chan}/messages",
                    headers=hdr(tok), files={"file": f}, timeout=15)
                if r.status_code == 429:
                    time.sleep(r.json().get("retry_after", 1))
            return True
        except: return False
    _enqueue(tok, chan, task, priority)

def grab_pic(url):
    try:
        r = requests.get(url, stream=True, timeout=10)
        if r.status_code == 200:
            p = f"tmp_{random.randint(1000,9999)}.jpg"
            with open(p, "wb") as f:
                for c in r.iter_content(1024): f.write(c)
            return p
    except: pass
    return None

def get_myid(tok):
    if tok in myid_cache: return myid_cache[tok]
    try:
        r = get_session(tok).get("https://discord.com/api/v9/users/@me",
                                headers=hdr(tok), timeout=10)
        if r.status_code == 200:
            myid_cache[tok] = r.json().get("id")
            return myid_cache[tok]
    except: pass
    return None

def check_tok(tok):
    try:
        r = requests.get("https://discord.com/api/v9/users/@me",
                         headers=hdr(tok), timeout=10)
        if r.status_code == 200:
            j = r.json(); myid_cache[tok] = j.get("id"); return j.get("id")
    except: pass
    return None

def get_name(uid, tok):
    try:
        r = get_session(tok).get(f"https://discord.com/api/v9/users/{uid}",
                                 headers=hdr(tok), timeout=10)
        if r.status_code == 200: return r.json().get("username")
    except: pass
    return None

def get_id_from_mention(m):
    m = m.replace("<@", "").replace(">", "").replace("!", "").replace("@", "")
    d = re.search(r"\d+", m)
    return d.group() if d else None

def target_name(m, tok):
    if m.startswith("<@") and m.endswith(">"):
        uid = m[2:-1].replace("!", "")
        n = get_name(uid, tok)
        return n if n else uid
    return m

def pad(t, n):
    if len(t) >= n: return t[:n]
    while len(t) < n:
        r = n - len(t) - 1
        if r <= 0: t += " "; break
        t += " " + t[:r]
    return t[:n]

def parse_delay(p):
    if len(p) < 2: return p, None
    try:
        d = float(p[-1])
        if 0.01 <= d <= 30: return p[:-1], d
    except: pass
    return p, None

def load_users():
    if os.path.exists(SUDO_FILE):
        try: return json.load(open(SUDO_FILE))
        except: return []
    return []

def save_users(u):
    json.dump(u, open(SUDO_FILE, "w"))

sudo = load_users()

# ==================== ORION EXTENSION — GC/NCMX TRACKING ====================
GC_CREATE_DELAY = 9.0
NCMX_DELAY = 2.0
ACTIVE_NCMX_GC = {}       # gc_id -> True/False
ORION_GC_IDS = []          # all GCs ever created by this run
GC_NCMX_TARGET = {"target": None}   # current target for NC
STOP_GC_FLAG = {"stop": False}      # when True, stop making new GCs

NC_BLAST_WORDS = ["𝘎𝘈𝘠","𝙉𝙄𝙂𝙂𝘼","𝙁𝘼𝙏𝙃𝙀𝙍𝙇𝙀𝙎𝙎","Bɪᴛᴄʜ","᭙ꫀꪖ𝘬","𝘴ꪶàꪜꫀ","𝑫𝑰𝑪𝑲 𝑬𝑨𝑻𝑬𝑹","𝖲𝖫𝖴𝖳"]
NC_BLAST_EMOJIS = ["💤","🎀","💋","💗","💫","✨","🌟","🩵","💙","🤍","💜","👑","🔱","⚜️","〽️","🕐","🕑","🕒","🕓","⏱️","🦁","🦅","🐺","🦂","🐍","🐆","🦈","⛓️‍💥","🖤","☠️","⚔️","🥀","🕯️","🎭"]
NC_BLAST_PATTERNS = [
    "𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫",
    "𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷",
    "🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫🩷𒐫",
    "𒐫🩵𒐫💙𒐫🤍𒐫💜𒐫🩷𒐫❤️𒐫💖𒐫💗𒐫💓𒐫💘𒐫💝𒐫💞𒐫💕𒐫💚𒐫🩵𒐫💙𒐫🤍𒐫💜𒐫🩷𒐫❤️"
]
NC_MX_PATTERNS = [
    "{target}-𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿-𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫🩷𒐫𒐫𒐫-💋",
    "{target}-𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿-𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫❤️𒐫𒐫𒐫-💋",
    "{target}-𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿-𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫💜𒐫𒐫𒐫-💋",
    "{target}-𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿-𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫💙𒐫𒐫𒐫𒐫-💋",
    "{target}-𝙈𝘼𝘿𝘼𝙍𝘾𝙃⭕𝘿-𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫🧡𒐫𒐫𒐫-💋"
]
# ============================================================


# ────────── DM / GC ──────────

# ==================== GCMAKER → NCMX (3s delay) WORKER ====================
ACTIVE_GCMAKER_NCMX = {}   # gc_id -> True/False (separate from $makegc ncmx)
GCMAKER_NCMX_DELAY = 3.0   # 3 second delay between each rename

def _gcmaker_ncmx_loop(g_id, target, tok):
    """Ares gcmaker → NC2 style: <target>      𝗖ʜᴜᴅ 𝗠ᴄ <emoji>⃤ (with filler)"""
    key = g_id
    idx = 0
    while ACTIVE_GCMAKER_NCMX.get(key, False):
        try:
            s = CHUD_MC_NC2[idx % len(CHUD_MC_NC2)]
            idx += 1

            base = f"{target}      {s}"
            if len(base) > 50:
                allow = 50 - len("      " + s)
                base = base[:50] if allow < 0 else target[:allow] + "      " + s

            need = 100 - 2 * len(base)
            if need < 0:
                base = base[:50]
                need = 100 - 2 * len(base)
            filler = "𒐫" * need

            final = (base + filler + base)[:100]

            _do_rename_api(g_id, final, tok)
            time.sleep(GCMAKER_NCMX_DELAY)
        except: time.sleep(GCMAKER_NCMX_DELAY)


def _gcmaker_start_ncmx(g_id, target, tok):
    """Start 3s NCMX on a single GC created by $gcmaker"""
    if ACTIVE_GCMAKER_NCMX.get(g_id, False): return
    ACTIVE_GCMAKER_NCMX[g_id] = True
    threading.Thread(target=_gcmaker_ncmx_loop,
                     args=(g_id, target, tok), daemon=True).start()

def _gcmaker_stop_ncmx_all():
    """Stop all $gcmaker NCMX loops"""
    for g in list(ACTIVE_GCMAKER_NCMX.keys()):
        ACTIVE_GCMAKER_NCMX[g] = False
# ==========================================================================



# ==================== OXR GC STATS (PERSISTENT) ====================
OXR_STATS_FILE = "oxr_stats.json"

def _oxr_load_stats():
    try:
        if os.path.exists(OXR_STATS_FILE):
            with open(OXR_STATS_FILE, "r") as f:
                return json.load(f)
    except: pass
    return {"total_made": 0, "gc_ids": []}

def _oxr_save_stats(stats):
    try:
        with open(OXR_STATS_FILE, "w") as f:
            json.dump(stats, f)
    except: pass

OXR_STATS = _oxr_load_stats()   # {"total_made": int, "gc_ids": [list]}

def _oxr_add_gc(g_id):
    """Add a GC to persistent stats + active NC tracking"""
    if g_id not in OXR_STATS["gc_ids"]:
        OXR_STATS["gc_ids"].append(g_id)
        OXR_STATS["total_made"] = OXR_STATS.get("total_made", 0) + 1
        _oxr_save_stats(OXR_STATS)

def _oxr_active_nc_count():
    """Count how many stored GCs currently have NC running"""
    try:
        all_ids = set(OXR_STATS.get("gc_ids", []))
        active = set()
        for g in ACTIVE_NCMX_GC.keys():
            if ACTIVE_NCMX_GC[g]: active.add(g)
        for g in ACTIVE_GCMAKER_NCMX.keys():
            if ACTIVE_GCMAKER_NCMX[g]: active.add(g)
        return len(all_ids & active)
    except:
        return 0
# ===================================================================


def create_gc(recipients, tok, name=None, max_retries=5):
    global _rl_backoff_create
    payload = {"recipients": recipients}
    if name: payload["name"] = name[:100]
    for _ in range(max_retries):
        try:
            r = get_session(tok).post("https://discord.com/api/v9/users/@me/channels",
                                      headers=hdr(tok, True), json=payload, timeout=15)
            if r.status_code == 429:
                wait = (r.json().get("retry_after", 5) * _rl_backoff_create) + random.uniform(1, 3)
                _rl_backoff_create = min(5.0, _rl_backoff_create * 1.2)
                pass  # silent retry
                time.sleep(wait); continue
            elif r.status_code in (500, 502, 503, 504):
                time.sleep(2 + random.uniform(1, 3)); continue
            _rl_backoff_create = max(1.0, _rl_backoff_create * 0.9)
            if r.status_code in (200, 201): return True, r.json().get("id")
            return False, f"HTTP {r.status_code}"
        except (requests.Timeout, requests.ConnectionError):
            time.sleep(1 + random.uniform(0.5, 1.5)); continue
        except Exception as e:
            return False, str(e)[:60]
    return False, "max retries"

def leave_guild(gid, tok):
    try:
        r = get_session(tok).delete(
            f"https://discord.com/api/v9/users/@me/guilds/{gid}",
            headers=hdr(tok, True), json={"lurking": False}, timeout=10)
        if r.status_code in (200, 204): return True, "ok"
        if r.status_code == 404: return False, "not in that server"
        if r.status_code == 403: return False, "403 - no perms / owner"
        if r.status_code == 401: return False, "bad token"
        if r.status_code == 429:
            time.sleep(r.json().get("retry_after", 2)); return False, "rate limited"
        return False, f"HTTP {r.status_code}"
    except Exception as e:
        return False, str(e)[:60]

def leave_dm(cid, tok):
    try:
        r = get_session(tok).delete(
            f"https://discord.com/api/v9/channels/{cid}/recipients/@me",
            headers=hdr(tok), timeout=10)
        if r.status_code in (200, 204): return True, "ok"
        r2 = get_session(tok).delete(
            f"https://discord.com/api/v9/channels/{cid}",
            headers=hdr(tok), timeout=10)
        if r2.status_code in (200, 204): return True, "ok"
        return False, f"HTTP {r.status_code}"
    except Exception as e:
        return False, str(e)[:60]



# ==================== ORION EXTENSION — NCMX WORKER ====================
def _orion_ncmx_loop(g_id, target, tok):
    """NCMX loop — keeps renaming a specific GC with target"""
    key = g_id
    idx = 0
    while ACTIVE_NCMX_GC.get(key, False):
        try:
            pat = NC_MX_PATTERNS[idx % len(NC_MX_PATTERNS)]
            idx += 1
            new = pat.replace("{target}", target)
            if len(new) >= 100: new = new[:100]
            _do_rename_api(g_id, new, tok)
            time.sleep(NCMX_DELAY + random.uniform(0, 0.5))
        except: time.sleep(NCMX_DELAY)

def _orion_start_ncmx_on_gc(g_id, target, tok):
    if ACTIVE_NCMX_GC.get(g_id, False): return
    ACTIVE_NCMX_GC[g_id] = True
    threading.Thread(target=_orion_ncmx_loop, args=(g_id, target, tok), daemon=True).start()

def _orion_stop_ncmx_all():
    for g in list(ACTIVE_NCMX_GC.keys()):
        ACTIVE_NCMX_GC[g] = False

def get_friend_ids(tok):
    try:
        r = get_session(tok).get("https://discord.com/api/v9/users/@me/relationships",
                                headers=hdr(tok), timeout=10)
        if r.status_code == 200:
            return [f['id'] for f in r.json() if not f.get('user', {}).get('bot', False)]
    except: pass
    return []

def create_gc(recipients, tok, name=None):
    try:
        payload = {"recipients": recipients}
        if name: payload["name"] = name[:100]
        r = get_session(tok).post("https://discord.com/api/v9/users/@me/channels",
                                  headers=hdr(tok, True), json=payload, timeout=15)
        if r.status_code == 429: return False, "rate limited"
        if r.status_code in (200, 201): return True, r.json().get("id")
        return False, f"HTTP {r.status_code}"
    except Exception as e:
        return False, str(e)[:60]

def _orion_makegc_worker(tname, user_ids, gc_count, cmd_channel, tok, mode):
    """mode: 'ncmx' or 'ncblast' or 'none'"""
    friend_ids = get_friend_ids(tok)
    valid_users = [uid for uid in user_ids if uid in friend_ids]
    if len(valid_users) < 1:
        send(cmd_channel, "Error: oxr:Friend not accepted", tok=tok, priority=0); return

    created = 0
    for i in range(1, gc_count + 1):
        if STOP_GC_FLAG["stop"]: break
        s = (i-1)*5; e = i*5
        members = valid_users[s:e]
        if len(members) < 2: members = valid_users[:min(5, len(valid_users))]
        if len(members) < 2:
            members = valid_users[:2] if len(valid_users) >= 2 else valid_users
        try:
            ok, res = create_gc(members, tok, f"{tname}-{i}")
            if ok:
                ORION_GC_IDS.append(res)
                created += 1
                if mode == "ncmx":
                    _orion_start_ncmx_on_gc(res, tname, tok)
                elif mode == "ncblast":
                    # reuse ncblast-style worker
                    ACTIVE_NCMX_GC[res] = True
                    def _blast(g_id=res):
                        pi = 0
                        while ACTIVE_NCMX_GC.get(g_id, False):
                            try:
                                em = random.choice(NC_BLAST_EMOJIS)
                                ins = random.choice(NC_BLAST_WORDS)
                                nm = f"{tname} {em} {ins}"
                                if len(nm) < 100:
                                    p = NC_BLAST_PATTERNS[pi % len(NC_BLAST_PATTERNS)]; pi += 1
                                    need = 100 - len(nm)
                                    nm += p * (need // len(p)) + p[:need % len(p)]
                                _do_rename_api(g_id, nm[:100], tok)
                                time.sleep(NCMX_DELAY + random.uniform(0, 0.5))
                            except: time.sleep(NCMX_DELAY)
                    threading.Thread(target=_blast, daemon=True).start()
                print(f"\033[92m[GC] ✅ {tname}-{i} ({created}/{gc_count})\033[0m")
            else:
                print(f"\033[91m[GC] ❌ {tname}-{i}: {res}\033[0m")
        except Exception as ex:
            print(f"\033[91m[GC] ❌ {i}: {ex}\033[0m")
        time.sleep(GC_CREATE_DELAY)
    send(cmd_channel, f"✅ Done: {created}/{gc_count} GCs created ({mode})", tok=tok, priority=0)


def do_join(code, tok):
    try:
        r = get_session(tok).post(f"https://discord.com/api/v9/invites/{code}",
                                  headers=hdr(tok), timeout=10)
        return r.status_code == 200
    except: return False

# ────────── LOOPS ──────────
def do_nc(gid, name, tok, delay=None):
    k = f"{gid}_{tok[:10]}"
    while nc_on.get(k):
        line = random.choice(nc_names)
        new = line.replace("𝐇𝐀𝐓𝐄𝐑𝐒", name)
        new = pad(new, 100) if len(new) < 100 else new[:100]
        rename(gid, new, tok, priority=8, check=lambda k=k: nc_on.get(k))
        time.sleep(CHANNEL_PACE)

def do_nc2(gid, name, tok, delay=None):
    k = f"{gid}_{tok[:10]}"
    if k not in nc2_i: nc2_i[k] = 0
    while nc2_on.get(k):
        s = nc2_stuff[nc2_i[k] % len(nc2_stuff)]
        nc2_i[k] = (nc2_i[k] + 1) % len(nc2_stuff)
        base = f"{name}      {s}"
        if len(base) > 50:
            allow = 50 - len("      " + s)
            base = base[:50] if allow < 0 else name[:allow] + "      " + s
        need = 100 - 2 * len(base)
        if need < 0:
            base = base[:50]; need = 100 - 2 * len(base)
        filler = "𒐫" * need
        final = (base + filler + base)[:100]
        rename(gid, final, tok, priority=8, check=lambda k=k: nc2_on.get(k))
        time.sleep(CHANNEL_PACE)

def do_cnc(gid, text, tok, delay=None):
    k = f"{gid}_{tok[:10]}"
    while cnc_on.get(k):
        final = text[:100] if len(text) >= 100 else pad(text, 100)
        rename(gid, final, tok, priority=8, check=lambda k=k: cnc_on.get(k))
        time.sleep(CHANNEL_PACE)

def do_spam(cid, name, tok, delay=None):
    k = f"{cid}_{tok[:10]}"
    while spam_on.get(k):
        for m in spam_msgs:
            if not spam_on.get(k): break
            msg = m.replace("##𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞", name).replace("𝗗ʀᴀ𝗩ɪ𝗢ɴ#𝗩ɪ𝗗𝗜𝗗ʜ𝗔ʏᴀ𝗞", name)
            if len(msg) > 2000: msg = msg[:2000]
            send(cid, msg, tok=tok, priority=8, check=lambda k=k: spam_on.get(k))
            time.sleep(CHANNEL_PACE)

def do_spam2(cid, name, tok, delay=None):
    k = f"{cid}_{tok[:10]}"
    while spam2_on.get(k):
        for m in spam2_msgs:
            if not spam2_on.get(k): break
            send(cid, pad(m.replace("{ph}", name), 2000), tok=tok, priority=8,
                 check=lambda k=k: spam2_on.get(k))
            time.sleep(CHANNEL_PACE)

def do_spam3(cid, name, tok, delay=None):
    k = f"{cid}_{tok[:10]}"
    while spam3_on.get(k):
        s = random.choice(nc2_stuff)
        line = f"{name}      {s}"
        block = "# " + line + "\n𒐫𒐫\n𒐫𒐫\n𒐫𒐫\n𒐫𒐫\n𒐫𒐫\n" + line
        msg = ""
        while True:
            test = msg + block + "\n" if msg else block
            if len(test) <= 2000: msg = test
            else: break
        if len(msg) < 2000: msg += " " * (2000 - len(msg))
        send(cid, msg, tok=tok, priority=8, check=lambda k=k: spam3_on.get(k))
        time.sleep(CHANNEL_PACE)

def do_cspam(cid, text, tok, delay=None):
    k = f"{cid}_{tok[:10]}"
    while cspam_on.get(k):
        send(cid, text[:2000], tok=tok, priority=8, check=lambda k=k: cspam_on.get(k))
        time.sleep(CHANNEL_PACE)

def do_pic(cid, path, tok, delay=None):
    k = f"{cid}_{tok[:10]}"
    while pic_on.get(k):
        send_pic(cid, path, tok, priority=8, check=lambda k=k: pic_on.get(k))
        time.sleep(CHANNEL_PACE)

# ────────── HELP ──────────
def send_help(cid, tok):
    part1 = (
        "```ansi\n"
        "\u001b[1;35m╔══════════════════════════════════════════════════════════╗\u001b[0m\n"
        "\u001b[1;35m║\u001b[0m      \u001b[1;36m𝐎 𝐗 𝐑 🪽💤 (orion X renux)\u001b[0m   \u001b[1;35m·\u001b[0m   \u001b[1;37mV 5\u001b[0m   \u001b[1;35m·\u001b[0m   \u001b[1;33mᴘ ʀ ᴇ ᴍ ɪ ᴜ ᴍ\u001b[0m           \u001b[1;35m║\u001b[0m\n"
        "\u001b[1;35m║\u001b[0m      \u001b[0;37mᴜɴʟᴇᴀꜱʜ · ᴅᴏᴍɪɴᴀᴛᴇ · ᴏᴡɴ ᴛʜᴇ ɢʀɪᴅ\u001b[0m            \u001b[1;35m║\u001b[0m\n"
        "\u001b[1;35m╚══════════════════════════════════════════════════════════╝\u001b[0m\n\n"
        "\u001b[1;36m▸ ɴᴀᴍᴇ ᴄʜᴀɴɢᴇ\u001b[0m\n"
        "   \u001b[1;33m$nc\u001b[0m @user [delay]         \u001b[0;37mclassic rename\u001b[0m\n"
        "   \u001b[1;33m$nc2\u001b[0m @user [delay]        \u001b[0;37mchud suffix cycle\u001b[0m\n"
        "   \u001b[1;33m$customnc\u001b[0m <text> [delay]  \u001b[0;37mcustom rename\u001b[0m\n"
        "   \u001b[1;33m$stopnc\u001b[0m · \u001b[1;33m$stopnc2\u001b[0m · \u001b[1;33m$stopcustomnc\u001b[0m\n\n"
        "\u001b[1;36m▸ ꜱᴘᴀᴍ\u001b[0m\n"
        "   \u001b[1;33m$spam\u001b[0m @user [delay]         \u001b[0;37mv1 flood\u001b[0m\n"
        "   \u001b[1;33m$spam2\u001b[0m <name> [delay]       \u001b[0;37mv2 flood\u001b[0m\n"
        "   \u001b[1;33m$spam3\u001b[0m @user [delay]         \u001b[0;37mv3 block flood\u001b[0m\n"
        "   \u001b[1;33m$customspam\u001b[0m <text> [delay] \u001b[0;37mown text\u001b[0m\n"
        "   \u001b[1;33m$picspam\u001b[0m <url> [delay]     \u001b[0;37mimage flood\u001b[0m\n"
        "   \u001b[1;33m$stopspam\u001b[0m · \u001b[1;33m$stopspam2\u001b[0m · \u001b[1;33m$stopspam3\u001b[0m\n"
        "   \u001b[1;33m$stopcustomspam\u001b[0m · \u001b[1;33m$stoppicspam\u001b[0m\n"
        "```"
    )
    send(cid, part1, tok=tok, priority=0)
    time.sleep(0.6)
    part2 = (
        "```ansi\n"
        "\u001b[1;36m▸ ɢᴄ ᴍᴀᴋᴇʀ\u001b[0m\n"
        "   \u001b[1;33m$gcmaker\u001b[0m <n> (<name>) @u1,@u2   \u001b[0;37mbulk (Ares style)\u001b[0m\n"
        "   \u001b[1;33m$makegc\u001b[0m <n> <target> @u1 @u2 [ncmx/ncblast]   \u001b[0;37mOrion GC maker\u001b[0m\n"
        "   \u001b[1;33m$startnc\u001b[0m <target>   \u001b[0;37mstart NCMX on all GCs\u001b[0m\n"
        "   \u001b[1;33m$stopncgc\u001b[0m   \u001b[0;37mstop NCMX in all GCs\u001b[0m\n"
        "   \u001b[1;33m$stopallgc\u001b[0m   \u001b[0;37mstop GC maker + NCMX\u001b[0m\n"
        "   \u001b[1;33m$stopgcmakernc\u001b[0m   \u001b[0;37mstop $gcmaker NCMX only\u001b[0m\n\n"
        "\u001b[1;36m▸ ꜱᴇʀᴠᴇʀ / ᴄʜᴀɴɴᴇʟ\u001b[0m\n"
        "   \u001b[1;33m$join\u001b[0m <invite>              \u001b[0;37mjoin server\u001b[0m\n"
        "   \u001b[1;33m$leave\u001b[0m                     \u001b[0;37mleave current\u001b[0m\n"
        "   \u001b[1;33m$leave\u001b[0m <guild_id>            \u001b[0;37mleave server id\u001b[0m\n\n"
        "\u001b[1;36m▸ ᴀᴜᴛᴏ\u001b[0m\n"
        "   \u001b[1;33m$autoreply\u001b[0m @user           \u001b[0;37madd target\u001b[0m\n"
        "   \u001b[1;33m$removeautoreply\u001b[0m @user   \u001b[0;37mremove target\u001b[0m\n"
        "   \u001b[1;33m$stopautoreply\u001b[0m\n"
        "   \u001b[1;33m$autoreact\u001b[0m <emoji>         \u001b[0;37mauto react\u001b[0m\n"
        "   \u001b[1;33m$stopautoreact\u001b[0m\n\n"
        "\u001b[1;36m▸ ꜱʏꜱᴛᴇᴍ\u001b[0m\n"
        "   \u001b[1;33m$stopall\u001b[0m                 \u001b[0;37mkill channel tasks\u001b[0m\n"
        "   \u001b[1;33m$ping\u001b[0m · \u001b[1;33m$status\u001b[0m           \u001b[0;37mlatency / info\u001b[0m\n"
        "   \u001b[1;33m$showusers\u001b[0m               \u001b[0;37maccess list\u001b[0m\n"
        "   \u001b[1;33m$access\u001b[0m @user            \u001b[0;37mowner only\u001b[0m\n"
        "   \u001b[1;33m$removeaccess\u001b[0m @user      \u001b[0;37mowner only\u001b[0m\n\n"
        "\u001b[1;35m──────────────────────────────────────────────────────────\u001b[0m\n"
        "   \u001b[0;37mᴅᴇʟᴀʏ ʀᴀɴɢᴇ\u001b[0m  0.01s - 30s (min effective 1.05s)\n"
        "   \u001b[0;37ᴇxᴀᴍᴘʟᴇ\u001b[0m      \u001b[1;33m$spam3 test 0.2\u001b[0m\n"
        "```"
    )
    send(cid, part2, tok=tok, priority=0)

    # OXR STATS APPENDED
    try:
        send(cid, f"```ansi\n\u001b[1;35mTotal GCs (NC running): {_oxr_active_nc_count()}\u001b[0m\n\u001b[0;37mTotal ever made: {OXR_STATS.get('total_made', 0)}\u001b[0m\n```", tok=tok, priority=0)
    except: pass


# ────────── BOT ──────────
def start_bot(tok, idx):
    def on_msg(ws, m):
        global PREFIX
        try: d = json.loads(m)
        except: return

        if d.get("op") == 10:
            iv = d["d"]["heartbeat_interval"] / 1000
            def hb():
                while True:
                    time.sleep(iv)
                    try: ws.send(json.dumps({"op": 1, "d": None}))
                    except: break
            threading.Thread(target=hb, daemon=True).start()
            ws.send(json.dumps({"op": 2, "d": {"token": tok,
                "properties": {"$os": "windows", "$browser": "chrome", "$device": "pc"}}}))
            print(f"\033[92m[ORION]\033[0m node #{idx+1} online · ...{tok[-8:]}")
            return

        if d.get("t") != "MESSAGE_CREATE": return
        msg = d["d"]
        aid = msg["author"]["id"]
        text = msg["content"].strip()
        cid = msg["channel_id"]
        mid = msg["id"]
        gid = msg.get("guild_id")
        k = f"{cid}_{tok[:10]}"

        myid = myid_cache.get(tok)
        if myid is None:
            threading.Thread(target=get_myid, args=(tok,), daemon=True).start()
            myid = ""

        if cid in autoreply and aid in autoreply[cid] and aid != myid:
            send(cid, random.choice(replies), reply=mid, tok=tok, priority=0)

        if cid in autoreact and aid != myid:
            def _r():
                try:
                    get_session(tok).put(
                        f"https://discord.com/api/v9/channels/{cid}/messages/{mid}/reactions/"
                        f"{requests.utils.quote(autoreact[cid])}/@me",
                        headers=hdr(tok), timeout=10)
                except: pass
            threading.Thread(target=_r, daemon=True).start()

        # ==================== PREFIX-ONLY ROAST (BEFORE AUTH) ====================
        # Works for EVERYONE — servers, DMs, GCs
        if text.startswith(PREFIX) and len(text) == len(PREFIX):
            if aid != OWNER_ID and aid not in sudo:
                def _roast_r():
                    try:
                        get_session(tok).post(
                            f"https://discord.com/api/v9/channels/{cid}/messages",
                            headers=hdr(tok, True),
                            json={
                                "content": "*BAAP SE SUDO LEKE A TATTE \U0001F525\U0001FABD*",
                                "message_reference": {"channel_id": cid, "message_id": mid}
                            }, timeout=10)
                    except: pass
                threading.Thread(target=_roast_r, daemon=True).start()
                return
        # ========================================================================

        if aid != OWNER_ID and aid not in sudo: return
        if not text.startswith(PREFIX): return
        c = text[len(PREFIX):].strip()
        cl = c.lower()


        # ==================== ORION EXTENSION COMMANDS ====================
        if cl.startswith("makegc "):
            p = c.split()
            if len(p) < 3:
                send(cid, "usage: $makegc <count> <target> @users [ncmx/ncblast]", tok=tok, priority=0); return
            try:
                gc_count = int(p[1])
                if gc_count < 1: raise ValueError
            except:
                send(cid, "invalid count", tok=tok, priority=0); return
            target_str = p[2]
            user_ids = []
            mode = "ncmx"
            for part in p[3:]:
                pl = part.lower()
                if pl in ("ncmx","ncblast","none"): mode = pl; continue
                uid = get_id_from_mention(part)
                if uid: user_ids.append(uid)
            if len(user_ids) < 1:
                send(cid, "need at least 1 user", tok=tok, priority=0); return
            STOP_GC_FLAG["stop"] = False
            GC_NCMX_TARGET["target"] = target_str
            threading.Thread(target=_orion_makegc_worker,
                args=(target_str, user_ids, gc_count, cid, tok, mode),
                daemon=True).start()
            send(cid, f"⚡ $makegc started | target: {target_str} | mode: {mode}", tok=tok, priority=0)
            return

        if cl == "stopgcmakernc":
            _gcmaker_stop_ncmx_all()
            send(cid, "🛑 stopped NCMX on all $gcmaker GCs", tok=tok, priority=0)
            return

        if cl == "startgcnc2":
            try:
                gcs = list(ACTIVE_GCMAKER_NCMX.keys())
            except:
                gcs = []
            if not gcs:
                send(cid, "❌ no $gcmaker GCs found", tok=tok, priority=0); return
            target = GC_NCMX_TARGET.get("target") or "orion"
            for g in gcs:
                _gcmaker_start_ncmx(g, target, tok)
            send(cid, f"⚡ NC2 started on {len(gcs)} GCs | target: {target}", tok=tok, priority=0)
            return

        if cl == "stopgcnc2":
            _gcmaker_stop_ncmx_all()
            send(cid, "🛑 NC2 stopped on all $gcmaker GCs", tok=tok, priority=0)
            return

        if cl == "oxrreset":
            if aid != OWNER_ID:
                send(cid, "owner only", tok=tok, priority=0); return
            OXR_STATS["total_made"] = 0
            OXR_STATS["gc_ids"] = []
            _oxr_save_stats(OXR_STATS)
            send(cid, "✅ OXR stats reset", tok=tok, priority=0)
            return

        if cl == "stopallgc":
            STOP_GC_FLAG["stop"] = True
            _orion_stop_ncmx_all()
            send(cid, "🛑 GC making stopped + NC stopped in all GCs", tok=tok, priority=0)
            return

        if cl.startswith("startnc "):
            p = c.split(maxsplit=1)
            if len(p) < 2:
                send(cid, "usage: $startnc <target>", tok=tok, priority=0); return
            target = p[1].strip()
            GC_NCMX_TARGET["target"] = target
            # Start NC in all tracked GCs
            gids = ORION_GC_IDS[:] if ORION_GC_IDS else list(ACTIVE_NCMX_GC.keys())
            if not gids:
                send(cid, "no GCs to start NC on", tok=tok, priority=0); return
            nums = []
            for g in gids:
                _orion_start_ncmx_on_gc(g, target, tok)
                # find index in ORION_GC_IDS for label
                try: nums.append(str(ORION_GC_IDS.index(g) + 1))
                except: nums.append("?")
            label = ", ".join(nums)
            send(cid, f"NOW starting `NC on =~ {target} ({label})`", tok=tok, priority=0)
            return

        if cl == "stopncgc":
            _orion_stop_ncmx_all()
            send(cid, "🛑 NC stopped in all GCs", tok=tok, priority=0)
            return

        # ==================== $setprefix ====================
        if cl.startswith("setprefix "):
            if aid != OWNER_ID and aid not in sudo:
                send(cid, "only authorized users can change prefix", tok=tok, priority=0); return
            p = c.split(maxsplit=1)
            if len(p) < 2 or not p[1].strip():
                send(cid, f"usage: $setprefix <new> | current: `{PREFIX}`", tok=tok, priority=0); return
            new_p = p[1].strip()
            if len(new_p) > 3:
                send(cid, "prefix max 3 chars", tok=tok, priority=0); return
            old_p = PREFIX
            globals()["PREFIX"] = new_p
            send(cid, f"✅ prefix changed: `{new_p}` | old: `{old_p}`", tok=tok, priority=0)
            return

        if cl == "showprefix":
            send(cid, f"current prefix: `{PREFIX}`", tok=tok, priority=0)
            return

        # ==================== $gcall (message in ALL GCs) ====================
        if cl.startswith("gcall "):
            msg_text = c[6:].strip()
            if not msg_text:
                send(cid, "usage: $gcall <message>", tok=tok, priority=0); return
            # Merge both GC lists (orion $makegc + gcmaker)
            gcs_to_send = []
            try:
                gcs_to_send.extend(list(ORION_GC_IDS))
            except: pass
            try:
                for g in ACTIVE_GCMAKER_NCMX.keys():
                    if g not in gcs_to_send: gcs_to_send.append(g)
            except: pass
            # Also include ORION's $makegc NCMX-tracked GCs
            try:
                for g in ACTIVE_NCMX_GC.keys():
                    if g not in gcs_to_send: gcs_to_send.append(g)
            except: pass

            if not gcs_to_send:
                send(cid, "❌ no GCs found in list", tok=tok, priority=0); return

            total = len(gcs_to_send)
            send(cid, f"⚡ $gcall sending to **{total}** GCs (3s delay each)...", tok=tok, priority=0)

            def _gcall_worker():
                sent_ok = 0
                sent_fail = 0
                for g in gcs_to_send:
                    try:
                        d = {"content": msg_text}
                        r = get_session(tok).post(
                            f"https://discord.com/api/v9/channels/{g}/messages",
                            headers=hdr(tok, True), json=d, timeout=10)
                        if r.status_code in (200, 201):
                            sent_ok += 1
                        elif r.status_code == 429:
                            time.sleep(r.json().get("retry_after", 2))
                            sent_fail += 1
                        else:
                            sent_fail += 1
                    except:
                        sent_fail += 1
                    time.sleep(3.0)  # 3 second delay per GC
                send(cid, f"✅ $gcall done | ✅ {sent_ok} | ❌ {sent_fail} | total {total}", tok=tok, priority=0)

            threading.Thread(target=_gcall_worker, daemon=True).start()
            return

        if cl == "help":
            threading.Thread(target=send_help, args=(cid, tok), daemon=True).start(); return

        if cl.startswith("nc "):
            p, dl = parse_delay(c.split())
            if len(p) < 2: send(cid, "usage: $nc @user [delay]", tok=tok, priority=0); return
            n = target_name(p[1], tok)
            nc_on[k] = True
            threading.Thread(target=do_nc, args=(cid, n, tok, dl), daemon=True).start()
            send(cid, f"nc on -> {n}" + (f" | delay {dl}s" if dl else ""), tok=tok, priority=0)
            return

        if cl == "stopnc":
            nc_on[k] = False; send(cid, "nc off", tok=tok, priority=0); return

        if cl.startswith("nc2 "):
            p, dl = parse_delay(c.split())
            if len(p) < 2: send(cid, "usage: $nc2 @user [delay]", tok=tok, priority=0); return
            n = target_name(p[1], tok)
            nc2_on[k] = True
            threading.Thread(target=do_nc2, args=(cid, n, tok, dl), daemon=True).start()
            send(cid, f"nc2 on -> {n}" + (f" | delay {dl}s" if dl else ""), tok=tok, priority=0); return

        if cl == "stopnc2":
            nc2_on[k] = False; send(cid, "nc2 off", tok=tok, priority=0); return

        if cl.startswith("customnc "):
            p, dl = parse_delay(c.split())
            if len(p) < 2: send(cid, "usage: $customnc <text> [delay]", tok=tok, priority=0); return
            txt = " ".join(p[1:])
            cnc_on[k] = True
            threading.Thread(target=do_cnc, args=(cid, txt, tok, dl), daemon=True).start()
            send(cid, "cnc on" + (f" | delay {dl}s" if dl else ""), tok=tok, priority=0); return

        if cl == "stopcustomnc":
            cnc_on[k] = False; send(cid, "cnc off", tok=tok, priority=0); return

        if cl.startswith("spam "):
            p, dl = parse_delay(c.split())
            if len(p) < 2: send(cid, "usage: $spam @user [delay]", tok=tok, priority=0); return
            n = target_name(p[1], tok)
            spam_on[k] = True
            threading.Thread(target=do_spam, args=(cid, n, tok, dl), daemon=True).start()
            send(cid, f"spam on -> {n}" + (f" | delay {dl}s" if dl else ""), tok=tok, priority=0); return

        if cl == "stopspam":
            spam_on[k] = False; send(cid, "spam off", tok=tok, priority=0); return

        if cl.startswith("spam2 "):
            p, dl = parse_delay(c.split())
            if len(p) < 2: send(cid, "usage: $spam2 <name> [delay]", tok=tok, priority=0); return
            n = target_name(p[1], tok)
            spam2_on[k] = True
            threading.Thread(target=do_spam2, args=(cid, n, tok, dl), daemon=True).start()
            send(cid, f"spam2 on -> {n}" + (f" | delay {dl}s" if dl else ""), tok=tok, priority=0); return

        if cl == "stopspam2":
            spam2_on[k] = False; send(cid, "spam2 off", tok=tok, priority=0); return

        if cl.startswith("spam3 "):
            p, dl = parse_delay(c.split())
            if len(p) < 2: send(cid, "usage: $spam3 @user [delay]", tok=tok, priority=0); return
            n = target_name(p[1], tok)
            spam3_on[k] = True
            threading.Thread(target=do_spam3, args=(cid, n, tok, dl), daemon=True).start()
            send(cid, f"spam3 on -> {n}" + (f" | delay {dl}s" if dl else ""), tok=tok, priority=0); return

        if cl == "stopspam3":
            spam3_on[k] = False; send(cid, "spam3 off", tok=tok, priority=0); return

        if cl.startswith("customspam "):
            p, dl = parse_delay(c.split())
            if len(p) < 2: send(cid, "usage: $customspam <text> [delay]", tok=tok, priority=0); return
            txt = " ".join(p[1:])
            cspam_on[k] = True
            threading.Thread(target=do_cspam, args=(cid, txt, tok, dl), daemon=True).start()
            send(cid, "cspam on" + (f" | delay {dl}s" if dl else ""), tok=tok, priority=0); return

        if cl == "stopcustomspam":
            cspam_on[k] = False; send(cid, "cspam off", tok=tok, priority=0); return

        if cl.startswith("picspam "):
            p, dl = parse_delay(c.split())
            if len(p) < 2: send(cid, "usage: $picspam <url> [delay]", tok=tok, priority=0); return
            path = grab_pic(p[1])
            if not path: send(cid, "couldnt grab image", tok=tok, priority=0); return
            pic_on[k] = True
            threading.Thread(target=do_pic, args=(cid, path, tok, dl), daemon=True).start()
            send(cid, "pic spam on" + (f" | delay {dl}s" if dl else ""), tok=tok, priority=0); return

        if cl == "stoppicspam":
            pic_on[k] = False; send(cid, "pic spam off", tok=tok, priority=0); return

        # ────────── GCMAKER WITH LIVE PROGRESS BAR ──────────
        if cl.startswith("gcmaker "):
            match = re.search(r"gcmaker\s+(\d+)\s+\((.*?)\)\s+(.*)", cl)
            if not match:
                send(cid, "usage: $gcmaker <count> (<name>) @u1,@u2", tok=tok, priority=0); return
            count = int(match.group(1))
            gc_name = match.group(2)
            user_ids = re.findall(r"\d+", match.group(3))
            if not user_ids:
                send(cid, "no valid user ids found", tok=tok, priority=0); return
            if len(user_ids) > 9: user_ids = user_ids[:9]

            def make():
                results = []   # list of (ok: bool, msg: str)

                def render(status_line):
                    done_n = len(results)
                    filled = int((done_n / count) * 16) if count else 0
                    bar = "█" * filled + "░" * (16 - filled)
                    lines = [f"**GC MAKER**  `[ {bar} ]` **{done_n}/{count}**"]
                    lines.append(f"```{status_line}```")
                    show = results[-6:]
                    if len(results) > 6:
                        lines.insert(1, f"_... +{len(results)-6} earlier_")
                    for ok, m in show:
                        lines.append(("✅ " if ok else "❌ ") + m)
                    out = "\n".join(lines)
                    return out[:1990]

                # initial message — direct (not queued) so it appears immediately
                mid_progress = _direct_send(cid, render(f"starting · {count} gc(s) · {len(user_ids)} user(s)"), tok)

                for i in range(count):
                    # wait for cooldown, live-updating the bar
                    while True:
                        with _gc_lock:
                            elapsed = time.time() - _gc_last[0]
                            if elapsed >= GC_COOLDOWN: break
                        remain = GC_COOLDOWN - elapsed
                        if mid_progress:
                            _direct_edit(cid, mid_progress,
                                         render(f"waiting cooldown · {remain:.1f}s left"), tok)
                        time.sleep(1)

                    if mid_progress:
                        _direct_edit(cid, mid_progress,
                                     render(f"creating gc {i+1}/{count}..."), tok)

                    # OXR: check friends before making
                    _fids = get_friend_ids(tok)
                    _nf = [u for u in user_ids if u not in _fids]
                    if _nf:
                        if mid_progress:
                            _direct_edit(cid, mid_progress,
                                f"**Error: oxr:Friend not accepted**", tok)
                        else:
                            send(cid, "Error: oxr:Friend not accepted", tok=tok, priority=0)
                        break
                    ok, res = create_gc(user_ids, tok, gc_name)
                    with _gc_lock:
                        _gc_last[0] = time.time()

                    if ok:
                        results.append((True, f"`#{i+1}` https://discord.com/channels/@me/{res}"))
                        # ⚡ AUTO-NCMX: 3s delay
                        try:
                            ORION_GC_IDS.append(res)
                            _oxr_add_gc(res)
                            _gcmaker_start_ncmx(res, gc_name, tok)
                        except: pass
                    else:
                        results.append((False, f"`#{i+1}` failed · {res}"))

                    if mid_progress:
                        _direct_edit(cid, mid_progress, render(f"progress {len(results)}/{count}"), tok)

                done_count = sum(1 for ok, _ in results if ok)
                if mid_progress:
                    _direct_edit(cid, mid_progress,
                                 render(f"done · {done_count}/{count} created ✓"), tok)
                else:
                    send(cid, f"gcmaker done · {done_count}/{count}", tok=tok, priority=0)

            threading.Thread(target=make, daemon=True).start()
            return

        if cl.startswith("join "):
            p = c.split()
            if len(p) < 2: send(cid, "usage: $join <code>", tok=tok, priority=0); return
            code = p[1].split("/")[-1]
            def _j():
                if do_join(code, tok): send(cid, "joined", tok=tok, priority=0)
                else: send(cid, "join failed", tok=tok, priority=0)
            threading.Thread(target=_j, daemon=True).start(); return

        if cl == "leave":
            def _l():
                send(cid, "𝐆𝐀𝐌𝐄 𝐎𝐕𝐄𝐑 𝐁𝐘 𝐎 𝐗 𝐑 🪽💤 (orion X renux)\nhttps://cdn.discordapp.com/attachments/1546499667565482024/1550756422944559165/video_20260919_120019-ezgif.com-video-to-gif-converter.gif?ex=6aaf7df6&is=6aae2c76&hm=4de30018a69b870368cd93af55df5a6ff590d11db0c0697ad3c0ca8b2127c92f&",
                     tok=tok, priority=0)
                time.sleep(1)
                if gid: leave_guild(gid, tok)
                else: leave_dm(cid, tok)
            threading.Thread(target=_l, daemon=True).start(); return

        if cl.startswith("leave "):
            p = c.split()
            if len(p) < 2 or not p[1].isdigit():
                send(cid, "usage: $leave <guild_id>", tok=tok, priority=0); return
            g2 = p[1]
            def _l2():
                ok, info = leave_guild(g2, tok)
                send(cid, ("left server" if ok else f"cant leave: {info}"), tok=tok, priority=0)
            threading.Thread(target=_l2, daemon=True).start(); return

        if cl == "stopall":
            tp = tok[:10]
            for dd in [nc_on, nc2_on, cnc_on, spam_on, spam2_on, spam3_on, cspam_on, pic_on]:
                for kk in list(dd.keys()):
                    if kk.startswith(f"{cid}_") and kk.endswith(tp): dd[kk] = False
            if cid in autoreply: del autoreply[cid]
            if cid in autoreact: del autoreact[cid]
            # ⚡ ANTIBAN/GC: ALSO stop GC maker + NCMX on all GCs
            try:
                STOP_GC_FLAG["stop"] = True
                _orion_stop_ncmx_all()
                _gcmaker_stop_ncmx_all()
            except: pass
            send(cid, "✅ stopped everything (nc + spam + gcmaker + ncmx)", tok=tok, priority=0); return

        if cl.startswith("autoreply "):
            p = c.split()
            if len(p) < 2: send(cid, "usage: $autoreply @user", tok=tok, priority=0); return
            ids = [get_id_from_mention(x) for x in p[1:]]
            ids = [i for i in ids if i]
            if not ids: send(cid, "no ids", tok=tok, priority=0); return
            if cid not in autoreply: autoreply[cid] = []
            for i in ids:
                if i not in autoreply[cid]: autoreply[cid].append(i)
            send(cid, f"added {len(ids)}", tok=tok, priority=0); return

        if cl.startswith("removeautoreply "):
            p = c.split()
            if len(p) < 2: send(cid, "usage: $removeautoreply @user", tok=tok, priority=0); return
            i = get_id_from_mention(p[1])
            if i and cid in autoreply and i in autoreply[cid]:
                autoreply[cid].remove(i)
                if not autoreply[cid]: del autoreply[cid]
                send(cid, "removed", tok=tok, priority=0)
            else: send(cid, "not found", tok=tok, priority=0)
            return

        if cl == "stopautoreply":
            if cid in autoreply: del autoreply[cid]
            send(cid, "cleared", tok=tok, priority=0); return

        if cl.startswith("autoreact "):
            p = c.split()
            if len(p) < 2: send(cid, "usage: $autoreact <emoji>", tok=tok, priority=0); return
            autoreact[cid] = p[1]
            send(cid, "set", tok=tok, priority=0); return

        if cl == "stopautoreact":
            if cid in autoreact: del autoreact[cid]
            send(cid, "stopped", tok=tok, priority=0); return

        if cl == "ping":
            def _p():
                t = time.time()
                try: get_session(tok).get("https://discord.com/api/v9/users/@me",
                                          headers=hdr(tok), timeout=5)
                except: pass
                ms = (time.time() - t) * 1000
                send(cid, f"```ansi\n\u001b[1;36m⚡ ᴘ ᴏ ɴ ɢ\u001b[0m · \u001b[1;33m{ms:.0f} ms\u001b[0m\n```",
                     tok=tok, priority=0)
            threading.Thread(target=_p, daemon=True).start(); return

        if cl == "status":
            up = round(time.time() - start_time, 1)
            mins = int(up // 60); secs = int(up % 60)
            on = "\u001b[1;32m●\u001b[0m"; off = "\u001b[1;31m○\u001b[0m"
            stat = (
                "```ansi\n"
                "\u001b[1;35m╔══════════════════════════════════════════╗\u001b[0m\n"
                "\u001b[1;35m║\u001b[0m      \u001b[1;36m𝐎 𝐗 𝐑 🪽💤 (orion X renux)\u001b[0m  \u001b[1;35m·\u001b[0m  \u001b[1;37mV 5  ꜱ ᴛ ᴀ ᴛ ᴜ ꜱ\u001b[0m        \u001b[1;35m║\u001b[0m\n"
                "\u001b[1;35m╚══════════════════════════════════════════╝\u001b[0m\n"
                f"   \u001b[1;36mᴜᴘᴛɪᴍᴇ\u001b[0m     ·  {mins}m {secs}s\n"
                f"   \u001b[1;36ᴛᴏᴋᴇɴꜱ\u001b[0m     ·  {len(TOKENS)}\n"
                f"   \u001b[1;36ᴜꜱᴇʀꜱ\u001b[0m      ·  {len(sudo)}\n\n"
                "   \u001b[1;33m── ɴᴏᴅᴇ ᴛʜʀᴇᴀᴅꜱ ──\u001b[0m\n"
                f"     nc  {on if nc_on.get(k) else off}   nc2  {on if nc2_on.get(k) else off}\n"
                f"     spam {on if spam_on.get(k) else off}   spam2 {on if spam2_on.get(k) else off}\n"
                f"     spam3 {on if spam3_on.get(k) else off}   pic  {on if pic_on.get(k) else off}\n"
                "```"
            )
            send(cid, stat, tok=tok, priority=0); return

        if cl == "showusers":
            if not sudo: send(cid, "no users", tok=tok, priority=0)
            else: send(cid, "\n".join(f"<@{u}>" for u in sudo), tok=tok, priority=0)
            return

        if cl.startswith("access "):
            if aid != OWNER_ID: send(cid, "owner only", tok=tok, priority=0); return
            p = c.split()
            if len(p) < 2: send(cid, "usage: $access @user", tok=tok, priority=0); return
            i = get_id_from_mention(p[1])
            if not i: send(cid, "bad id", tok=tok, priority=0); return
            if i in sudo: send(cid, "already has it", tok=tok, priority=0)
            else:
                sudo.append(i); save_users(sudo); send(cid, "given", tok=tok, priority=0)
            return

        if cl.startswith("removeaccess "):
            if aid != OWNER_ID: send(cid, "owner only", tok=tok, priority=0); return
            p = c.split()
            if len(p) < 2: send(cid, "usage: $removeaccess @user", tok=tok, priority=0); return
            i = get_id_from_mention(p[1])
            if i and i in sudo:
                sudo.remove(i); save_users(sudo); send(cid, "removed", tok=tok, priority=0)
            else: send(cid, "no access", tok=tok, priority=0)
            return

    while True:
        try:
            ws = websocket.WebSocketApp("wss://gateway.discord.gg/?v=9&encoding=json", on_message=on_msg)
            ws.run_forever()
        except:
            time.sleep(5)

print("\033[95m╔══════════════════════════════════════════════════════════╗")
print("\033[95m║\033[0m          \033[1;36m𝐀 𝐑 𝐄 𝐒\u001b[0m   \033[1;35m·\033[0m   \033[1;37mV 5\u001b[0m                     \033[95m║\033[0m")
print("\033[95m║\033[0m          \033[1;33mᴘ ʀ ᴇ ᴍ ɪ ᴜ ᴍ   ꜱ ᴇ ʟ ꜰ ʙ ᴏ ᴛ\033[0m          \033[95m║\033[0m")
print("\033[95m╚══════════════════════════════════════════════════════════╝\033[0m\n")

good = []
for i, t in enumerate(TOKENS):
    u = check_tok(t)
    if u:
        print(f"\033[92m[✓]\033[0m node #{i+1}  ·  {u}")
        good.append(t)
    else:
        print(f"\033[91m[✗]\033[0m node #{i+1}  ·  dead")

print()
for i, t in enumerate(good):
    threading.Thread(target=start_bot, args=(t, i), daemon=True).start()
    time.sleep(2)

print(f"\n\033[1;36m{len(good)} node(s) online. ctrl+c to stop.\033[0m")
while True:
    time.sleep(1)
