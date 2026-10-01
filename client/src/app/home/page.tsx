import { AppHeader } from "@/features/shared/presentation/components/layout/app-header";

export default function HomePage() {
  return (
    <div className="flex min-h-screen flex-col bg-white text-zinc-900">
      <AppHeader />

      <main className="flex flex-1 flex-col items-center justify-center px-6 py-12">
        <div className="text-center space-y-3 max-w-md mx-auto">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-[#F4F2FE] text-[#6355DE] mb-2 shadow-inner">
            <svg
              className="w-8 h-8"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              strokeWidth="2"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-zinc-900">
            ¡Bienvenido a Súmate!
          </h1>
          <p className="text-sm text-zinc-500 leading-relaxed">
            Has iniciado sesión correctamente. Esta es la página principal de tu
            cuenta de voluntariado.
          </p>
        </div>
      </main>
    </div>
  );
}

