# Smart Energy Consumption Dashboard

# 1. Import all the required libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 2. Add custom CSS styling for better UI/UX
st.set_page_config(page_title="Smart Energy Dashboard", layout="wide")

st.markdown("""
<style>
    body {
        background-color: #f5f5f5;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
    }
    div[data-testid="metric-container"] {
        background-color: #E8F6F3;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0px;
        box-shadow: 0 0 10px rgba(0,0,0,0.05);
    }
    section[data-testid="stSidebar"] {
        background-color: #D6EAF8;
    }
</style>
""", unsafe_allow_html=True)

# 3. Load Dataset
df = pd.read_csv("energy_data.csv")


# 4. Title
st.title("⚡ Smart Energy Consumption Dashboard")

# 5. Sidebar Filters
st.sidebar.header("🔍 Filter Options")
region = st.sidebar.selectbox("Select Region", ["All"] + sorted(df["Region"].unique().tolist()))
if region != "All":
    df = df[df["Region"] == region]

# 6. Show Data
st.subheader("📋 Household Energy Consumption Overview")
st.write(df.head())

# 7. Key Metrics
avg_energy = df["Monthly_Energy_Consumption_kWh"].mean()
total_energy = df["Monthly_Energy_Consumption_kWh"].sum()

col1, col2 = st.columns(2)
col1.metric("Average Monthly Consumption (kWh)", f"{avg_energy:.2f}")
col2.metric("Total Energy Consumption (kWh)", f"{total_energy:.0f}")

# 8. Visualizations
st.subheader("📈 Income vs Energy Consumption")
fig1, ax1 = plt.subplots()
sns.scatterplot(data=df, x="Monthly_Income_INR", y="Monthly_Energy_Consumption_kWh", hue="Region", ax=ax1)
st.pyplot(fig1)

# Appliance-wise analysis
st.subheader("🔌 Appliance Count vs Energy Consumption")
appliances = ["Appliance_AC", "Appliance_Fan", "Appliance_Light", "Fridge", "Washing_Machine", "EV_Charging"]
selected_appliance = st.selectbox("Select Appliance", appliances)
fig2, ax2 = plt.subplots()
sns.barplot(x=df[selected_appliance], y=df["Monthly_Energy_Consumption_kWh"], ax=ax2)
ax2.set_xlabel(f"No. of {selected_appliance.replace('_', ' ')}")
ax2.set_ylabel("Energy Consumption (kWh)")
st.pyplot(fig2)

# 9. Recommendations
st.subheader("💡 Smart Recommendations")
recommendations = []

for _, row in df.iterrows():
    if row["Monthly_Energy_Consumption_kWh"] > 250:
        message = f"Household ID {row['Household_ID']} - ⚠ High usage! Recommend switching to solar and LED bulbs."
        recommendations.append(message)
        st.warning(message)
    elif row["EV_Charging"] == 1:
        message = f"Household ID {row['Household_ID']} - 🚗 Consider installing a separate EV meter for optimal billing."
        recommendations.append(message)
        st.info(message)

# 10. Download Recommendations
if recommendations:
    st.download_button(
        label="📥 Download Recommendations",
        data="\n".join(recommendations),
        file_name="recommendations.txt",
        mime="text/plain"
    )

# 11. Footer
st.markdown("---")
st.markdown("<p style='text-align:center;'>🚀 Built with ❤ using Streamlit | Add your GitHub link here</p>", unsafe_allow_html=True)