import { AppHeader } from "@/features/shared/presentation/components/layout/app-header";
import { AppNavbar } from "@/features/shared/presentation/components/layout/app-navbar";

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="h-[100dvh] max-h-[100dvh] bg-white text-slate-800 flex justify-center selection:bg-[#ece9fc] selection:text-[#4334b8] overflow-hidden">
      <div className="w-full max-w-md h-full flex flex-col relative overflow-hidden bg-white">
        <header className="shrink-0 z-40 bg-white">
          <AppHeader />
          <AppNavbar />
        </header>
        <main className="flex-1 flex flex-col min-h-0 overflow-hidden px-5">
          {children}
        </main>
      </div>
    </div>
  );
}
