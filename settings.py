ERR_MSG = {"GET_URL": "ERROR GETTING URL",
           "FIND_ELEMENT": "ERROR FINDING ELEMENT"}

PAGE_LOAD_TIMEOUT = 30

FRAVEGA_WEBSITE = "https://www.fravega.com"
FRAVEGA_WEBSITE_NEXT_PAGE_CLASS = 'ant-pagination-next'
FRAVEGA_WEBSITE_PRODUCT_NAME_ATTRIBUTE = "itemTitle"
FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE = "price"
FRAVEGA_WEBSITE_PRODUCT_INFO_WRAPPER = "infoWrapper"
FRAVEGA_WEBSITE_SECTIONS = ["/tv-y-video/tv/",
                            "/climatizacion/"
                            ]

GARBARINO_WEBSITE = "https://www.garbarino.com"
GARBARINO_WEBSITE_NEXT_PAGE_XPATH = "/html/body/div[4]/div[2]/div[2]/nav/ul/li[4]/a"
GARBARINO_WEBSITE_PRODUCT_NAME_ATTRIBUTE = "itemBox--title"
GARBARINO_WEBSITE_PRODUCT_PRICE_ATTRIBUTE = "value-note"
GARBARINO_WEBSITE_PRODUCT_PRICE_DISCOUNT_ATTRIBUTE = "value-item"
GARBARINO_WEBSITE_PRODUCT_INFO_WRAPPER = "itemBox--info"
GARBARINO_WEBSITE_SECTIONS = ["/productos/tv-led-y-smart-tv/4342",
                              "/productos/ventilacion-y-calefaccion/4277"
                              ]

GARBARINO_CRAWLER_SETTINGS = {"company": "GARBARINO",
                              "url": GARBARINO_WEBSITE,
                              "next_page": GARBARINO_WEBSITE_NEXT_PAGE_XPATH,
                              "product_name_attribute": GARBARINO_WEBSITE_PRODUCT_NAME_ATTRIBUTE,
                              "product_price_attribute": GARBARINO_WEBSITE_PRODUCT_PRICE_ATTRIBUTE,
                              "sections": GARBARINO_WEBSITE_SECTIONS,
                              "info_wrapper": GARBARINO_WEBSITE_PRODUCT_INFO_WRAPPER,
                              }

FRAVEGA_CRAWLER_SETTINGS = {"company": "FRAVEGA",
                            "url": FRAVEGA_WEBSITE,
                            "next_page": FRAVEGA_WEBSITE_NEXT_PAGE_CLASS,
                            "product_name_attribute": FRAVEGA_WEBSITE_PRODUCT_NAME_ATTRIBUTE,
                            "product_price_attribute": FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE,
                            "sections": FRAVEGA_WEBSITE_SECTIONS,
                            "info_wrapper": FRAVEGA_WEBSITE_PRODUCT_INFO_WRAPPER
                            }

CHROME_DRIVER_PATH = "/usr/local/bin/chromedriver"

TV_COMMON_WORDS = {
                    "FRAVEGA": {
                        "NAME": ["TV", "SMART", "LED"],
                        "BRAND": ["SAMSUNG", "KEN", "BROWN", "PHILIPS", "LG", "SONY", "HITACHI", "NOBLEX", "PHILCO", "HISENSE", "RCA", "SANYO", "TELEFUNKEN", "TCL",
                                  "TOSHIBA", "JVC", "ADMIRAL", "SKYWORTH", "HYUNDAI"
                                  ],
                        "SIZE": ['24', '32', '32”', '40', '42', '43', '49', '50', '55', '65', '75'],
                        "RESOLUTION": ["4K", "FULLHD", "FULL", "HD", "ULTRA", "UHD"],
                    },
                    "GARBARINO": {
                        "NAME": ["TV"],
                        "BRAND": ["SAMSUNG", "KEN", "BROWN", "PHILIPS", "LG", "SONY", "HITACHI", "NOBLEX", "PHILCO", "HISENSE", "RCA", "SANYO", "TELEFUNKEN", "TCL",
                                  "TOSHIBA", "JVC", "ADMIRAL", "SKYWORTH", "HYUNDAI"
                                  ],
                        "SIZE": ['24', '32', '40', '42', '43', '49', '50', '55', '65', '75'],
                        "RESOLUTION": ["4K", "FULLHD", "FULL", "HD", "ULTRA", "UHD"]
                    }
}

RESOLUTION_DICT = {"4K": ["4KULTRAHD", "4KUHD", "ULTRAHD"]}

AC_COMMON_WORDS = {
                           "FRAVEGA": {
                               "NAME": ["SPLIT"],
                               "BRAND": ["SURREY", "YORK", "BGH", "COVENTRY", "CARRIER", "ELECTRA",
                                         "SAMSUNG", "MIDEA", "PHILCO", "HISENSE"
                                         ],
                               "POWER": ["F", "FG", "FRIGORIAS"],
                               "SPLIT": ["SPLIT"],
                               "HEAT": ["FRíO/CALOR", "FRIO/CALOR", "CALOR", "FRIOCALOR", "FRÍO/CALOR"]
                           },
                           "GARBARINO": {
                               "NAME": ["SPLIT"],
                               "BRAND": ["HISENSE", "SURREY", "BGH", "PHILCO", "CARRIER", "ELECTRA", "MIDEA", "COVENTRY",
                                         "SAMSUNG", "YORK"
                                         ],
                               "POWER": ["F", "FG", "FRIGORIAS"],
                               "SPLIT": ["SPLIT"],
                               "HEAT": ["FRÍO/CALOR", "FRIO/CALOR", "CALOR", "FRIOCALOR", "FRÍO/CALOR"]
                           }
}