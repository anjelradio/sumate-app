import { AppHeader } from "@/features/shared/presentation/components/layout/app-header";
import { AppNavbar } from "@/features/shared/presentation/components/layout/app-navbar";

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-white text-slate-800 flex justify-center selection:bg-[#ece9fc] selection:text-[#4334b8]">
      <div className="w-full max-w-md min-h-screen flex flex-col relative overflow-x-hidden bg-white">
        <AppHeader />
        <AppNavbar />
        <main className="flex-1 px-5 pt-3 pb-24 overflow-y-auto no-scrollbar">
          {children}
        </main>
      </div>
    </div>
  );
}
