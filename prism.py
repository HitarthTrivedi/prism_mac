"""
AI Agent Router System with Grok API (using requests - no base URL)
"""
"""
AI Agent Router System - Playwright Version
"""
import undetected_chromedriver as uc
import requests
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
import time
import json
import pyautogui
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration — key is loaded from .env, never hardcoded
GROK_API_KEY = os.getenv("GROQ_API_KEY")
if not GROK_API_KEY:
    raise EnvironmentError("❌ GROQ_API_KEY not found. Please set it in your .env file.")

# AI Agent Specializations
AI_AGENTS = {
    "claude": {
        "url": "https://claude.ai",
        "specialty": "coding, debugging, technical implementation, code review, algorithms",
        "textarea_selector": "div[contenteditable='true']",
    },
    "perplexity": {
    "url": "https://www.perplexity.ai",
    "specialty": "research, fact-checking, current events, academic queries, citations",
    "textarea_selector": "div[contenteditable='true']#ask-input",
    },
    "chatgpt": {
        "url": "https://chatgpt.com",
        "specialty": "general conversation, brainstorming, creative writing, everyday tasks",
        "textarea_selector": "#prompt-textarea",
    },
    "gemini": {
        "url": "https://gemini.google.com",
        "specialty": "multimodal tasks, Google integration, data analysis, summaries",
        "textarea_selector": "div[contenteditable='true'][role='textbox']",
    }
}


def analyze_and_route_with_grok(notes):
    """Use your working Grok API implementation"""

    routing_prompt = f"""You are an intelligent AI routing system that creates INTERDEPENDENT, CROSS-REFERENCING prompts across multiple AI agents.

    CORE PRINCIPLE - INTERDEPENDENT PROMPTS:
    All prompts across ALL agents must be CONNECTED and RELATED to the same overarching topic(s).
    Each agent should tackle a DIFFERENT ANGLE of the same subject, and the prompts should 
    explicitly reference or build upon what other agents are exploring.
    
    Think of it as a COLLABORATIVE RESEARCH TEAM where each agent has a specialized role:
    - One agent explains the CONCEPTS (ChatGPT)
    - One agent provides the IMPLEMENTATION/CODE (Claude)  
    - One agent researches LATEST FACTS & REAL-WORLD DATA (Perplexity)
    - One agent SYNTHESIZES & ANALYZES everything together (Gemini)

    TASK:
    1. Read each question/topic in the user's notes
    2. Identify the CENTRAL THEME(s) across all notes
    3. For EACH topic, distribute INTERDEPENDENT prompts across multiple agents where each agent's 
       prompts are RELATED to what other agents receive:
       - The prompts should CROSS-REFERENCE each other (e.g., "Based on the core concepts of X, 
         write code that implements..." or "Find the latest research papers on X that validate...")
       - Each agent gets 2-4 prompts that play to its SPECIALTY but stay ON THE SAME TOPIC
       - Together, all agents' prompts should provide a 360-degree comprehensive view of the topic
    4. Route prompts to the BEST agent based on the type of question

    Available AI Agents:
    - claude: {AI_AGENTS['claude']['specialty']}
    - perplexity: {AI_AGENTS['perplexity']['specialty']}
    - chatgpt: {AI_AGENTS['chatgpt']['specialty']}
    - gemini: {AI_AGENTS['gemini']['specialty']}

    User's notes/questions:
    {notes}

    EXAMPLE OF INTERDEPENDENT PROMPTS:
    If user asks: "How to learn Python?"
    
    chatgpt should get (conceptual/learning angle):
    - "Create a structured 3-month Python learning roadmap from beginner to intermediate, covering core concepts, OOP, and popular frameworks"
    - "What are the most common mistakes beginners make when learning Python, and how to avoid them?"
    
    claude should get (implementation/code angle):
    - "Based on a Python learning roadmap covering core concepts and OOP, write 5 progressively harder Python coding exercises with solutions that a beginner can use to practice"
    - "Write a well-commented Python project template that demonstrates best practices a beginner should learn (proper structure, error handling, type hints, docstrings)"
    
    perplexity should get (research/facts angle):
    - "What are the most in-demand Python skills and libraries in the job market in 2025-2026? Include salary data and job posting trends"
    - "What are the latest Python learning platforms and courses released in 2025, and how do they compare in terms of reviews and completion rates?"
    
    gemini should get (synthesis/analysis angle):
    - "Compare and analyze the different Python learning approaches (self-taught vs bootcamp vs university) - which produces better developers based on available data?"
    - "Summarize the Python ecosystem in 2025: key libraries, frameworks, and tools a learner should focus on, organized by domain (web, data science, AI, automation)"

    Notice how ALL prompts revolve around the SAME TOPIC (learning Python) but each agent 
    tackles it from its specialty angle, and the prompts REFERENCE common themes.

    ROUTING RULES:
    1. For coding/debugging/implementation/writing code → claude
    2. For research/facts/current events/latest data → perplexity  
    3. For general explanations/conceptual understanding/creative/learning advice → chatgpt
    4. For data analysis/synthesis/comparisons/summaries → gemini
    
    IMPORTANT: Try to involve AT LEAST 2-3 agents for each topic to ensure comprehensive, 
    interdependent coverage. Only use 1 agent if the topic is extremely narrow and specific.

    Return ONLY valid JSON with this structure:
    {{
        "agent_name": {{
            "questions": ["question 1", "question 2", "question 3", ...],
            "reasoning": "why this agent is best for these specific questions and how they connect to other agents' prompts"
        }}
    }}

    Only include agents that are needed. Return ONLY the JSON, no extra text."""

    try:
        # YOUR WORKING GROK API CALL HERE
        headers = {
            "Authorization": f"Bearer {GROK_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": routing_prompt}],
            "temperature": 0.3
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )

        response_text = response.json()['choices'][0]['message']['content']
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1

        if json_start == -1:
            return {}

        routing_data = json.loads(response_text[json_start:json_end])
        return routing_data

    except Exception as e:
        print(f"❌ Grok API Error: {e}")
        return {}


