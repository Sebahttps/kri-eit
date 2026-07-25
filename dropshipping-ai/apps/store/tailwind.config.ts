import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  darkMode: "media",
  theme: {
    extend: {
      colors: {
        // Paleta validada (dataviz): superficies, tinta y series por rol
        surface: "rgb(var(--surface) / <alpha-value>)",
        plane: "rgb(var(--plane) / <alpha-value>)",
        ink: "rgb(var(--ink) / <alpha-value>)",
        "ink-2": "rgb(var(--ink-2) / <alpha-value>)",
        muted: "rgb(var(--muted) / <alpha-value>)",
        grid: "rgb(var(--grid) / <alpha-value>)",
      },
    },
  },
  plugins: [],
};
export default config;
