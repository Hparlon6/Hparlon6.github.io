import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import sys
import os
import urllib.parse
from urllib.parse import urlencode, parse_qsl
import requests
from bs4 import BeautifulSoup
import json

# Define el handle del addon
addon_handle = int(sys.argv[1])
BASE_URL = sys.argv[0]

# Obtener los parámetros enviados al addon
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
selected_category = params.get('category', '')

# Obtener la ruta del addon
addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path')

# Asegurarse de que la ruta del addon sea válida
if not os.path.exists(addon_path):
    raise Exception(f"La ruta del addon no se encuentra: {addon_path}")

# Ruta de las carpetas dentro del addon
requests_path = os.path.join(addon_path, 'requests')
urllib3_path = os.path.join(addon_path, 'urllib3')
bs4_path = os.path.join(addon_path, 'bs4')
idna_path = os.path.join(addon_path, 'idna')
charset_normalizer_path = os.path.join(addon_path, 'charset_normalizer')
certifi_path = os.path.join(addon_path, 'certifi')
soupsieve_path = os.path.join(addon_path, 'soupsieve')

# Verificar que las carpetas existan
for path in [requests_path, urllib3_path, bs4_path, idna_path, charset_normalizer_path, certifi_path, soupsieve_path]:
    if not os.path.exists(path):
        raise Exception(f"La carpeta no se encuentra: {path}")

# Añadir las carpetas al sys.path para importarlas correctamente
sys.path.insert(0, requests_path)
sys.path.insert(0, urllib3_path)
sys.path.insert(0, bs4_path)
sys.path.insert(0, idna_path)
sys.path.insert(0, charset_normalizer_path)
sys.path.insert(0, certifi_path)
sys.path.insert(0, soupsieve_path)

# Intentar importar los módulos
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    raise Exception(f"Error al importar los módulos: {e}")

# Obtener el handle del addon desde los argumentos
addon_handle = int(sys.argv[1])  # Este es el handle del addon

# Define the URL base of the plugin
BASE_URL = sys.argv[0]
HANDLE = int(sys.argv[1])

# Get the addon path and define the resources path
ADDON_PATH = xbmcaddon.Addon().getAddonInfo('path')
RESOURCES_PATH = f"{ADDON_PATH}/resources"

# Define categories with automatic icon path
CATEGORIES = [
    {"name": "AGENDA", "subcategories": [], "icon": f"{RESOURCES_PATH}/agenda.png"},
    {"name": "DEPORTES", "subcategories": [], "icon": f"{RESOURCES_PATH}/deportes.png"},
    {"name": "FÚTBOL", "subcategories": [], "icon": f"{RESOURCES_PATH}/futbol.png"},
    {"name": "CHAMPIONS", "subcategories": [], "icon": f"{RESOURCES_PATH}/champions.png"},
    {"name": "GOLF", "subcategories": [], "icon": f"{RESOURCES_PATH}/golf.png"},
    {"name": "DAZN", "subcategories": [], "icon": f"{RESOURCES_PATH}/dazn.png"},
    {"name": "F1", "subcategories": [], "icon": f"{RESOURCES_PATH}/f1.png"},
    {"name": "BALONCESTO", "subcategories": [], "icon": f"{RESOURCES_PATH}/baloncesto.png"},
]

