# Themes

Customize the chat UI with theme variables. The docs preview shows a few example styles, but in code the `theme` prop accepts a `theme.json` object rather than a preset string.

## Custom Themes

Create a `theme.json` file with three sections: `theme`, `light`, and `dark`:

```json
{
  "theme": {},
  "light": {},
  "dark": {}
}
```

Pass it to the component:

```tsx
import theme from "./theme.json"

<AgentChat theme={theme} />
```

## Theme Properties

- **theme** - shared CSS variables such as typography, spacing, and display options
- **light** - light-mode color variables
- **dark** - dark-mode color variables