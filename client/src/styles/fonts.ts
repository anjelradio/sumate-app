import { Plus_Jakarta_Sans, JetBrains_Mono } from "next/font/google";

/*
 * Plus Jakarta Sans como fuente principal para toda la aplicación
 * (titulares, textos, labels y controles de formulario).
 */
const plusJakartaSans = Plus_Jakarta_Sans({
  subsets: ["latin"],
  variable: "--app-font-sans",
});

const mono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--app-font-mono",
});

export const appFontVariables = `${plusJakartaSans.variable} ${mono.variable}`;
