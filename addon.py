import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import sys
from urllib.parse import urlencode, parse_qsl

# Define the URL base of the plugin
BASE_URL = sys.argv[0]
HANDLE = int(sys.argv[1])

# Get the addon path and define the resources path
ADDON_PATH = xbmcaddon.Addon().getAddonInfo('path')
RESOURCES_PATH = f"{ADDON_PATH}/resources"

# Define categories with automatic icon path
CATEGORIES = [
    {"name": "FÚTBOL", "subcategories": [], "icon": f"{RESOURCES_PATH}/futbol.png"},
    {"name": "CHAMPIONS", "subcategories": [], "icon": f"{RESOURCES_PATH}/champions.png"},
    {"name": "GOLF", "subcategories": [], "icon": f"{RESOURCES_PATH}/golf.png"},
    {"name": "DAZN", "subcategories": [], "icon": f"{RESOURCES_PATH}/dazn.png"},
    {"name": "F1", "subcategories": [], "icon": f"{RESOURCES_PATH}/f1.png"},
    {"name": "BALONCESTO", "subcategories": [], "icon": f"{RESOURCES_PATH}/baloncesto.png"},
    {"name": "OTROS", "subcategories": [], "icon": f"{RESOURCES_PATH}/otros.png"},
]

# Define AceStream channels
ACESTREAM_CHANNELS = [
    # ... your existing AceStream channel definitions here ...
    {"name": "F1 | DAZN F1 | 1080", "url": "acestream://5789ca155323664edd293b848606688edf803f4d"},
    {"name": "F1 | DAZN F1 | 1080 (OP2)", "url": "acestream://9dad717d99b29a05672166258a77c25b57713dd5"},
    {"name": "F1 | DAZN F1 | 720", "url": "acestream://e1fcad9de0c782c157fde6377805c58297ab65c2"},
    {"name": "F1 | DAZN F1 MULTICAMARA (FÓRMULA 1)", "url": "acestream://968627d24eec1c16b51d88e4a4a6c02211e3346e"},
    {"name": "F1 | DAZN F1 UHD", "url": "acestream://6b94479c24898700089e6b87d28a3ccc72dc4041"},
    {"name": "FÚTBOL | M. LA LIGA | 4K", "url": "acestream://dce1579e3a2e5bd29071fca8eae364f1eb3205cf"},
    {"name": "FÚTBOL | M. LA LIGA | 1080P", "url": "acestream://aa82e7d4f03061f2144a2f4be22f2e2210d42280"},
    {"name": "FÚTBOL | M. LA LIGA | 720", "url": "acestream://f031f5728b32f6089dda28edebe990cf198108d8"},
    {"name": "FÚTBOL | M. LA LIGA 2 | 1080", "url": "acestream://26029f72a4ca831d09deefe89534818db1d105bc"},
    {"name": "FÚTBOL | M. LA LIGA 2 | 720", "url": "acestream://80126b240f3e4e004754fd8f8103e857ab2556a0"},
    {"name": "FÚTBOL | M. LA LIGA 3 | 1080", "url": "acestream://4c4844564313e39a888f593511f299f5ba3cf929"},
    {"name": "FÚTBOL | M. LA LIGA 4 | 1080", "url": "acestream://aa8f826da70e27a26b29c7b32402f17e8a67a8b0"},
    {"name": "FÚTBOL | M. LA LIGA 5 | 1080", "url": "acestream://535394f62a810bc5aeb25be75ea5ff7d03e070b2"},
    {"name": "FÚTBOL | M. LA LIGA 6 | 1080", "url": "acestream://c896d37778f9e43549a788fc22206a655895b51b"},
    {"name": "FÚTBOL | LA LIGA BAR | 1080", "url": "acestream://aa82e7d4f03061f2144a2f4be22f2e2210d42280"},
    {"name": "FÚTBOL | DAZN LaLiga | 1080", "url": "acestream://1960a9be8ae9e8c755330218eac4c5805466290a"},
    {"name": "FÚTBOL | DAZN LaLiga | 1080", "url": "acestream://75251ba975132ec9a202806ba5bf606e87280c96"},
    {"name": "FÚTBOL | DAZN LaLiga | 720", "url": "acestream://a3bca895c58d3fc7d5e4259d3d5e3cf0291d1914"},
    {"name": "FÚTBOL | DAZN LaLiga 2 | 1080", "url": "acestream://e33e666c393ef04ebe99a9b92135d2e0b48c4d10"},
    {"name": "FÚTBOL | DAZN LaLiga 2 | 720", "url": "acestream://02b9307c5c97c86914cc5939d6bbeb5b4ec60b47"},
    {"name": "FÚTBOL | DAZN LaLiga 3 | 1080", "url": "acestream://8c71f0e0a5476e10950fc827f9d2a507340aba74"},
    {"name": "FÚTBOL | DAZN LaLiga 4 | 1080", "url": "acestream://2792a8a5f4a3f53cd72dec377a2639cd12a6973e"},
    {"name": "FÚTBOL | DAZN LaLiga 5 | 1080", "url": "acestream://99e544cddbee13798e854c1009ee7d1a93fdedf7"},
    {"name": "FÚTBOL | LaLiga Smartbank | 1080", "url": "acestream://4c46585214b23b1d802ef2168060c7649a3894cf"},
    {"name": "FÚTBOL | LaLiga Smartbank | 720", "url": "acestream://06b367c22394a1358c9cefa0cb5d0b64b9b2b3f4"},
    {"name": "FÚTBOL | LaLiga Smartbank 2 | 1080", "url": "acestream://d81b4f2f3fde433539c097b2edc9b587ca47b087"},
    {"name": "FÚTBOL | LaLiga Smartbank 2 | 720", "url": "acestream://2709d0ab86cb6ce7ba4d3ad188d7fa80668f2924"},
    {"name": "FÚTBOL | LaLiga Smartbank 3", "url": "acestream://b4a076c1f67a5c1f1ba899ac61b9401b1dc30f41"},
    {"name": "FÚTBOL | LaLiga Smartbank 4", "url": "acestream://2cacf21476b036e319bcb7c7e747766e6ccc082e"},
    {"name": "FÚTBOL | LaLiga Smartbank 5", "url": "acestream://a1146358aa50c99c887108b17f62f9264186a16a"},
    {"name": "FÚTBOL | LaLiga Smartbank 6", "url": "acestream://7a9bb1b9cccb759c44ed84f3c1283922e6854670"},
    {"name": "FÚTBOL | LaLiga Smartbank 7", "url": "acestream://446e73a22582921393b020ed08b768ad8e14d754"},
    {"name": "FÚTBOL | LaLiga Smartbank 8", "url": "acestream://4d52fc1994fe927702aeb7bc8778e2f23b1260e2"},
    {"name": "FÚTBOL | M.Plus | 1080", "url": "acestream://5a236fbbe6e5bbfec03db548c244a7c858d675c0"},
    {"name": "FÚTBOL | Copa | 1080", "url": "acestream://8ba764f6a3bce6eae87ec71208fad1aa3a20528d"},
    {"name": "FÚTBOL | Copa | 1080 plus", "url": "acestream://d6cdd724a97fcf851e7ef641c28d6beb8663496e"},
    {"name": "FÚTBOL | Copa | 1080", "url": "acestream://3a4c8ac955d451bf3c29b45256e74aa0ea82d281"},
    {"name": "FÚTBOL | Copa | 1080", "url": "acestream://7d70685696722c2b1b48a5ae1a7f92c445d9443d"},
    {"name": "FÚTBOL | Copa | 720", "url": "acestream://dab7cab5d6d177df36c3b333ca363c2266d91a03"},
    {"name": "FÚTBOL | #VAMOS | 1080", "url": "acestream://859bb6295b8d0f224224d3063d9db7cdeca03122"},
    {"name": "FÚTBOL | #VAMOS | 720", "url": "acestream://3bba7c95857c2502c7e03ced1a6a9b00eb567fa0"},
    {"name": "FÚTBOL | #ELLAS | 1080", "url": "acestream://67654e63b5065cdaa6c8e8d41bb5428b42b32830"},
    {"name": "FÚTBOL | M. DEPORTES | 1080", "url": "acestream://d00223931b1854163e24c5c22475015d7d45c112"},
    {"name": "FÚTBOL | M. DEPORTES | 720", "url": "acestream://77d83a79afcf6c865289cd8cdb42223cd4b66501c"},
    {"name": "FÚTBOL | M. DEPORTES 2 | 1080", "url": "acestream://e6f06d697f66a8fa606c4d61236c24b0d604d917"},
    {"name": "FÚTBOL | M. DEPORTES 3 | 1080", "url": "acestream://aee0a595220e0f1c2fee725fd1dbc602d7152a9a"},
    {"name": "FÚTBOL | M. DEPORTES 4 | 1080", "url": "acestream://42e83c337ece0af9ca7808859f84c7960e9cb6f5"},
    {"name": "FÚTBOL | M. DEPORTES 5 | 1080", "url": "acestream://b1e5abc48195b7ca9b2ee1b352e790eb9f729a2e3"},
    {"name": "FÚTBOL | M. DEPORTES 6 | 720", "url": "acestream://8587ed8ac36ac477e1d4176d3159a38bd154d4ce"},
    {"name": "FÚTBOL | M. DEPORTES 7 | 1080", "url": "acestream://2448f1d084f440eed2fbe847e24f1c02f5659a78"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 1080 MULTIAUDIO", "url": "acestream://931b1984badcb821df7b47a66ac0835ac871b51c"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 1080 MULTIAUDIO", "url": "acestream://f096a64dd756a6d549aa7b12ee9acf7eee27e833"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 1080P", "url": "acestream://1d79a7543d691666135669f89f3541f54e2dd0a9"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 720", "url": "acestream://e2e2aca792aae5da19995ac516b1d620531bd49c"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 2 1080", "url": "acestream://fc2fe31b0bce25e2dc7ab4d262bf645e2be5a393"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 2 720", "url": "acestream://6753492c1908274c268a1b28e2a054a0ff8f86f9"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 3 1080", "url": "acestream://ad372cba73aa0ece207a79532b3e30b731136bb2"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 3 720", "url": "acestream://d59fe9978eed49f256b312a60671b5bce43d3f24"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 4 1080", "url": "acestream://f2df4f96b23388b45e75d848a48a510cf8af560f"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 5 1080", "url": "acestream://67b353ab1c4c2f6396b3ca5c4b45023bd9927561"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 6 1080", "url": "acestream://64a9353032efa2acb093d0bb86481f20f482d47e"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 7 SD", "url": "acestream://5932623d2fd7ed16b01787251b418e4f59a01cda"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 8 1080", "url": "acestream://6c445141445b06d7b4328d80e2dd936bd0ca52ca"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 9 SD", "url": "acestream://7244379f8f6382d40afec871fb8e4219a803840b"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 10 SD", "url": "acestream://d42e1b592b840ea34394fd3e1b1d3a4d0f399213"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 11 SD", "url": "acestream://e737c681a92a4328703761c6ed9d8a951655f3e4"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 12 SD", "url": "acestream://bb50397b3f49167eed95264005fae851baa7e3ee"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 13 SD", "url": "acestream://60296c246e3596f334903fefd48cfaa724a5053b"},
    {"name": "GOLF | M. GOLF | 1080", "url": "acestream://4f945b0ba4206fa2676b61e9eaa465ac3dcc8122"},
    {"name": "GOLF | M. GOLF2 | 1080", "url": "acestream://9a4f3ae6563668b7709dac509dedc709441b3fd9"},
    {"name": "DAZN 1 | 1080", "url": "acestream://8ca07071b39185431f8e940ec98d1add9e561639"},
    {"name": "DAZN 1 | 720", "url": "acestream://eaff9293c76a324c750ef5094c2a4e2c96518d1f"},
    {"name": "DAZN 2 | 1080", "url": "acestream://60dbeeb299ec04bf02bc7426d827547599d3d9fc"},
    {"name": "DAZN 2 | 720", "url": "acestream://7aa402bab9fff43258fbcf401881a39475f30aaf"},
    {"name": "DAZN 3 | 1080", "url": "acestream://a8ffddef56f082d4bb5c0be0d3d2fdd8c16dbd97"},
    {"name": "DAZN 4 | 1080", "url": "acestream://2fcdf7a19c0858f686efdfabd3c8c2b92bf6bcfd"},
    {"name": "OTROS | EUROSPORT 1 | 1080", "url": "acestream://5e4cd48c79f991fcbee2de8b9d30c4b16de3b952"},
    {"name": "OTROS | EUROSPORT 2 | 1080", "url": "acestream://c373da9e901d414b7384e671112e64d5a2310c29"},
    {"name": "OTROS | GOL TV | 1080", "url": "acestream://d4627f7b6b237a8556819445b3283d866caceca2"},
    {"name": "OTROS | TDP | 1080", "url": "acestream://e2395d28ad19423212fd3aa0e81f387db3e8bb9f"},
    {"name": "OTROS | TENNIS CHANNEL", "url": "acestream://9292d3b32432efb56db4014933cbdec0a7cf2e36"},
    {"name": "OTROS | CUATRO | 1080", "url": "acestream://e8eec35f4662be1af96963245bfa88fb7d0242c4"},
    {"name": "OTROS | BEMAD | 1080", "url": "acestream://5c267a00f264736c1d47c1cc3e754447ca8f770c"},
    {"name": "OTROS | TELECINCO | 1080", "url": "acestream://bb1982ae8d2d409d4ccd7a9f498042684e3532b5"},
    {"name": "OTROS | SPORT TV 1 | 1080", "url": "acestream://ce235921dac95e1da2dd5e54673c2fecb9e806de"},
    {"name": "OTROS | SPORT TV 2 | 1080", "url": "acestream://396d82ca6f5445abcd32e6b609d67e332ee12ace"},
    {"name": "OTROS | SPORT TV 3 | 1080", "url": "acestream://f8cb9d9e3077eb3ae417b2d95a69c5f590760eb9"},
    {"name": "OTROS | BEIN SPORTS Ñ", "url": "acestream://41af6926a6010b68ba2540975761436bb077748f"},
    {"name": "OTROS | BARÇA TV | 720", "url": "acestream://e3362507e7c732b9461bd7bdc74bd054c49b3ba7"},
    {"name": "OTROS | REAL MADRID TV | 1080", "url": "acestream://0ec3f3786318acd8dca2588f74c3759cda76cd11"},
    {"name": "OTROS | REAL MADRID TV | 720", "url": "acestream://0827cf7d290967985892965c6e61244a479d6dcd"},
    {"name": "OTROS | WIMBLEDON UHD", "url": "acestream://78aa81aedb1e2b6a9ba178398148940857155f6a"},
    {"name": "OTROS | MUNDO TORO HD", "url": "acestream://f763ab71f6f646e6c993f37e237be97baf2143ef"},
    {"name": "BALONCESTO | NBA", "url": "acestream://e72d03fb9694164317260f684470be9ab781ed95"},
    {"name": "BALONCESTO | NBA USA 1", "url": "acestream://39db49bc89dcc3c8797566231f869dca57f1a47e"},
    {"name": "BALONCESTO | NBA USA 2", "url": "acestream://f1c84ec8ea0c0bfff8a24272b66c64354a522110"},
]

# Define HTML5 channels
HTML5_CHANNELS = [
    {"name": "OTROS | Studio Universal", "url": "https://jactvpro.xyz:443/Upb93ECM5B/RRzkDRt6w8/10270.m3u8"},
    # ... add more HTML5 channels here ...
]

def build_url(query):
    return BASE_URL + '?' + urlencode(query)

def list_categories():
    # Recorre cada categoría y la agrega a la interfaz de Kodi con su ícono
    for category in CATEGORIES:
        list_item = xbmcgui.ListItem(label=category["name"])
        list_item.setArt({"icon": category["icon"]})  # Establece el ícono de la categoría
        url = f"{BASE_URL}?action=list_channels&category={category['name']}"
        xbmcplugin.addDirectoryItem(handle=HANDLE, url=url, listitem=list_item, isFolder=True)

    # Finaliza el listado del directorio
    xbmcplugin.endOfDirectory(HANDLE)

def list_channels(category):
    # Find the selected category
    selected_category = next((cat for cat in CATEGORIES if cat["name"] == category), None)

    if selected_category:
        # Populate subcategories with appropriate channels
        for channel in ACESTREAM_CHANNELS:
            if channel["name"].upper().startswith(category.upper()):
                selected_category["subcategories"].append(channel)

        for channel in HTML5_CHANNELS:
            if channel["name"].upper().startswith(category.upper()) and category.upper() == "OTROS":  # Only add m3u8 channel to "OTROS"
                selected_category["subcategories"].append(channel)

        # Display channels within the category
        for channel in selected_category["subcategories"]:
            url = build_url({"action": "play_acestream" if "acestream://" in channel["url"] else "play_html5", "url": channel["url"]})
            list_item = xbmcgui.ListItem(label=channel["name"])
            list_item.setInfo("video", {"title": channel["name"]})
            xbmcplugin.addDirectoryItem(handle=HANDLE, url=url, listitem=list_item, isFolder=False)

    xbmcplugin.endOfDirectory(HANDLE)

def play_acestream(url):
    acestream_id = url.replace("acestream://", "")
    play_url = f"plugin://script.module.horus/?action=play&id={acestream_id}"

    try:
        xbmc.Player().play(play_url)
    except Exception as e:
        xbmcgui.Dialog().notification("Error", str(e), xbmcgui.NOTIFICATION_ERROR)

def play_html5(url):
    try:
        xbmc.Player().play(url)
    except Exception as e:
        xbmcgui.Dialog().notification("Error", str(e), xbmcgui.NOTIFICATION_ERROR)

if __name__ == '__main__':
    # Analyze parameters based on action
    args = dict(parse_qsl(sys.argv[2][1:]))
    action = args.get("action")
    
    # Check for different actions and call the appropriate functions
    if action == "list_channels":
        list_channels(args["category"])
    elif action == "play_acestream":
        play_acestream(args["url"])
    elif action == "play_html5":
        play_html5(args["url"])
    else:
        list_categories()