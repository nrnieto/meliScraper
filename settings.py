FRAVEGA_WEBSITE = "https://shopping.fravega.com"  # fravega.com redirects to shopping subdomain  # TODO shopping != fravega.com
FRAVEGA_WEBSITE_NEXT_PAGE_CLASS = 'ant-pagination-next'
FRAVEGA_WEBSITE_PRODUCT_NAME_ATTRIBUTE = "itemTitle"
FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE = "price"
FRAVEGA_WEBSITE_PRODUCT_INFO_WRAPPER = "infoWrapper"
FRAVEGA_WEBSITE_SECTIONS = ["/tv-y-video/tv/",
                            "/heladeras-freezers-y-cavas/",
                            "/lavado/",
                            "/climatizacion/"]

FRAVEGA_CRAWLER_SETTINGS = {"company": "FRAVEGA",
                            "url": FRAVEGA_WEBSITE,
                            "next_page": FRAVEGA_WEBSITE_NEXT_PAGE_CLASS,
                            "product_name_attribute": FRAVEGA_WEBSITE_PRODUCT_NAME_ATTRIBUTE,
                            "product_price_attribute": FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE,
                            "sections": FRAVEGA_WEBSITE_SECTIONS,
                            "info_wrapper": FRAVEGA_WEBSITE_PRODUCT_INFO_WRAPPER
                            }

GARBARINO_WEBSITE = "https://www.garbarino.com"
GARBARINO_WEBSITE_NEXT_PAGE_CLASS = 'pagination__page'
GARBARINO_WEBSITE_PRODUCT_NAME_ATTRIBUTE = "itemBox--title"
GARBARINO_WEBSITE_PRODUCT_PRICE_ATTRIBUTE = "value-note"
GARBARINO_WEBSITE_PRODUCT_PRICE_DISCOUNT_ATTRIBUTE = "value-item"
GARBARINO_WEBSITE_PRODUCT_INFO_WRAPPER = "itemBox--info"
GARBARINO_WEBSITE_SECTIONS = ["/productos/tv-led-y-smart-tv/4342",
                              "/productos/heladeras-y-freezers/4290",
                              "/productos/lavado/4297",
                              "/productos/ventilacion-y-calefaccion/4277"
                              ]

GARBARINO_CRAWLER_SETTINGS = {"company": "GARBARINO",
                              "url": GARBARINO_WEBSITE,
                              "next_page": GARBARINO_WEBSITE_NEXT_PAGE_CLASS,
                              "product_name_attribute": GARBARINO_WEBSITE_PRODUCT_NAME_ATTRIBUTE,
                              "product_price_attribute": GARBARINO_WEBSITE_PRODUCT_PRICE_ATTRIBUTE,
                              "sections": GARBARINO_WEBSITE_SECTIONS,
                              "info_wrapper": GARBARINO_WEBSITE_PRODUCT_INFO_WRAPPER,
                              }


CHROME_DRIVER_PATH = "/usr/local/bin/chromedriver"

TV_COMMON_WORDS = {
                    "FRAVEGA": {
                        "NAME": ["TV", "SMART", "LED"],
                        "BRAND": ["SAMSUNG", "KEN", "BROWN", "PHILIPS", "LG", "SONY", "HITACHI", "NOBLEX", "PHILCO", "HISENSE", "RCA", "SANYO", "TELEFUNKEN", "TCL",
                                  "TOSHIBA", "JVC", "ADMIRAL", "SKYWORTH", "HYUNDAI"
                                  ],
                        "SIZE": ['24"', '32"', '42"', '43"', '49"', '50"', '55"', '65"', '75"'],
                        "RESOLUTION": ["4K", "FULLHD", "FULL", "HD", "ULTRA", "UHD"],
                    },
                    "GARBARINO": {
                        "NAME": ["TV"],
                        "BRAND": ["SAMSUNG", "KEN", "BROWN", "PHILIPS", "LG", "SONY", "HITACHI", "NOBLEX", "PHILCO", "HISENSE", "RCA", "SANYO", "TELEFUNKEN", "TCL",
                                  "TOSHIBA", "JVC", "ADMIRAL", "SKYWORTH", "HYUNDAI"
                                  ],
                        "SIZE": ['24', '32', '42', '43', '49', '50', '55', '65', '75'],
                        "RESOLUTION": ["4K", "FULLHD", "FULL", "HD", "ULTRA", "UHD"]
                    }
}

HELADERA_COMMON_WORDS = {
                           "FRAVEGA": {
                               "NAME": ["HELADERA"]
                           },
                           "GARBARINO": {
                               "NAME": ["HELADERA"]
                           }
}