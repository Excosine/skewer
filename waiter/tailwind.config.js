/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js}"],
  theme: {
    extend: {
      colors: {
        surface: "#121010",
        flame: {
          50: "#fff5f0", 100: "#ffede5", 200: "#ffd4c4", 300: "#ffb499",
          400: "#ff8c42", 500: "#ff4a22", 600: "#e63a1a", 700: "#cc2e12",
        },
        brand: {
          50: "#fff5f0", 100: "#ffede5", 200: "#ffd4c4", 300: "#ffb499",
          400: "#ff8c42", 500: "#ff4a22", 600: "#e63a1a", 700: "#cc2e12",
        },
        cream: "#F5EFE4",
        muted: "#C9A77A",
      },
    },
  },
  plugins: [],
};