# Define AceStream channels
ACESTREAM_CHANNELS = [
    # ... your existing AceStream channel definitions here ...
    {"name": "F1 | DAZN F1 1080", "url": "acestream://d6281d4e6310269b416180442a470d23a4a99dc9"},
    {"name": "F1 | DAZN F1 1080 | OPCION 2", "url": "acestream://2c6e4c897661e6b0257bfe931b66d20b2ec763b6"},
    {"name": "F1 | DAZN F1 1080 | OPCION 3", "url": "acestream://71eef80158aa8b37f3dc59f6793c6696df9a2dfa"},
    {"name": "F1 | DAZN F1 720", "url": "acestream://268289e7a3c5209960b53b4d43c8c65fab294b85"},
    {"name": "FÚTBOL | M. LA LIGA 1080", "url": "acestream://94d34491106e00394835c8cb68aa94481339b53f"},
    {"name": "FÚTBOL | M. LA LIGA 1080 | OPCION 2", "url": "acestream://d3de78aebe544611a2347f54d5796bd87f16c92d"},
    {"name": "FÚTBOL | M. LA LIGA 1080 | OPCION 3", "url": "acestream://6d05b31e5e8fdae312fbd57897363a7b10ddb163"},
    {"name": "FÚTBOL | M. LA LIGA 720", "url": "acestream://1bc437bce57b4b0450f6d1f8d818b7e97000745e"},
    {"name": "FÚTBOL | M. LA LIGA 2 1080", "url": "acestream://83c6c4942d69f4aa324aa746c5d7dbfd7d1572b3"},
    {"name": "FÚTBOL | M. LA LIGA 2 720", "url": "acestream://f31a586422c9244196c810c84b6c85da350318a5"},
    {"name": "FÚTBOL | M. LA LIGA 3 1080", "url": "acestream://ebe14f1edeb49f2253e3b355a8beeadc9b4f0bc4"},
    {"name": "FÚTBOL | LA LIGA BAR 1080", "url": "acestream://608b0faf7d3d25f6fe5dba13d5e4b4142949990e"},
    {"name": "FÚTBOL | LA LIGA BAR 1080 | OPCION 2", "url": "acestream://94d34491106e00394835c8cb68aa94481339b53f"},
    {"name": "FÚTBOL | DAZN LaLiga 1080", "url": "acestream://110d441ddc9713a7452588770d2bc85504672f47"},
    {"name": "FÚTBOL | DAZN LaLiga 1080 | OPCION 2", "url": "acestream://ec29289b0b14756e686c03a501bae1efa05be70c"},
    {"name": "FÚTBOL | DAZN LaLiga 1080 | OPCION 3", "url": "acestream://6de4794cd02f88f14354b5996823413a59a1de0f"},
    {"name": "FÚTBOL | DAZN LaLiga 720", "url": "acestream://8c8c1e047a1c5ed213ba74722a5345dc55c3c0eb"},
    {"name": "FÚTBOL | DAZN LaLiga 2 1080", "url": "acestream://97ba38d47680954be40e48bd8f43e17222fefecb"},
    {"name": "FÚTBOL | DAZN LaLiga 2 720", "url": "acestream://51dbbfb42f8091e4ea7a2186b566a40e780953d9"},
    {"name": "FÚTBOL | LaLiga Smartbank 1080", "url": "acestream://b2706a7ffbea236a3b398139a3a606ada664c0eb"},
    {"name": "FÚTBOL | LaLiga Smartbank 720", "url": "acestream://121f719ebb94193c6086ef92865cf9b197750980"},
    {"name": "FÚTBOL | LaLiga Smartbank 2 1080", "url": "acestream://0cfdfde1b70623b8c210b0f7301be2a87456481d"},
    {"name": "FÚTBOL | LaLiga Smartbank 2 720", "url": "acestream://0a335406bad0b658aeddb2d38f8c0614b2e5623a"},
    {"name": "FÚTBOL | LaLiga Smartbank 3", "url": "acestream://fefd45ed6ff415e05f1341b7d9da2988eacd13ea"},
    {"name": "DEPORTES | M.Plus 1080", "url": "acestream://56ac8e227d526e722624675ccdd91b0cc850582f"},
    {"name": "FÚTBOL | Copa 1080", "url": "acestream://f6beccbc4eea4bc0cda43b3e8ac14790a98b61b4"},
    {"name": "FÚTBOL | Copa 720", "url": "acestream://b51f2d9a15b6956a44385b6be531bcabeb099d9d"},
    {"name": "DEPORTES | #VAMOS 1080", "url": "acestream://d03c13b6723f66155d7a0df3692a3b073fe630f2"},
    {"name": "DEPORTES| #VAMOS 720", "url": "acestream://12ba546d229bc39f01c3c18988a034b215fe6adb"},
    {"name": "FÚTBOL | #ELLAS 1080", "url": "acestream://d8c2ed470e847154a88f011137cc206319f6bed5"},
    {"name": "DEPORTES | M. DEPORTES 1080", "url": "acestream://55d4602cb22b0d8a33c10c2c2f42dae64a9e8895"},
    {"name": "DEPORTES | M. DEPORTES 720", "url": "acestream://3a74d9869b13e763476800740c6625e715a39879"},
    {"name": "DEPORTES | M. DEPORTES 2 1080", "url": "acestream://639c561dd57fa3fc91fde715caeb696c5efb7ce7"},
    {"name": "DEPORTES | M. DEPORTES 3 1080", "url": "acestream://571bff4d12b1791eb99dbf20bec38e630693a6a3"},
    {"name": "DEPORTES | M. DEPORTES 4 1080", "url": "acestream://b4d1308a61e4caf8c06ac3d6ce89d165c015c2fb"},
    {"name": "DEPORTES | M. DEPORTES 5 1080", "url": "acestream://fcc0fd75bf1dba40b108fcf0d3514e0e549bfbac"},
    {"name": "DEPORTES | M. DEPORTES 6 1080", "url": "acestream://cc5782d37ae6b6e0bab396dd64074982d0879046"},
    {"name": "DEPORTES | M. DEPORTES 7 1080", "url": "acestream://070f82d6443a52962d6a2ed9954c979b29404932"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 1080 MULTIAUDIO", "url": "acestream://0a26e20f39845e928411e09a124374fccb6e1478"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 1080 MULTIAUDIO", "url": "acestream://775abd8697715c48a357906d40734ccd2a10513c"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 720", "url": "acestream://8edb264520569b2280c5e86b2dc734e120032903"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 2 1080", "url": "acestream://c070cdb701fc46bb79d17568d99fc64620443d63"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 2 720", "url": "acestream://abdf9058786a48623d0de51a3adb414ae10b6e72"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 3 1080", "url": "acestream://3618edda333dad5374ac2c801f5f14483934b97d"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 3 720", "url": "acestream://0b348cc1ae499e810729661878764a0fab88ab69"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 4 1080", "url": "acestream://65a18a6bd83918a9586b673fec12405aaf4e9f7d"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 5 1080", "url": "acestream://11744c25a594e17d587ed0871fe40ff21b4bd1e0"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 6 1080", "url": "acestream://fdda1f0dd8c33fbdc5a66ab98e291f570cae67cd"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 7 1080", "url": "acestream://b7f47db93dced60f54e8f89e2366ed061b534049"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 8 1080", "url": "acestream://d298c6e5c8be71f5995b45289c6388b225318b3c"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 9 SD", "url": "acestream://2d7c4cfb3987b652a779afc894cca2fccbbacf21"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 10 SD", "url": "acestream://c056f9e180cd7d40963129a17ff54f4ee8259353"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 11 SD", "url": "acestream://a12a16f74cf12799d4475ae867dc61eb60e1ba2e"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 12 SD", "url": "acestream://df7d145fcaf0566db4098d2f10236185d92bc9fd"},
    {"name": "CHAMPIONS | M.L. CAMPEONES 13 SD", "url": "acestream://bdfe9ebe62d690c1b13eef4346d72e618cfbe804"},
    {"name": "GOLF | M. GOLF 1080", "url": "acestream://f41f1096862767289620be5bd85727f946a434db"},
    {"name": "GOLF | M. GOLF2 1080", "url": "acestream://e258e75e0e802afa5fcc53d46b47d8801a254ad5"},
    {"name": "DAZN 1 1080", "url": "acestream://7cf0086fa7d478f51dbba952865c79e66cb9add5"},
    {"name": "DAZN 1 720", "url": "acestream://35c7f0c966ecde3390f4510bb4caded40018c07a"},
    {"name": "DAZN 2 1080", "url": "acestream://ca923c9873fd206a41c1e83ff8fc40e3cf323c9a"},
    {"name": "DAZN 2 720", "url": "acestream://a929eeec1268d69d1556a2e3ace793b2577d8810"},
    {"name": "DAZN 3 1080", "url": "acestream://19cd05c7ae26f22737ae5728b571ca36abd8a2e8"},
    {"name": "DAZN 4 1080", "url": "acestream://4e83f23945ab3e43982045f88ec31daaa4683102"},
    {"name": "DEPORTES | EUROSPORT 1 1080", "url": "acestream://16ffa1713f42aa27317ee039a2bd0cdbc89a1580"},
    {"name": "DEPORTES | EUROSPORT 2 1080", "url": "acestream://98784fa0714190de289f42eb5b84e405df7e685a"},
    {"name": "DEPORTES | REAL MADRID TV 1080", "url": "acestream://0ec3f3786318acd8dca2588f74c3759cda76cd11"},
    {"name": "DEPORTES | REAL MADRID TV 720", "url": "acestream://0827cf7d290967985892965c6e61244a479d6dcd"},
    {"name": "DEPORTES | WIMBLEDON UHD", "url": "acestream://78aa81aedb1e2b6a9ba178398148940857155f6a"},
    {"name": "DEPORTES | MUNDO TORO HD", "url": "acestream://f763ab71f6f646e6c993f37e237be97baf2143ef"},
    {"name": "BALONCESTO | NBA", "url": "acestream://e72d03fb9694164317260f684470be9ab781ed95"},
    {"name": "BALONCESTO | NBA USA 1", "url": "acestream://39db49bc89dcc3c8797566231f869dca57f1a47e"},
    {"name": "BALONCESTO | NBA USA 2", "url": "acestream://f1c84ec8ea0c0bfff8a24272b66c64354a522110"},
    {"name": "DEPORTES | RED BULL TV", "url": "acestream://6994af284ecab2996f9b140ef44b8da8bfee0006"},
    {"name": "DEPORTES | UFC CHANNEL", "url": "acestream://7cf437be950f3525e735be57c63f7824cab822c9"},
    {"name": "DEPORTES | FOX SPORTS 2", "url": "acestream://ad6f4e8e329d6a97c7e7d7b0b8e5d04d8dd0bb48"},
]

# Define HTML5 channels
HTML5_CHANNELS = [
    # ... add more HTML5 channels here ...
]

def build_url(query):
    return BASE_URL + '?' + urlencode(query)

def buscar_enlace_por_nombre(nombre):
    """
    Busca en ACESTREAM_CHANNELS un canal cuyo nombre contenga palabras clave del nombre proporcionado.
    """
    nombre = nombre.lower()
    for canal in ACESTREAM_CHANNELS:
        canal_nombre = canal["name"].lower()
        # Coincidencia parcial por palabras clave
        if all(palabra in canal_nombre for palabra in nombre.split()):
            return canal["url"]
    return None

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

# Función para mostrar los eventos en la categoría "Agenda"
def list_agenda_events(selected_category):
    events = fetch_events_from_zeronet()

    for event in events:
        # Crear una cadena de texto con el formato deseado
        event_line = f"{event['time']} | {event['category']} | {event['event']}"
        list_item = xbmcgui.ListItem(label=event_line)

        # Agregar propiedades y enlaces a los elementos de la lista (si es necesario)
        # ...

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=event["links"][0], listitem=list_item, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)

