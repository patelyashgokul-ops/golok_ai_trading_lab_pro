{
    "name": "Golok AI Trading Lab Pro",
    "summary": "Historical equity research and market data quality",
    "version": "20.0.6.0.0",
    "author": "Golok Technology",
    "license": "LGPL-3",
    "category": "Productivity",
    "depends": ["web"],
    "data": [
        "security/groups.xml",
        "security/ir.access.csv",
        "views/lab.xml",
        "views/p03.xml",
        "views/p04.xml",
        "views/p05.xml",
        "views/p06.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "golok_ai_trading_lab_pro/static/src/overview.js",
            "golok_ai_trading_lab_pro/static/src/overview.xml",
            "golok_ai_trading_lab_pro/static/src/overview.scss",
        ],
    },
    "application": True,
    "installable": True,
}
