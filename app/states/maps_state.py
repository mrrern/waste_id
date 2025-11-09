import reflex as rx
import plotly.graph_objects as go
import requests

class MapeoDeFlujosState(rx.State):
    # Bounding boxes for centering the map
    countries_bbox = {
        "Argentina": [-54.8, -34.0, -72.0, -22.0],
        "Bolivia": [-69.6, -9.7, -57.5, -22.9],
        "Brasil": [-73.9, 5.2, -28.7, -33.7],
        "Chile": [-75.7, -17.5, -66.4, -55.9],
        "Colombia": [-79.2, 12.5, -66.8, -4.2],
        "Costa Rica": [-85.9, 11.2, -82.5, 8.0],
        "Cuba": [-85.0, 23.2, -74.1, 19.8],
        "Ecuador": [-91.7, 1.4, -75.2, -5.0],
        "El Salvador": [-90.1, 14.4, -87.7, 13.1],
        "Guatemala": [-92.2, 17.8, -88.2, 13.7],
        "Honduras": [-89.3, 16.5, -83.2, 12.9],
        "México": [-117.1, 32.7, -86.7, 14.5],
        "Nicaragua": [-87.7, 15.0, -82.7, 10.7],
        "Panamá": [-83.0, 9.6, -77.1, 7.2],
        "Paraguay": [-62.6, -19.3, -54.3, -27.6],
        "Perú": [-81.3, 0.0, -68.6, -18.3],
        "República Dominicana": [-72.0, 19.9, -68.3, 17.6],
        "Uruguay": [-58.4, -30.1, -53.1, -34.9],
        "Venezuela": [-73.3, 12.2, -59.8, 0.7],
    }
    
    # ISO3166-1 alpha-2 codes for Overpass API
    country_codes = {
        "Argentina": "AR",
        "Bolivia": "BO",
        "Brasil": "BR",
        "Chile": "CL",
        "Colombia": "CO",
        "Costa Rica": "CR",
        "Cuba": "CU",
        "Ecuador": "EC",
        "El Salvador": "SV",
        "Guatemala": "GT",
        "Honduras": "HN",
        "México": "MX",
        "Nicaragua": "NI",
        "Panamá": "PA",
        "Paraguay": "PY",
        "Perú": "PE",
        "República Dominicana": "DO",
        "Uruguay": "UY",
        "Venezuela": "VE",
    }

    selected_country: str = "Argentina"
    map_figure: go.Figure = go.Figure()

    @rx.var
    def country_list(self) -> list[str]:
        return list(self.countries_bbox.keys())

    def get_e_waste_data(self):
        country_code = self.country_codes[self.selected_country]
        overpass_url = "http://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json][timeout:120];
        area["ISO3166-1"="{country_code}"]->.searchArea;
        (
          node["landuse"="landfill"](area.searchArea);
          node["amenity"="recycling"](area.searchArea);
          node["amenity"="waste_disposal"](area.searchArea);
          node["transfer_station"](area.searchArea);
        );
        out center;
        """
        response = requests.get(overpass_url, params={'data': overpass_query})
        data = response.json()

        lats = []
        lons = []
        texts = []

        for element in data['elements']:
            lat = None
            lon = None
            if 'lat' in element and 'lon' in element:
                lat = element['lat']
                lon = element['lon']
            elif 'center' in element:
                lat = element['center']['lat']
                lon = element['center']['lon']
            
            if lat and lon:
                lats.append(lat)
                lons.append(lon)
                tags = element.get('tags', {})
                name = tags.get('name', 'N/A')
                amenity = tags.get('amenity', '')
                landuse = tags.get('landuse', '')
                texts.append(f"Name: {name}<br>Type: {amenity or landuse}")


        bbox = self.countries_bbox[self.selected_country]
        center_lat = (bbox[1] + bbox[3]) / 2
        center_lon = (bbox[0] + bbox[2]) / 2

        fig = go.Figure(go.Scattermap(
            lat=lats,
            lon=lons,
            mode='markers',
            marker=go.scattermap.Marker(
                size=9
            ),
            text=texts,
        ))

        fig.update_layout(
            mapbox_style="open-street-map",
            autosize=True,
            hovermode='closest',
            mapbox=dict(
                center=dict(
                    lat=center_lat,
                    lon=center_lon
                ),
                zoom=4
            ),
            margin={"r":0,"t":0,"l":0,"b":0}
        )
        
        self.map_figure = fig

    def on_country_change(self, country: str):
        self.selected_country = country
        self.get_e_waste_data()
