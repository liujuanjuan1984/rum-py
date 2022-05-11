# hours: 最近x小时内的内容才会被推送
commands = {
    "0": {"text": "取消所有订阅", "group_id": None},
    "1": {
        "text": "订阅 去中心微博",
        "group_id": "3bb7a3be-d145-44af-94cf-e64b992ff8f0",
        "hours": -3,
    },
    "2": {
        "text": "订阅 Huoju在Rum上说了啥",
        "group_id": "f1bcdebd-4f1d-43b9-89d0-88d5fc896660",
        "hours": -12,
    },
    "3": {
        "text": "订阅 去中心推特",
        "group_id": "bd119dd3-081b-4db6-9d9b-e19e3d6b387e",
        "hours": -3,
    },
    "4": {
        "text": "订阅 RUM流动池与汇率",
        "group_id": "0be13ee2-10dc-4e3a-b3ba-3f2c440a6436",
        "hours": -1,
    },
    "5": {
        "text": "订阅 MOB流动池与汇率",
        "group_id": "dd90f5ec-2f63-4cff-b838-91695fe9150f",
        "hours": -1,
    },
    "10": {
        "text": "订阅 刘娟娟的朋友圈",
        "group_id": "4e784292-6a65-471e-9f80-e91202e3358c",
        "hours": -6,
    },
    "11": {
        "text": "订阅 杰克深的朋友圈",
        "group_id": "cfb42114-0ee1-429b-86e5-7659108972be",
        "hours": -6,
    },
    "20": {
        "text": "订阅 每天一分钟，知晓天下事",
        "group_id": "a6aac332-7c8d-4632-bf3c-725368bb89d5",
        "hours": -24,
    },
    "99": {"text": "订阅以上所有", "group_id": -1},
}


rum_adds = "\n👨‍👩‍👧‍👦 获取最佳用户体验，安装 Rum Apps 🥂: https://rumsystem.net/apps\n"


welcome_text = "👋 hello 您有任何疑问或建议，请私聊刘娟娟" + (
    "\n🤖 输入数字，订阅相应的种子网络：\n" + "\n".join([key + " " + commands[key]["text"] for key in commands]) + rum_adds
)
