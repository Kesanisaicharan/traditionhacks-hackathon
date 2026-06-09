import streamlit as st
import random
from datetime import datetime

st.set_page_config(
    page_title="CitySense - Traffic & Pollution Analyzer",
    page_icon="🌆",
    layout="centered"
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
    }
    .chat-message {
        padding: 0.75rem 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        font-size: 15px;
    }
    .user-msg {
        background-color: #1976D2;
        color: white;
        margin-left: 20%;
    }
    .bot-msg {
        background-color: #f0f4f8;
        color: #1a1a1a;
        margin-right: 20%;
    }
    .aqi-card {
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 18px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ----- Data -----
CITY_DATA = {
    "kolkata": {
        "zones": {
            "park street":     {"aqi": 142, "traffic": "Heavy",    "pm25": 68,  "no2": 45},
            "salt lake":       {"aqi": 88,  "traffic": "Moderate", "pm25": 32,  "no2": 28},
            "howrah":          {"aqi": 178, "traffic": "Very Heavy","pm25": 95,  "no2": 62},
            "new town":        {"aqi": 65,  "traffic": "Light",    "pm25": 22,  "no2": 18},
            "esplanade":       {"aqi": 155, "traffic": "Heavy",    "pm25": 78,  "no2": 55},
            "jadavpur":        {"aqi": 110, "traffic": "Moderate", "pm25": 48,  "no2": 35},
            "dumdum":          {"aqi": 135, "traffic": "Heavy",    "pm25": 60,  "no2": 42},
            "behala":          {"aqi": 120, "traffic": "Moderate", "pm25": 52,  "no2": 38},
        }
    }
}

def get_aqi_label(aqi):
    if aqi <= 50:   return ("Good", "#4CAF50")
    if aqi <= 100:  return ("Moderate", "#FFC107")
    if aqi <= 150:  return ("Unhealthy for Sensitive Groups", "#FF9800")
    if aqi <= 200:  return ("Unhealthy", "#F44336")
    if aqi <= 300:  return ("Very Unhealthy", "#9C27B0")
    return ("Hazardous", "#7B1FA2")

def get_health_tip(aqi):
    if aqi <= 50:   return "✅ Air quality is great! Safe for all outdoor activities."
    if aqi <= 100:  return "😷 Acceptable air quality. Sensitive individuals should limit prolonged outdoor exertion."
    if aqi <= 150:  return "⚠️ Unhealthy for sensitive groups. Children and elderly should avoid prolonged outdoor activities."
    if aqi <= 200:  return "🚨 Unhealthy! Everyone should reduce outdoor exertion. Wear a mask if going out."
    return "🆘 Very Unhealthy / Hazardous! Avoid going outside. Keep windows closed."

def get_safest_zone():
    zones = CITY_DATA["kolkata"]["zones"]
    safest = min(zones, key=lambda z: zones[z]["aqi"])
    return safest, zones[safest]

def get_worst_zone():
    zones = CITY_DATA["kolkata"]["zones"]
    worst = max(zones, key=lambda z: zones[z]["aqi"])
    return worst, zones[worst]

def chatbot_response(user_input):
    user_input_lower = user_input.lower()
    zones = CITY_DATA["kolkata"]["zones"]

    # Check pollution/AQI for a specific zone
    for zone_name, data in zones.items():
        if zone_name in user_input_lower:
            label, color = get_aqi_label(data["aqi"])
            tip = get_health_tip(data["aqi"])
            return (
                f"📍 **{zone_name.title()} — Air Quality Report**\n\n"
                f"🌫️ AQI: **{data['aqi']}** ({label})\n"
                f"🚗 Traffic: **{data['traffic']}**\n"
                f"💨 PM2.5: {data['pm25']} µg/m³\n"
                f"🧪 NO₂: {data['no2']} µg/m³\n\n"
                f"{tip}"
            )

    # Safest route / area
    if any(w in user_input_lower for w in ["safe", "best", "cleanest", "less pollution", "safest"]):
        zone, data = get_safest_zone()
        label, _ = get_aqi_label(data["aqi"])
        return (
            f"🌿 **Safest Zone Right Now: {zone.title()}**\n\n"
            f"AQI: {data['aqi']} ({label})\n"
            f"Traffic: {data['traffic']}\n\n"
            f"✅ This is the cleanest area in Kolkata right now. "
            f"Recommended for outdoor walks, cycling, and sensitive individuals."
        )

    # Worst zone
    if any(w in user_input_lower for w in ["worst", "most polluted", "avoid", "dangerous"]):
        zone, data = get_worst_zone()
        label, _ = get_aqi_label(data["aqi"])
        return (
            f"🚨 **Most Polluted Zone Right Now: {zone.title()}**\n\n"
            f"AQI: {data['aqi']} ({label})\n"
            f"Traffic: {data['traffic']}\n\n"
            f"⚠️ Avoid this area if possible, especially if you have respiratory issues."
        )

    # Traffic query
    if any(w in user_input_lower for w in ["traffic", "congestion", "jam", "road"]):
        heavy_zones = [z for z, d in zones.items() if d["traffic"] in ["Heavy", "Very Heavy"]]
        light_zones = [z for z, d in zones.items() if d["traffic"] == "Light"]
        return (
            f"🚗 **Traffic Summary — Kolkata**\n\n"
            f"🔴 Heavy Traffic: {', '.join([z.title() for z in heavy_zones])}\n"
            f"🟢 Light Traffic: {', '.join([z.title() for z in light_zones])}\n\n"
            f"💡 Tip: Consider New Town or Salt Lake for smoother commutes today."
        )

    # All zones summary
    if any(w in user_input_lower for w in ["all zones", "summary", "overview", "all areas"]):
        response = "📊 **Kolkata Air Quality Overview**\n\n"
        for zone, data in zones.items():
            label, _ = get_aqi_label(data["aqi"])
            emoji = "🟢" if data["aqi"] <= 100 else "🟡" if data["aqi"] <= 150 else "🔴"
            response += f"{emoji} {zone.title()}: AQI {data['aqi']} ({label})\n"
        return response

    # Health tips
    if any(w in user_input_lower for w in ["health", "tip", "advice", "mask", "outdoor"]):
        return (
            "🏥 **Health Tips for Polluted Days**\n\n"
            "1. 😷 Wear N95 masks when AQI > 100\n"
            "2. 🌿 Prefer indoor exercises on high pollution days\n"
            "3. 💧 Stay hydrated — water helps flush toxins\n"
            "4. 🕐 Avoid outdoor activity between 7–9 AM (peak traffic hours)\n"
            "5. 🪟 Keep windows closed when AQI > 150\n"
            "6. 🌳 Prefer green zones like New Town for outdoor walks"
        )

    # Greeting
    if any(w in user_input_lower for w in ["hi", "hello", "hey", "namaste"]):
        return (
            "👋 **Welcome to CitySense!**\n\n"
            "I'm your AI assistant for real-time traffic and pollution analysis in Kolkata.\n\n"
            "You can ask me:\n"
            "• 🌫️ 'What is the AQI in Howrah?'\n"
            "• 🚗 'How is traffic today?'\n"
            "• 🌿 'Which is the safest zone?'\n"
            "• ⚠️ 'Which area to avoid?'\n"
            "• 🏥 'Give me health tips'\n"
            "• 📊 'Show all zones summary'"
        )

    # Default
    return (
        "🤖 I can help you with:\n\n"
        "• AQI & pollution levels for Kolkata zones\n"
        "• Traffic congestion updates\n"
        "• Safest routes and areas\n"
        "• Health tips based on air quality\n\n"
        "Try asking: *'What is the pollution in Salt Lake?'* or *'Which zone is safest?'*"
    )


# ----- UI -----
st.markdown("<div class='main-header'><h2>🌆 CitySense</h2><p style='color:gray;'>AI-Powered Traffic & Pollution Analyzer — Kolkata</p></div>", unsafe_allow_html=True)

# Quick stats bar
col1, col2, col3 = st.columns(3)
safest_zone, safest_data = get_safest_zone()
worst_zone, worst_data = get_worst_zone()

with col1:
    st.metric("🌿 Cleanest Zone", safest_zone.title(), f"AQI {safest_data['aqi']}")
with col2:
    st.metric("🚨 Most Polluted", worst_zone.title(), f"AQI {worst_data['aqi']}")
with col3:
    now = datetime.now().strftime("%I:%M %p")
    st.metric("🕐 Last Updated", now, "Live")

st.divider()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Welcome to CitySense! Ask me about AQI, traffic, or safe zones in Kolkata."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Quick action buttons
st.markdown("**Quick Questions:**")
qcol1, qcol2, qcol3 = st.columns(3)
with qcol1:
    if st.button("🌿 Safest Zone"):
        user_q = "Which is the safest zone?"
        st.session_state.messages.append({"role": "user", "content": user_q})
        reply = chatbot_response(user_q)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
with qcol2:
    if st.button("📊 All Zones"):
        user_q = "Show all zones summary"
        st.session_state.messages.append({"role": "user", "content": user_q})
        reply = chatbot_response(user_q)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
with qcol3:
    if st.button("🚗 Traffic Update"):
        user_q = "How is traffic today?"
        st.session_state.messages.append({"role": "user", "content": user_q})
        reply = chatbot_response(user_q)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

# Chat input
if prompt := st.chat_input("Ask about pollution, traffic or safe zones..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    response = chatbot_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
