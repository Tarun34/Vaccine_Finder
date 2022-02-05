import datetime
import json
import numpy as np
import requests
import pandas as pd
from copy import deepcopy
from fake_useragent import UserAgent
import streamlit as st
import webbrowser
from PIL import Image
import streamlit.components.v1 as components
def app():
    st.markdown("""<link rel= "stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">""",unsafe_allow_html=True)
    st.markdown('<link rel= stylesheet href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">',unsafe_allow_html=True)
    st.markdown("""
         <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color:#3498DB; color:#FFFFF">
         <a class="navbar-brand fa fa-stethoscope" style="font-size:30px" href="http://localhost:8501/" target="_blank"> &#xf0f1; Sanjeevnam </a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item active">
            <a class="nav-link disabled" href="http://localhost:8501/">Home <span class="sr-only">(current)</span></a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="http://localhost:8502/" target="_blank"> Vaccine </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="http://localhost:8503/" target="_blank">Disease</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="http://localhost:8504/" target="_blank">Health Insurance</a>
          </li>
        </ul>
      </div>
    </nav>
    """, unsafe_allow_html=True)
    st.image("try.jpg")
    st.markdown("<h1 style='text-align:justify; color:red; font-family:archia;'><b> Why Vaccine Is Important ? </b> </h1>",unsafe_allow_html=True)
    st.video("impvaccine.mp4",format="video/ogg")
    col2, col3, col4 = st.columns([4, 4, 4])
    with col2:
        st.image("Capture.JPG")
    with col3:
        st.image("1.JPG")
    with col4:
        st.image("2.JPG")

    col1, col2 = st.columns([27,17])
    with col1:
        st.header("Vaccination by Age")
        im = Image.open("ratio.png")
        size = (400,250)
        im = im.resize(size)
        st.image(im)
    with col2:
        st.header("Vaccination - Category")
        im = Image.open("category.png")
        size=(450,200)
        im=im.resize(size)
        st.image(im)
    col1,col2,col3 = st.columns([3,7,2])
    with col2:
        st.header("Please tap on the Vaccine button to Book the slot")
    col1, col2, col3 = st.columns([7,6,3])
    with col2:
        url ="https://selfregistration.cowin.gov.in/"
        if st.button("Book your Slot"):
            st.balloons()
            webbrowser.open_new_tab(url)

    st.subheader("Covaxin")
    col2,col1=st.columns([1,3])
    with col2:
        size=(200,300)
        image = Image.open("bharat.jpg")
        image=image.resize(size)
        st.image(image)
    with col1:
        st.write("COVAXIN®, India's indigenous COVID-19 vaccine by Bharat Biotech is developed in collaboration with the Indian Council of Medical Research (ICMR) - National Institute of Virology (NIV).")
        st.write("The indigenous, inactivated vaccine is developed and manufactured in Bharat Biotech's BSL-3 (Bio-Safety Level 3) high containment facility.")
        st.write("The vaccine is developed using Whole-Virion Inactivated Vero Cell derived platform technology. Inactivated vaccines do not replicate and are therefore unlikely to revert and cause pathological effects. They contain dead virus, incapable of infecting people but still able to instruct the immune system to mount a defensive reaction against an infection.")
    st.subheader("Covishiled")
    col3, col4 = st.columns([1,3])
    with col3:
        size=(200,300)
        image1 = Image.open("product_covishield.jpg")
        image1=image1.resize(size)
        st.image(image1)
    with col4:
        st.write("Covishield has been prepared using the viral vector platform which is a totally different technology.")
        st.write("A chimpanzee adenovirus – ChAdOx1 – has been modified to enable it to carry the COVID-19 spike protein into the cells of humans. Well, this cold virus is basically incapable of infecting the receiver but can very well teach the immune system to prepare a mechanism against such viruses.")
        st.write("The exact technology was used to prepare vaccines for viruses like Ebola.")

    @st.cache(allow_output_mutation=True, suppress_st_warning=True)
    def load_mapping():
        df = pd.read_csv("district_mapping.csv")
        return df

    def filter_column(df, col, value):
        df_temp = deepcopy(df.loc[df[col] == value, :])
        return df_temp

    def filter_capacity(df, col, value):
        df_temp = deepcopy(df.loc[df[col] > value, :])
        return df_temp

    @st.cache(allow_output_mutation=True)
    def Pageviews():
        return []

    mapping_df = load_mapping()

    rename_mapping = {
        'date': 'Date',
        'min_age_limit': 'Minimum Age Limit',
        'available_capacity': 'Available Capacity',
        'vaccine': 'Vaccine',
        'pincode': 'Pincode',
        'name': 'Hospital Name',
        'state_name': 'State',
        'district_name': 'District',
        'block_name': 'Block Name',
        'fee_type': 'Fees'
    }

    st.title('CoWIN Vaccination Slot Availability')
    st.info('The CoWIN APIs are geo-fenced so sometimes you may not see an output! Please try after sometime ')

    valid_states = list(np.unique(mapping_df["state_name"].values))

    left_column_1, center_column_1, right_column_1 = st.columns(3)
    with left_column_1:
        numdays = st.slider('Select Date Range', 0, 100, 3)

    with center_column_1:
        state_inp = st.selectbox('Select State', [""] + valid_states)
        if state_inp != "":
            mapping_df = filter_column(mapping_df, "state_name", state_inp)

    mapping_dict = pd.Series(mapping_df["district id"].values,
                             index=mapping_df["district name"].values).to_dict()

    unique_districts = list(mapping_df["district name"].unique())
    unique_districts.sort()
    with right_column_1:
        dist_inp = st.selectbox('Select District', unique_districts)

    DIST_ID = mapping_dict[dist_inp]

    base = datetime.datetime.today()
    date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
    date_str = [x.strftime("%d-%m-%Y") for x in date_list]

    temp_user_agent = UserAgent()
    browser_header = {'User-Agent': temp_user_agent.random}

    final_df = None
    for INP_DATE in date_str:
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(
            DIST_ID, INP_DATE)
        response = requests.get(URL, headers=browser_header)
        if (response.ok) and ('centers' in json.loads(response.text)):
            resp_json = json.loads(response.text)['centers']
            if resp_json is not None:
                df = pd.DataFrame(resp_json)
                if len(df):
                    df = df.explode("sessions")
                    df['min_age_limit'] = df.sessions.apply(lambda x: x['min_age_limit'])
                    df['vaccine'] = df.sessions.apply(lambda x: x['vaccine'])
                    df['available_capacity'] = df.sessions.apply(lambda x: x['available_capacity'])
                    df['date'] = df.sessions.apply(lambda x: x['date'])
                    df = df[["date", "available_capacity", "vaccine", "min_age_limit", "pincode", "name", "state_name",
                             "district_name", "block_name", "fee_type"]]
                    if final_df is not None:
                        final_df = pd.concat([final_df, df])
                    else:
                        final_df = deepcopy(df)
            else:
                st.error("No rows in the data Extracted from the API")
    #     else:
    #         st.error("Invalid response")

    if (final_df is not None) and (len(final_df)):
        final_df.drop_duplicates(inplace=True)
        final_df.rename(columns=rename_mapping, inplace=True)

        left_column_2, center_column_2, right_column_2, right_column_2a, right_column_2b = st.columns(5)
        with left_column_2:
            valid_pincodes = list(np.unique(final_df["Pincode"].values))
            pincode_inp = st.selectbox('Select Pincode', [""] + valid_pincodes)
            if pincode_inp != "":
                final_df = filter_column(final_df, "Pincode", pincode_inp)

        with center_column_2:
            valid_age = [15,18, 45]
            age_inp = st.selectbox('Select Minimum Age', [""] + valid_age)
            if age_inp != "":
                final_df = filter_column(final_df, "Minimum Age Limit", age_inp)

        with right_column_2:
            valid_payments = ["Free", "Paid"]
            pay_inp = st.selectbox('Select Free or Paid', [""] + valid_payments)
            if pay_inp != "":
                final_df = filter_column(final_df, "Fees", pay_inp)

        with right_column_2a:
            valid_capacity = ["Available"]
            cap_inp = st.selectbox('Select Availablilty', [""] + valid_capacity)
            if cap_inp != "":
                final_df = filter_capacity(final_df, "Available Capacity", 0)

        with right_column_2b:
            valid_vaccines = ["COVISHIELD", "COVAXIN"]
            vaccine_inp = st.selectbox('Select Vaccine', [""] + valid_vaccines)
            if vaccine_inp != "":
                final_df = filter_column(final_df, "Vaccine", vaccine_inp)

        table = deepcopy(final_df)
        table.reset_index(inplace=True, drop=True)
        st.table(table)
    else:
        st.error("Unable to fetch data currently, please try after sometime")

    pageviews = Pageviews()
    pageviews.append('dummy')
    col1,col2, col3 = st.columns([4.5,2,4])
    with col1:
        st.markdown("<h2 class='first'><b> Share Your Vaccination Status </b><h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:Grey'>Be a Fighter! If you are fully or partially vaccinated, you can now share your vaccination status in your social circle. Let's encourage our friends and followers in joining India's battle against COVID-19.<h4>",unsafe_allow_html=True)
        if st.button("Share your Status"):
            st.balloons()
            webbrowser.open_new_tab("https://www.instagram.com/accounts/login/")

    with col3:
        st.header(" ")
        st.image("ty.png")

    img = Image.open(("Capture.PNG"))
    buff, col, buff = st.columns([4.5, 3, 4.5])
    col.image(img)
    buff, col4, buff = st.columns(3)
    col.markdown( "<h5 <p style ='font-family:archia; text-align: center; color: grey;'>We stand with everyone fighting on the frontlines</p></h5>",unsafe_allow_html=True)
st.set_page_config(
    layout="wide", page_icon="injection1.png")
app()
st.header("")
st.header("")
st.markdown("<h5><center> Made By Tarun Kumar </center></h5>",unsafe_allow_html=True)
st.markdown("<h5><center> For Further Info Drop Mail At : Tarun_063@yahoo.com </center></h5>",unsafe_allow_html=True)
url1="https://forms.gle/LV7kVB84fqVMwYNeA"
col1,col2,col3 = st.columns([1.65,1,1])
with col2:
    if st.button("Feedback Form"):
        webbrowser.open_new_tab(url1)
st.error("These Images are taken from Cowin Website for College Project and Not For Commercial Use")