def obtener_eventos_desde_html():
    url = "http://141.145.210.168"  # URL de la web
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        eventos = []

        # Encuentra y extrae datos de la tabla
        tabla_eventos = soup.find('table', class_='styled-table')
        for fila in tabla_eventos.find_all('tr')[1:]:  # Ignora el encabezado
            columnas = fila.find_all('td')
            if len(columnas) >= 5:
                hora = columnas[0].text.strip()
                categoria = columnas[1].text.strip()
                equipo_1 = columnas[2].text.strip()
                equipo_2 = columnas[3].text.strip()

                # Obtén enlaces únicos con nombres únicos
                enlaces = []
                urls_añadidas = set()  # Para evitar duplicados basados en la URL

                for enlace_tag in columnas[4].find_all('a'):
                    nombre_canal = enlace_tag.text.strip()
                    url_canal = buscar_enlace_por_nombre(nombre_canal)
                    enlace_web = enlace_tag['href']  # Enlace de la web

                    # Añadir el enlace desde `ACESTREAM_CHANNELS` si existe
                    if url_canal and url_canal not in urls_añadidas:
                        enlaces.append({"name": nombre_canal, "url": url_canal})
                        urls_añadidas.add(url_canal)

                    # Añadir el enlace directo de la web si no es duplicado
                    if enlace_web not in urls_añadidas:
                        # Si ya existe un canal con el mismo nombre, agrega un sufijo de opción
                        nombre_unico = nombre_canal
                        if any(enlace['name'] == nombre_canal for enlace in enlaces):
                            opcion_num = sum(1 for enlace in enlaces if enlace['name'].startswith(nombre_canal)) + 1
                            nombre_unico = f"{nombre_canal} Opción {opcion_num}"

                        enlaces.append({"name": nombre_unico, "url": enlace_web})
                        urls_añadidas.add(enlace_web)

                # Solo agregar el evento si tiene enlaces válidos
                if enlaces:
                    eventos.append({
                        'hora': hora,
                        'categoria': categoria,
                        'evento': f"{equipo_1} vs {equipo_2}",
                        'enlaces': enlaces
                    })

        eventos.sort(key=lambda x: x['hora'])
        return eventos
    except requests.exceptions.RequestException as e:
        xbmcgui.Dialog().notification("Error", f"Error al obtener eventos: {e}", xbmcgui.NOTIFICATION_ERROR)
        return []

