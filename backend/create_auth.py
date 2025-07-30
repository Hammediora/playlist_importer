#!/usr/bin/env python3
"""
Script to create YouTube Music auth file from headers
"""

import json

def create_auth_file():
    # Headers from the user's request
    headers = {
        "Cookie": "VISITOR_INFO1_LIVE=BY8k6kBJYZ0; VISITOR_PRIVACY_METADATA=CgJVUxIEGgAgNQ%3D%3D; LOGIN_INFO=AFmmF2swRQIgF1yGC8VgOK2FGUliiZdR5mtja0ZJIsc8uCGSMj37Um0CIQD1nZcKiGOxC34p0_6KwSeCGbTP05SIAIETj1R73CgxZQ:QUQ3MjNmek5rbXA2S1NvSXo1OUpybVRHZnJPY2tMUTRxTVB1b25TRVpjVm0wdmhXV3VVUXg4VjFPZTBmdU9pS3dCV2tSOWs5M0xaY3BWb1BrdVk0Ym0wS3V4N2hTdFU3d21VeTBMWkFVSnNhQWxaMW14S3NvVEMyeHJOdDNZeWdQa29nQmQ4WlE5SUNTcWo3R2tuelNISktxYVdULUxFcEZB; _ga=GA1.1.1812519507.1734142392; _ga_2D63NQQFBG=GS1.1.1734142392.1.0.1734142400.0.0.0; HSID=ANHQl17VFZ7crGDt8; SSID=AEd5hUpkubiRA2qTv; APISID=SzoskHXvirF_-nma/A_IkzS4ReSFVBXTt9; SAPISID=AN7Y7TVhH6WlAn1X/Agg-RToiN9weI66tu; __Secure-1PAPISID=AN7Y7TVhH6WlAn1X/Agg-RToiN9weI66tu; __Secure-3PAPISID=AN7Y7TVhH6WlAn1X/Agg-RToiN9weI66tu; PREF=tz=America.Chicago&f7=100&f5=20000&repeat=NONE&autoplay=true&f6=40000000&volume=31; _gcl_au=1.1.966196942.1744393140; SID=g.a000yQiJ6gLXTkMUZllWZjBN1Ptl_sKO3XihUKXZZnpWdmrLWjH4WQl77BGMaf5r6tJCmzqE9AACgYKARQSARcSFQHGX2MiSc2IitCVTF4sdVlbk11EHRoVAUF8yKqdbS0IC-dIKb5WaZVGhjAM0076; __Secure-1PSID=g.a000yQiJ6gLXTkMUZllWZjBN1Ptl_sKO3XihUKXZZnpWdmrLWjH4mJozhl349n7VzcTg8S5hPQACgYKAeASARcSFQHGX2MiAvjAFm5uylcutjAeOkY00RoVAUF8yKrAHRP3e1QVh4i1IF0namJO0076; __Secure-3PSID=g.a000yQiJ6gLXTkMUZllWZjBN1Ptl_sKO3XihUKXZZnpWdmrLWjH4XAbK6sroGLvB9EIKICbe_gACgYKAXMSARcSFQHGX2MiQIJenh5mUnyJSfwBulKneRoVAUF8yKr3QfMGTfns_7mFm8L5vL7C0076; YSC=MVYEXPewpTg; __Secure-ROLLOUT_TOKEN=CLnxoqrJ0ZuRlgEQlcrSlN2AiwMY_-OYy6OtjgM%3D; __Secure-1PSIDTS=sidts-CjIB5H03P5PdOHQljFarGNalvcX41SdRc7PcimoUqqCjpK4rPNdLUHmY28jxTdXxIeiSeBAA; __Secure-3PSIDTS=sidts-CjIB5H03P5PdOHQljFarGNalvcX41SdRc7PcimoUqqCjpK4rPNdLUHmY28jxTdXxIeiSeBAA; SIDCC=AKEyXzUYk93IIpaREifyAU2Wq0KVl7ZIWyIlr7I5xwWCs1LlhF7fhkLwQ-Xkd1U65NrLIVP7g40; __Secure-1PSIDCC=AKEyXzXgYNCtqvGihC6rK2Mk-vKIHcpDS1qvL77aCuU1b2PUZ-5bP-OgFZzP7wymMzq-JlKHs1QT; __Secure-3PSIDCC=AKEyXzUqL-cly5X5YnmqtoXykPHBpgsNKye1L15qH7eBlmbXrlDJYVEXqyu6ffiZpgYjV1EmRtY; CONSISTENCY=AKreu9tbz4LxLu9fMsLgXYxiJkoJoknYzN9_5woCwWNmvEVCD3iQaOS0oX-tm1FC5R8uq6g_8GGFKmn4yyrhzdnhBxAc82U8H_qKq38W0QBtEfiIlbHjHT0WKDe2MroWc-f3ccQvmTJBmORESgfsKaBb",
        "X-Goog-AuthUser": "0",
        "X-Goog-Visitor-Id": "CgtCWThrNmtCSllaMCiFu7fDBjIKCgJVUxIEGgAgNQ%3D%3D",
        "Authorization": "SAPISIDHASH 1752030759_22860914d52194c9661cbccf59e7d3768805a6b5_u SAPISID1PHASH 1752030759_22860914d52194c9661cbccf59e7d3768805a6b5_u SAPISID3PHASH 1752030759_22860914d52194c9661cbccf59e7d3768805a6b5_u",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/json",
        "X-Origin": "https://music.youtube.com",
        "X-YouTube-Bootstrap-Logged-In": "true",
        "X-YouTube-Client-Name": "67",
        "X-YouTube-Client-Version": "1.20250707.03.00"
    }
    
    # Write to temp_auth.json
    with open('temp_auth.json', 'w') as f:
        json.dump(headers, f, indent=2)
    
    print("✅ Auth file created: temp_auth.json")
    print("You can now copy the contents of this file and paste it into your app!")

if __name__ == "__main__":
    create_auth_file() 