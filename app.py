import logging

import streamlit as st
from google import genai

st.set_page_config(
    page_title="SupportBot AI | Blessed Nikah",
    page_icon="💬",
    layout="centered",
)

st.title("💬 SupportBot AI")
st.caption("Customer support assistant for Blessed Nikah")

COMPANY_KNOWLEDGE = """
ABOUT BLESSED NIKAH
Blessed Nikah is a Muslim matrimonial platform.

REGISTRATION
Registration is advertised as free. Users can create a profile through the
website's registration process. The website has described WhatsApp OTP login.
If a customer needs help with a specific account or login problem, direct them
to official support rather than requesting passwords or OTPs.

MEMBERSHIP AND FEATURES
Free features listed on the website:
- Create a profile and browse matches.
- View full profiles.
- Send unlimited profile-view invitations.
- View and reply to messages from paid members.

Paid features listed on the website:
- Initiate new messages.
- Send or accept photo-exchange requests.

HOMEPAGE-LISTED MEMBERSHIP PRICES
- 1 month: Rs. 499
- 3 months: Rs. 999
- 6 months: Rs. 1,699

Based on these homepage-listed prices:
- Cheapest total payment: 1-month plan at Rs. 499.
- Approximate monthly cost: 1-month Rs. 499; 3-month Rs. 333;
  6-month Rs. 283.17.
- Best monthly value among these listed options: 6-month plan.

IMPORTANT PRICE CAUTION:
The website FAQ and homepage have had inconsistent descriptions.
Treat the prices and feature descriptions above as homepage-listed information,
not a guarantee of the current offer. Ask customers to confirm current prices
and terms with Blessed Nikah support before payment.

PROFILE PRIVACY
The website describes profile photos as blurred by default, with photo sharing
controlled by user choices and platform permissions. Do not promise that any
specific profile or photo is visible to a particular person. Never disclose
private member details.

WALI / GUARDIAN
The platform advertises guardian (Wali) integration. Do not invent details
about how it works; direct detailed questions to official support.

REFUNDS
The published refund information describes subscriptions as generally
non-refundable, with limited exceptional cases such as duplicate payments or
payment deducted without subscription activation. Requests are described as
needing to be raised within 7 days with proof. Do not approve, promise, or
guarantee a refund. Ask the customer to contact official support for review
under the current policy.

OFFICIAL SUPPORT CONTACTS
Email: support@blessednikah.com
Additional email: info@blessednikah.com
WhatsApp: +91 8851 862 970

GENERAL SAFETY
- Use only the company information above.
- Never invent policies, prices, features, or guarantees.
- If information is missing or may have changed, say so and refer the customer
  to official support.
- Never ask for or reveal passwords, OTPs, payment-card details, or private
  matrimonial member information.
- Do not claim to search, edit, verify, or access a customer's account.
"""

SYSTEM_INSTRUCTIONS = """
You are SupportBot AI, the customer-support assistant for Blessed Nikah.
Answer politely in the same language and writing style used by the customer in their latest message.
- If the customer writes in English, reply in simple English.
- If the customer writes in Hindi using Devanagari, reply in simple Hindi using Devanagari.
- If the customer writes in Hinglish or Hindi using English letters, reply in natural Hinglish using English letters.
- If the customer mixes languages, naturally match their mix.
- Keep answers concise, clear, and respectful.
- Do not start every reply with "Assalamu Alaikum", "Wa Alaikum Assalam", or any other greeting.
- The app already displays a welcome greeting at the start of the chat. Do not repeat a greeting in normal answers.
- If the customer greets you for the first time, respond to that greeting briefly once; after that, answer questions directly without repeating greetings.
- Never add a greeting when answering a follow-up question in the same conversation.
Use only the supplied company knowledge. Be transparent when information is
missing, inconsistent, or may have changed.
Never invent company policies or promise refunds.
Never reveal private member information or request passwords, OTPs, or
payment-card details. For account-specific issues, refer the customer to the
official support contacts in the knowledge base.
"""

def get_answer(chat_messages):
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

    conversation = "\n".join(
        f"{'Customer' if item['role'] == 'user' else 'SupportBot AI'}: {item['content']}"
        for item in chat_messages[-12:]
    )

    prompt = f"""
{SYSTEM_INSTRUCTIONS}

BLESSED NIKAH COMPANY KNOWLEDGE:
{COMPANY_KNOWLEDGE}

RECENT CONVERSATION:
{conversation}

Respond to the customer's latest message. Keep the answer helpful and concise.
"""
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )
    return response.text or "I'm sorry, I couldn't prepare an answer. Please try again."

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Assalamu Alaikum! Welcome to Blessed Nikah. How can I help you today?",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about Blessed Nikah..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            answer = get_answer(st.session_state.messages)
            st.markdown(answer)
        except KeyError:
            logging.exception("SupportBot configuration error: GEMINI_API_KEY may be missing.")
            answer = (
                "SupportBot AI is not configured yet. Please check the app configuration "
                "or contact Blessed Nikah support."
            )
            st.error(answer)
        except Exception as e:
            logging.exception("Gemini API request failed. See this traceback in Streamlit logs.")
            error_text = str(e)
            if "API_KEY_INVALID" in error_text or "API key not valid" in error_text:
                answer = (
                    "SupportBot AI needs a valid Gemini API key. "
                    "The app owner should create a new key in Google AI Studio "
                    "and replace GEMINI_API_KEY in Streamlit Secrets."
                )
            else:
                answer = (
                    "I'm sorry, the support service is temporarily unavailable. "
                    "Please try again later or contact Blessed Nikah support."
                )
            st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

with st.sidebar:
    st.subheader("About")
    st.write("SupportBot AI provides general information about Blessed Nikah.")
    st.caption(
        "For current prices, account-specific questions, or policy decisions, "
        "please contact official Blessed Nikah support."
    )
    if st.button("Clear conversation"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Assalamu Alaikum! Welcome to Blessed Nikah. How can I help you today?",
            }
        ]
        st.rerun()
