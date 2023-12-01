import streamlit as st
import pandas as pd
import numpy as np
import eda

st.title('Utah Snow Patterns Over Time, 1979-Present')

eda.plot1
eda.plot2

# Side by side (doesn't work with map)
# col1, col2 = st.columns(2)

# with col1:
#     st.plotly_chart(eda.plot2)

# with col2:
#     st.plotly_chart(eda.plot1)