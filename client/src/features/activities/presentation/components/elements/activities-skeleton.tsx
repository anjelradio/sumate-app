import { Skeleton } from "@/components/ui/skeleton";

export function ActivitiesSkeleton() {
  return (
    <div className="flex-1 flex flex-col min-h-0 h-full overflow-hidden" data-purpose="activities-skeleton">
      <div className="flex items-center justify-between gap-1.5 pt-4 pb-2.5 border-b border-slate-100/80 px-1 bg-white shrink-0">
        {[1, 2, 3, 4].map((i) => (
          <Skeleton key={i} className="h-7 w-20 rounded-full bg-slate-100" />
        ))}
      </div>
      <div className="flex-1 overflow-y-auto no-scrollbar pt-3 pb-24 space-y-6">
        {[1, 2, 3].map((item) => (
          <div
            key={item}
            className="pb-6 border-b border-slate-100 last:border-b-0 animate-pulse duration-700"
          >
            {/* Skeleton para imagen */}
            <Skeleton className="w-full h-44 rounded-2xl bg-slate-200/90" />

            {/* Skeleton para textos */}
            <div className="pt-3 px-1 space-y-2.5">
              <Skeleton className="h-5 w-4/5 rounded-md bg-slate-200/90" />
              <Skeleton className="h-4 w-1/3 rounded-md bg-slate-200/80" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
