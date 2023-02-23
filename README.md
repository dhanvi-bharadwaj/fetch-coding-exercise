# Background
Our users have points in their accounts. Users only see a single balance in their account. But for reporting purposes, we actually track their
points per payer. In our system, each transaction record contains: payer (string), points (integer), timestamp (date).
For earning points, it is easy to assign a payer. We know which actions earned the points. And thus, which partner should be paying for the
points.
When a user spends points, they don't know or care which payer the points come from. But, our accounting team does care how the points are
spent. There are two rules for determining what points to "spend" first:
  ● We want the oldest points to be spent first (oldest based on transaction timestamp, not the order they’re received)
  ● We want no payer's points to go negative.
We expect your code to:
1. Read the transactions from a CSV file.
2. Spend points based on the argument using the rules above.
3. Return all payer point balances.
