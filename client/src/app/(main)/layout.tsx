import { MainLayoutHeader } from "@/features/shared/presentation/components/layout/main-layout-header";
import { listCausesQuery } from "@/features/activities/presentation/queries/activity.query";
import { CausesInitializer } from "@/features/activities/presentation/components/elements/causes-initializer";
import type { Cause } from "@/features/activities/domain/entities/activity.entity";

export default async function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  let causes: Cause[] = [];
  try {
    causes = await listCausesQuery();
  } catch {
    causes = [];
  }

  return (
    <div className="h-[100dvh] max-h-[100dvh] bg-white text-slate-800 flex justify-center selection:bg-[#ece9fc] selection:text-[#4334b8] overflow-hidden">
      <CausesInitializer initialCauses={causes} />
      <div className="w-full max-w-md h-full flex flex-col relative overflow-hidden bg-white">
        <MainLayoutHeader />
        <main className="flex-1 flex flex-col min-h-0 overflow-hidden px-5">
          {children}
        </main>
      </div>
    </div>
  );
}
