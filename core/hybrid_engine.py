import json
from core.llm import GroqLLM
from evolution.user_evolution import UserEvolution

class HybridEngine:
    def __init__(self):
        self.llm = GroqLLM()
        self.evolution = UserEvolution()

    def get_profile(self):
        return self.evolution.get_profile()

    def run(self, request):
        profile = self.get_profile()
        context = json.dumps(profile, indent=2)

        main = self.llm.ask(
            """You are AI-1, the Main AI of a personal hybrid-intelligence system.
Your job is to understand the user's request, reason about it, create a practical
workflow, and give the user a useful answer. You coordinate with AI-2 and AI-3,
but you are the primary execution/planning intelligence.
Never claim that you changed production code unless a real tool performed that action.
Current user-specific profile:
""" + context,
            request,
        )

        review = self.llm.ask(
            """You are AI-2, the independent Workflow Reviewer.
Review AI-1's proposed answer/workflow. Find missing assumptions, risks,
incorrect reasoning, unclear steps, or requirements that should be verified.
Do not simply agree. Give concrete corrections and say what AI-1 should change.
You are reviewing this specific user request.

USER REQUEST:
""" + request + "\n\nAI-1 RESPONSE:\n" + main,
            "Review AI-1's response rigorously.",
        )

        human = self.llm.ask(
            """You are AI-3, the Human Thinking Partner.
Your job is to help the human think better, not make the final decision for them.
Explore useful questions, alternatives, creative possibilities, trade-offs,
and decision criteria. Keep the user's agency central.

USER REQUEST:
""" + request + "\n\nAI-1:\n" + main + "\n\nAI-2:\n" + review,
            "Help the human explore this situation and decide what to do.",
            temperature=0.5,
        )

        evolution = self.llm.ask(
            """You are the Personal Evolution Detector.
Determine whether the user's request reveals a recurring or missing capability
that this user's personal AI should eventually gain.
Return either:
NO_EVOLUTION_NEEDED
or a concise proposal with:
- missing capability
- why it is useful for this user
- what kind of module/tool/workflow could provide it
Do NOT write executable code and do NOT modify production systems.""",
            "USER REQUEST:\n" + request + "\n\nCURRENT PROFILE:\n" + context,
        )

        if evolution != "NO_EVOLUTION_NEEDED":
            self.evolution.add_proposal({
                "request": request,
                "proposal": evolution,
            })

        return {
            "main": main,
            "review": review,
            "human": human,
            "evolution": None if evolution == "NO_EVOLUTION_NEEDED" else evolution,
        }
