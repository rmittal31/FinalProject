'''
Name: Ritika Mittal
CS230: Section 6
Data: Rest Areas in California
URL: Link to your web application on Streamlit Cloud (if posted)

Description: This program shows a map of California and all the rest areas in the state. It has 3 interactive queries
that you can select from a dropdown to access. The first query allows the user to select a city or cities and shows all
the rest areas in that city or cities. The second query shows a pie chart of the distribution of traffic direction per
route. The final query allows the user to sort rest areas by the number of facilities they have, using a slider.
'''


import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt

# Load the data
rest_areas = pd.read_csv('Rest_Areas.csv')

def rest_areas_by_city():
    # [ST1], [VIZ1]
    selected_cities = st.multiselect('Select cities:', rest_areas['CITY'].unique())
    city_rest_areas = rest_areas[rest_areas['CITY'].isin(selected_cities)] #[DA4]
    st.write(city_rest_areas[['NAME', 'ADDRESS', 'CITY', 'ZIPCODE']])


def traffic_direction():
    routes = rest_areas['ROUTE'].unique()
    sorted_routes = sorted(routes)  #[DA2]

    selected_route = st.selectbox('Select a highway or route:', sorted_routes)
    route_rest_areas = rest_areas[rest_areas['ROUTE'] == selected_route]
    direction_counts = route_rest_areas['TRAFFICDIR'].value_counts()

    colors = ['pink', 'purple', 'magenta']

    chart_type = st.radio("Select Chart Type", ("Pie Chart", "Bar Chart"))

    fig, ax = plt.subplots()

    if chart_type == "Pie Chart": #[VIZ2]
        ax.pie(direction_counts, labels=direction_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')
    elif chart_type == "Bar Chart": #[VIZ3]
        ax.bar(direction_counts.index, direction_counts, color=colors)

    st.pyplot(fig)


def map(rest_areas): #[VIZ4]
    view_state = pdk.ViewState(
        latitude=rest_areas['LATITUDE'].mean(), #[DA9]
        longitude=rest_areas['LONGITUDE'].mean(),
        zoom=5,
        bearing=0,
        pitch=0
    )

    tooltip = {"html": "<b>{NAME}</b>", "style": {"backgroundColor": "pink", "color": "black"}}

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=rest_areas,
        get_position=['LONGITUDE', 'LATITUDE'],
        get_fill_color=[230, 100, 120],
        get_radius=5500,
        pickable=True,
        auto_highlight=True)

    deck = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[layer],
        tooltip=tooltip
    )

    st.pydeck_chart(deck)


def facilities(): #[PY1]
    # [ST2]
    selected_facility_count = st.sidebar.slider('Select number of facilities:', 0, 8, 3)
    filtered_rest_areas = rest_areas[(rest_areas.iloc[:, 20:27] == 'Yes').sum(axis=1) == selected_facility_count] #[PY4], [DA5]

    if not filtered_rest_areas.empty:
        st.write(filtered_rest_areas[['NAME', 'RESTROOM', 'WATER', 'PICNICTAB', 'PHONE', 'HANDICAP', 'RV_STATION', 'VENDING', 'PET_AREA']].reset_index(drop=True))
    else:
        st.write("No rest areas with {} facilities.".format(selected_facility_count))


def main():
    # [ST3]
    st.markdown('<h1 style="color: pink;">Rest Areas in California</h1>', unsafe_allow_html=True)

    image_path = "restimg.jpg"

    st.sidebar.image(image_path)
    # [ST4]
    query = st.sidebar.selectbox('Select an option:',['Map of Rest Areas in California',
                                                    'Rest Areas by City',
                                                     'Distribution of Traffic Direction by Route',
                                                     'Rest Areas by Number of Facilities'])

    if query == 'Map of Rest Areas in California':
        map(rest_areas)
    elif query == 'Rest Areas by City':
        rest_areas_by_city()
    elif query == 'Distribution of Traffic Direction by Route':
        traffic_direction()
    elif query == 'Rest Areas by Number of Facilities':
        facilities()
        image_path = "petarea.jpg"
        st.image(image_path)


if __name__ == '__main__':
    main()