def automate_ai_agents(routing_data):
    """Selenium + undetected-chromedriver version"""

    if not routing_data:
        print("❌ No agents to route to")
        return {}

    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # Setup undetected Chrome
    # Copy Chrome profile to a temp dir to avoid SingletonLock conflicts
    import shutil
    import tempfile
    chrome_profile_src = "/Users/hitarthtrivedi/Library/Application Support/Google/Chrome"
    temp_profile_dir = os.path.join(tempfile.gettempdir(), "uc_chrome_profile")

    # Clean up any previous temp profile
    if os.path.exists(temp_profile_dir):
        shutil.rmtree(temp_profile_dir, ignore_errors=True)

    # Copy only the Default profile (not the entire Chrome data dir)
    os.makedirs(temp_profile_dir, exist_ok=True)
    src_default = os.path.join(chrome_profile_src, "Default")
    dst_default = os.path.join(temp_profile_dir, "Default")
    if os.path.exists(src_default):
        shutil.copytree(src_default, dst_default, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("SingletonLock", "SingletonCookie", "SingletonSocket", "*.lock"))

    # Also copy essential top-level files (Local State, etc.)
    for fname in ["Local State"]:
        src_file = os.path.join(chrome_profile_src, fname)
        if os.path.exists(src_file):
            shutil.copy2(src_file, os.path.join(temp_profile_dir, fname))

    options = uc.ChromeOptions()
    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Use UC's built-in user_data_dir parameter (NOT as a Chrome argument)
    driver = uc.Chrome(
        options=options,
        user_data_dir=temp_profile_dir
    )

    agent_tabs = {}

    # Open required agents in separate tabs
    print("\n" + "=" * 70)
    print("📋 GENERATED QUESTIONS PER AGENT:")
    print("=" * 70)
    for agent_name, data in routing_data.items():
        if agent_name not in AI_AGENTS:
            continue

        agent_config = AI_AGENTS[agent_name]  # Define BEFORE try block
        print(f"\n🚀 Opening {agent_name.upper()}...")
        print(f"   Reason: {data.get('reasoning', 'N/A')}")

        try:
            # Open new tab
            if agent_tabs:
                pyautogui.hotkey('command', 't')
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[-1])

            driver.get(agent_config["url"])  # Now agent_config is defined
            time.sleep(4)

            # Send prompts
            for idx, prompt in enumerate(data["questions"], 1):
                try:
                    print(f"   → Question {idx}/{len(data['questions'])}: {prompt[:80]}...")

                    textarea = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, agent_config["textarea_selector"]))
                    )
                    textarea.clear()
                    textarea.send_keys(prompt)
                    time.sleep(1)
                    textarea.send_keys(Keys.ENTER)

                    time.sleep(45)  # Delay between prompts

                except Exception as e:
                    print(f"   ❌ Prompt error: {e}")

            agent_tabs[agent_name] = {
                "window_handle": driver.current_window_handle,
                "question_count": len(data["questions"])
            }
            time.sleep(100)
        except Exception as e:
            print(f"   ❌ Failed to open {agent_name}: {e}")

    # Wait for responses
    print(f"\n⏳ Waiting 5 minutes for responses...")
    time.sleep(200)

    # Fetch responses
    print(f"\n\n{'=' * 70}")
    print("📥 COLLECTING RESPONSES")
    print(f"{'=' * 70}\n")

    all_responses = {}

    for agent_name, tab_data in agent_tabs.items():
        try:
            driver.switch_to.window(tab_data["window_handle"])

            possible_selectors = [
                "[data-testid*='message']",
                ".message-content",
                ".response",
                "[class*='response']",
                "[class*='message']"
            ]

            responses = []
            for selector in possible_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        for elem in elements[-tab_data["question_count"]:]:
                            text = elem.text.strip()
                            if text and len(text) > 50:
                                responses.append(text)
                        break
                except:
                    continue

            if responses:
                all_responses[agent_name] = responses
                print(f"\n{'─' * 70}")
                print(f"🤖 AI AGENT: {agent_name.upper()}")
                print(f"{'─' * 70}")

                for idx, resp in enumerate(responses, 1):
                    print(f"\n[Response {idx}]")
                    print(resp[:800] + ("..." if len(resp) > 800 else ""))
            else:
                print(f"\n⚠️ {agent_name}: No responses captured")

        except Exception as e:
            print(f"\n❌ Error fetching from {agent_name}: {e}")

    print(f"\n{'=' * 70}\n")

    # Keep windows open


    return all_responses


