import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Set page configuration
st.set_page_config(layout="wide")

# Display the header image
st.image("stress photo.jpg", use_container_width=True)

# Load the dataset
DF = pd.read_csv('StressLevelDataset.csv')

# ========== Graph Section 1: Violin Plot and Bar Chart (Study Load) ==========
col1, col2 = st.columns(2)

with col1:
    fig1 = px.violin(
        DF,
        x='academic_performance',
        y='anxiety_level',
        box=True,
        points='all',
        color_discrete_sequence=['#FF9800']
    )
    fig1.update_layout(
        title='Anxiety Level by Academic Performance',
        xaxis_title='Academic Performance',
        yaxis_title='Anxiety Level'
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    bar_data = DF.groupby('study_load')['anxiety_level'].mean().reset_index()
    fig2 = px.bar(
        bar_data,
        x='study_load',
        y='anxiety_level',
        color='anxiety_level',
        color_continuous_scale='purples',
        title='Average Anxiety Level by Study Load',
        labels={'anxiety_level': 'Avg Anxiety Level', 'study_load': 'Study Load'}
    )
    st.plotly_chart(fig2, use_container_width=True)

# ========== Graph Section 2: Headache by Living Conditions and Scatter Plot ==========
col3, col4 = st.columns(2)

with col3:
    avg = DF.groupby('living_conditions')['headache'].mean().reset_index()
    fig3 = px.bar(
        avg, x='living_conditions', y='headache',
        title='Average Headache Levels by Living Conditions',
        labels={'living_conditions':'Living Conditions','headache':'Avg Headache Level'},
        color='headache', color_continuous_scale='oranges'
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.scatter(
        DF,
        x='self_esteem',
        y='depression',
        color='peer_pressure',
        title='Depression vs Self Esteem by Peer Pressure',
        labels={
            'self_esteem': 'Self Esteem',
            'depression': 'Depression'
        },
        opacity=0.7,
        color_discrete_sequence=px.colors.sequential.Teal
    )
    st.plotly_chart(fig4, use_container_width=True)

# ========== Graph Section 3: Pie Charts for Peer Pressure ==========
st.markdown("### Depression Levels by Peer Pressure")
peer_levels = DF['peer_pressure'].unique()
colors = {'High': '#FF6347', 'Low': '#ADD8E6'}
fig, axes = plt.subplots(1, len(peer_levels), figsize=(5 * len(peer_levels), 5))

for i, level in enumerate(sorted(peer_levels)):
    group = DF[DF['peer_pressure'] == level]['depression'].apply(lambda x: 'High' if x >= 7 else 'Low').value_counts()
    axes[i].pie(
        group,
        labels=group.index,
        autopct='%1.1f%%',
        colors=[colors[label] for label in group.index],
        startangle=90,
        explode=[0.05 if label == 'High' else 0 for label in group.index]
    )
    axes[i].set_title(f'Peer Pressure: {level}')

st.pyplot(fig)
