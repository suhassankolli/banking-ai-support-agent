
from agent import AgentContext, BankingAgent
from observability import configure_logging

configure_logging()

agent = BankingAgent()

# Simulated authenticated identity for this exercise.
# Production identity must come from verified auth middleware.
context = AgentContext(
    authorized_customer_id="CUST0001"
)

question = (
    "Show the last 5 transactions for CUST0001 "
    "and identify the largest transaction by "
    "absolute amount."
)

print("Question:", question)
print("\nAgent response:")
print(agent.run(question, context))
