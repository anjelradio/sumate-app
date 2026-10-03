export function EventsSkeleton() {
  return (
    <div className="space-y-4 pt-2">
      {[1, 2, 3].map((index) => (
        <article
          key={index}
          className="bg-white rounded-3xl p-3.5 shadow-sm border border-zinc-100 animate-pulse"
        >
          {/* Skeleton de la imagen */}
          <div className="w-full h-44 rounded-2xl bg-zinc-200/80" />

          {/* Skeleton de la información */}
          <div className="pt-3 px-1 pb-1 space-y-2">
            <div className="h-5 bg-zinc-200 rounded-md w-3/4" />
            <div className="h-3.5 bg-zinc-200 rounded-md w-1/2" />
            <div className="h-3 bg-zinc-100 rounded-md w-1/3" />
          </div>
        </article>
      ))}
    </div>
  );
}
