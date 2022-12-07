import panel as pn
import pathlib
import param

pn.extension(sizing_mode="stretch_width")

RENDER = """
function map_node(target_id){
    if (target_id===null | !target_id.includes("-")){ return "" }
    target_id = target_id.split("-")[0]
    if (Object.keys( data.node_map ).length === 0){ return target_id }
    if (target_id in data.node_map){
        return data.node_map[target_id]
    } else {
        return ""
    }
}
function map_target_ids(node){
    if (node===null){ return "" }
    if (Object.keys( data.node_map ).length === 0){ return node }
    var lst = []
    Object.keys( data.node_map ).forEach(key => {
        var node_map = data.node_map
        if ( node_map[key] === node ){
            lst.push(key)
        }
    })
    return lst
}
function getTarget(targetId){
    targetId = targetId + "-" + interactiveSVG.id.split("-")[1]
    return document.getElementById(targetId)
}
function addClassName(targetId, className){
    getTarget(targetId).classList.add(className)
}
function removeClassName(targetId, className){
    getTarget(targetId).classList.remove(className)
}
state.mouseoverTargetIds=[];
state.activeTargetIds=[];
if (interactiveSVG !== null){
    interactiveSVG.addEventListener('click', (e) => {
        data.node_clicks = data.node_clicks + 1;
        data.node_click= map_node(e.target.id);

        if (data.value === data.node_click){
            data.value=""
        } else {
            data.value = data.node_click
        }

        state.activeTargetIds.forEach(targetId => {
            removeClassName(targetId, "interactiveSVG-active")
        })
        state.activeTargetIds = map_target_ids(data.value)
        state.activeTargetIds.forEach(targetId => {
            addClassName(targetId, "interactiveSVG-active")
        })
    });
    interactiveSVG.addEventListener('mouseover', (e) => {
        data.node_mouseover = map_node(e.target.id);
        state.mouseoverTargetIds.forEach(targetId => {
            removeClassName(targetId, "interactiveSVG-mouseover")
        })
        state.mouseoverTargetIds = map_target_ids(data.node_mouseover)
        state.mouseoverTargetIds.forEach(targetId => {
            addClassName(targetId, "interactiveSVG-mouseover")
        })
    })
}
"""
class SVGInteractive(pn.reactive.ReactiveHTML):
    svg = param.String(doc="""
        A SVG text string. The elements you want to be able to hover or click
        needs to have an id. For example <path ... id="path5645" />""")

    value = param.String(doc="""The node on the svg currently selected""")

    node_clicks = param.Integer(doc="""The total number of clicks on the svg""")
    node_click = param.String(doc="""The node last clicked or ''""")
    node_mouseover = param.String(doc="""The node the mouse is currently over or ''""")
    node_mouseleave = param.String(doc="""The node the mouse was previously over or ''""")

    node_map = param.Dict(allow_None=False, doc="""
        Used to combine multiple elements (key) into one node (value).""")

    _template = """<div id="interactiveSVG" style="height:100%">{{svg}}</div>"""

    _scripts = {
        "render": RENDER,
    }

    def __init__(self, **params):
        params["node_map"] = params.get("node_map", {})
        super().__init__(**params)

        self.param.watch(self._handle_node_mouseover, "node_mouseover")

    def _handle_node_mouseover(self, event):
        self.node_mouseleave = event.old

WIND_TURBINE_PATH = "wind_turbine_int.svg"
WIND_TURBINE_SVG = pathlib.Path(WIND_TURBINE_PATH).read_text()

NODE_MAP = {
    "path3437": "Foundation",
    "path5624": "Foundation",
    "path4721": "Connection to the electric grid",
    "path5627": "Connection to the electric grid",
    "path5642": "Tower",
    "path4727": "Tower",
    "path4733": "Access ladder",
    "path5639": "Access ladder",
    "path4739": "Yaw control",
    "path5636": "Yaw control",
    "path5633": "Nacelle",
    "path4745": "Nacelle",
    "path4751": "Generator",
    "path5630": "Generator",
    "path3445": "Anemomenter",
    "path5653": "Anemomenter",
    "path4757": "Brake",
    "path5650": "Brake",
    "path5645": "Gearbox",
    "path5647": "Gearbox",
    "path4763": "Gearbox",
    "path4769": "Rotor blade",
    "path5668": "Rotor blade",
    "path5666": "Rotor blade",
    "path4775": "Blade pitch control",
    "path5661": "Blade pitch control",
    "path5663": "Blade pitch control",
    "path4781": "Rotor hub",
    "path5658": "Rotor hub",
    "path5656": "Rotor hub",
}

