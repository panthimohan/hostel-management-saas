/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        fog: "#F1F3F1",
        surface: "#FFFFFF",
        ink: "#12242B",
        "ink-soft": "#4B5D62",
        primary: {
          DEFAULT: "#145C5A",
          dark: "#0D423F",
          light: "#1E7A76",
        },
        brass: {
          DEFAULT: "#C98A2C",
          dark: "#A96E1B",
          light: "#E0A94E",
        },
        moss: {
          DEFAULT: "#3F7A5D",
          light: "#E7F1EA",
        },
        clay: {
          DEFAULT: "#B3492E",
          light: "#F7E7E2",
        },
        border: "#DDE3E0",
      },
      fontFamily: {
        display: ["'Fraunces'", "serif"],
        sans: ["'IBM Plex Sans'", "system-ui", "sans-serif"],
        mono: ["'IBM Plex Mono'", "monospace"],
      },
      boxShadow: {
        card: "0 1px 2px rgba(18, 36, 43, 0.06), 0 1px 0 rgba(18, 36, 43, 0.04)",
        panel: "0 12px 32px rgba(18, 36, 43, 0.14)",
      },
      borderRadius: {
        xl2: "1.25rem",
      },
    },
  },
  plugins: [],
};
