import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CSV Telemetry Viewer", layout="wide")
st.title("📈 Interactive CSV Data Viewer")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        
        columns = df.columns.tolist()
        col1, col2 = st.columns(2)
        
        with col1:
            x_axis = st.selectbox("Select X-Axis", options=columns, index=0)
            
            # Automatically check this box if the column name contains 'time'
            convert_time = st.checkbox("Convert X-Axis to Readable Time", value='time' in x_axis.lower())
            if convert_time:
                # Default to nanoseconds ('ns') for high-frequency telemetry
                time_unit = st.selectbox("Timestamp Unit", options=['s', 'ms', 'us', 'ns'], index=3)
            
        with col2:
            y_axes = st.multiselect(
                "Select Y-Axis (Multiple Allowed)", 
                options=columns, 
                default=[columns[1]] if len(columns) > 1 else []
            )
            
        if y_axes:
            plot_df = df.copy()
            
            # Convert the raw Unix timestamps to actual Datetime objects
            if convert_time:
                plot_df[x_axis] = pd.to_datetime(plot_df[x_axis], unit=time_unit)

            fig = px.line(plot_df, x=x_axis, y=y_axes, title=f"Plot of {', '.join(y_axes)} over {x_axis}")
            
            fig.update_layout(
                xaxis_title=x_axis,
                yaxis_title="Values",
                legend_title="Variables",
                hovermode="x unified",
                margin=dict(l=20, r=20, t=40, b=20),
                dragmode="pan" 
            )
            
            # Plotly will now natively format the datetimes on the x-axis
            st.plotly_chart(
                fig, 
                use_container_width=True, 
                config={
                    'scrollZoom': True,
                    'displayModeBar': True,
                    'modeBarButtonsToRemove': ['lasso2d', 'select2d']
                }
            )
            
        else:
            st.warning("Please select at least one column for the Y-axis.")
            
    except Exception as e:
        st.error(f"Error reading the CSV file: {e}")