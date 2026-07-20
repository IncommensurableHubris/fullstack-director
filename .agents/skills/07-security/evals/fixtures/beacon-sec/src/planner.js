// Build the planner prompt for the orchestrator LLM.
const SYSTEM = "You are Beacon's planner. Decide which sources to search and how to synthesize.";

function buildPlannerPrompt(userQuestion, fetchedSnippets) {
  // NOTE: userQuestion and fetchedSnippets are untrusted (user input + retrieved web content).
  // They are concatenated RAW into the system prompt with no separation or provenance boundary.
  return SYSTEM + "\nUser question: " + userQuestion + "\nContext from sources:\n" + fetchedSnippets.join("\n");
}

module.exports = { buildPlannerPrompt };