def mostrar_agenda():
    eventos = obtener_eventos_desde_html()
    if not eventos:
        xbmcgui.Dialog().notification("Agenda", "No hay eventos disponibles", xbmcgui.NOTIFICATION_INFO, 3000)
        return

    for evento in eventos:
        titulo = f"{evento['hora']} | {evento['categoria']} | {evento['evento']}"
        list_item = xbmcgui.ListItem(label=titulo)
        
        # Serializar los enlaces como JSON
        url = build_url({"action": "mostrar_enlaces_evento", "enlaces": json.dumps(evento['enlaces'])})
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=list_item, isFolder=True)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def mostrar_enlaces_evento(enlaces):
    import json

    # Deserializar enlaces desde JSON si están en formato de cadena
    if isinstance(enlaces, str):
        enlaces = json.loads(enlaces)  # Convertir la cadena JSON a lista de diccionarios

    # Iterar sobre los enlaces deserializados
    for enlace in enlaces:
        nombre_canal = enlace["name"]  # Nombre del canal
        list_item = xbmcgui.ListItem(label=nombre_canal)
        url = build_url({"action": "play_acestream", "url": enlace["url"]})
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=list_item, isFolder=False)
    
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def ejecutar_categoria(categoria):
    if categoria == "AGENDA":
        mostrar_agenda()
    else:
        xbmcgui.Dialog().notification("Error", f"Categoría '{categoria}' no encontrada", xbmcgui.NOTIFICATION_ERROR)

# Parsear argumentos desde Kodi
args = urllib.parse.parse_qs(sys.argv[2][1:])
categoria = args.get('categoria', [None])[0]

# Llamar a la función para manejar la categoría
if categoria:
    ejecutar_categoria(categoria)
else:
    # Muestra categorías iniciales o manejo de errores
    pass

# Aquí es donde debes asegurar que se llama la función con la categoría correcta
if __name__ == '__main__':
    args = dict(parse_qsl(sys.argv[2][1:]))
    action = args.get("action")

    if action == "list_channels":
        if args.get("category") == "AGENDA":
            mostrar_agenda()
        else:
            list_channels(args["category"])
    elif action == "mostrar_enlaces_evento":
        mostrar_enlaces_evento(args["enlaces"])
    elif action == "play_acestream":
        play_acestream(args["url"])  # Llama a la función con solo el ID
    elif action == "play_html5":
        play_html5(args["url"])
    else:
        list_categories()
