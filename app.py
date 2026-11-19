import logging

import streamlit as st
from google import genai

st.set_page_config(
    page_title="SupportBot AI | Blessed Nikah",
    page_icon="💬",
    layout="centered",
)


st.markdown("""
<style>
:root { --bn-green: #123f35; --bn-green-light: #1d5b4b; --bn-gold: #c6a15b; --bn-cream: #f7f5ef; }
.stApp { background: linear-gradient(180deg, #f7f5ef 0%, #ffffff 36%); }
.block-container { max-width: 860px; padding-top: 2rem; padding-bottom: 3rem; }
.bn-hero {
  background: linear-gradient(125deg, #103c32 0%, #1d5b4b 100%);
  color: #fff; padding: 1.55rem 1.65rem; border-radius: 18px;
  border: 1px solid rgba(198,161,91,.55); margin-bottom: 1.1rem;
  box-shadow: 0 8px 24px rgba(16,60,50,.12);
}
.bn-kicker { color: #e3c98f; font-size: .76rem; letter-spacing: .16em; font-weight: 700; }
.bn-hero h1 { color: #fff; margin: .35rem 0 .25rem 0; font-size: 2rem; }
.bn-hero p { color: #edf4f0; margin: 0; font-size: .98rem; }
.bn-pill { display:inline-block; margin-top:.9rem; padding:.28rem .7rem; border:1px solid rgba(255,255,255,.3); border-radius:99px; color:#f2dfb5; font-size:.78rem; }
div[data-testid="stChatMessage"] { border: 1px solid #e9e5da; border-radius: 15px; padding: .55rem .75rem; background: #fff; }
div[data-testid="stChatInput"] { border-color: #d8d1c1; }
.stButton > button { border-radius: 11px; border: 1px solid #d9d2c3; color: #17483d; background: #fff; min-height: 2.7rem; }
.stButton > button:hover { border-color: #b9944e; color: #123f35; }
section[data-testid="stSidebar"] { background: #f1efe7; }
.bn-foot { text-align:center; color:#77766f; font-size:.78rem; padding-top:1rem; }
</style>
<div class="bn-hero">
  <div class="bn-kicker">BLESSED NIKAH · CUSTOMER CARE</div>
  <h1>SupportBot AI</h1>
  <p>Clear, respectful help for your Blessed Nikah journey.</p>
  <span class="bn-pill">Privacy · Guidance · Support</span>
</div>
""", unsafe_allow_html=True)
st.caption("Ask about registration, memberships, features, or how to contact our team.")

st.markdown("#### How can I help you today?")



def queue_question(question):
    st.session_state["pending_prompt"] = question

quick_cols = st.columns(2)
quick_questions = [
    "What features are free?",
    "What are the membership plans?",
    "How do photo-exchange requests work?",
    "How can I contact Blessed Nikah?",
]
for index, question in enumerate(quick_questions):
    with quick_cols[index % 2]:
        st.button(
            question,
            key=f"quick_question_{index}",
            use_container_width=True,
            on_click=queue_question,
            args=(question,),
        )

st.markdown("---")

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

QUICK FAQ GUIDANCE
Q: Is registration free?
A: Registration is advertised as free. Do not claim that every feature is free.

Q: Can free members browse profiles?
A: The listed free features include creating a profile, browsing matches, viewing full profiles, and sending profile-view invitations.

Q: Can free members send messages?
A: The listed free features allow users to view and reply to messages from paid members. Initiating new messages is listed as a paid feature.

Q: How do photo requests work?
A: Sending or accepting photo-exchange requests is listed as a paid feature. Do not promise that a particular member will accept or share photos.

Q: Which membership is cheapest?
A: The 1-month plan has the lowest listed total price at Rs. 499. The 6-month plan has the lowest approximate monthly cost among the listed prices. Always remind customers to confirm current offers before payment.

Q: Can I get a refund?
A: Subscriptions are generally described as non-refundable, with limited exceptions. Only official support can review a request under the current policy. Never guarantee approval.

Q: Can you check my profile, payment, or account?
A: No. SupportBot AI cannot access customer accounts or payment records. Direct the customer to official support.

Q: How do I contact Blessed Nikah?
A: Email support@blessednikah.com or info@blessednikah.com, or WhatsApp +91 8851 862 970.

WHEN A QUESTION IS NOT COVERED
Say clearly that the available information does not confirm the answer. Do not guess. Offer the relevant official support contact.
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

V5 CUSTOMER-SUPPORT AGENT PLAYBOOK
First identify the customer's main intent internally. Use one or more of these
categories: registration/login, membership/pricing, payment/subscription,
profile/matches, messaging, photo exchange/privacy, technical problem,
complaint/feedback, refund request, or general enquiry. Do not show internal
classification labels unless they genuinely help the customer.

RESPONSE RULES
- Answer the actual question first. If the message contains several issues,
  address each one separately.
- For a technical problem, give a short, numbered troubleshooting sequence.
  Start with low-risk steps such as checking the internet connection, refreshing
  the page, reopening the website, or trying an updated browser. Do not claim
  that a step will definitely fix the issue.
- For login, payment, subscription, profile, or other account-specific problems,
  clearly explain that you cannot access or change the customer's account.
  Direct them to support@blessednikah.com or WhatsApp +91 8851 862 970.
- For payment deducted but membership not activated, advise the customer to
  contact official support for verification. Never claim that payment has been
  received or that a plan has been activated.
- For complaints, acknowledge the inconvenience calmly, avoid arguing or
  blaming the customer, explain what you can, and provide the official support
  route when human review is needed.
- For refund requests, explain the published general policy cautiously and say
  that only the official team can review eligibility. Never approve or promise
  a refund.
- If the issue remains unresolved after safe basic steps, stop guessing and
  offer a handoff to the official support team.
- Do not ask customers to post personal documents, payment details, OTPs,
  passwords, private profile information, or sensitive screenshots in this chat.
  If evidence is needed, tell them to share it only through official support.
- Be transparent: you are an AI assistant, not a human agent, and you cannot
  create tickets, contact staff, inspect accounts, or perform actions unless
  the app explicitly provides those capabilities.
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

Answer the customer's latest message using only the knowledge above.
If the customer asks multiple questions in one message, answer each question separately
using a short numbered list. Do not skip any part of the message.
For comparisons, distinguish lowest total price from best approximate monthly value.
Do not repeat the full FAQ unless needed. If the answer is unknown, say so and direct
the customer to official support. Apply the V5 customer-support agent playbook:
identify intent, acknowledge complaints, provide safe numbered troubleshooting
steps when useful, and escalate account-specific or unresolved issues to the
official support contacts. Never imply that you have created a ticket or accessed
an account. Keep the answer helpful, concise, and easy to read.
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

typed_prompt = st.chat_input("Type your question here...")
queued_prompt = st.session_state.pop("pending_prompt", None)
prompt = queued_prompt or typed_prompt

if prompt:
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
    st.markdown("---")
    st.markdown("**Official support**")
    st.write("support@blessednikah.com")
    st.write("WhatsApp: +91 8851 862 970")
    st.markdown("---")
    st.caption("A respectful support experience, built around member privacy.")
    if st.button("Clear conversation"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Assalamu Alaikum! Welcome to Blessed Nikah. How can I help you today?",
            }
        ]
        st.rerun()

st.markdown(
    '<div class="bn-foot">Blessed Nikah SupportBot AI · General information only · '
    'Your private account details are handled by the official support team.</div>',
    unsafe_allow_html=True,
)
