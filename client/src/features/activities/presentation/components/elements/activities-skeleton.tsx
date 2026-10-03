import { Skeleton } from "@/components/ui/skeleton";

export function ActivitiesSkeleton() {
  return (
    <div className="pt-2 space-y-6" data-purpose="activities-skeleton">
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
  );
}
