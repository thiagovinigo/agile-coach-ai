# Messages & History

How message persistence works, lazy loading history, and restoring conversations on mount.

## How are messages stored?

Messages are stored on 21st Agents side in our database. When you send a message, we persist both your message and the agent's response. You can retrieve the full history via `client.threads.get({ sandboxId, threadId })`.

## How does message sending work under the hood?

On each `sendMessage` call, you send the full conversation history plus the new message. The platform feeds only the last message to the agent - Claude already knows the full history from its local conversation file. The full history you send is what gets persisted in our database.

## How do I restore history on page mount?

After mounting your chat component, fetch the existing messages using `client.threads.get()` and pass them to the AI SDK. This lets users see previous conversation when they return to the page.

## Is lazy loading of message history supported?

Lazy loading for scrolling through long histories is on the roadmap. Currently, you fetch the full thread history on mount.

## Can I have multiple conversation threads?

Yes. Create multiple threads within the same sandbox. Each thread has its own message history while sharing the same sandbox environment.