def main():
    prev=open('prev_notes.txt','r')
    prev_content=prev.read()
    print(prev_content)
    # Google Drive Authentication with settings
    gauth = GoogleAuth(settings_file='settings.yaml')

    # Try to load saved credentials
    gauth.LoadCredentialsFile("credentials.json")

    if gauth.credentials is None:
        # Authenticate if no credentials
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh if expired
        gauth.Refresh()
    else:
        # Initialize with valid credentials
        gauth.Authorize()

    # Save credentials for next time
    gauth.SaveCredentialsFile("credentials.json")

    drive = GoogleDrive(gauth)

    # Read notes.txt from Drive
    file_list = drive.ListFile({'q': "title='notes.txt'"}).GetList()

    if not file_list:
        print("❌ notes.txt not found in Google Drive!")
        return

    file = file_list[0]
    user_notes = file.GetContentString()
    if user_notes!=prev_content:
        print("\n" + "=" * 70)
        print("🤖 AI AGENT ROUTER SYSTEM (Playwright)")
        print("=" * 70)
        print("\n📝 Your Notes:")
        print(user_notes)
        with open('prev_notes.txt','w') as u_notes:
            u_notes.write(user_notes)



        print("\n🧠 Grok analyzing and routing...\n")
        routing_data = analyze_and_route_with_grok(user_notes)

        if routing_data:
            print("📊 ROUTING DECISIONS:")
            print(json.dumps(routing_data, indent=2))

            responses = automate_ai_agents(routing_data)

            if responses:
                with open("ai_responses.json", "w", encoding="utf-8") as f:
                    json.dump(responses, f, indent=2, ensure_ascii=False)
                print("\n💾 Responses saved to ai_responses.json")
        else:
            print("\n❌ No routing data from Grok")

    else:
        print("its the same")

# Rest of your existing code...





if __name__ == "__main__":
    main()