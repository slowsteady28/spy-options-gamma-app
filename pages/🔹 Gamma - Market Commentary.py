import streamlit as st
from datetime import datetime
now = datetime.now()

st.set_page_config(page_title="Market Commentary", page_icon="🧑‍💻")

# Custom sidebar background color (soft green)
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #343c47;
            color: #fcfcfe;
        }
        [data-testid="stSidebar"] * {
            color: #fcfcfe !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("5/20/2024")

st.markdown("""


📊 SPY Gamma Setup: Bulls in Control, But Fatigue May Be Setting In


This morning’s gamma landscape is clean: SPY’s Key Gamma and Call Wall both sit at 600, with ~10 days of call gamma duration and ~$300M in net call gamma—well above average.

That setup, along with recent price action, suggests short-term bullish traders remain in control. But positioning tells us something more nuanced:

🔻 Call interest has been withdrawn at both Key Gamma and the Call Wall

📉 SpotGamma's TRACE shows dealers selling deltas, likely in response to traders unwinding upside exposure via call sales or put buying

SPY 600 has acted as a magnet—being both a gamma inflection point and a long-duration target into June OPEX. But with price nearly there and upside scenarios increasingly priced in, we may now be approaching a pause point.

🧭 A calm gamma environment still favors bulls, but signs of exhaustion suggest consolidation is likely.

Let’s see if 600 becomes a ceiling—or base—for the next leg.

""")

st.image("assets/TRACE.jpg", caption="Spot Gamma TRACE")
st.caption(f"Updated: {now.strftime('%b %d, %Y %I:%M %p')}")  # ✅ This will now work



st.title("5/19/2024")

st.markdown("""

📉 Post-OPEX Gamma Reset: Who Gains Control?

Following May's OPEX, the SPY ETF saw a meaningful reduction in positioning:

* 🔻 ~700K in call open interest and ~2M in put OI rolled off
* 🔻 Net call gamma dropped by ~$1B
* 🔺 Net put gamma increased by ~$600M

This effectively removed much of the short-dated gamma that had been supporting price action — leaving the market in a temporary “neutral zone.”

So what now?

🔹 SPY 580 becomes critical.

It holds long-duration call gamma extending into September. If bulls want to maintain control, price must hold this level — signaling continued institutional support heading into the summer.

If bears gain control, expect:

* The Put Wall to rise just below price
* Duration to drop
* Net put gamma to climb

That’s exactly how we’re setting up this morning:

📍 The Put Wall has risen to SPY 588.

But the big question is:

Will price break below SPY 588 and test support at 580?

Or will long-duration put gamma at SPY 550 and 540 come into play?

🧭 We’ll know bulls are back in control if:

* Price holds near 580
* Short-term call interest builds
* The Call Wall moves sideways to higher
* Volatility measures remain subdued

OPEX has cleared the deck. Now we wait to see who takes the wheel.

""")


st.title("5/16/2024")

st.markdown("""

📊 SPY Positioning Update – May 15, 2025

Price continues to drift higher — likely the result of put holders throwing in the towel, dealers adjusting hedges, and short-term players leaning long via call exposure.

With the Call Wall now up to SPY 600 and Memorial Day around the corner, the path of least resistance remains to the upside.

But signs of positioning fatigue are emerging:

* Call interest at Key Gamma has been withdrawn over the last few sessions
* The main Call Wall saw a net decline in interest
* OPEX is approaching, which may strip out short-dated gamma that’s been helping fuel the rally

📉 This dynamic opens the door to sideways consolidation in the days ahead.

Always watching gamma shifts, not just price.

""")



st.title("5/15/2024")

st.markdown("""

📍SPY 590: Where Institutional Hedging Meets Short-Term Exhaustion?

On April 2nd, SPY 590 held the longest call gamma duration (~47 trading days) — a sign that dealers or MMs saw this level as a potential cap for a Vanna-fueled rally.

Fast forward to now:<br>
📅 May 15th
✅ Price has reached SPY 590
✅ VIX6M is perking up
✅ Key Gamma has lost call interest three days in a row (-54K, -37K, -12.6K)
✅ Today, we see an uptick in call gamma duration at Key Gamma

This sequence tells a story:
Short-term traders that helped drive the rally are now likely taking profits, increasing the odds of sideways consolidation heading into next week.

Adding to this view:

SPY's Put Wall has moved up to 586, with ~3-day duration and slight net put gamma bump

This morning’s gap down comes with no panic in vol, suggesting those puts may be sold, placing dealers in a positive gamma zone

🧭 Heading into May OPEX, the question becomes:
Will support hold near SPY 570/560 once short-dated gamma decays?

Watch how Call Wall, Put Wall, and Key Gamma evolve. That’s the roadmap.

""")

st.title("5/12/2024")

st.markdown("""

📈 SPY 580: A Key Inflection Point into June OPEX

On Friday, May 9th, traders added ~80K in call interest at SPY 580 — notably ahead of trade talks. Why does this matter?

SPY 580 has consistently represented the upper bound of the potential price path into the June quarterly OPEX and Q2-end rebalancing. This level isn’t just technical — it’s behavioral.

Earlier this year, before April’s OPEX, SPY 580 emerged as the largest Call Wall, measured by net call gamma (call gamma minus put gamma). The positioning likely reflected risk mitigation by dealers or large shorts anticipating a possible squeeze into June. This demand showed up as long-duration gamma, offering a signal of strategic hedging, not speculation.

Layered on top of that:

· Massive volume spikes in early April (on April 7th, 8th, and 9th SPY volume on a daily basis was 6.5, 3.5, and 6.0 standard deviations above the mean, respectively),

·  Strikes with short-duration, significant near-the-money call gamma, which has an outsized effect on dealer hedging behavior.

Once SPY began holding above those high-volume levels and gamma piled in, the probability of a gamma-driven melt-up — the very risk large players were hedging — increased meaningfully.

Yes, markets can still pull back. But this setup tells us that key players were preparing for exactly this kind of squeeze — and may now be fueling it.

""")

st.title("5/9/2024")

st.markdown("""

📈 SPY Gamma Recap — A Week of Reset and Positioning for Upside

This week, SPY gave traders a clearer picture of where the market might be heading.

🔹 The Call Wall held firm at 570, and is now showing signs of moving sideways to higher as:

• Call interest was added at 580, SPY’s 2nd largest Call Wall
• Additional activity hit the 590 and 600 strikes — suggesting upside positioning by active participants

🔹 Notably, the duration at the 570 Key Gamma Strike dropped, while total gamma remained flat. This tells me traders are rotating into near-term expirations to fuel momentum rather than fading strength.

Earlier this week, on Tuesday (May 6), SPY briefly dipped below its 560 Put Wall — but with no downside follow-through and no bid to longer-term vol (VIX3M, VIX6M), the move felt like post-expiration digestion (roughly 16.5% of SPY’s total gamma expired May 2).

🧭 What I’m watching now: If the Call Wall continues drifting higher and short-dated call interest builds near price, that could be the confirmation bulls need.

📊 Gamma exposure continues to be one of the cleanest windows into institutional positioning.

""")

st.title("5/8/2024")

st.markdown("""

📈 SPY Gamma Roadmap: 560 & 570 Are the Levels to Watch

Overnight, SPY’s Call Wall shifted sideways to 570 as ~6.5K calls were added. Price also moved higher in tandem, while the Put Wall remains anchored well below at 540 — suggesting the path of least resistance remains to the upside.

💡 But here’s where it gets interesting:

 At the close on April 30 and May 1, SPY’s total options gamma was minimal — a typical sign that liquidity was pulled ahead of key events like the FOMC decision. When this happens, we often get a clearer signal of long-duration gamma strikes — levels that represent where institutions are committed.

📍 April 30 Key Gamma Strike (long duration): 560
 📍 May 1 Key Gamma Strike (long duration): 570

▶️ Going forward:
 If SPY pulls back into 560 or 570 and finds support, and we see short-dated call interest build near those levels, it may signal that bulls remain in control and the market has absorbed the Fed outcome constructively.
—
📊 Watch the strikes. Watch the flows. Watch the gamma.

""")

st.title("5/7/2024")

st.markdown("""

📊 Gamma Positioning Insights – SPY 540 & SPY 570 in Focus

SPY 540 currently holds the largest net put gamma, and with an average expiration greater than 40 days, it's likely this level is being defended by institutional players. This type of positioning often signals a tactical long bias anchored to that strike.

Meanwhile, the largest net call gamma—or Call Wall—sits at SPY 570. Historically, when the Call Wall shifts sideways or higher, SPY price tends to follow. Although the Call Wall eased today, I’ll be watching closely to see if it reclaims or advances tomorrow.

🔁 These gamma dynamics suggest a market at an inflection point—hedging pressure vs. directional intent. Stay nimble.

""")

st.title("5/6/2024")

st.markdown("""

🔍 Gamma Spotlight: SPY 560 Becoming a Key Battleground

Yesterday (May 5), roughly 60,000 puts were added to SPY's 560 strike—marking it as a growing area of interest. As of today (May 6), most of that open interest remains intact, reinforcing the level's relevance in the near term.

What makes SPY 560 notable?

📌 It holds the largest overall gamma concentration—with put gamma now outweighing call gamma.

 📆 Much of that put gamma expires within the next 5 trading days, suggesting this level could act as a gravitational magnet in the short term, potentially suppressing volatility or creating sharp directional risk if breached.

📈 If SPY trades below 560, that gamma profile may flip from stabilizing to destabilizing, amplifying downside moves.

 🧘‍♂️ Above 560, price action could consolidate as short-dated gamma decays and market makers rebalance.
—
💭 Are you positioning around key gamma levels like SPY 560?

""")