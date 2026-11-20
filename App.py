import streamlit as st

st.set_page_config(page_title="Gold Planner", page_icon="🥇", layout="centered")
st.title("🥇 Gold (XAUUSD) Planner")

CONTRACT_SIZE = 100  # 1 lot gold = 100 oz, so $1 move = $100 per lot

balance = st.number_input("Account Balance ($)", min_value=1.0, value=1000.0, step=100.0)
direction = st.radio("Direction", ["Buy", "Sell"], horizontal=True)
entry = st.number_input("Entry Price", min_value=0.0, value=2650.00, step=0.10, format="%.2f")
sl = st.number_input("Stop Loss Price", min_value=0.0, value=2645.00, step=0.10, format="%.2f")
lot = st.number_input("Lot Size (aap khud likho)", min_value=0.01, value=0.10, step=0.01, format="%.2f")

# Validation
if direction == "Buy" and sl >= entry:
    st.error("Buy mein Stop Loss Entry se NEECHE hona chahiye.")
    st.stop()
if direction == "Sell" and sl <= entry:
    st.error("Sell mein Stop Loss Entry se UPAR hona chahiye.")
    st.stop()

sl_dist = abs(entry - sl)
risk_usd = sl_dist * CONTRACT_SIZE * lot
risk_pct = risk_usd / balance * 100

st.subheader("Risk")
c1, c2, c3 = st.columns(3)
c1.metric("SL Distance", f"${sl_dist:.2f}")
c2.metric("Risk ($)", f"${risk_usd:.2f}")
c3.metric("Risk (%)", f"{risk_pct:.2f}%")

if risk_pct > 2:
    st.warning("Risk 2% se zyada hai. Lot size kam karne par ghor karo.")
else:
    st.success("Risk 2% ke andar hai.")

st.subheader("Take Profit Levels")
rows = []
for rr in (1, 2, 3):
    tp = entry + sl_dist * rr if direction == "Buy" else entry - sl_dist * rr
    rows.append({
        "RR": f"1:{rr}",
        "TP Price": f"{tp:.2f}",
        "Profit ($)": f"${risk_usd * rr:.2f}",
        "Profit (%)": f"{risk_pct * rr:.2f}%",
    })
st.table(rows)

st.caption("Note: Calculation XAUUSD ke liye hai (1 lot = 100 oz). Broker ke contract size ke mutabiq check kar lena.")
