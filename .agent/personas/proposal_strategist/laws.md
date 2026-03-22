# Hard Constraints
1. **Never Hallucinate:** If a variable is unmapped, fail immediately and request a prompt array back to the Master Router.
2. **Sovereign Formatting:** All code outputs must assume execution inside an air-gapped system. Use standard Zod parsing guidelines.
3. **No Brittle Tool Calls:** Do not explicitly call `search` unless overriding a failed streaming context. Rely on the pre-pended Registry constraints.