UNDER_CONSTRUCTION = "https://www.seekpng.com/png/full/66-668827_jbvgodih4wzfrk-bob-the-builder-under-construction.png"

NODE_IMAGE = {
    "Gearbox": "https://3ohkdk3zdzcq1dul50oqjvvf-wpengine.netdna-ssl.com/wp-content/uploads/2018/02/1a_SKF_Windturbine_with_gearbox_3point_suspension_04-smaller.jpg",
    "Yaw control": "https://upload.wikimedia.org/wikipedia/en/thumb/2/21/Wind.turbine.components.and.coordinates.svg/1200px-Wind.turbine.components.and.coordinates.svg.png",
    "Generator": "http://www.fiddlersgreen.net/miscellanous/Wind-Turbine/IMAGES/Wind-Turbine-Cutaway.jpg?w=640",
    "Rotor hub": "https://d2t1xqejof9utc.cloudfront.net/screenshots/pics/d380d23e7ae374af96cc732bad701c34/large.png",
    "Access ladder": "https://cdn.offshorewind.biz/wp-content/uploads/sites/2/2019/09/23085556/%C3%98rsted-Buys-Into-Pict-Offshore-Develops-New-OW-Access-System2.jpg",
    "Connection to the electric grid": "https://www.turbinas-eolicas.com/2000w.files/on-grid.gif",
    "Blade pitch control": "https://media.springernature.com/lw685/springer-static/image/art%3A10.1007%2Fs40313-020-00584-x/MediaObjects/40313_2020_584_Fig1_HTML.png",
    "Tower": "http://xn--drmstrre-64ad.dk/wp-content/wind/miller/windpower%20web/res/twrssk.jpg",
    "Rotor blade": "https://cached.imagescaler.hbpl.co.uk/resize/scaleWidth/882/cached.offlinehbpl.hbpl.co.uk/news/OPW/5BC5CE1D-B770-CD9B-E2A992251B7F901B.gif",
    "Foundation": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Concrete_base_for_turbine_23_-_geograph.org.uk_-_517353.jpg/220px-Concrete_base_for_turbine_23_-_geograph.org.uk_-_517353.jpg",
    "Anemomenter": "http://www.windturbinestar.com/uploads/images/Anemometer/Anemoscope-2.jpg",
    "Brake": "https://app01.balluff.com/image-fit/471-0/fileadmin/user_upload/industries/energie/wind-energy/appl_energy_wind-energy_better-maintenance.jpg",
    "Nacelle": "https://upload.wikimedia.org/wikipedia/commons/d/de/Scout_moor_gearbox%2C_rotor_shaft_and_brake_assembly.jpg",
}

wind_turbine = SVGInteractive(svg=WIND_TURBINE_SVG, node_map=NODE_MAP, height=600)
# , node_map=NODE_MAP
ACCENT_BASE_COLOR = "#926AA6"

DESCRIPTION = """# ReactiveHTML Makes It Easy to Make SVGs Interactive

## The `ReactiveHTML` component of Panel makes it much easier to make SVGs interactive.

I am not an expert on wind turbine design and do not know if the information is meaningful. It's used
here to illustrate the interactivity of a SVG image. Not wind turbine design.

You can learn more about [Wind Turbine Design](https://en.wikipedia.org/wiki/Wind_turbine_design) on Wikipedia
and find the [Wind_turbine_int.svg](https://upload.wikimedia.org/wikipedia/commons/a/ac/Wind_turbine_int.svg) on
Wikimedia.
"""


def show_info(node, no_text):
    print(node)
    if node in NODE_IMAGE:
        image = NODE_IMAGE[node]
        return f"""
# {node}

<img alt="{node}" src="{image}" height="400px">
"""
    return no_text


show_info_mouseover = pn.bind(show_info, node=wind_turbine.param.node_mouseover, no_text="Hover over a node to show image")
show_info_value = pn.bind(show_info, node=wind_turbine.param.value, no_text="Click a node to show image")

component = pn.Row(
    wind_turbine,
    pn.panel(show_info_mouseover, height=100),
    pn.panel(show_info_value, height=100),
)

template = pn.template.FastListTemplate(
    site="Awesome Panel",
    title="Interactive Wind Turbine with Panel",
    logo="https://panel.holoviz.org/_static/logo_stacked.png",
    header_background=ACCENT_BASE_COLOR,
    accent_base_color=ACCENT_BASE_COLOR,
    sidebar=[
        pn.Param(
            wind_turbine,
            parameters=["node_clicks", "node_click", "node_mouseover", "node_mouseleave", "value"],
        )
    ],
    main=[DESCRIPTION, component],
).servable()
