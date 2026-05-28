import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx,mdx}", "./components/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        ink: "#172026",
        muted: "#65717B",
        panel: "#F7F9FA",
        line: "#D8E0E5",
        accent: "#0F766E",
        warn: "#B45309",
        danger: "#B91C1C",
      },
    },
  },
  plugins: [],
};

export default config;
